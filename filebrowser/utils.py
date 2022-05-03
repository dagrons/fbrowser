import urllib.parse
from typing import Dict


def build_url(schema: str, host: str, port: str, path: str = "", query: Dict[str, str] = {}) -> str:
    query_str = ""
    if len(query) != 0:
        query_str = "?" + urllib.parse.urlencode(query)
    return '%s://%s:%s%s%s' % (schema, host, port, path, query_str)


def build_http_url(host: str, port: str, path: str = "", query: Dict[str, str] = {}) -> str:
    return build_url("http", host, port, path, query)


def build_url_from_base_url(base_url: str, path: str = "", query: Dict[str, str] = {}) -> str:
    query_str = urllib.parse.urlencode(query)
    return '%s%s?%s' % (base_url, path, query_str)
