import json
from utils import make_request

def setup_parser(subparsers):
    parser = subparsers.add_parser("tags", help="管理和查询分类标签")
    sub_subparsers = parser.add_subparsers(dest="subcommand", help="可用操作")
    sub_subparsers.required = True

    list_parser = sub_subparsers.add_parser("list", help="查询分类标签")
    list_parser.add_argument("--skip", type=int, default=0, help="跳过 N 个记录")
    list_parser.add_argument("--limit", type=int, default=100, help="限制返回 N 个记录")
    list_parser.set_defaults(func=execute_list)

def execute_list(args):
    data = make_request("/tags", {"skip": args.skip, "limit": args.limit})
    if data:
        tags = [{
            "id": tag["id"],
            "name": tag["tag_name"],
            "count": tag["count"]
        } for tag in data]
        print(json.dumps(tags, indent=2, ensure_ascii=False))
    else:
        print("未查询到分类标签记录")
