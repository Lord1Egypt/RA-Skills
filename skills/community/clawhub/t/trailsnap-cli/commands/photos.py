import json
from utils import make_request

def setup_parser(subparsers):
    parser = subparsers.add_parser("photos", help="管理和查询照片")
    sub_subparsers = parser.add_subparsers(dest="subcommand", help="可用操作")
    sub_subparsers.required = True

    # list subcommand
    list_parser = sub_subparsers.add_parser("list", help="查询照片列表")
    list_parser.add_argument("--skip", type=int, default=0, help="跳过 N 张照片")
    list_parser.add_argument("--limit", type=int, default=10, help="限制返回 N 张照片")
    list_parser.add_argument("--album-id", help="按相册 ID 过滤")
    list_parser.add_argument("--city", help="按城市过滤")
    list_parser.add_argument("--province", help="按省份过滤")
    list_parser.add_argument("--make", help="按相机品牌过滤")
    list_parser.add_argument("--model", help="按相机型号过滤")
    list_parser.set_defaults(func=execute_list)

    # info subcommand
    info_parser = sub_subparsers.add_parser("info", help="获取单张照片信息")
    info_parser.add_argument("--photo-id", required=True, help="照片ID")
    info_parser.set_defaults(func=execute_info)

    # delete subcommand
    delete_parser = sub_subparsers.add_parser("delete", help="删除照片")
    delete_parser.add_argument("--photo-id", required=True, help="照片ID")
    delete_parser.set_defaults(func=execute_delete)

def execute_list(args):
    params = {
        "skip": args.skip,
        "limit": args.limit,
        "album_id": args.album_id,
        "city": args.city,
        "province": args.province,
        "make": args.make,
        "model": args.model
    }
    data = make_request("/photos", params)
    if data:
        photos = [
            {
                "id": photo["id"],
                "filename": photo["filename"],
                "file_type": photo["file_type"],
                "photo_time": photo["photo_time"]
            }
            for photo in data
        ]
        print(json.dumps(photos, indent=2, ensure_ascii=False))
    else:
        print("没有查询到照片列表")

def execute_info(args):
    data = make_request(f"/photos/{args.photo_id}/metadata")
    description_data = make_request(f"/photos/{args.photo_id}/description")
    if not description_data:
        description_data = {}
    if data:
        info = {
            "file_path": data["file_path"],
            "address": data["address"],
            "albums": data["albums"],
            "tags": data["tags"],
            "faces_identities": data["faces_identities"],
            "description": description_data
        }
        print(json.dumps(info, indent=2, ensure_ascii=False))
    else:
        print("未查询到照片信息")

def execute_delete(args):
    data = make_request(f"/photos/{args.photo_id}", method="DELETE")
    if data:
        print(f"照片 {args.photo_id} 删除成功")
    else:
        print("照片删除失败或不存在")
