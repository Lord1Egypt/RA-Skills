#!/usr/bin/env python3
"""上传日报到 IMA 知识库

用法:
    python3 ima_upload.py --file <日报文件> --kb-id <知识库ID> --title <文件标题>

环境要求:
    - ~/.config/ima/client_id  包含 IMA client_id
    - ~/.config/ima/api_key    包含 IMA api_key
    - Node.js 环境中有 cos-upload.cjs 脚本（来自 ima-skills skill）
"""
import json
import urllib.request
import os
import subprocess
import argparse
import sys

def load_credentials():
    """加载 IMA API 凭证"""
    client_id_path = os.path.expanduser("~/.config/ima/client_id")
    api_key_path = os.path.expanduser("~/.config/ima/api_key")
    
    if not os.path.exists(client_id_path):
        print(f"错误：找不到 IMA client_id 文件: {client_id_path}")
        print("请先配置 IMA API 凭证。参考 ima-skills skill 的配置说明。")
        sys.exit(1)
    
    if not os.path.exists(api_key_path):
        print(f"错误：找不到 IMA api_key 文件: {api_key_path}")
        print("请先配置 IMA API 凭证。参考 ima-skills skill 的配置说明。")
        sys.exit(1)
    
    with open(client_id_path) as f:
        client_id = f.read().strip()
    with open(api_key_path) as f:
        api_key = f.read().strip()
    
    return client_id, api_key


def ima_api(path, body, client_id, api_key):
    """调用 IMA OpenAPI"""
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        f"https://ima.qq.com/{path}",
        data=data,
        headers={
            "ima-openapi-clientid": client_id,
            "ima-openapi-apikey": api_key,
            "ima-openapi-ctx": "skill_version=1.0.0",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def find_cos_upload_script():
    """查找 cos-upload.cjs 脚本路径"""
    possible_paths = [
        os.path.expanduser("~/.workbuddy/skills/ima-skills/knowledge-base/scripts/cos-upload.cjs"),
        os.path.expanduser("~/.workbuddy/skills/腾讯ima/knowledge-base/scripts/cos-upload.cjs"),
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    # 尝试搜索
    for root, dirs, files in os.walk(os.path.expanduser("~/.workbuddy/skills")):
        for f in files:
            if f == "cos-upload.cjs":
                return os.path.join(root, f)
    
    return None


def find_node_path():
    """查找 Node.js 可执行文件路径"""
    # 优先使用 managed node
    managed_node = os.path.expanduser("~/.workbuddy/binaries/node/versions/22.12.0/bin/node")
    if os.path.exists(managed_node):
        return managed_node
    
    # 尝试系统 node
    result = subprocess.run(["which", "node"], capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    
    return None


def upload_to_ima(file_path, kb_id, title, client_id, api_key):
    """上传文件到 IMA 知识库"""
    # 1. 读取文件
    with open(file_path, "rb") as f:
        file_content = f.read()
    file_size = len(file_content)
    print(f"文件大小: {file_size} bytes")
    
    media_type = 7  # markdown
    
    # 2. 创建 media
    print("\n=== 创建 Media ===")
    result = ima_api("openapi/wiki/v1/create_media", {
        "file_name": title,
        "file_size": file_size,
        "content_type": "text/markdown",
        "knowledge_base_id": kb_id,
        "file_ext": "md"
    }, client_id, api_key)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    if result.get("code") != 0:
        print(f"创建 Media 失败: {result.get('msg')}")
        return False
    
    media_id = result["data"]["media_id"]
    cos_credential = result["data"]["cos_credential"]
    
    # 3. 上传到 COS
    print("\n=== 上传到 COS ===")
    cos_script = find_cos_upload_script()
    if not cos_script:
        print("错误：找不到 cos-upload.cjs 脚本")
        print("请确保 ima-skills skill 已安装")
        return False
    
    node_path = find_node_path()
    if not node_path:
        print("错误：找不到 Node.js 可执行文件")
        return False
    
    cos_cmd = [
        node_path, cos_script,
        "--file", file_path,
        "--secret-id", cos_credential["secret_id"],
        "--secret-key", cos_credential["secret_key"],
        "--token", cos_credential["token"],
        "--bucket", cos_credential["bucket_name"],
        "--region", cos_credential["region"],
        "--cos-key", cos_credential["cos_key"],
        "--content-type", "text/markdown",
        "--start-time", str(cos_credential["start_time"]),
        "--expired-time", str(cos_credential["expired_time"])
    ]
    
    result_cos = subprocess.run(cos_cmd, capture_output=True, text=True)
    print("COS stdout:", result_cos.stdout)
    if result_cos.stderr:
        print("COS stderr:", result_cos.stderr)
    
    if result_cos.returncode != 0:
        print("COS 上传失败！")
        return False
    
    # 4. 添加到知识库
    print("\n=== 添加到知识库 ===")
    result = ima_api("openapi/wiki/v1/add_knowledge", {
        "media_type": media_type,
        "media_id": media_id,
        "title": title,
        "knowledge_base_id": kb_id,
        "file_info": {
            "cos_key": cos_credential["cos_key"],
            "file_size": file_size,
            "file_name": title
        }
    }, client_id, api_key)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    if result.get("code") == 0:
        print("\n上传成功！已添加到知识库")
        return True
    else:
        print(f"\n添加到知识库失败: {result.get('msg')}")
        return False


def main():
    parser = argparse.ArgumentParser(description="上传日报到 IMA 知识库")
    parser.add_argument("--file", required=True, help="日报文件路径")
    parser.add_argument("--kb-id", required=True, help="IMA 知识库 ID")
    parser.add_argument("--title", default=None, help="文件标题（默认使用文件名）")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        print(f"错误：文件不存在: {args.file}")
        sys.exit(1)
    
    title = args.title or os.path.basename(args.file)
    
    client_id, api_key = load_credentials()
    success = upload_to_ima(args.file, args.kb_id, title, client_id, api_key)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
