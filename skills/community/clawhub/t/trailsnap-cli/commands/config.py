from utils import save_env

def setup_parser(subparsers):
    parser = subparsers.add_parser("config", help="配置 CLI")
    sub_subparsers = parser.add_subparsers(dest="subcommand", help="可用操作")
    sub_subparsers.required = True

    set_parser = sub_subparsers.add_parser("set", help="配置 API URL 和 Token")
    set_parser.add_argument("--url", help="API 基础地址 (例如: http://localhost:8000)", required=True)
    set_parser.add_argument("--token", help="API Token (Bearer 凭证)", required=True)
    set_parser.set_defaults(func=execute_set)

def execute_set(args):
    save_env(args.url, args.token)
