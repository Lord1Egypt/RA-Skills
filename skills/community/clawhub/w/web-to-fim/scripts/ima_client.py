#!/usr/bin/env python3
"""
Tencent IMA Notes API Client (v1.1.7 — updated 2026-07-10)

云端 API 服务，无需本地客户端。
基于 IMA OpenAPI 1.1.7 规范更新，修复了 API 端点和请求格式。

API 信息:
- Base URL: https://ima.qq.com
- Notes API Path: /openapi/note/v1/
- 认证: ima-openapi-clientid + ima-openapi-apikey (header)
- 环境变量: IMA_OPENAPI_CLIENTID / IMA_OPENAPI_APIKEY (优先)
           或 IMA_CLIENT_ID / IMA_API_KEY (兼容旧版)

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
    BASE_URL = "https://ima.qq.com"
    NOTES_PATH = "/openapi/note/v1"
    WIKI_PATH = "/openapi/wiki/v1"

    def __init__(self, client_id: str = None, api_key: str = None):
        self.client_id = (
            client_id
            or os.environ.get("IMA_OPENAPI_CLIENTID")
            or os.environ.get("IMA_CLIENT_ID")
        )
        self.api_key = (
            api_key
            or os.environ.get("IMA_OPENAPI_APIKEY")
            or os.environ.get("IMA_API_KEY")
        )

        if not self.client_id or not self.api_key:
            raise ValueError(
                "缺少 IMA 凭证。请设置环境变量 IMA_OPENAPI_CLIENTID 和 IMA_OPENAPI_APIKEY，"
                "或参考 references/ima-setup.md 获取凭证"
            )

    def _headers(self) -> Dict[str, str]:
        return {
            "ima-openapi-clientid": self.client_id,
            "ima-openapi-apikey": self.api_key,
            "Content-Type": "application/json"
        }

    def _post(self, api_name: str, payload: dict, path: str = None) -> dict:
        """Send POST request to IMA API and return parsed data.

        Args:
            api_name: API endpoint name (e.g. "import_doc", "add_knowledge")
            payload: Request body
            path: API path prefix. Defaults to NOTES_PATH. Use WIKI_PATH for knowledge base APIs.
        """
        base_path = path or self.NOTES_PATH
        url = f"{self.BASE_URL}{base_path}/{api_name}"
        resp = requests.post(url, headers=self._headers(), json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != 0:
            raise Exception(f"IMA API 错误 [{api_name}]: {data.get('msg', '未知错误')} (code={data.get('code')})")
        return data.get("data", {})

    def test_connection(self) -> bool:
        """Test connection by listing notebooks (limit 1)."""
        try:
            url = f"{self.BASE_URL}{self.NOTES_PATH}/list_notebook"
            payload = {"cursor": "0", "limit": 1}
            resp = requests.post(url, headers=self._headers(), json=payload, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("code") == 0
            return False
        except Exception:
            return False

    def list_notebooks(self, cursor: str = "0", limit: int = 20) -> List[Dict[str, Any]]:
        """List notebooks (笔记本列表)."""
        payload = {"cursor": cursor, "limit": limit}
        data = self._post("list_notebook", payload)
        return data.get("note_folder_infos", [])

    def list_notes(self, folder_id: str = None, cursor: str = "", limit: int = 20) -> List[Dict[str, Any]]:
        """List notes in a notebook (列出笔记)."""
        payload = {"cursor": cursor, "limit": limit}
        if folder_id:
            payload["folder_id"] = folder_id
        data = self._post("list_note", payload)
        return data.get("note_book_list", [])

    def create_note(self, title: str, content: str = "", folder_name: str = None, folder_id: str = None) -> Dict[str, Any]:
        """Create a new note from Markdown content (新建笔记).

        Uses import_doc API. Note: IMA API doesn't accept a separate title field;
        the title is extracted from the first H1 in the content.
        """
        payload = {
            "content_format": 1,  # MARKDOWN
            "content": content,
        }
        if folder_name:
            payload["folder_name"] = folder_name
        if folder_id:
            payload["folder_id"] = folder_id

        data = self._post("import_doc", payload)
        note_id = data.get("note_id", "")
        return {
            "note_id": note_id,
            "title": title,
            "url": f"https://ima.qq.com/note/{note_id}" if note_id else ""
        }

    # ========== Knowledge Base (Wiki) API ==========

    def search_knowledge_base(self, query: str, cursor: str = "", limit: int = 20) -> List[Dict[str, Any]]:
        """Search knowledge bases by name (搜索知识库列表)."""
        payload = {"query": query, "cursor": cursor, "limit": limit}
        data = self._post("search_knowledge_base", payload, path=self.WIKI_PATH)
        return data.get("info_list", [])

    def get_addable_knowledge_base_list(self, cursor: str = "", limit: int = 50) -> List[Dict[str, Any]]:
        """List knowledge bases that the user can add content to (获取可添加的知识库列表)."""
        payload = {"cursor": cursor, "limit": limit}
        data = self._post("get_addable_knowledge_base_list", payload, path=self.WIKI_PATH)
        return data.get("addable_knowledge_base_list", [])

    def find_knowledge_base_by_name(self, name: str) -> str:
        """Find a knowledge base ID by exact name match. Raises if not found."""
        results = self.search_knowledge_base(query=name)
        for kb in results:
            if kb.get("kb_name") == name or kb.get("name") == name:
                return kb.get("kb_id") or kb.get("id")
        raise ValueError(f"未找到名为「{name}」的知识库。可用知识库：{[kb.get('kb_name', kb.get('name')) for kb in results]}")

    def get_root_folder_id(self, knowledge_base_id: str) -> str:
        """Get the root folder ID of a knowledge base.

        IMA API docs say "root folder_id equals knowledge_base_id", but in practice
        the root folder has a separate numeric ID. This method fetches it via
        get_knowledge_list and extracts from current_path[0].folder_id.
        """
        data = self.get_knowledge_list(knowledge_base_id=knowledge_base_id, limit=1)
        current_path = data.get("current_path", [])
        if current_path:
            return current_path[0].get("folder_id", "")
        raise ValueError(f"无法获取知识库 {knowledge_base_id} 的根目录 folder_id")

    def add_note_to_knowledge_base(self, note_id: str, title: str, knowledge_base_id: str, folder_id: str = None) -> Dict[str, Any]:
        """Add an existing note to a knowledge base (添加笔记到知识库).

        Two-step flow: create_note() → add_note_to_knowledge_base().
        Uses add_knowledge API with media_type=11 (笔记).

        Args:
            note_id: The note ID returned by create_note()
            title: Note title
            knowledge_base_id: Target knowledge base ID
            folder_id: Target folder ID within the knowledge base (optional, defaults to root)
        """
        payload = {
            "media_type": 11,  # 笔记
            "title": title,
            "knowledge_base_id": knowledge_base_id,
            "note_info": {"content_id": note_id},
        }
        if folder_id:
            payload["folder_id"] = folder_id

        data = self._post("add_knowledge", payload, path=self.WIKI_PATH)
        return {
            "media_id": data.get("media_id", ""),
            "knowledge_base_id": knowledge_base_id,
            "note_id": note_id,
        }

    def get_knowledge_list(self, knowledge_base_id: str, folder_id: str = None, cursor: str = "", limit: int = 50) -> Dict[str, Any]:
        """Browse knowledge base contents (浏览知识库内容)."""
        payload = {
            "knowledge_base_id": knowledge_base_id,
            "cursor": cursor,
            "limit": limit,
        }
        if folder_id:
            payload["folder_id"] = folder_id
        return self._post("get_knowledge_list", payload, path=self.WIKI_PATH)

    def import_urls(self, knowledge_base_id: str, urls: List[str], folder_id: str = None) -> List[Dict[str, Any]]:
        """Import web URLs / WeChat articles to a knowledge base (导入URL).

        IMA server-side fetches the URL content, preserving images and layout.
        This is the preferred method for 公众号/网页 URLs (vs create_note which is plain text).

        Args:
            knowledge_base_id: Target knowledge base ID
            urls: List of URLs (1-10)
            folder_id: Target folder ID. If None, auto-fetches root folder ID
                       (note: root folder_id is NOT equal to knowledge_base_id despite docs)
        """
        if not folder_id:
            folder_id = self.get_root_folder_id(knowledge_base_id)
        payload = {
            "knowledge_base_id": knowledge_base_id,
            "folder_id": folder_id,
            "urls": urls,
        }
        data = self._post("import_urls", payload, path=self.WIKI_PATH)
        results = []
        for url, info in data.get("results", {}).items():
            results.append({
                "url": url,
                "ret_code": info.get("ret_code", -1),
                "media_id": info.get("media_id", ""),
                "success": info.get("ret_code") == 0,
            })
        return results

    def append_note(self, note_id: str, content: str) -> bool:
        """Append content to an existing note (追加内容到笔记)."""
        payload = {
            "note_id": note_id,
            "content_format": 1,  # MARKDOWN
            "content": content,
        }
        self._post("append_doc", payload)
        return True

    def get_note_content(self, note_id: str, content_format: int = 0) -> str:
        """Get note content (获取笔记内容). content_format: 0=PLAINTEXT, 1=MARKDOWN(not supported), 2=JSON."""
        payload = {
            "note_id": note_id,
            "target_content_format": content_format,
        }
        data = self._post("get_doc_content", payload)
        return data.get("content", "")

    def search_notes(self, keyword: str, search_type: int = 0, start: int = 0, end: int = 20) -> List[Dict[str, Any]]:
        """Search notes (搜索笔记). search_type: 0=TITLE, 1=CONTENT."""
        payload = {
            "search_type": search_type,
            "query_info": {"title": keyword} if search_type == 0 else {"content": keyword},
            "start": start,
            "end": end,
        }
        data = self._post("search_note", payload)
        return data.get("search_note_infos", [])


def main():
    import argparse

    parser = argparse.ArgumentParser(description="腾讯 IMA 笔记 API 客户端 (v1.1.7)")
    parser.add_argument("--action", choices=["test", "list", "list-notebook", "create", "search"], default="test", help="操作类型")
    parser.add_argument("--title", help="笔记标题（用于 create 时信息展示，实际标题从 content H1 提取）")
    parser.add_argument("--content", help="笔记内容或内容文件路径")
    parser.add_argument("--note-id", help="笔记 ID")
    parser.add_argument("--keyword", help="搜索关键词")
    parser.add_argument("--limit", type=int, default=20, help="返回数量限制")
    args = parser.parse_args()

    try:
        client = IMAClient()

        if args.action == "test":
            if client.test_connection():
                print("✅ IMA 连接成功")
            else:
                print("❌ IMA 连接失败")

        elif args.action == "list":
            notes = client.list_notes(limit=args.limit)
            print(f"📚 笔记列表 ({len(notes)} 个):")
            for note in notes:
                info = note.get("note_book_info", note)
                print(f"   - {info.get('title', '未命名')} (ID: {info.get('note_id')})")

        elif args.action == "list-notebook":
            notebooks = client.list_notebooks(limit=args.limit)
            print(f"📓 笔记本列表 ({len(notebooks)} 个):")
            for nb in notebooks:
                print(f"   - {nb.get('name', '未命名')} (ID: {nb.get('folder_id')}, 笔记数: {nb.get('note_number', 0)})")

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

            # 确保内容以 H1 标题开头（IMA 从 H1 提取标题）
            if not content.startswith("# "):
                content = f"# {args.title}\n\n{content}"

            result = client.create_note(title=args.title, content=content)
            print(f"✅ 笔记创建成功!")
            print(f"   ID: {result['note_id']}")
            print(f"   URL: {result['url']}")

        elif args.action == "search":
            if not args.keyword:
                print("❌ 需要指定 --keyword")
                return

            results = client.search_notes(keyword=args.keyword)
            print(f"🔍 搜索结果 ({len(results)} 个):")
            for r in results:
                info = r.get("note_book_info", r)
                print(f"   - {info.get('title', '未命名')} (ID: {info.get('note_id')})")

    except Exception as e:
        print(f"❌ 错误: {e}")


if __name__ == "__main__":
    main()
