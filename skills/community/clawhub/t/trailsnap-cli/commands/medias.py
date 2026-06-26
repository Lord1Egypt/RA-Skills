import json
import os
from utils import make_request,load_env

def setup_parser(subparsers):
    parser = subparsers.add_parser("medias", help="获取和管理媒体文件")
    sub_subparsers = parser.add_subparsers(dest="subcommand", help="可用操作")
    sub_subparsers.required = True

    get_parser = sub_subparsers.add_parser("get", help="获取媒体文件")
    get_parser.add_argument("--photo-id", type=str, default=100, help="照片ID")
    get_parser.add_argument("--size", type=str, default="medium", help="照片质量，默认 medium，可选值：small,medium,large")
    # 输出格式，默认 URL
    get_parser.add_argument("--format", type=str, default="url", help="输出格式，默认 URL，可选值：url,base64,file")
    # 输出文件路径，默认不保存
    get_parser.add_argument("--output", type=str, default=None, help="输出文件路径，默认不保存，仅当format为file时有效")
    get_parser.set_defaults(func=execute_get)

def execute_get(args):
    env = load_env()
    photo_id = args.photo_id
    size = args.size
    if size not in ["small", "medium", "large"]:
        print("错误：size参数值必须为 small,medium,large 中的一个")
        return
    format = args.format
    if format not in ["url", "base64", "file"]:
        print("错误：format参数值必须为 url,base64,file 中的一个")
        return
    output = args.output
    if format == "url":
        base_url = env.get("TRAILSNAP_API_URL", "")
        if not base_url:
            print("错误：TRAILSNAP_API_URL环境变量未设置")
            return
        if size == 'large':
            print(base_url + f"/medias/{photo_id}/file")
        else:
            print(base_url + f"/medias/{photo_id}/thumbnail?size={size}")
    elif format == "base64":
        data = make_request(f"/medias/{photo_id}/thumbnail?size={size}&format=base64")
        print(data["base64"])
    elif format == "file":
        if not output:
            print("错误：output参数值不能为空")
            return
        data = make_request(f"/medias/{photo_id}/file", method="GET", response_type="bytes")
        with open(output, "wb") as f:
            f.write(data)
        print(f"将文件保存到 {output}")
