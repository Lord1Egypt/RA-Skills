#!/usr/bin/env python3
"""
智能记忆建议器 - 基于用户行为模式提供主动建议

功能：
- 分析用户查询习惯，主动推荐可能需要的记忆
- 基于时间/场景的智能提示
- 遗忘提醒（长时间未访问的重要记忆）
- 知识补全建议
"""

import sys
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import Counter

sys.path.insert(0, str(Path(__file__).parent.parent))
from paths import get_vectors_db


class MemorySuggester:
    """智能记忆建议器"""
    
    def __init__(self):
        self.db_path = get_vectors_db()
        self.conn = None
        self._connect()
    
    def _connect(self):
        if Path(self.db_path).exists():
            self.conn = sqlite3.connect(str(self.db_path))
            self.conn.row_factory = sqlite3.Row
    
    def analyze_query_patterns(self, days: int = 7) -> Dict:
        """分析查询模式"""
        # 分析高频类型
        cursor = self.conn.execute("""
            SELECT type, COUNT(*) as count
            FROM l1_records
            WHERE created_time > datetime('now', ?)
            GROUP BY type
            ORDER BY count DESC
            LIMIT 5
        """, (f'-{days} days',))
        
        type_freq = {row['type']: row['count'] for row in cursor.fetchall()}
        
        # 分析高频关键词
        cursor = self.conn.execute("""
            SELECT content FROM l1_records
            WHERE created_time > datetime('now', ?)
        """, (f'-{days} days',))
        
        all_words = []
        for row in cursor.fetchall():
            content = row['content'] or ''
            words = content.split()[:10]  # 取前10个词
            all_words.extend(words)
        
        top_words = Counter(all_words).most_common(10)
        
        return {
            'top_types': type_freq,
            'top_keywords': dict(top_words),
            'analysis_period_days': days
        }
    
    def suggest_forgotten_memories(self, days_threshold: int = 30, min_priority: int = 70) -> List[Dict]:
        """建议被遗忘的记忆（长时间未访问的高优先级记忆）"""
        cursor = self.conn.execute("""
            SELECT record_id, content, type, priority, created_time
            FROM l1_records
            WHERE priority >= ?
            AND created_time < datetime('now', ?)
            ORDER BY priority DESC
            LIMIT 10
        """, (min_priority, f'-{days_threshold} days'))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def suggest_knowledge_gaps(self) -> List[str]:
        """建议知识缺口（基于常见查询但缺失的类型）"""
        suggestions = []
        
        # 检查缺失的类型
        cursor = self.conn.execute("SELECT DISTINCT type FROM l1_records")
        existing_types = {row['type'] for row in cursor.fetchall()}
        
        important_types = ['preference', 'habit', 'goal', 'skill', 'contact']
        
        for important_type in important_types:
            if important_type not in existing_types:
                suggestions.append(f"建议添加 '{important_type}' 类型的记忆")
        
        # 检查是否有足够的决策记录
        cursor = self.conn.execute("""
            SELECT COUNT(*) as count FROM l1_records WHERE type = 'decision'
        """)
        decision_count = cursor.fetchone()['count']
        
        if decision_count < 5:
            suggestions.append("决策记录较少，建议记录一些重要决策及其背景")
        
        return suggestions
    
    def suggest_related_memories(self, query: str, limit: int = 5) -> List[Dict]:
        """基于查询建议相关记忆"""
        keywords = query.lower().split()[:3]  # 取前3个关键词
        
        if not keywords:
            return []
        
        # 简单相似度搜索
        like_patterns = [f'%{kw}%' for kw in keywords]
        
        query_str = """
            SELECT record_id, content, type, priority
            FROM l1_records
            WHERE """ + " OR ".join(["content LIKE ?" for _ in like_patterns]) + """
            ORDER BY priority DESC
            LIMIT ?
        """
        
        cursor = self.conn.execute(query_str, like_patterns + [limit])
        return [dict(row) for row in cursor.fetchall()]
    
    def suggest_daily_review(self) -> Dict:
        """每日复习建议"""
        suggestions = {
            'high_priority': [],
            'recent_additions': [],
            'forgotten': []
        }
        
        # 高优先级未复习
        cursor = self.conn.execute("""
            SELECT record_id, content, type, priority
            FROM l1_records
            WHERE priority >= 80
            ORDER BY priority DESC
            LIMIT 5
        """)
        suggestions['high_priority'] = [dict(row) for row in cursor.fetchall()]
        
        # 最近添加
        cursor = self.conn.execute("""
            SELECT record_id, content, type, priority
            FROM l1_records
            WHERE created_time > datetime('now', '-7 days')
            ORDER BY created_time DESC
            LIMIT 5
        """)
        suggestions['recent_additions'] = [dict(row) for row in cursor.fetchall()]
        
        # 遗忘提醒
        suggestions['forgotten'] = self.suggest_forgotten_memories(days_threshold=14, min_priority=60)
        
        return suggestions
    
    def generate_suggestion_report(self) -> str:
        """生成建议报告"""
        lines = ["# 💡 智能记忆建议报告", ""]
        lines.append(f"**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        # 查询模式分析
        lines.append("## 📊 查询模式分析")
        patterns = self.analyze_query_patterns()
        if patterns['top_types']:
            lines.append("**高频类型**：")
            for t, c in patterns['top_types'].items():
                lines.append(f"- {t}: {c}条")
        if patterns['top_keywords']:
            lines.append("**高频关键词**：")
            keywords = ', '.join([f"`{k}`" for k in list(patterns['top_keywords'].keys())[:5]])
            lines.append(keywords)
        lines.append("")
        
        # 知识缺口
        lines.append("## 🔍 知识缺口建议")
        gaps = self.suggest_knowledge_gaps()
        if gaps:
            for gap in gaps:
                lines.append(f"- {gap}")
        else:
            lines.append("✅ 知识库类型覆盖良好")
        lines.append("")
        
        # 每日复习
        lines.append("## 📅 每日复习建议")
        review = self.suggest_daily_review()
        
        if review['high_priority']:
            lines.append("**🔴 高优先级记忆**：")
            for mem in review['high_priority']:
                content_preview = (mem['content'] or '')[:50]
                lines.append(f"- [{mem['type']}] {content_preview}...")
        
        if review['recent_additions']:
            lines.append("**🆕 最近添加**：")
            for mem in review['recent_additions']:
                content_preview = (mem['content'] or '')[:50]
                lines.append(f"- [{mem['type']}] {content_preview}...")
        
        if review['forgotten']:
            lines.append("**⚠️ 可能遗忘**：")
            for mem in review['forgotten'][:3]:
                content_preview = (mem['content'] or '')[:50]
                lines.append(f"- [{mem['type']}] {content_preview}...")
        
        return "\n".join(lines)
    
    def close(self):
        if self.conn:
            self.conn.close()


def main():
    suggester = MemorySuggester()
    print(suggester.generate_suggestion_report())
    suggester.close()


if __name__ == '__main__':
    main()
