import json
from utils import make_request

def setup_parser(subparsers):
    parser = subparsers.add_parser("people", help="管理和查询人物（面部识别）")
    sub_subparsers = parser.add_subparsers(dest="subcommand", help="可用操作")
    sub_subparsers.required = True

    list_parser = sub_subparsers.add_parser("list", help="查询人物列表")
    list_parser.add_argument("--limit", type=int, default=100, help="返回的记录数，默认 100")
    # types: named,unnamed,hidden（允许多个值）
    list_parser.add_argument("--types", type=str, default="named", help="查询类型，默认 named, 可选值：named,unnamed,hidden 中的一个或多个,逗号分隔")
    list_parser.set_defaults(func=execute_list)

def execute_list(args):
    # 验证types参数值是否有效
    valid_types = {"named", "unnamed", "hidden"}
    if not set(args.types.split(",")) <= valid_types:
        print("错误：types参数值必须为 named,unnamed,hidden 中的一个或多个")
        return

    # 转换types参数值为列表
    args.types = args.types.split(",")
    data = make_request("/faces/identities", {"page": 1, "limit": args.limit, "types": args.types})
    if data:
        identities = [{
            "id": identity["id"],
            "name": identity["identity_name"],
            "tags": identity["tags"],
            "description": identity["description"],
            "face_count": identity["face_count"]
        } for identity in data]
        print(json.dumps(identities, indent=2, ensure_ascii=False))
    else:
        print("未查询到人物记录")
