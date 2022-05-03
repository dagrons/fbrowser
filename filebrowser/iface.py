class FileBrowserClientIFace(object):

    def authenticate(self, username, password): # 认证之后才能下载auth file
        raise NotImplementedError

    def download_shared_file(self, code: str, fpath: str, share_password: str, save_path: str):
        raise NotImplementedError

    def download_auth_file(self, fpath: str, save_path: str):
        raise NotImplementedError

