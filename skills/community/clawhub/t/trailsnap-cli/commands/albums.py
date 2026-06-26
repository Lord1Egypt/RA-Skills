import json
from utils import make_request

def setup_parser(subparsers):
    parser = subparsers.add_parser("albums", help="管理和查询相册")
    sub_subparsers = parser.add_subparsers(dest="subcommand", help="可用操作")
    sub_subparsers.required = True

    list_parser = sub_subparsers.add_parser("list", help="查询相册列表")
    list_parser.add_argument("--skip", type=int, default=0, help="跳过 N 张相册")
    list_parser.add_argument("--limit", type=int, default=100, help="限制返回 N 张相册")
    list_parser.set_defaults(func=execute_list)

def execute_list(args):
    data = make_request("/albums", {"skip": args.skip, "limit": args.limit})
    if data:
        albums = [{
            "id": album["id"],
            "name": album["name"],
            "count": album["num_photos"],
            "description": album["description"],
            "condition": album["condition"],
            "type": album["type"]
        } for album in data]
        print(json.dumps(albums, indent=2, ensure_ascii=False))
    else:
        print("未查询到相册记录")
