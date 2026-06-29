# -*- coding: utf-8 -*-
"""
列出公众号草稿箱内容
"""
import urllib.request
import json
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from get_token import get_access_token

TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/draft/batchget?access_token={token}"
COUNT_URL = "https://api.weixin.qq.com/cgi-bin/draft/count?access_token={token}"


def count_drafts(token):
    url = COUNT_URL.format(token=token)
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"errcode": str(e)}


def list_drafts(token, offset=0, count=10, no_content=1):
    url = TOKEN_URL.format(token=token)
    data = json.dumps({"offset": offset, "count": count, "no_content": no_content}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def main():
    token = get_access_token()
    count_info = count_drafts(token)
    print(f"草稿总数: {count_info.get('total_count', 'N/A')}")
    print("=" * 50)

    result = list_drafts(token)
    if "item" in result and result["item"]:
        for item in result["item"]:
            for art in item.get("content", {}).get("news_item", []):
                print(f"标题: {art.get('title', 'N/A')}")
                print(f"作者: {art.get('author', 'N/A')}")
                print(f"摘要: {art.get('digest', 'N/A')[:80]}")
                print(f"Media ID: {item.get('media_id', 'N/A')}")
                print("-" * 50)
    else:
        print(f"草稿箱为空或接口返回: {result}")


if __name__ == "__main__":
    main()
