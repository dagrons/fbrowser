import argparse

import filebrowser


def main():
    parser = argparse.ArgumentParser(description="filebrowser cli tools")
    parser.add_argument("--ip", type=str, help="server ip", default="10.112.108.112")
    parser.add_argument("--port", type=str, help="server port", default="8081")
    parser.add_argument("--type", type=str, help="auth or share", default="share")
    parser.add_argument("--username", type=str, help="username")
    parser.add_argument("--password", type=str, help="password")
    parser.add_argument("--code", type=str, help="shared code")
    parser.add_argument("--spass", type=str, help="shared password")
    parser.add_argument("source", metavar='source', type=str)
    parser.add_argument("target", metavar="target", type=str)
    args = parser.parse_args()

    s = filebrowser.FileBrowserClient(args.ip, args.port)
    if args.type == "share":
        s.download_shared_file(args.code, args.source, args.spass, args.target)
    elif args.type == "auth":
        s.authenticate(args.username, args.password)
        s.download_auth_file(args.source, args.target)
    else:
        print(f'Unknown Type {args.type}')
        exit(-1)


if __name__ == "__main__":
    main()
