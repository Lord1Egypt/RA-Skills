import os
import sys
import zipfile
import requests
import argparse
import tempfile
import json
from pathlib import Path

def create_zip(source_dir, zip_path):
    """将目录打包为 ZIP，确保 index.html 在根目录或一级子目录"""
    has_index = False
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                if arcname == "index.html" or arcname.endswith("/index.html"):
                    has_index = True
                zipf.write(file_path, arcname)
    return has_index

def check_zip_for_index(zip_path):
    """检查 ZIP 文件内部是否包含 index.html"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            for name in zipf.namelist():
                if name == "index.html" or name.endswith("/index.html"):
                    return True
    except zipfile.BadZipFile:
        return False
    return False

def call_api(method, url, api_key, files=None, data=None, params=None):
    """通用 API 调用封装"""
    headers = {"X-ProtoHub-API-Key": api_key}
    try:
        response = requests.request(method, url, headers=headers, files=files, data=data, params=params)
        if response.status_code == 200:
            res_json = response.json()
            if res_json.get("code") == 0:
                return res_json.get("data")
            else:
                print(f"❌ API 错误: {res_json.get('msg')}")
        else:
            print(f"❌ HTTP 错误: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ 请求异常: {str(e)}")
    return None

def upload_prototype(api_url, api_key, zip_path, name=None, remark=None, prototype_id=None):
    """上传或更新原型"""
    with open(zip_path, "rb") as f:
        files = {"file": f}
        data = {}
        if name: data["name"] = name
        if remark: data["remark"] = remark

        if prototype_id:
            url = f"{api_url}/admin-api/proto/agent/update/{prototype_id}"
            print(f"正在更新原型 (ID: {prototype_id})...")
            result = call_api("PUT", url, api_key, files=files, data=data)
            if result:
                print("\n✅ 更新成功!")
                return result
        else:
            url = f"{api_url}/admin-api/proto/agent/upload"
            print("正在上传新原型...")
            result = call_api("POST", url, api_key, files=files, data=data)
            if result:
                print("\n✅ 发布成功!")
                print(f"原型 ID:   {result.get('id')}")
                print(f"预览链接:  {result.get('previewUrl')}")
                print(f"分享链接:  {result.get('shareUrl')}")
                return result
    return None

def list_prototypes(api_url, api_key, name=None, page_no=1, page_size=10):
    """查询原型列表"""
    url = f"{api_url}/admin-api/proto/agent/page"
    params = {"pageNo": page_no, "pageSize": page_size}
    if name:
        params["name"] = name
    
    print(f"正在查询原型列表 (名称: {name if name else '所有'})...")
    result = call_api("GET", url, api_key, params=params)
    if result and "list" in result:
        print(f"\n找到 {result['total']} 个原型:")
        print("-" * 120)
        print(f"{'ID':<8} | {'名称':<20} | {'分享链接':<60} | {'预览链接'}")
        print("-" * 120)
        for item in result["list"]:
            print(f"{item['id']:<8} | {item['name']:<20} | {item['shareUrl']:<60} | {item['previewUrl']}")
        return result
    return None

def get_preview_link(api_url, api_key, prototype_id):
    """获取原型链接"""
    url = f"{api_url}/admin-api/proto/agent/get-link/{prototype_id}"
    print(f"正在获取原型 ID: {prototype_id} 的链接...")
    result = call_api("GET", url, api_key)
    if result:
        print(f"\n预览链接: {result.get('previewUrl')}")
        print(f"分享链接: {result.get('shareUrl')}")
        return result
    return None

def main():
    parser = argparse.ArgumentParser(description="ProtoHub AI Agent 工具箱")
    subparsers = parser.add_subparsers(dest="action", help="执行操作")

    # Upload/Update sub-command
    publish_parser = subparsers.add_parser("publish", help="发布或更新原型")
    publish_parser.add_argument("source", help="原型目录路径或 ZIP 文件路径")
    publish_parser.add_argument("--id", type=int, help="要更新的原型 ID (可选)")
    publish_parser.add_argument("--name", help="原型的友好名称")
    publish_parser.add_argument("--remark", help="版本备注")

    # List sub-command
    list_parser = subparsers.add_parser("list", help="查询原型列表")
    list_parser.add_argument("--name", help="按名称筛选")
    list_parser.add_argument("--page", type=int, default=1, help="页码")
    list_parser.add_argument("--size", type=int, default=10, help="每页数量")

    # Get Link sub-command
    link_parser = subparsers.add_parser("get-link", help="获取预览链接")
    link_parser.add_argument("id", type=int, help="原型 ID")

    # Global options
    default_url = os.environ.get("PROTOHUB_URL", "http://localhost:48080")
    parser.add_argument("--url", default=default_url, help=f"ProtoHub API 基础地址 (当前默认: {default_url})")
    parser.add_argument("--key", help="ProtoHub API 密钥 (也可通过环境变量 PROTOHUB_API_KEY 设置)")

    # Legacy support for direct path (assumes publish)
    if len(sys.argv) > 1 and sys.argv[1] not in ["publish", "list", "get-link", "-h", "--help"]:
        # If the first argument is a path, insert 'publish'
        if os.path.exists(sys.argv[1]):
            sys.argv.insert(1, "publish")

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        sys.exit(0)

    api_key = args.key or os.environ.get("PROTOHUB_API_KEY")
    api_url = args.url

    if not api_key:
        print("❌ 错误：缺少 API 密钥。")
        sys.exit(1)

    if args.action == "publish":
        source_path = Path(args.source).resolve()
        if not source_path.exists():
            print(f"❌ 错误：路径 {source_path} 不存在。")
            sys.exit(1)

        final_zip_path = None
        is_temp_zip = False

        try:
            if source_path.is_dir():
                with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp_zip:
                    final_zip_path = tmp_zip.name
                is_temp_zip = True
                print(f"正在打包目录: {source_path} ...")
                if not create_zip(source_path, final_zip_path):
                    print("❌ 错误：在源目录中未找到 index.html 入口文件。上传已取消。")
                    sys.exit(1)
            elif source_path.suffix.lower() == ".zip":
                final_zip_path = str(source_path)
                print(f"检测到 ZIP 文件: {source_path}，正在验证内容...")
                if not check_zip_for_index(final_zip_path):
                    print("❌ 错误：指定的 ZIP 文件中未找到 index.html 入口文件。上传已取消。")
                    sys.exit(1)
            else:
                print(f"❌ 错误：{source_path} 既不是目录也不是 ZIP 文件。")
                sys.exit(1)

            upload_prototype(api_url, api_key, final_zip_path, args.name, args.remark, args.id)
        finally:
            if is_temp_zip and final_zip_path and os.path.exists(final_zip_path):
                os.remove(final_zip_path)

    elif args.action == "list":
        list_prototypes(api_url, api_key, args.name, args.page, args.size)

    elif args.action == "get-link":
        get_preview_link(api_url, api_key, args.id)

if __name__ == "__main__":
    main()
