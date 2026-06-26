#!/usr/bin/env python3
"""
记忆时间线模块 - 生成记忆时间线和历史视图

功能：
- 按时间生成记忆时间线
- 生成每日/每周/每月摘要
- 生成里程碑时间线
- 生成关系时间线
- ASCII 可视化
"""

import sys
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent))
from paths import get_vectors_db, get_memory_base


class MemoryTimeline:
    """记忆时间线"""
    
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
    
    def get_daily_timeline(self, days: int = 7) -> Dict[str, List[Dict]]:
        """获取每日时间线"""
        if not self.conn:
            return {}
        
        cursor = self.conn.execute("""
            SELECT record_id, content, type, priority, created_time
            FROM l1_records
            WHERE created_time >= date('now', ?)
            ORDER BY created_time DESC
        """, (f'-{days} days',))
        
        timeline = defaultdict(list)
        
        for row in cursor.fetchall():
            date = row['created_time'][:10] if row['created_time'] else 'unknown'
            timeline[date].append({
                'id': row['record_id'],
                'content': row['content'],
                'type': row['type'],
                'priority': row['priority'],
                'time': row['created_time'][11:16] if row['created_time'] and len(row['created_time']) > 16 else ''
            })
        
        return dict(timeline)
    
    def get_weekly_summary(self, weeks: int = 4) -> List[Dict]:
        """获取每周摘要"""
        if not self.conn:
            return []
        
        summaries = []
        
        for week in range(weeks):
            offset = f'-{week * 7} days'
            
            cursor = self.conn.execute("""
                SELECT 
                    COUNT(*) as total,
                    type,
                    AVG(priority) as avg_priority
                FROM l1_records
                WHERE created_time >= date('now', ?) AND created_time < date('now', ?, '+7 days')
                GROUP BY type
            """, (offset, offset))
            
            week_data = {
                'week': week,
                'offset': offset,
                'total': 0,
                'by_type': {},
                'avg_priority': 0
            }
            
            type_counts = []
            priorities = []
            
            for row in cursor.fetchall():
                week_data['total'] += row['total']
                week_data['by_type'][row['type'] or 'unknown'] = row['total']
                if row['avg_priority']:
                    priorities.append(row['avg_priority'])
            
            if priorities:
                week_data['avg_priority'] = sum(priorities) / len(priorities)
            
            summaries.append(week_data)
        
        return summaries
    
    def get_monthly_summary(self, months: int = 6) -> List[Dict]:
        """获取每月摘要"""
        if not self.conn:
            return []
        
        summaries = []
        
        for month in range(months):
            offset = f'-{month} months'
            
            cursor = self.conn.execute("""
                SELECT 
                    COUNT(*) as total,
                    type,
                    AVG(priority) as avg_priority
                FROM l1_records
                WHERE created_time >= date('now', ?) AND created_time < date('now', ?, '+1 month')
                GROUP BY type
            """, (offset, offset))
            
            month_data = {
                'month': month,
                'total': 0,
                'by_type': {},
                'avg_priority': 0
            }
            
            priorities = []
            
            for row in cursor.fetchall():
                month_data['total'] += row['total']
                month_data['by_type'][row['type'] or 'unknown'] = row['total']
                if row['avg_priority']:
                    priorities.append(row['avg_priority'])
            
            if priorities:
                month_data['avg_priority'] = round(sum(priorities) / len(priorities), 1)
            
            summaries.append(month_data)
        
        return summaries
    
    def get_milestones(self, limit: int = 10) -> List[Dict]:
        """获取里程碑（高优先级记忆）"""
        if not self.conn:
            return []
        
        cursor = self.conn.execute("""
            SELECT record_id, content, type, priority, created_time
            FROM l1_records
            WHERE priority >= 80
            ORDER BY priority DESC, created_time DESC
            LIMIT ?
        """, (limit,))
        
        milestones = []
        for row in cursor.fetchall():
            milestones.append({
                'id': row['record_id'],
                'content': row['content'][:80],
                'type': row['type'],
                'priority': row['priority'],
                'date': row['created_time'][:10] if row['created_time'] else ''
            })
        
        return milestones
    
    def generate_ascii_timeline(self, days: int = 7) -> str:
        """生成 ASCII 时间线"""
        lines = ["# 📅 记忆时间线", ""]
        
        daily = self.get_daily_timeline(days)
        
        if not daily:
            lines.append("_（暂无记忆）_")
            return "\n".join(lines)
        
        # 生成时间线
        for date, memories in sorted(daily.items(), reverse=True):
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            date_str = date_obj.strftime('%m/%d')
            weekday = date_obj.strftime('%a')
            
            # 日期头部
            bar_length = min(len(memories), 20)
            bar = "█" * bar_length + "░" * (20 - bar_length)
            
            lines.append(f"[{date_str} {weekday}] {bar} ({len(memories)}条)")
            
            # 显示高优先级记忆
            high_priority = [m for m in memories if m['priority'] >= 70]
            for m in high_priority[:3]:
                content = m['content'][:40].replace('\n', ' ')
                lines.append(f"  📌 [{m['type']}] {content}...")
            
            lines.append("")
        
        return "\n".join(lines)
    
    def generate_relationship_timeline(self, entity: str, limit: int = 20) -> str:
        """生成与某个实体相关的时间线"""
        if not self.conn:
            return ""
        
        cursor = self.conn.execute("""
            SELECT record_id, content, type, priority, created_time
            FROM l1_records
            WHERE content LIKE ?
            ORDER BY created_time DESC
            LIMIT ?
        """, (f'%{entity}%', limit))
        
        lines = [f"# 🔗 关于「{entity}」的时间线", ""]
        
        memories = [dict(row) for row in cursor.fetchall()]
        
        if not memories:
            lines.append("_（暂无相关记忆）_")
            return "\n".join(lines)
        
        current_month = None
        for m in memories:
            date = m['created_time'][:10] if m['created_time'] else ''
            month = date[:7] if date else ''
            
            if month != current_month:
                current_month = month
                lines.append(f"\n## 📆 {month}")
                lines.append("-" * 40)
            
            content = m['content'][:50].replace('\n', ' ')
            lines.append(f"**{date}** [{m['type']}] {content}...")
        
        return "\n".join(lines)
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        if not self.conn:
            return {}
        
        stats = {}
        
        # 总记忆数
        cursor = self.conn.execute("SELECT COUNT(*) as count FROM l1_records")
        stats['total'] = cursor.fetchone()['count']
        
        # 各类型数量
        cursor = self.conn.execute("""
            SELECT type, COUNT(*) as count 
            FROM l1_records 
            GROUP BY type
        """)
        stats['by_type'] = {row['type'] or 'unknown': row['count'] for row in cursor.fetchall()}
        
        # 高优先级数量
        cursor = self.conn.execute("""
            SELECT COUNT(*) as count FROM l1_records WHERE priority >= 80
        """)
        stats['high_priority'] = cursor.fetchone()['count']
        
        # 平均优先级
        cursor = self.conn.execute("""
            SELECT AVG(priority) as avg FROM l1_records WHERE priority IS NOT NULL
        """)
        avg = cursor.fetchone()['avg']
        stats['avg_priority'] = round(avg, 1) if avg else 0
        
        # 时间范围
        cursor = self.conn.execute("""
            SELECT MIN(created_time) as oldest, MAX(created_time) as newest
            FROM l1_records
        """)
        row = cursor.fetchone()
        stats['oldest'] = row['oldest'][:10] if row['oldest'] else None
        stats['newest'] = row['newest'][:10] if row['newest'] else None
        
        return stats
    
    def close(self):
        """关闭连接"""
        if self.conn:
            self.conn.close()


def main():
    """CLI 入口"""
    import argparse
    parser = argparse.ArgumentParser(description='记忆时间线')
    parser.add_argument('--days', '-d', type=int, default=7, help='显示天数')
    parser.add_argument('--timeline', '-t', action='store_true', help='ASCII 时间线')
    parser.add_argument('--weekly', '-w', action='store_true', help='每周摘要')
    parser.add_argument('--monthly', '-m', action='store_true', help='每月摘要')
    parser.add_argument('--milestones', '-M', action='store_true', help='里程碑')
    parser.add_argument('--stats', '-s', action='store_true', help='统计信息')
    parser.add_argument('--entity', '-e', type=str, help='实体时间线')
    args = parser.parse_args()
    
    timeline = MemoryTimeline()
    
    if args.timeline:
        print(timeline.generate_ascii_timeline(args.days))
    elif args.weekly:
        summaries = timeline.get_weekly_summary()
        print("# 📊 每周摘要")
        for s in summaries:
            print(f"\n## 第 {s['week'] + 1} 周")
            print(f"总记忆：{s['total']} 条")
            print(f"平均优先级：{s['avg_priority']}")
            for t, c in s['by_type'].items():
                print(f"  - {t}：{c}")
    elif args.monthly:
        summaries = timeline.get_monthly_summary()
        print("# 📊 每月摘要")
        for s in summaries:
            print(f"\n## {s['month']} 个月前")
            print(f"总记忆：{s['total']} 条")
            print(f"平均优先级：{s['avg_priority']}")
    elif args.milestones:
        milestones = timeline.get_milestones()
        print("# ⭐ 里程碑")
        for m in milestones:
            print(f"\n## {m['date']} [P{m['priority']}]")
            print(f"{m['content']}")
    elif args.entity:
        print(timeline.generate_relationship_timeline(args.entity))
    elif args.stats:
        stats = timeline.get_statistics()
        print("# 📊 时间线统计")
        print(f"- 总记忆：{stats['total']} 条")
        print(f"- 高优先级：{stats['high_priority']} 条")
        print(f"- 平均优先级：{stats['avg_priority']}")
        print(f"- 时间范围：{stats['oldest']} ~ {stats['newest']}")
        print("\n## 类型分布")
        for t, c in stats['by_type'].items():
            print(f"- {t}：{c}")
    else:
        print(timeline.generate_ascii_timeline(args.days))
    
    timeline.close()


if __name__ == '__main__':
    main()
