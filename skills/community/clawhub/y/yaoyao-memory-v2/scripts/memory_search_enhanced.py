#!/usr/bin/env python3
"""
增强搜索模块 - 高级搜索功能

功能：
- 模糊搜索
- 正则搜索
- 搜索高亮
- 搜索历史
- 搜索建议
- 布尔搜索（AND/OR/NOT）
"""

import sys
import re
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Set, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent))
from paths import get_vectors_db, get_memory_base


class EnhancedSearch:
    """增强搜索"""
    
    def __init__(self):
        self.db_path = get_vectors_db()
        self.memory_base = get_memory_base()
        self.conn = None
        self._search_history = []
        self._search_history_file = None
        self._connect()
        self._load_history()
    
    def _connect(self):
        if Path(self.db_path).exists():
            self.conn = sqlite3.connect(str(self.db_path))
            self.conn.row_factory = sqlite3.Row
    
    def _load_history(self):
        """加载搜索历史"""
        self._search_history_file = self.memory_base / ".cache" / "search_history.json"
        if self._search_history_file.exists():
            try:
                import json
                with open(self._search_history_file) as f:
                    self._search_history = json.load(f)
            except:
                self._search_history = []
    
    def _save_history(self):
        """保存搜索历史"""
        if self._search_history_file:
            self._search_history_file.parent.mkdir(parents=True, exist_ok=True)
            try:
                import json
                with open(self._search_history_file, 'w') as f:
                    json.dump(self._search_history[-50:], f)  # 只保留最近50条
            except:
                pass
    
    def fuzzy_search(self, query: str, limit: int = 20) -> List[Dict]:
        """模糊搜索"""
        if not self.conn or not query:
            return []
        
        # 使用 LIKE 进行模糊匹配
        pattern = f'%{query}%'
        
        cursor = self.conn.execute("""
            SELECT record_id, content, type, priority, created_time
            FROM l1_records
            WHERE content LIKE ?
            ORDER BY priority DESC, created_time DESC
            LIMIT ?
        """, (pattern, limit))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'id': row['record_id'],
                'content': row['content'],
                'type': row['type'],
                'priority': row['priority'],
                'date': row['created_time'],
                'match_type': 'fuzzy'
            })
        
        return results
    
    def regex_search(self, pattern: str, limit: int = 20) -> List[Dict]:
        """正则搜索"""
        if not self.conn:
            return []
        
        try:
            regex = re.compile(pattern, re.IGNORECASE)
        except re.error:
            return []
        
        cursor = self.conn.execute("""
            SELECT record_id, content, type, priority, created_time
            FROM l1_records
            LIMIT 200
        """)
        
        results = []
        for row in cursor.fetchall():
            content = row['content'] or ''
            if regex.search(content):
                results.append({
                    'id': row['record_id'],
                    'content': content,
                    'type': row['type'],
                    'priority': row['priority'],
                    'date': row['created_time'],
                    'match_type': 'regex',
                    'matched_text': regex.findall(content)[:3]
                })
                
                if len(results) >= limit:
                    break
        
        return results
    
    def boolean_search(self, query: str, limit: int = 20) -> List[Dict]:
        """布尔搜索（支持 AND/OR/NOT）"""
        if not self.conn or not query:
            return []
        
        # 解析布尔表达式
        must_have = []
        must_not = []
        optional = []
        
        parts = query.split()
        i = 0
        while i < len(parts):
            part = parts[i]
            
            if part.upper() == 'NOT' and i + 1 < len(parts):
                must_not.append(parts[i + 1])
                i += 2
            elif part.upper() == 'AND':
                i += 1
            elif part.upper() == 'OR' or i == 0:
                optional.append(part)
                i += 1
            else:
                optional.append(part)
                i += 1
        
        # 构建 SQL
        sql = "SELECT record_id, content, type, priority, created_time FROM l1_records WHERE 1=1"
        params = []
        
        if must_have:
            for term in must_have:
                sql += " AND content LIKE ?"
                params.append(f'%{term}%')
        
        if must_not:
            for term in must_not:
                sql += " AND content NOT LIKE ?"
                params.append(f'%{term}%')
        
        if optional:
            or_clause = " OR ".join(["content LIKE ?" for _ in optional])
            sql += f" AND ({or_clause})"
            params.extend([f'%{term}%' for term in optional])
        
        sql += " ORDER BY priority DESC LIMIT ?"
        params.append(limit)
        
        cursor = self.conn.execute(sql, params)
        
        return [dict(row) for row in cursor.fetchall()]
    
    def highlight_matches(self, content: str, query: str) -> str:
        """高亮匹配文本"""
        if not query or not content:
            return content
        
        # 转义特殊字符
        escaped = re.escape(query)
        
        # 高亮
        highlighted = re.sub(f'({escaped})', '**\\1**', content, flags=re.IGNORECASE)
        
        return highlighted
    
    def add_to_history(self, query: str):
        """添加到搜索历史"""
        self._search_history.append({
            'query': query,
            'timestamp': datetime.now().isoformat()
        })
        self._save_history()
    
    def get_history(self, limit: int = 20) -> List[Dict]:
        """获取搜索历史"""
        return self._search_history[-limit:]
    
    def get_suggestions(self, partial: str, limit: int = 5) -> List[str]:
        """获取搜索建议"""
        if not partial:
            return []
        
        # 基于历史建议
        history_queries = [h['query'] for h in self._search_history if h['query'].startswith(partial)]
        
        # 基于数据库内容建议
        pattern = f'{partial}%'
        cursor = self.conn.execute("""
            SELECT DISTINCT content FROM l1_records
            WHERE content LIKE ?
            LIMIT 20
        """, (pattern,))
        
        content_suggestions = []
        for row in cursor.fetchall():
            content = row['content'] or ''
            # 提取包含该词的部分
            idx = content.lower().find(partial.lower())
            if idx >= 0:
                start = max(0, idx - 20)
                end = min(len(content), idx + len(partial) + 20)
                snippet = content[start:end]
                content_suggestions.append(snippet)
        
        # 合并去重
        suggestions = list(dict.fromkeys(history_queries + content_suggestions))
        return suggestions[:limit]
    
    def search_with_context(self, query: str, context_words: int = 20) -> List[Dict]:
        """带上下文搜索"""
        if not self.conn or not query:
            return []
        
        pattern = f'%{query}%'
        
        cursor = self.conn.execute("""
            SELECT record_id, content, type, priority, created_time
            FROM l1_records
            WHERE content LIKE ?
            ORDER BY priority DESC
            LIMIT 30
        """, (pattern,))
        
        results = []
        for row in cursor.fetchall():
            content = row['content'] or ''
            
            # 找到匹配位置
            idx = content.lower().find(query.lower())
            if idx >= 0:
                # 提取上下文
                start = max(0, idx - context_words)
                end = min(len(content), idx + len(query) + context_words)
                snippet = content[start:end]
                
                if start > 0:
                    snippet = '...' + snippet
                if end < len(content):
                    snippet = snippet + '...'
                
                results.append({
                    'id': row['record_id'],
                    'content': snippet,
                    'type': row['type'],
                    'priority': row['priority'],
                    'date': row['created_time'],
                    'full_content': content,
                    'match_position': idx
                })
        
        return results
    
    def close(self):
        if self.conn:
            self.conn.close()


def main():
    import argparse
    parser = argparse.ArgumentParser(description='增强搜索')
    parser.add_argument('--query', '-q', type=str, help='搜索查询')
    parser.add_argument('--fuzzy', '-f', action='store_true', help='模糊搜索')
    parser.add_argument('--regex', '-r', type=str, help='正则搜索')
    parser.add_argument('--boolean', '-b', type=str, help='布尔搜索')
    parser.add_argument('--history', action='store_true', help='搜索历史')
    parser.add_argument('--suggest', '-s', type=str, help='搜索建议')
    parser.add_argument('--limit', '-l', type=int, default=20, help='结果数量')
    args = parser.parse()
    
    search = EnhancedSearch()
    
    if args.history:
        history = search.get_history()
        print(f"# 📜 搜索历史 ({len(history)} 条)")
        for h in history[-10:]:
            print(f"- {h['query']} ({h['timestamp'][:10]})")
    
    elif args.suggest:
        suggestions = search.get_suggestions(args.suggest)
        print(f"# 💡 搜索建议")
        for s in suggestions:
            print(f"- {s}")
    
    elif args.regex:
        results = search.regex_search(args.regex, args.limit)
        print(f"# 🔍 正则搜索「{args.regex}」({len(results)} 条)")
        for r in results[:10]:
            print(f"\n## {r['id']}")
            print(f"{r['content'][:100]}...")
    
    elif args.boolean:
        results = search.boolean_search(args.boolean, args.limit)
        print(f"# 🔍 布尔搜索「{args.boolean}」({len(results)} 条)")
        for r in results[:10]:
            print(f"\n## {r['id']} [P{r['priority']}]")
            print(f"{r['content'][:100]}...")
    
    elif args.query:
        results = search.search_with_context(args.query)
        print(f"# 🔍 搜索「{args.query}」({len(results)} 条)")
        for r in results[:10]:
            print(f"\n## {r['id']} [P{r['priority']}]")
            highlighted = search.highlight_matches(r['content'], args.query)
            print(highlighted)
        
        search.add_to_history(args.query)
    
    else:
        print("# 🔍 增强搜索")
        print("用法：")
        print("  --query <词>     带上下文搜索")
        print("  --fuzzy          模糊搜索")
        print("  --regex <正则>   正则搜索")
        print("  --boolean <表达式> 布尔搜索")
        print("  --history        搜索历史")
        print("  --suggest <词>   搜索建议")
    
    search.close()


if __name__ == '__main__':
    main()
