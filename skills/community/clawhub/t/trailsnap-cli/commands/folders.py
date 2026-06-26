import json
from utils import make_request

def setup_parser(subparsers):
    parser = subparsers.add_parser("folders", help="管理和查询挂载的存储目录")
    sub_subparsers = parser.add_subparsers(dest="subcommand", help="可用操作")
    sub_subparsers.required = True

    list_parser = sub_subparsers.add_parser("list", help="查询挂载的存储目录")
    list_parser.set_defaults(func=execute_list)

def execute_list(args):
    data = make_request("/settings/directories")
    if data is not None:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print("未查询到存储目录信息")
