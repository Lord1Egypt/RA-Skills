#!/usr/bin/env python3
"""
智能查询推荐模块 - 基于记忆内容和使用模式推荐查询

功能：
- 基于历史查询推荐
- 基于记忆内容关键词推荐
- 基于用户行为模式推荐
- 基于时间上下文推荐（如早晨问天气）
- 查询补全建议
"""

import sys
import sqlite3
from pathlib import Path
from datetime import datetime, time
from typing import Dict, List, Optional, Set
from collections import Counter
import re

sys.path.insert(0, str(Path(__file__).parent.parent))
from paths import get_vectors_db, get_memory_base


class SmartQueryRecommender:
    """智能查询推荐器"""
    
    def __init__(self):
        self.db_path = get_vectors_db()
        self.memory_base = get_memory_base()
        self.conn = None
        self._connect()
    
    def _connect(self):
        """连接数据库"""
        if Path(self.db_path).exists():
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
    
    def get_common_keywords(self, limit: int = 20) -> List[str]:
        """从记忆内容中提取高频关键词"""
        if not self.conn:
            return []
        
        cursor = self.conn.execute("""
            SELECT content FROM memories LIMIT 500
        """)
        
        # 简单分词（中文按字符，英文按空格）
        keywords = []
        for row in cursor.fetchall():
            content = row['content']
            # 提取中文词
            chinese_words = re.findall(r'[\u4e00-\u9fff]+', content)
            for word in chinese_words:
                if len(word) >= 2:
                    keywords.append(word)
        
        # 统计词频
        counter = Counter(keywords)
        return [word for word, count in counter.most_common(limit)]
    
    def get_frequent_topics(self) -> List[str]:
        """获取用户关注的高频话题"""
        if not self.conn:
            return []
        
        # 基于类型分布推断
        cursor = self.conn.execute("""
            SELECT type, COUNT(*) as count
            FROM memories
            GROUP BY type
            ORDER BY count DESC
            LIMIT 5
        """)
        
        topics = []
        type_names = {
            'info': '信息',
            'decision': '决策',
            'preference': '偏好',
            'fact': '事实',
            'task': '任务',
            'learning': '学习',
            'social': '社交'
        }
        
        for row in cursor.fetchall():
            t = row['type']
            topic = type_names.get(t, t)
            topics.append(f"{topic}（{row['count']}条）")
        
        return topics
    
    def get_time_based_suggestions(self) -> List[str]:
        """基于时间上下文的推荐"""
        now = datetime.now()
        hour = now.hour
        suggestions = []
        
        if 6 <= hour < 9:
            suggestions.append("今天的待办事项")
            suggestions.append("今日记忆回顾")
        elif 9 <= hour < 12:
            suggestions.append("当前项目进展")
            suggestions.append("上午工作总结")
        elif 12 <= hour < 14:
            suggestions.append("下午会议安排")
            suggestions.append("午休提醒")
        elif 14 <= hour < 18:
            suggestions.append("今日任务完成情况")
            suggestions.append("待处理事项")
        elif 18 <= hour < 21:
            suggestions.append("今日收获总结")
            suggestions.append("明天计划")
        else:
            suggestions.append("本周记忆回顾")
            suggestions.append("重要决策记录")
        
        return suggestions
    
    def get_actionable_suggestions(self) -> List[Dict]:
        """获取可执行的建议"""
        suggestions = []
        
        # 检查记忆数量
        if self.conn:
            cursor = self.conn.execute("SELECT COUNT(*) as count FROM memories")
            count = cursor.fetchone()['count']
            
            if count < 10:
                suggestions.append({
                    "type": "action",
                    "title": "记忆不足",
                    "description": f"当前只有 {count} 条记忆，建议多与 AI 交流",
                    "action": "与摇摇聊天，让它记住更多信息"
                })
        
        # 基于高频话题推荐
        keywords = self.get_common_keywords(5)
        if keywords:
            top_keywords = "、".join(keywords[:3])
            suggestions.append({
                "type": "explore",
                "title": "深入探索",
                "description": f"你经常关注：{top_keywords}",
                "action": f"搜索「{keywords[0]}」相关记忆"
            })
        
        return suggestions
    
    def get_query_completions(self, partial: str) -> List[str]:
        """查询补全建议"""
        if not partial or not self.conn:
            return []
        
        # 搜索包含该关键词的记忆
        cursor = self.conn.execute("""
            SELECT DISTINCT content FROM memories
            WHERE content LIKE ?
            LIMIT 10
        """, (f'%{partial}%',))
        
        completions = []
        for row in cursor.fetchall():
            content = row['content']
            # 找到包含该词的部分
            idx = content.find(partial)
            if idx >= 0:
                # 提取前后各20个字符
                start = max(0, idx - 20)
                end = min(len(content), idx + len(partial) + 20)
                snippet = content[start:end]
                if start > 0:
                    snippet = "..." + snippet
                if end < len(content):
                    snippet = snippet + "..."
                completions.append(snippet)
        
        return completions
    
    def generate_recommendations(self) -> str:
        """生成推荐报告"""
        lines = ["# 🔍 智能查询推荐", ""]
        
        # 时间上下文
        time_suggestions = self.get_time_based_suggestions()
        if time_suggestions:
            lines.append("## 💡 现在可以问")
            for s in time_suggestions[:3]:
                lines.append(f"- 「{s}」")
            lines.append("")
        
        # 高频话题
        topics = self.get_frequent_topics()
        if topics:
            lines.append("## 📊 你关注的话题")
            for topic in topics:
                lines.append(f"- {topic}")
            lines.append("")
        
        # 可执行建议
        actions = self.get_actionable_suggestions()
        if actions:
            lines.append("## ⚡ 推荐操作")
            for a in actions:
                lines.append(f"### {a['title']}")
                lines.append(f"{a['description']}")
                lines.append(f"→ {a['action']}")
                lines.append("")
        
        # 热门关键词
        keywords = self.get_common_keywords(10)
        if keywords:
            lines.append("## 🔑 热门关键词")
            lines.append("、".join(keywords[:10]))
            lines.append("")
        
        return "\n".join(lines)
    
    def close(self):
        """关闭连接"""
        if self.conn:
            self.conn.close()


class QueryPredictor:
    """查询预测器 - 基于历史模式预测下一个查询"""
    
    def __init__(self):
        self.db_path = get_vectors_db()
        self.conn = None
        self._connect()
    
    def _connect(self):
        """连接数据库"""
        if Path(self.db_path).exists():
            self.conn = sqlite3.connect(self.db_path)
    
    def learn_query_pattern(self, query: str):
        """学习查询模式"""
        if not self.conn:
            return
        
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS query_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.execute(
            "INSERT INTO query_history (query) VALUES (?)",
            (query,)
        )
        self.conn.commit()
    
    def predict_next(self) -> List[str]:
        """预测下一个查询"""
        if not self.conn:
            return []
        
        cursor = self.conn.execute("""
            SELECT query, COUNT(*) as freq
            FROM query_history
            WHERE timestamp >= datetime('now', '-7 days')
            GROUP BY query
            ORDER BY freq DESC
            LIMIT 5
        """)
        
        return [row['query'] for row in cursor.fetchall()]
    
    def close(self):
        """关闭连接"""
        if self.conn:
            self.conn.close()


def main():
    """CLI 入口"""
    import argparse
    parser = argparse.ArgumentParser(description='智能查询推荐')
    parser.add_argument('--suggest', '-s', action='store_true', help='显示推荐')
    parser.add_argument('--complete', '-c', type=str, help='查询补全')
    parser.add_argument('--keywords', '-k', action='store_true', help='显示热门关键词')
    parser.add_argument('--topics', '-t', action='store_true', help='显示关注话题')
    args = parser.parse_args()
    
    recommender = SmartQueryRecommender()
    
    if args.complete:
        completions = recommender.get_query_completions(args.complete)
        print(f"关于「{args.complete}」的补全建议：")
        for i, c in enumerate(completions, 1):
            print(f"{i}. {c}")
    elif args.keywords:
        keywords = recommender.get_common_keywords(20)
        print("热门关键词：")
        print("、".join(keywords))
    elif args.topics:
        topics = recommender.get_frequent_topics()
        print("关注的话题：")
        for t in topics:
            print(f"- {t}")
    else:
        print(recommender.generate_recommendations())
    
    recommender.close()


if __name__ == '__main__':
    main()
