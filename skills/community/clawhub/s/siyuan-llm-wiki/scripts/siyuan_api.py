#!/usr/bin/env python3
"""
Siyuan Notes API Python Client
用于 LLM Wiki 工作流的思源笔记 API 封装

使用方法:
    from siyuan_api import SiyuanClient
    
    client = SiyuanClient(token="your-token", notebook_id="your-notebook-id")
    
    # 创建文档
    doc_id = client.create_doc("/sources/test", "# Hello\n\nWorld")
    
    # SQL 查询
    results = client.sql_query("SELECT * FROM blocks LIMIT 10")
"""

import json
import os
import requests
from typing import Optional, List, Dict, Any


class SiyuanClient:
    """思源笔记 API 客户端"""
    
    def __init__(self, token: str, notebook_id: str, base_url: str = None):
        if base_url is None:
            base_url = os.environ.get("SIYUAN_API", "http://127.0.0.1:6806")
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.notebook_id = notebook_id
        self.headers = {
            "Authorization": f"Token {token}",
            "Content-Type": "application/json"
        }
    
    def _post(self, endpoint: str, data: dict) -> dict:
        """发送 POST 请求"""
        url = f"{self.base_url}{endpoint}"
        resp = requests.post(url, headers=self.headers, json=data, timeout=30)
        resp.raise_for_status()
        result = resp.json()
        if result.get("code") != 0:
            raise RuntimeError(f"API Error: {result.get('msg', 'Unknown error')}, code={result.get('code')}")
        return result
    
    # ========== 系统 ==========
    
    def get_version(self) -> str:
        """获取思源版本"""
        result = self._post("/api/system/version", {})
        return result["data"]
    
    # ========== 笔记本 ==========
    
    def list_notebooks(self) -> List[Dict]:
        """列出所有笔记本"""
        result = self._post("/api/notebook/lsNotebooks", {})
        return result["data"]["notebooks"]
    
    # ========== 文档树 ==========
    
    def list_doc_tree(self, path: str = "/") -> List[Dict]:
        """获取文档树"""
        result = self._post("/api/filetree/listDocTree", {
            "notebook": self.notebook_id,
            "path": path
        })
        return result.get("data", [])
    
    def search_docs(self, keyword: str) -> List[Dict]:
        """搜索文档"""
        result = self._post("/api/filetree/searchDocs", {
            "k": keyword,
            "flashcard": False
        })
        return result.get("data", [])
    
    # ========== 文档操作 ==========
    
    def create_doc(self, path: str, markdown: str) -> str:
        """
        用 Markdown 创建文档
        
        Args:
            path: 文档路径，如 "/sources/my-article"
            markdown: Markdown 内容
            
        Returns:
            新文档的 ID
        """
        result = self._post("/api/filetree/createDocWithMd", {
            "notebook": self.notebook_id,
            "path": path,
            "markdown": markdown
        })
        return result["data"]
    
    def append_block(self, parent_id: str, markdown: str) -> List[str]:
        """
        追加块到文档或块
        
        Args:
            parent_id: 父文档 ID 或块 ID
            markdown: Markdown 内容
            
        Returns:
            新创建的块 ID 列表
        """
        result = self._post("/api/block/appendBlock", {
            "parentID": parent_id,
            "dataType": "markdown",
            "data": markdown
        })
        return result.get("data", [])
    
    def update_block(self, block_id: str, markdown: str) -> dict:
        """更新块内容"""
        return self._post("/api/block/updateBlock", {
            "id": block_id,
            "dataType": "markdown",
            "data": markdown
        })
    
    def delete_block(self, block_id: str) -> dict:
        """删除块"""
        return self._post("/api/block/deleteBlock", {
            "id": block_id
        })
    
    def get_block_kramdown(self, block_id: str) -> str:
        """获取块的 Kramdown 源码"""
        result = self._post("/api/block/getBlockKramdown", {
            "id": block_id
        })
        return result["data"]["kramdown"]
    
    def get_doc_info(self, block_id: str) -> Dict:
        """获取文档信息"""
        result = self._post("/api/block/getDocInfo", {
            "id": block_id
        })
        return result["data"]
    
    # ========== SQL 查询 ==========
    
    def sql_query(self, stmt: str) -> List[Dict]:
        """
        执行 SQL 查询
        
        常用查询示例：
        - 查找文档: SELECT * FROM blocks WHERE path LIKE '/LLM-Wiki/%' AND type = 'd'
        - 查找段落: SELECT * FROM blocks WHERE content LIKE '%关键词%' AND type = 'p'
        - 查找引用: SELECT * FROM refs WHERE defBlockPath LIKE '/LLM-Wiki/%'
        """
        result = self._post("/api/query/sql", {"stmt": stmt})
        return result.get("data", [])
    
    def find_doc_by_title(self, title: str, folder: str = "") -> List[Dict]:
        """按标题查找文档"""
        path_filter = f"/LLM-Wiki{folder}/%" if folder else "/LLM-Wiki/%"
        stmt = f"""
            SELECT id, content, path 
            FROM blocks 
            WHERE path LIKE '{path_filter}' 
              AND type = 'd' 
              AND content LIKE '%{title}%'
        """
        return self.sql_query(stmt)
    
    def find_blocks_by_keyword(self, keyword: str, limit: int = 30) -> List[Dict]:
        """按关键词搜索内容块"""
        stmt = f"""
            SELECT id, content, path, type, updated 
            FROM blocks 
            WHERE content LIKE '%{keyword}%' 
              AND path LIKE '/LLM-Wiki/%'
            ORDER BY updated DESC 
            LIMIT {limit}
        """
        return self.sql_query(stmt)
    
    def count_docs_by_type(self) -> List[Dict]:
        """统计各类文档数量"""
        stmt = """
            SELECT 
                CASE 
                    WHEN path LIKE '/LLM-Wiki/sources/%' THEN 'sources'
                    WHEN path LIKE '/LLM-Wiki/entities/%' THEN 'entities'
                    WHEN path LIKE '/LLM-Wiki/concepts/%' THEN 'concepts'
                    WHEN path LIKE '/LLM-Wiki/syntheses/%' THEN 'syntheses'
                    ELSE 'other'
                END as doc_type,
                COUNT(*) as count
            FROM blocks 
            WHERE path LIKE '/LLM-Wiki/%' AND type = 'd'
            GROUP BY doc_type
        """
        return self.sql_query(stmt)
    
    def find_orphan_docs(self) -> List[Dict]:
        """查找孤立页面（未被引用的文档）"""
        stmt = """
            SELECT b.path, b.content 
            FROM blocks b 
            WHERE b.path LIKE '/LLM-Wiki/%' 
              AND b.type = 'd'
              AND b.id NOT IN (
                  SELECT DISTINCT defBlockID 
                  FROM refs 
                  WHERE defBlockPath LIKE '/LLM-Wiki/%'
              )
        """
        return self.sql_query(stmt)
    
    def recent_docs(self, days: int = 7) -> List[Dict]:
        """查找最近更新的文档"""
        stmt = f"""
            SELECT DISTINCT path, updated 
            FROM blocks 
            WHERE path LIKE '/LLM-Wiki/%' 
              AND type = 'd' 
              AND updated > strftime('%Y%m%d%H%M%S', 'now', '-{days} days')
            ORDER BY updated DESC
        """
        return self.sql_query(stmt)
    
    # ========== 属性 ==========
    
    def set_block_attrs(self, block_id: str, attrs: Dict[str, str]) -> dict:
        """设置块属性"""
        return self._post("/api/attr/setBlockAttrs", {
            "id": block_id,
            "attrs": attrs
        })
    
    def get_block_attrs(self, block_id: str) -> Dict[str, str]:
        """获取块属性"""
        result = self._post("/api/attr/getBlockAttrs", {
            "id": block_id
        })
        return result.get("data", {})
    
    # ========== 高级操作 ==========
    
    def doc_exists(self, path: str) -> bool:
        """检查文档是否已存在"""
        stmt = f"SELECT id FROM blocks WHERE path LIKE '%{path}.sy' AND type = 'd'"
        results = self.sql_query(stmt)
        return len(results) > 0
    
    def create_or_update_doc(self, path: str, markdown: str) -> str:
        """
        创建文档，如果已存在则追加内容
        
        Returns:
            文档 ID
        """
        # 检查是否已存在
        stmt = f"SELECT id FROM blocks WHERE path LIKE '%{path}.sy' AND type = 'd'"
        existing = self.sql_query(stmt)
        
        if existing:
            doc_id = existing[0]["id"]
            self.append_block(doc_id, markdown)
            return doc_id
        else:
            return self.create_doc(path, markdown)


# ========== 快捷命令行工具 ==========

def main():
    import argparse
    import os
    
    parser = argparse.ArgumentParser(description="思源笔记 LLM Wiki 工具")
    parser.add_argument("--token", default=os.environ.get("SIYUAN_TOKEN"), help="API Token")
    parser.add_argument("--notebook", default=os.environ.get("SIYUAN_NOTEBOOK"), help="笔记本 ID")
    parser.add_argument("--url", default=os.environ.get("SIYUAN_API", "http://127.0.0.1:6806"), help="API 地址")
    
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # version
    subparsers.add_parser("version", help="获取思源版本")
    
    # list
    subparsers.add_parser("list", help="列出笔记本")
    
    # search
    search_parser = subparsers.add_parser("search", help="搜索文档")
    search_parser.add_argument("keyword", help="搜索关键词")
    
    # query
    query_parser = subparsers.add_parser("query", help="SQL 查询")
    query_parser.add_argument("sql", help="SQL 语句")
    
    # stats
    subparsers.add_parser("stats", help="统计文档数量")
    
    # orphans
    subparsers.add_parser("orphans", help="查找孤立页面")
    
    args = parser.parse_args()
    
    if not args.token:
        print("错误：请提供 API Token（--token 或环境变量 SIYUAN_TOKEN）")
        return
    
    client = SiyuanClient(token=args.token, notebook_id=args.notebook or "", base_url=args.url)
    
    if args.command == "version":
        print(f"思源版本: {client.get_version()}")
    
    elif args.command == "list":
        for nb in client.list_notebooks():
            print(f"{nb['id']}  {nb['name']}")
    
    elif args.command == "search":
        for doc in client.search_docs(args.keyword):
            print(f"{doc['hPath']}")
    
    elif args.command == "query":
        for row in client.sql_query(args.sql):
            print(row)
    
    elif args.command == "stats":
        for row in client.count_docs_by_type():
            print(f"{row['doc_type']}: {row['count']}")
    
    elif args.command == "orphans":
        for row in client.find_orphan_docs():
            print(f"{row['path']}: {row['content'][:50]}...")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
