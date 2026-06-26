#!/usr/bin/env python3
"""
Feishu (Lark) Cloud Document API Client

安全说明:
- 所有凭证通过环境变量读取，不硬编码
- 支持 .env 文件加载（需 python-dotenv）
- 凭证不写入日志或任何输出

Usage:
    from feishu_client import FeishuClient
    client = FeishuClient()
    doc_id = client.create_document(title="我的笔记", content_md="# Hello")
"""

import os
import json
import re
import time
from typing import Optional, Dict, Any, List
from urllib.parse import urlencode

try:
    import requests
except ImportError:
    print("❌ requests 库未安装: pip install requests")
    raise


class FeishuClient:
    BASE_URL = "https://open.feishu.cn/open-apis"

    def __init__(self, app_id: str = None, app_secret: str = None):
        self.app_id = app_id or os.environ.get("FEISHU_APP_ID")
        self.app_secret = app_secret or os.environ.get("FEISHU_APP_SECRET")
        self._tenant_access_token = None
        self._token_expires_at = 0

        if not self.app_id or not self.app_secret:
            raise ValueError(
                "缺少飞书凭证。请设置环境变量 FEISHU_APP_ID 和 FEISHU_APP_SECRET，"
                "或参考 references/feishu-setup.md 获取凭证"
            )

    def _get_token(self) -> str:
        """获取 tenant_access_token，带缓存"""
        if self._tenant_access_token and time.time() < self._token_expires_at:
            return self._tenant_access_token

        url = f"{self.BASE_URL}/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }

        resp = requests.post(url, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        if data.get("code") != 0:
            raise Exception(f"获取飞书 Token 失败: {data.get('msg')}")

        self._tenant_access_token = data["tenant_access_token"]
        self._token_expires_at = time.time() + data.get("expire", 7200) - 60
        return self._tenant_access_token

    def _headers(self) -> Dict[str, str]:
        """生成认证头"""
        return {
            "Authorization": f"Bearer {self._get_token()}",
            "Content-Type": "application/json"
        }

    def test_connection(self) -> bool:
        """验证飞书连接"""
        try:
            self._get_token()
            return True
        except Exception:
            return False

    def create_document(self, title: str, content_md: str = "") -> Dict[str, Any]:
        """
        创建飞书云文档

        Args:
            title: 文档标题
            content_md: Markdown 格式的文档内容

        Returns:
            包含文档信息的字典，包括 document_id
        """
        url = f"{self.BASE_URL}/docx/v1/documents"
        payload = {"title": title}
        resp = requests.post(url, headers=self._headers(), json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        if data.get("code") != 0:
            raise Exception(f"创建飞书文档失败: {data.get('msg')}")

        doc = data["data"]["document"]
        document_id = doc["document_id"]

        if content_md:
            self._insert_blocks(document_id, content_md)

        return {
            "document_id": document_id,
            "title": title,
            "url": f"https://.feishu.cn/docx/{document_id}"
        }

    def _insert_blocks(self, document_id: str, content_md: str) -> None:
        """将 Markdown 内容插入文档"""
        blocks = self._md_to_blocks(content_md)

        url = f"{self.BASE_URL}/docx/v1/documents/{document_id}/blocks/{document_id}/children"
        payload = {"children": blocks, "index": -1}

        resp = requests.post(url, headers=self._headers(), json=payload, timeout=30)
        resp.raise_for_status()

    def _md_to_blocks(self, md: str) -> List[Dict]:
        """将 Markdown 转换为飞书文档块格式"""
        blocks = []
        lines = md.split("\n")
        in_code_block = False
        code_content = []

        for line in lines:
            stripped = line.strip()

            if stripped.startswith("```"):
                if not in_code_block:
                    in_code_block = True
                    code_content = []
                else:
                    blocks.append({
                        "block_type": 2,
                        "code": {
                            "elements": [{"type": "text_run", "text_run": {"content": "\n".join(code_content)}}],
                            "language": 1
                        }
                    })
                    in_code_block = False
                    code_content = []
                continue

            if in_code_block:
                code_content.append(line)
                continue

            if stripped.startswith("# "):
                blocks.append({
                    "block_type": 3,
                    "heading1": {
                        "elements": [{"type": "text_run", "text_run": {"content": stripped[2:]}}],
                        "style": {}
                    }
                })
            elif stripped.startswith("## "):
                blocks.append({
                    "block_type": 4,
                    "heading2": {
                        "elements": [{"type": "text_run", "text_run": {"content": stripped[3:]}}],
                        "style": {}
                    }
                })
            elif stripped.startswith("### "):
                blocks.append({
                    "block_type": 5,
                    "heading3": {
                        "elements": [{"type": "text_run", "text_run": {"content": stripped[4:]}}],
                        "style": {}
                    }
                })
            elif stripped.startswith("- ") or stripped.startswith("* "):
                blocks.append({
                    "block_type": 12,
                    "bullet": {
                        "elements": [{"type": "text_run", "text_run": {"content": stripped[2:]}}],
                        "style": {}
                    }
                })
            elif stripped.startswith("> "):
                blocks.append({
                    "block_type": 11,
                    "quote": {
                        "elements": [{"type": "text_run", "text_run": {"content": stripped[2:]}}],
                        "style": {}
                    }
                })
            elif stripped.startswith("!["):
                match = re.match(r'!\[(.*?)\]\((.*?)\)', stripped)
                if match:
                    blocks.append({
                        "block_type": 10,
                        "image": {
                            "uri": match.group(2)
                        }
                    })
            elif stripped:
                blocks.append({
                    "block_type": 2,
                    "text": {
                        "elements": [{"type": "text_run", "text_run": {"content": stripped}}],
                        "style": {}
                    }
                })
            else:
                blocks.append({
                    "block_type": 2,
                    "text": {
                        "elements": [{"type": "text_run", "text_run": {"content": " "}}],
                        "style": {}
                    }
                })

        return blocks

    def get_document_info(self, document_id: str) -> Dict[str, Any]:
        """获取文档信息"""
        url = f"{self.BASE_URL}/docx/v1/documents/{document_id}"
        resp = requests.get(url, headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="飞书云文档 API 客户端")
    parser.add_argument("--action", choices=["test", "create"], default="test", help="操作类型")
    parser.add_argument("--title", help="文档标题")
    parser.add_argument("--content", help="Markdown 内容文件路径")
    args = parser.parse_args()

    try:
        client = FeishuClient()

        if args.action == "test":
            if client.test_connection():
                print("✅ 飞书连接成功")
            else:
                print("❌ 飞书连接失败")

        elif args.action == "create":
            if not args.title:
                print("❌ 需要指定 --title")
                return

            content = ""
            if args.content:
                with open(args.content, "r", encoding="utf-8") as f:
                    content = f.read()

            result = client.create_document(args.title, content)
            print(f"✅ 文档创建成功:")
            print(f"   ID: {result['document_id']}")
            print(f"   URL: {result['url']}")

    except ValueError as e:
        print(f"❌ 配置错误: {e}")
    except Exception as e:
        print(f"❌ 错误: {e}")


if __name__ == "__main__":
    main()
