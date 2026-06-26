#!/usr/bin/env python3
"""
智能记忆召回模块 - 根据当前情境智能召回记忆

功能：
- 情境感知记忆召回
- 时间衰减召回
- 重要性加权召回
- 相关性提升召回
- 多维度排序
"""

import sys
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent))
from paths import get_vectors_db, get_memory_base


class IntelligentRecall:
    """智能召回引擎"""
    
    def __init__(self):
        self.db_path = get_vectors_db()
        self.memory_base = get_memory_base()
        self.conn = None
        self._connect()
        
        # 召回权重配置
        self.weights = {
            'recency': 0.3,      # 时间衰减
            'importance': 0.25,   # 重要性
            'relevance': 0.25,   # 相关性
            'frequency': 0.1,    # 访问频率
            'context': 0.1       # 上下文匹配
        }
    
    def _connect(self):
        """连接数据库"""
        if Path(self.db_path).exists():
            self.conn = sqlite3.connect(str(self.db_path))
            self.conn.row_factory = sqlite3.Row
    
    def calculate_recency_score(self, created_time: str) -> float:
        """计算时间衰减分数"""
        if not created_time:
            return 0.5
        
        try:
            created = datetime.fromisoformat(created_time)
            days_old = (datetime.now() - created).days
            
            # 指数衰减
            score = 1.0 / (1.0 + days_old * 0.1)
            return score
        except:
            return 0.5
    
    def calculate_importance_score(self, priority: int) -> float:
        """计算重要性分数"""
        # priority 0-100 映射到 0-1
        return priority / 100.0
    
    def calculate_frequency_score(self, access_count: int) -> float:
        """计算访问频率分数"""
        # 访问次数越多分数越高，但有上限
        return min(access_count / 10.0, 1.0)
    
    def calculate_relevance_score(self, query: str, content: str) -> float:
        """计算相关性分数（简化版）"""
        query_lower = query.lower()
        content_lower = content.lower()
        
        # 词重叠
        query_words = set(query_lower.split())
        content_words = set(content_lower.split())
        
        if not query_words:
            return 0.5
        
        overlap = len(query_words & content_words)
        return overlap / len(query_words)
    
    def recall_by_query(self, query: str, limit: int = 10, context: Optional[Dict] = None) -> List[Dict]:
        """根据查询召回记忆"""
        if not self.conn:
            return []
        
        # 获取所有记忆
        cursor = self.conn.execute("""
            SELECT record_id, content, type, priority, created_time, updated_time
            FROM l1_records
            ORDER BY created_time DESC
            LIMIT 100
        """)
        
        scored_memories = []
        
        for row in cursor.fetchall():
            content = row['content'] or ''
            
            # 计算各项分数
            recency = self.calculate_recency_score(row['created_time'])
            importance = self.calculate_importance_score(row['priority'] or 50)
            relevance = self.calculate_relevance_score(query, content)
            frequency = self.calculate_frequency_score(0)  # 简化
            
            # 综合分数
            total_score = (
                self.weights['recency'] * recency +
                self.weights['importance'] * importance +
                self.weights['relevance'] * relevance +
                self.weights['frequency'] * frequency
            )
            
            scored_memories.append({
                'id': row['record_id'],
                'content': content,
                'type': row['type'],
                'priority': row['priority'],
                'created': row['created_time'],
                'score': round(total_score, 3),
                'breakdown': {
                    'recency': round(recency, 2),
                    'importance': round(importance, 2),
                    'relevance': round(relevance, 2)
                }
            })
        
        # 排序并返回
        scored_memories.sort(key=lambda x: x['score'], reverse=True)
        return scored_memories[:limit]
    
    def recall_by_time_context(self, hour: Optional[int] = None, weekday: Optional[int] = None, limit: int = 5) -> List[Dict]:
        """根据时间上下文召回（如早晨问天气相关）"""
        if not self.conn:
            return []
        
        # 构建时间条件
        time_conditions = []
        if hour is not None:
            time_conditions.append(f"CAST(strftime('%H', created_time) AS INTEGER) = {hour}")
        if weekday is not None:
            time_conditions.append(f"strftime('%w', created_time) = '{weekday}'")
        
        where_clause = " AND ".join(time_conditions) if time_conditions else "1=1"
        
        cursor = self.conn.execute(f"""
            SELECT record_id, content, type, priority, created_time
            FROM l1_records
            WHERE {where_clause}
            ORDER BY priority DESC, created_time DESC
            LIMIT ?
        """, (limit,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def recall_by_entity(self, entity: str, limit: int = 10) -> List[Dict]:
        """根据实体召回（如提到某个人名的所有记忆）"""
        if not self.conn:
            return []
        
        cursor = self.conn.execute("""
            SELECT record_id, content, type, priority, created_time
            FROM l1_records
            WHERE content LIKE ?
            ORDER BY priority DESC, created_time DESC
            LIMIT ?
        """, (f'%{entity}%', limit))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def recall_by_type(self, memory_type: str, limit: int = 10) -> List[Dict]:
        """根据类型召回"""
        if not self.conn:
            return []
        
        cursor = self.conn.execute("""
            SELECT record_id, content, type, priority, created_time
            FROM l1_records
            WHERE type = ?
            ORDER BY priority DESC, created_time DESC
            LIMIT ?
        """, (memory_type, limit))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def recall_diverse(self, query: str, limit: int = 10) -> List[Dict]:
        """多样性召回（不同类型各取一些）"""
        if not self.conn:
            return []
        
        # 先获取各类型的top记忆
        type_top = {}
        types = ['info', 'decision', 'preference', 'fact', 'task']
        
        for t in types:
            cursor = self.conn.execute("""
                SELECT record_id, content, type, priority, created_time
                FROM l1_records
                WHERE type = ? OR type IS NULL OR type = ''
                ORDER BY priority DESC
                LIMIT ?
            """, (t, limit))
            type_top[t] = [dict(row) for row in cursor.fetchall()]
        
        # 交错选取，保证多样性
        result = []
        max_per_type = max(1, limit // len(types))
        
        for t in types:
            for i, mem in enumerate(type_top[t][:max_per_type]):
                if len(result) < limit:
                    result.append(mem)
        
        # 按重要性排序
        result.sort(key=lambda x: x.get('priority', 50), reverse=True)
        return result[:limit]
    
    def get_recall_insights(self) -> Dict:
        """获取召回洞察"""
        if not self.conn:
            return {}
        
        insights = {}
        
        # 最常见的记忆类型
        cursor = self.conn.execute("""
            SELECT type, COUNT(*) as count
            FROM l1_records
            GROUP BY type
            ORDER BY count DESC
            LIMIT 5
        """)
        insights['top_types'] = [dict(row) for row in cursor.fetchall()]
        
        # 最近7天新增记忆
        cursor = self.conn.execute("""
            SELECT COUNT(*) as count
            FROM l1_records
            WHERE created_time >= date('now', '-7 days')
        """)
        insights['recent_7days'] = cursor.fetchone()['count']
        
        # 高优先级记忆数量
        cursor = self.conn.execute("""
            SELECT COUNT(*) as count
            FROM l1_records
            WHERE priority >= 80
        """)
        insights['high_priority'] = cursor.fetchone()['count']
        
        return insights
    
    def close(self):
        """关闭连接"""
        if self.conn:
            self.conn.close()


def main():
    """CLI 入口"""
    import argparse
    parser = argparse.ArgumentParser(description='智能记忆召回')
    parser.add_argument('--query', '-q', type=str, help='搜索查询')
    parser.add_argument('--type', '-t', type=str, help='按类型召回')
    parser.add_argument('--entity', '-e', type=str, help='按实体召回')
    parser.add_argument('--limit', '-l', type=int, default=10, help='返回数量')
    parser.add_argument('--insights', '-i', action='store_true', help='显示召回洞察')
    args = parser.parse_args()
    
    recall = IntelligentRecall()
    
    if args.insights:
        insights = recall.get_recall_insights()
        print("# 🔍 召回洞察")
        print(f"- 最近7天新增：{insights.get('recent_7days', 0)} 条")
        print(f"- 高优先级：{insights.get('high_priority', 0)} 条")
        print("\n## 类型分布")
        for t in insights.get('top_types', []):
            print(f"- {t['type']}：{t['count']} 条")
    
    elif args.type:
        results = recall.recall_by_type(args.type, args.limit)
        print(f"# 📂 类型: {args.type} ({len(results)} 条)")
        for r in results:
            print(f"\n## {r['record_id']} [P{r['priority']}]")
            print(f"{r['content'][:100]}...")
    
    elif args.entity:
        results = recall.recall_by_entity(args.entity, args.limit)
        print(f"# 👤 实体: {args.entity} ({len(results)} 条)")
        for r in results:
            print(f"\n## {r['record_id']}")
            print(f"{r['content'][:100]}...")
    
    elif args.query:
        results = recall.recall_by_query(args.query, args.limit)
        print(f"# 🔍 查询: \"{args.query}\" ({len(results)} 条)")
        for r in results:
            print(f"\n## [{r['score']}] {r['record_id']} [P{r['priority']}]")
            print(f"{r['content'][:100]}...")
            print(f"   分数明细: {r['breakdown']}")
    
    else:
        print("# 💡 智能召回")
        print("用法：")
        print("  --query <关键词>     按关键词召回")
        print("  --type <类型>       按类型召回")
        print("  --entity <实体>     按实体召回")
        print("  --insights          召回洞察")
    
    recall.close()


if __name__ == '__main__':
    main()
