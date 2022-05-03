class GetTokenFailedException(Exception):  # if this happened, quit the job and let me decide what to do next
    def __init__(self, code: int, path: str, share_token: str):
        self.code = code
        self.path = path
        self.share_token = share_token

    def __str__(self):
        return f'Get token failed, statusCode={self.code}, with path={self.path}, share_token={self.share_token}'


class AuthenticationFailedException(Exception):
    def __init__(self, code: int, username: str, password: str):
        self.code = code
        self.username = username
        self.password = password

    def __str__(self):
        return f'Authentication failed,  status_code={self.code}, with self.username={self.username}, password={self.password}'


class DownLoadException(Exception):
    def __init__(self, code: int, url: str):
        self.code = code
        self.url = url

    def __str__(self):
        return f'Download failed, status_code={self.code}, with url={self.url}'


class NoCredentialsException(Exception):
    def __str__(self):
        return "No Credentials supplied!"
