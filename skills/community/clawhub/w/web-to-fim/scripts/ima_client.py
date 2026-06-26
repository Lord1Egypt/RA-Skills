#!/usr/bin/env python3
"""
Tencent IMA Notes API Client

云端 API 服务，无需本地客户端。

API 信息:
- 端点: https://ima.qq.com/openapi/note/v1
- 认证: ima-openapi-clientid + ima-openapi-apikey

Usage:
    from scripts.ima_client import IMAClient
    client = IMAClient()
    note = client.create_note(title="我的笔记", content="# Hello")
"""

import os
import json
from typing import Optional, Dict, Any, List

try:
    import requests
except ImportError:
    print("❌ requests 库未安装: pip install requests")
    raise


class IMAClient:
    BASE_URL = "https://ima.qq.com/openapi/note/v1"

    def __init__(self, client_id: str = None, api_key: str = None):
        self.client_id = client_id or os.environ.get("IMA_CLIENT_ID")
        self.api_key = api_key or os.environ.get("IMA_API_KEY")

        if not self.client_id or not self.api_key:
            raise ValueError(
                "缺少 ima 凭证。请设置环境变量 IMA_CLIENT_ID 和 IMA_API_KEY，"
                "或参考 references/ima-setup.md 获取凭证"
            )

    def _headers(self) -> Dict[str, str]:
        return {
            "ima-openapi-clientid": self.client_id,
            "ima-openapi-apikey": self.api_key,
            "Content-Type": "application/json"
        }

    def test_connection(self) -> bool:
        try:
            url = f"{self.BASE_URL}/note/list"
            resp = requests.get(url, headers=self._headers(), timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("code") == 0
            return False
        except Exception:
            return False

    def list_notes(self, limit: int = 20) -> List[Dict[str, Any]]:
        url = f"{self.BASE_URL}/note/list"
        payload = {"limit": limit}
        resp = requests.post(url, headers=self._headers(), json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != 0:
            raise Exception(f"获取笔记列表失败: {data.get('msg')}")
        return data.get("data", {}).get("notes", [])

    def create_note(self, title: str, content: str = "", folder_id: str = None) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/note/create"
        payload = {
            "title": title,
            "content": content,
            "format": "markdown"
        }
        if folder_id:
            payload["folder_id"] = folder_id

        resp = requests.post(url, headers=self._headers(), json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        if data.get("code") != 0:
            raise Exception(f"创建 ima 笔记失败: {data.get('msg')}")

        note_data = data.get("data", {}).get("note", {})
        return {
            "note_id": note_data.get("note_id"),
            "title": title,
            "url": note_data.get("url", f"https://ima.qq.com/note/{note_data.get('note_id')}")
        }

    def update_note(self, note_id: str, content: str, append: bool = True) -> bool:
        url = f"{self.BASE_URL}/note/update"
        payload = {
            "note_id": note_id,
            "content": content,
            "append": append
        }

        resp = requests.post(url, headers=self._headers(), json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get("code") == 0

    def get_note(self, note_id: str) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/note/get"
        payload = {"note_id": note_id}
        resp = requests.get(url, headers=self._headers(), params=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != 0:
            raise Exception(f"获取笔记失败: {data.get('msg')}")
        return data.get("data", {}).get("note", {})

    def search_notes(self, keyword: str, limit: int = 10) -> List[Dict[str, Any]]:
        url = f"{self.BASE_URL}/note/search"
        payload = {
            "query": keyword,
            "limit": limit
        }
        resp = requests.post(url, headers=self._headers(), json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != 0:
            raise Exception(f"搜索笔记失败: {data.get('msg')}")
        return data.get("data", {}).get("notes", [])


def main():
    import argparse

    parser = argparse.ArgumentParser(description="腾讯 ima 笔记 API 客户端")
    parser.add_argument("--action", choices=["test", "list", "create", "search"], default="test", help="操作类型")
    parser.add_argument("--title", help="笔记标题")
    parser.add_argument("--content", help="笔记内容或内容文件路径")
    parser.add_argument("--note-id", help="笔记 ID")
    parser.add_argument("--keyword", help="搜索关键词")
    parser.add_argument("--limit", type=int, default=20, help="返回数量限制")
    args = parser.parse_args()

    try:
        client = IMAClient()

        if args.action == "test":
            if client.test_connection():
                print("✅ ima 连接成功")
            else:
                print("❌ ima 连接失败")

        elif args.action == "list":
            notes = client.list_notes(limit=args.limit)
            print(f"📚 笔记列表 ({len(notes)} 个):")
            for note in notes:
                print(f"   - {note.get('title', '未命名')} (ID: {note.get('note_id')})")

        elif args.action == "create":
            if not args.title:
                print("❌ 需要指定 --title")
                return

            content = ""
            if args.content:
                if os.path.isfile(args.content):
                    with open(args.content, "r", encoding="utf-8") as f:
                        content = f.read()
                else:
                    content = args.content

            result = client.create_note(title=args.title, content=content)
            print(f"✅ 笔记创建成功!")
            print(f"   ID: {result['note_id']}")
            print(f"   URL: {result['url']}")

        elif args.action == "search":
            if not args.keyword:
                print("❌ 需要指定 --keyword")
                return

            notes = client.search_notes(keyword=args.keyword, limit=args.limit)
            print(f"🔍 搜索结果 ({len(notes)} 个):")
            for note in notes:
                print(f"   - {note.get('title', '未命名')} (ID: {note.get('note_id')})")

    except Exception as e:
        print(f"❌ 错误: {e}")


if __name__ == "__main__":
    main()
