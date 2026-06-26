#!/usr/bin/env python3
"""
记忆搜索引擎 - 智能检索长期记忆

用法:
    # 关键词搜索
    python memory_search.py query "用户偏好"
    
    # 高级搜索
    python memory_search.py query "项目" --category decision --importance-above 7
    
    # 语义搜索（基于关键词相似度）
    python memory_search.py semantic "用户喜欢什么"
    
    # 时间范围搜索
    python memory_search.py range --from 2024-03-01 --to 2024-03-26 --tag "重要"
"""

import argparse
import json
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from difflib import SequenceMatcher


class MemorySearch:
    """记忆搜索引擎"""
    
    def __init__(self, base_dir: str = "/root/.openclaw/workspace"):
        self.base_dir = Path(base_dir)
        self.memory_dir = self.base_dir / "memory"
        self.core_memory_file = self.base_dir / "MEMORY.md"
    
    def keyword_search(self, query: str, category: str = None,
                       importance_above: int = None, tag: str = None,
                       days: int = 30) -> List[Dict]:
        """
        关键词搜索
        
        Args:
            query: 搜索关键词
            category: 分类过滤
            importance_above: 重要性过滤
            tag: 标签过滤
            days: 搜索最近N天的记忆
        """
        results = []
        query_lower = query.lower()
        
        # 搜索日常记忆文件
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            memory_file = self.memory_dir / f"{date_str}.md"
            
            if not memory_file.exists():
                continue
            
            content = memory_file.read_text(encoding='utf-8')
            memories = self._parse_memories(content, date_str)
            
            for memory in memories:
                # 应用过滤
                if category and memory.get('category') != category:
                    continue
                if importance_above and memory.get('importance', 0) < importance_above:
                    continue
                if tag and tag not in memory.get('tags', []):
                    continue
                
                # 关键词匹配
                content_lower = memory.get('content', '').lower()
                if query_lower in content_lower:
                    # 计算相关性分数
                    score = self._calculate_relevance(query, memory)
                    memory['relevance_score'] = score
                    memory['source_file'] = str(memory_file)
                    results.append(memory)
        
        # 搜索核心记忆
        if self.core_memory_file.exists():
            core_results = self._search_core_memory(query)
            results.extend(core_results)
        
        # 按相关性排序
        results.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        return results
    
    def semantic_search(self, query: str, top_k: int = 10) -> List[Dict]:
        """
        语义搜索（基于关键词相似度）
        
        简单实现：基于关键词重叠和相似度计算
        """
        # 提取查询关键词
        query_keywords = set(self._extract_keywords(query))
        
        all_memories = []
        
        # 收集所有记忆
        for memory_file in self.memory_dir.glob("*.md"):
            date_str = memory_file.stem
            content = memory_file.read_text(encoding='utf-8')
            memories = self._parse_memories(content, date_str)
            all_memories.extend(memories)
        
        # 计算相似度
        results = []
        for memory in all_memories:
            memory_keywords = set(self._extract_keywords(memory.get('content', '')))
            
            # Jaccard相似度
            if query_keywords and memory_keywords:
                intersection = query_keywords & memory_keywords
                union = query_keywords | memory_keywords
                jaccard = len(intersection) / len(union)
                
                # 序列相似度
                seq_sim = SequenceMatcher(None, query, memory.get('content', '')).ratio()
                
                # 综合分数
                score = jaccard * 0.6 + seq_sim * 0.4
                
                if score > 0.1:  # 阈值
                    memory['relevance_score'] = round(score, 3)
                    results.append(memory)
        
        # 排序并返回前K个
        results.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        return results[:top_k]
    
    def time_range_search(self, from_date: str, to_date: str,
                          category: str = None, tag: str = None) -> List[Dict]:
        """时间范围搜索"""
        results = []
        
        from_dt = datetime.strptime(from_date, "%Y-%m-%d")
        to_dt = datetime.strptime(to_date, "%Y-%m-%d")
        
        current = from_dt
        while current <= to_dt:
            date_str = current.strftime("%Y-%m-%d")
            memory_file = self.memory_dir / f"{date_str}.md"
            
            if memory_file.exists():
                content = memory_file.read_text(encoding='utf-8')
                memories = self._parse_memories(content, date_str)
                
                for memory in memories:
                    if category and memory.get('category') != category:
                        continue
                    if tag and tag not in memory.get('tags', []):
                        continue
                    
                    results.append(memory)
            
            current += timedelta(days=1)
        
        return results
    
    def _parse_memories(self, content: str, date_str: str) -> List[Dict]:
        """解析记忆内容"""
        memories = []
        
        pattern = r'### (\d{2}:\d{2}:\d{2}) \[重要性:(\d+)/10\]\n- \*\*内容\*\*: (.+?)\n- \*\*分类\*\*: (.+?)\n- \*\*标签\*\*: (.+?)\n'
        
        for match in re.finditer(pattern, content, re.DOTALL):
            memories.append({
                "timestamp": f"{date_str} {match.group(1)}",
                "importance": int(match.group(2)),
                "content": match.group(3).strip(),
                "category": match.group(4).strip(),
                "tags": [t.strip() for t in match.group(5).split(',') if t.strip() != '无'],
                "date": date_str
            })
        
        return memories
    
    def _search_core_memory(self, query: str) -> List[Dict]:
        """搜索核心记忆文件"""
        results = []
        query_lower = query.lower()
        
        content = self.core_memory_file.read_text(encoding='utf-8')
        
        # 按行搜索
        for line in content.split('\n'):
            if line.strip().startswith('-') or line.strip().startswith('*'):
                if query_lower in line.lower():
                    results.append({
                        "content": line.strip()[2:],  # 移除 "- " 或 "* "
                        "category": "core_memory",
                        "importance": 9,  # 核心记忆重要性较高
                        "source": "MEMORY.md",
                        "relevance_score": 1.0
                    })
        
        return results
    
    def _calculate_relevance(self, query: str, memory: Dict) -> float:
        """计算相关性分数"""
        score = 0.0
        query_lower = query.lower()
        content_lower = memory.get('content', '').lower()
        
        # 完全匹配
        if query_lower in content_lower:
            score += 1.0
        
        # 重要性加成
        importance = memory.get('importance', 5)
        score += importance / 10.0
        
        # 时效性（越新的记忆分数越高）
        date_str = memory.get('date', '2024-01-01')
        try:
            memory_date = datetime.strptime(date_str, "%Y-%m-%d")
            days_ago = (datetime.now() - memory_date).days
            recency_bonus = max(0, (30 - days_ago) / 30.0)
            score += recency_bonus * 0.3
        except:
            pass
        
        return round(score, 2)
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        # 简单分词（去除停用词）
        stopwords = {'的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'}
        
        # 清理文本
        text = re.sub(r'[^\w\s]', ' ', text)
        words = text.lower().split()
        
        # 过滤停用词和短词
        keywords = [w for w in words if len(w) >= 2 and w not in stopwords]
        
        return keywords


def main():
    parser = argparse.ArgumentParser(description='记忆搜索引擎')
    parser.add_argument('mode', choices=['query', 'semantic', 'range'],
                       help='搜索模式')
    parser.add_argument('--query', type=str, help='搜索关键词')
    parser.add_argument('--category', type=str, help='分类过滤')
    parser.add_argument('--importance-above', type=int, help='重要性阈值')
    parser.add_argument('--tag', type=str, help='标签过滤')
    parser.add_argument('--days', type=int, default=30, help='搜索最近N天')
    parser.add_argument('--from', dest='from_date', type=str, help='起始日期')
    parser.add_argument('--to', dest='to_date', type=str, help='结束日期')
    parser.add_argument('--top', type=int, default=10, help='返回结果数量')
    
    args = parser.parse_args()
    
    search = MemorySearch()
    
    if args.mode == 'query':
        if not args.query:
            print("[X] 请提供 --query")
            return
        
        results = search.keyword_search(
            query=args.query,
            category=args.category,
            importance_above=args.importance_above,
            tag=args.tag,
            days=args.days
        )
        
        print(f"[*] 找到 {len(results)} 条相关记忆")
        print("-" * 60)
        
        for i, r in enumerate(results[:args.top], 1):
            print(f"\n[{i}] 相关性: {r.get('relevance_score', 0)}")
            print(f"    日期: {r.get('date', 'N/A')}")
            print(f"    分类: {r.get('category', 'N/A')}")
            print(f"    内容: {r.get('content', '')[:100]}...")
            print(f"    标签: {', '.join(r.get('tags', []))}")
    
    elif args.mode == 'semantic':
        if not args.query:
            print("[X] 请提供 --query")
            return
        
        results = search.semantic_search(args.query, top_k=args.top)
        
        print(f"[*] 语义搜索结果 (Top {len(results)})")
        print("-" * 60)
        
        for i, r in enumerate(results, 1):
            print(f"\n[{i}] 相似度: {r.get('relevance_score', 0)}")
            print(f"    内容: {r.get('content', '')[:100]}...")
    
    elif args.mode == 'range':
        if not args.from_date or not args.to_date:
            print("[X] 请提供 --from 和 --to")
            return
        
        results = search.time_range_search(
            from_date=args.from_date,
            to_date=args.to_date,
            category=args.category,
            tag=args.tag
        )
        
        print(f"[*] 找到 {len(results)} 条记忆")
        print("-" * 60)
        
        for r in results:
            print(f"\n[{r.get('date')}] [{r.get('category')}]")
            print(f"    {r.get('content', '')[:80]}...")


if __name__ == '__main__':
    main()
