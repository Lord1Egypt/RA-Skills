#!/usr/bin/env python3
"""
文件搜索模块
根据关键词/功能描述快速查找相关文件
"""

import sqlite3
import os
import json
from typing import List, Dict, Any, Optional
from datetime import datetime

from indexer import FileIndexer, DEFAULT_DB_PATH


class FileSearcher:
    """文件搜索类"""

    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        """初始化搜索器"""
        self.db_path = db_path
        self.indexer = FileIndexer(db_path)

    def search(self, query: str, limit: int = 10, include_deleted: bool = False) -> List[Dict[str, Any]]:
        """
        搜索文件

        Args:
            query: 搜索关键词
            limit: 返回结果数量限制
            include_deleted: 是否包含已删除文件

        Returns:
            匹配的文件列表，按相关度排序
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # 构建搜索查询 - 搜索文件名、描述、内容摘要和标签
        query_pattern = f'%{query}%'

        if include_deleted:
            cursor.execute('''
                SELECT path, filename, file_type, description, content_summary,
                       created_at, updated_at, deleted_at, size, tags,
                       (CASE WHEN filename LIKE ? THEN 3 ELSE 0 END) +
                       (CASE WHEN description LIKE ? THEN 2 ELSE 0 END) +
                       (CASE WHEN content_summary LIKE ? THEN 1 ELSE 0 END) as relevance
                FROM files
                WHERE filename LIKE ? OR description LIKE ? OR content_summary LIKE ?
                ORDER BY relevance DESC, updated_at DESC
                LIMIT ?
            ''', (query_pattern, query_pattern, query_pattern, query_pattern, query_pattern, query_pattern, limit))
        else:
            cursor.execute('''
                SELECT path, filename, file_type, description, content_summary,
                       created_at, updated_at, deleted_at, size, tags,
                       (CASE WHEN filename LIKE ? THEN 3 ELSE 0 END) +
                       (CASE WHEN description LIKE ? THEN 2 ELSE 0 END) +
                       (CASE WHEN content_summary LIKE ? THEN 1 ELSE 0 END) as relevance
                FROM files
                WHERE deleted_at IS NULL
                  AND (filename LIKE ? OR description LIKE ? OR content_summary LIKE ?)
                ORDER BY relevance DESC, updated_at DESC
                LIMIT ?
            ''', (query_pattern, query_pattern, query_pattern, query_pattern, query_pattern, query_pattern, limit))

        rows = cursor.fetchall()
        conn.close()

        results = []
        for row in rows:
            result = dict(row)
            result['is_deleted'] = result['deleted_at'] is not None
            result['deleted_at'] = result['deleted_at']
            # 解析 tags
            try:
                result['tags'] = json.loads(result['tags'] or '[]')
            except json.JSONDecodeError:
                result['tags'] = []
            # 截断内容摘要
            if result['content_summary'] and len(result['content_summary']) > 200:
                result['content_summary'] = result['content_summary'][:200] + '...'
            results.append(result)

        return results

    def search_by_type(self, file_type: str, limit: int = 20) -> List[Dict[str, Any]]:
        """按文件类型搜索"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('''
            SELECT path, filename, file_type, description, content_summary,
                   created_at, updated_at, size, tags
            FROM files
            WHERE deleted_at IS NULL AND file_type = ?
            ORDER BY updated_at DESC
            LIMIT ?
        ''', (file_type, limit))

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def search_by_tag(self, tag: str, limit: int = 20) -> List[Dict[str, Any]]:
        """按标签搜索"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        tag_pattern = f'%"{tag}"%'
        cursor.execute('''
            SELECT path, filename, file_type, description, content_summary,
                   created_at, updated_at, size, tags
            FROM files
            WHERE deleted_at IS NULL AND tags LIKE ?
            ORDER BY updated_at DESC
            LIMIT ?
        ''', (tag_pattern, limit))

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_recent_files(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取最近修改的文件"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('''
            SELECT path, filename, file_type, description, content_summary,
                   created_at, updated_at, size, tags
            FROM files
            WHERE deleted_at IS NULL
            ORDER BY updated_at DESC
            LIMIT ?
        ''', (limit,))

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_file_by_path(self, filepath: str) -> Optional[Dict[str, Any]]:
        """根据路径获取文件信息"""
        return self.indexer.get_file_info(filepath)

    def suggest_files(self, intent: str) -> List[Dict[str, Any]]:
        """
        根据用户意图推荐相关文件

        Args:
            intent: 用户意图描述，如"加密"、"文件操作"、"数据库"等

        Returns:
            推荐的文件列表
        """
        # 意图到关键词的映射
        intent_keywords = {
            '加密': ['encrypt', 'decrypt', 'cipher', 'crypto', '加密', '解密'],
            '文件操作': ['file', 'read', 'write', 'open', 'close', '文件', '读写'],
            '数据库': ['database', 'sql', 'query', 'db', '数据库', '表'],
            '网络': ['http', 'request', 'api', 'url', 'network', '网络', '接口'],
            '解析': ['parse', 'json', 'xml', 'csv', '解析', '转换'],
            '日志': ['log', 'logger', 'logging', '日志', '记录'],
            '配置': ['config', 'setting', 'config', '配置', '设置'],
            '测试': ['test', 'unittest', 'pytest', '测试', '断言'],
            '工具': ['util', 'helper', 'tool', '工具', '辅助'],
            '技能': ['skill', 'agent', 'tool', '技能', 'agent'],
        }

        # 查找匹配的关键词
        keywords = []
        for intent_key, kw_list in intent_keywords.items():
            if intent_key in intent or any(kw in intent for kw in kw_list[:2]):
                keywords.extend(kw_list)

        # 如果没有匹配，直接使用 intent 中的词
        if not keywords:
            keywords = [intent]

        # 组合搜索
        all_results = []
        for keyword in keywords[:3]:  # 最多用 3 个关键词
            results = self.search(keyword, limit=5)
            all_results.extend(results)

        # 去重并按相关度排序
        seen = set()
        unique_results = []
        for result in all_results:
            if result['path'] not in seen:
                seen.add(result['path'])
                unique_results.append(result)

        return sorted(unique_results, key=lambda x: x.get('relevance', 0), reverse=True)[:10]

    def format_result(self, result: Dict[str, Any]) -> str:
        """格式化单个搜索结果"""
        status = " [已删除]" if result.get('is_deleted') else ""
        file_type = result.get('file_type', 'unknown')
        description = result.get('description', '') or '无描述'

        lines = [
            f"📄 {result['filename']}{status}",
            f"   路径：{result['path']}",
            f"   类型：{file_type}",
            f"   描述：{description}",
        ]

        if result.get('tags'):
            lines.append(f"   标签：{', '.join(result['tags'])}")

        if result.get('content_summary'):
            lines.append(f"   内容：{result['content_summary']}")

        return '\n'.join(lines)

    def format_results(self, results: List[Dict[str, Any]], show_full: bool = False) -> str:
        """格式化搜索结果列表"""
        if not results:
            return "未找到匹配的文件"

        output = [f"找到 {len(results)} 个相关文件:\n"]

        for i, result in enumerate(results, 1):
            output.append(f"\n{i}. {self.format_result(result)}")

        return '\n'.join(output)


def quick_search(query: str, limit: int = 5) -> str:
    """快速搜索并返回格式化结果"""
    searcher = FileSearcher()
    results = searcher.search(query, limit=limit)
    return searcher.format_results(results)


def suggest_for_intent(intent: str) -> str:
    """根据意图推荐文件"""
    searcher = FileSearcher()
    results = searcher.suggest_files(intent)
    return searcher.format_results(results)


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python searcher.py <query>")
        print("Or: python searcher.py --intent <intent_description>")
        sys.exit(1)

    searcher = FileSearcher()

    if sys.argv[1] == '--intent' and len(sys.argv) > 2:
        intent = ' '.join(sys.argv[2:])
        print(suggest_for_intent(intent))
    else:
        query = ' '.join(sys.argv[1:])
        print(quick_search(query))
