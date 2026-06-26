"""
upload_cover.py - 仅上传封面图到永久素材

用法:
  python upload_cover.py <封面图路径>

输出:
  media_id - 用于后续创建草稿
"""
import json
import os
import sys

try:
    import requests
except ImportError:
    print("❌ 缺少 requests 库，请安装：pip install requests")
    sys.exit(1)


API_BASE = "https://api.weixin.qq.com"
CREDENTIALS_FILE = "wechat_credentials.json"


def load_credentials():
    if not os.path.exists(CREDENTIALS_FILE):
        raise FileNotFoundError(f"❌ 找不到凭证文件：{CREDENTIALS_FILE}")

    with open(CREDENTIALS_FILE, "r", encoding="utf-8") as f:
        creds = json.load(f)

    return creds["appid"], creds["appsecret"]


def get_access_token(appid, appsecret):
    url = f"{API_BASE}/cgi-bin/token"
    params = {
        "grant_type": "client_credential",
        "appid": appid,
        "secret": appsecret
    }
    resp = requests.get(url, params=params, timeout=30)
    data = resp.json()

    if "errcode" in data and data["errcode"] != 0:
        raise Exception(f"获取 Token 失败：{data.get('errmsg', '未知错误')}")

    return data["access_token"]


def upload_cover(token, file_path):
    url = f"{API_BASE}/cgi-bin/material/add_material"
    params = {"access_token": token, "type": "image"}

    print(f"上传封面图：{os.path.basename(file_path)}...")

    with open(file_path, "rb") as f:
        files = {"media": (os.path.basename(file_path), f, "image/png")}
        resp = requests.post(url, params=params, files=files, timeout=60)

    data = resp.json()

    if "errcode" in data and data["errcode"] != 0:
        raise Exception(f"上传失败：{data.get('errmsg', '未知错误')}")

    return data["media_id"]


def main():
    if len(sys.argv) < 2:
        print("用法: python upload_cover.py <封面图路径>")
        print("输出: media_id")
        sys.exit(1)

    cover_path = sys.argv[1]

    if not os.path.exists(cover_path):
        print(f"❌ 找不到封面图：{cover_path}")
        sys.exit(1)

    # 检查文件大小
    file_size = os.path.getsize(cover_path)
    max_size = 2 * 1024 * 1024
    if file_size > max_size:
        print(f"❌ 图片太大（{file_size / 1024 / 1024:.1f}MB），限制 2MB")
        sys.exit(1)

    appid, appsecret = load_credentials()
    token = get_access_token(appid, appsecret)
    media_id = upload_cover(token, cover_path)

    print(f"\n✅ 上传成功！")
    print(f"media_id = {media_id}")
    print(f"\n下一步：使用此 media_id 创建草稿")


if __name__ == "__main__":
    main()
