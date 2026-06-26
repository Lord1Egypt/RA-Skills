#!/usr/bin/env python3
"""
记忆对比模块 - 比较两个记忆或时间点的差异

功能：
- 记忆版本对比
- 时间点快照对比
- 类型分布变化
- 重要性变化追踪
- 生成差异报告
"""

import sys
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Set
from collections import Counter, defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent))
from paths import get_vectors_db, get_memory_base


class MemoryDiff:
    """记忆对比器"""
    
    def __init__(self):
        self.db_path = get_vectors_db()
        self.memory_base = get_memory_base()
        self.conn = None
        self._connect()
    
    def _connect(self):
        """连接数据库"""
        if Path(self.db_path).exists():
            self.conn = sqlite3.connect(str(self.db_path))
            self.conn.row_factory = sqlite3.Row
    
    def get_snapshot(self, days_ago: int = 0) -> Dict:
        """获取指定天数的快照"""
        if not self.conn:
            return {}
        
        cursor = self.conn.execute("""
            SELECT record_id, content, type, priority, created_time
            FROM l1_records
            WHERE created_time >= date('now', ?) AND created_time < date('now', ?, '+1 day')
        """, (f'-{days_ago + 1} days', f'-{days_ago} days'))
        
        snapshot = {
            'date': (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d'),
            'count': 0,
            'by_type': Counter(),
            'by_priority': Counter(),
            'ids': set(),
            'content_hashes': set()
        }
        
        import hashlib
        for row in cursor.fetchall():
            snapshot['count'] += 1
            snapshot['by_type'][row['type'] or 'unknown'] += 1
            snapshot['by_priority'][str((row['priority'] or 50) // 10 * 10)] += 1  # 按10分组
            snapshot['ids'].add(row['record_id'])
            # 内容哈希
            content_hash = hashlib.md5((row['content'] or '').encode()).hexdigest()[:8]
            snapshot['content_hashes'].add(content_hash)
        
        return snapshot
    
    def compare_snapshots(self, snapshot1: Dict, snapshot2: Dict) -> Dict:
        """比较两个快照"""
        # 共同记忆和新记忆
        common_ids = snapshot1['ids'] & snapshot2['ids']
        new_in_snapshot2 = snapshot2['ids'] - snapshot1['ids']
        removed_from_snapshot1 = snapshot1['ids'] - snapshot2['ids']
        
        # 类型变化
        added_types = dict(snapshot2['by_type'] - snapshot1['by_type'])
        removed_types = dict(snapshot1['by_type'] - snapshot2['by_type'])
        
        # 优先级变化
        priority_change = {}
        for level in ['0', '10', '20', '30', '40', '50', '60', '70', '80', '90', '100']:
            c1 = snapshot1['by_priority'].get(level, 0)
            c2 = snapshot2['by_priority'].get(level, 0)
            if c2 != c1:
                priority_change[f'{level}'] = {'before': c1, 'after': c2, 'delta': c2 - c1}
        
        return {
            'common_count': len(common_ids),
            'new_count': len(new_in_snapshot2),
            'removed_count': len(removed_from_snapshot1),
            'count_delta': snapshot2['count'] - snapshot1['count'],
            'added_types': added_types,
            'removed_types': removed_types,
            'priority_changes': priority_change,
            'growth_rate': round((snapshot2['count'] - snapshot1['count']) / max(snapshot1['count'], 1) * 100, 1)
        }
    
    def compare_memories(self, id1: str, id2: str) -> Dict:
        """比较两条记忆"""
        if not self.conn:
            return {}
        
        cursor = self.conn.execute("""
            SELECT record_id, content, type, priority, created_time
            FROM l1_records
            WHERE record_id IN (?, ?)
        """, (id1, id2))
        
        memories = {}
        for row in cursor.fetchall():
            memories[row['record_id']] = {
                'content': row['content'],
                'type': row['type'],
                'priority': row['priority'],
                'created': row['created_time']
            }
        
        if id1 not in memories or id2 not in memories:
            return {'error': 'Memory not found'}
        
        m1 = memories[id1]
        m2 = memories[id2]
        
        # 简单相似度
        words1 = set((m1['content'] or '').split())
        words2 = set((m2['content'] or '').split())
        similarity = len(words1 & words2) / max(len(words1 | words2), 1)
        
        return {
            'memory1': m1,
            'memory2': m2,
            'similarity': round(similarity, 2),
            'content_length_delta': len(m2['content'] or '') - len(m1['content'] or ''),
            'priority_delta': (m2['priority'] or 50) - (m1['priority'] or 50)
        }
    
    def find_similar_memories(self, content: str, threshold: float = 0.3, limit: int = 5) -> List[Dict]:
        """查找相似记忆"""
        if not self.conn:
            return []
        
        content_words = set(content.lower().split())
        
        cursor = self.conn.execute("""
            SELECT record_id, content, type, priority, created_time
            FROM l1_records
            LIMIT 100
        """)
        
        similar = []
        for row in cursor.fetchall():
            row_words = set((row['content'] or '').lower().split())
            
            if not content_words or not row_words:
                continue
            
            similarity = len(content_words & row_words) / max(len(content_words | row_words), 1)
            
            if similarity >= threshold:
                similar.append({
                    'id': row['record_id'],
                    'content': row['content'][:50],
                    'similarity': round(similarity, 2),
                    'type': row['type'],
                    'priority': row['priority']
                })
        
        similar.sort(key=lambda x: x['similarity'], reverse=True)
        return similar[:limit]
    
    def generate_diff_report(self, days_ago1: int, days_ago2: int) -> str:
        """生成差异报告"""
        snapshot1 = self.get_snapshot(days_ago1)
        snapshot2 = self.get_snapshot(days_ago2)
        
        if not snapshot1['ids'] and not snapshot2['ids']:
            return "# 📊 记忆对比\n\n（两个时间点都暂无记忆）"
        
        comparison = self.compare_snapshots(snapshot1, snapshot2)
        
        lines = ["# 📊 记忆对比报告", ""]
        lines.append(f"**对比时间**：{snapshot1['date']} vs {snapshot2['date']}")
        lines.append("")
        
        # 数量变化
        lines.append("## 📈 数量变化")
        delta_emoji = "📈" if comparison['count_delta'] > 0 else "📉" if comparison['count_delta'] < 0 else "➡️"
        lines.append(f"{delta_emoji} {snapshot1['count']} → {snapshot2['count']} (Δ {comparison['count_delta']:+d})")
        lines.append(f"增长率：{comparison['growth_rate']:+}%")
        lines.append("")
        
        # 新增和删除
        lines.append("## 🆕 新增 / 🗑️ 删除")
        lines.append(f"- 新增：{comparison['new_count']} 条")
        lines.append(f"- 删除：{comparison['removed_count']} 条")
        lines.append("")
        
        # 类型变化
        if comparison['added_types'] or comparison['removed_types']:
            lines.append("## 📂 类型变化")
            for t, c in comparison['added_types'].items():
                lines.append(f"- 🆕 {t}：+{c}")
            for t, c in comparison['removed_types'].items():
                lines.append(f"- 🗑️ {t}：-{c}")
            lines.append("")
        
        # 优先级变化
        if comparison['priority_changes']:
            lines.append("## ⚖️ 优先级变化")
            for level, change in sorted(comparison['priority_changes'].items()):
                if change['delta'] != 0:
                    emoji = "⬆️" if change['delta'] > 0 else "⬇️"
                    lines.append(f"- P{level}: {emoji} {change['before']} → {change['after']} ({change['delta']:+d})")
            lines.append("")
        
        return "\n".join(lines)
    
    def get_memory_evolution(self, limit: int = 10) -> List[Dict]:
        """获取记忆演进（按时间排序的高优先级记忆）"""
        if not self.conn:
            return []
        
        cursor = self.conn.execute("""
            SELECT record_id, content, type, priority, created_time
            FROM l1_records
            ORDER BY created_time ASC, priority DESC
            LIMIT ?
        """, (limit,))
        
        evolution = []
        for row in cursor.fetchall():
            evolution.append({
                'id': row['record_id'],
                'content': row['content'][:60],
                'type': row['type'],
                'priority': row['priority'],
                'date': row['created_time'][:10] if row['created_time'] else ''
            })
        
        return evolution
    
    def close(self):
        """关闭连接"""
        if self.conn:
            self.conn.close()


def main():
    """CLI 入口"""
    import argparse
    parser = argparse.ArgumentParser(description='记忆对比')
    parser.add_argument('--days', nargs=2, type=int, metavar=('BEFORE', 'AFTER'), help='对比两个时间点')
    parser.add_argument('--similar', '-s', type=str, help='查找相似记忆')
    parser.add_argument('--evolution', '-e', action='store_true', help='记忆演进')
    args = parser.parse_args()
    
    diff = MemoryDiff()
    
    if args.days:
        report = diff.generate_diff_report(args.days[0], args.days[1])
        print(report)
    elif args.similar:
        similar = diff.find_similar_memories(args.similar)
        print(f"# 🔍 与「{args.similar[:30]}」相似的记忆：")
        for s in similar:
            print(f"\n## [{s['similarity']}] {s['id']} [P{s['priority']}]")
            print(f"{s['content']}...")
    elif args.evolution:
        evo = diff.get_memory_evolution()
        print("# 📈 记忆演进")
        for i, e in enumerate(evo):
            print(f"\n{i+1}. {e['date']} [P{e['priority']}] {e['type']}")
            print(f"   {e['content']}...")
    else:
        # 默认对比昨天和今天
        report = diff.generate_diff_report(1, 0)
        print(report)
    
    diff.close()


if __name__ == '__main__':
    main()
