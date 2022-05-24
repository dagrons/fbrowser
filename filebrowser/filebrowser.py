import logging
from dataclasses import dataclass

import requests
from typing import List

from .errors import GetTokenFailedException, AuthenticationFailedException, DownLoadException, NoCredentialsException
from .iface import FileBrowserClientIFace
from .utils import *


@dataclass
class HostInfo:
    host: str
    port: str
    username: str
    password: str


class FileBrowserClient:
    def __init__(self, hosts: List[HostInfo] = []):
        self.machine_list = []
        for info in hosts:
            self.machine_list.append(Machine(info.host, info.port).authenticate(info.username, info.password))

    def download_auth_file(self, fpath: str, save_path: str):
        error = None
        for machine in self.machine_list:
            try:
                machine.download_auth_file(fpath, save_path)
                return True
            except DownLoadException as err:
                error = err
                pass
        if error is not None:
            raise error


# wrap the http api as a client
class Machine(FileBrowserClientIFace):

    def __init__(self, host: str, port: str):
        self.s = requests.Session()
        self.base_url = build_http_url(host, port)
        self.auth_token = None
        self.share_token_cache = {}  # caches for token to avoid replicated http request

    def authenticate(self, username: str, password: str):
        auth_url = build_url_from_base_url(self.base_url, "/api/login")
        resp = self.s.post(auth_url, json={
            "username": username,
            "password": password,
        })
        if resp.status_code != 200:
            raise AuthenticationFailedException(resp.status_code, username, password)
        self.auth_token = resp.text
        return self

    def download_shared_file(self, code: str, fpath: str, share_password: str, save_path: str):
        url = self.__build_share_download_url(code, fpath, self.__get_share_token(code, share_password))
        self.__download(save_path, url)

    def download_auth_file(self, fpath: str, save_path: str):
        if not self.is_authenticated():
            raise NoCredentialsException()
        url = self.__build_auth_download_url(fpath)
        self.__download(save_path, url, headers={
            "X-Auth": self.auth_token,
        })

    def __download(self, save_path: str, url: str, headers={}):
        resp = self.s.get(url, headers=headers)
        if resp.status_code != 200:
            raise DownLoadException(resp.status_code, url)
        with open(save_path, 'wb') as f:
            f.write(resp.content)

    def is_authenticated(self) -> bool:
        return self.auth_token is not None

    def __get_share_token(self, code: str, share_password: str) -> str:
        if code in self.share_token_cache:
            return self.share_token_cache[code]
        file_url = build_url_from_base_url(self.base_url, f'/api/public/share/{code}')
        resp = self.s.get(file_url, headers={
            "X-SHARE-PASSWORD": share_password
        })
        if resp.status_code != 200:
            raise GetTokenFailedException(resp.status_code, code, share_password)
        token = resp.json()["token"]
        self.share_token_cache[code] = token
        return token

    def __build_share_download_url(self, code: str, fpath: str, token: str) -> str:
        return build_url_from_base_url(self.base_url, f'/api/public/dl/{code}/{fpath}', query={
            "token": token,
        })

    def __build_auth_download_url(self, fpath: str) -> str:
        return build_url_from_base_url(self.base_url, f'/api/raw/{fpath}')
