#!/usr/bin/env python3
"""
记忆统计模块 - 详细统计分析

功能：
- 类型分布统计
- 时间分布统计
- 重要性分布
- 访问频率统计
- 成长趋势
- 健康度评分
"""

import sys
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import Counter, defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent))
from paths import get_vectors_db, get_memory_base


class MemoryStats:
    """记忆统计器"""
    
    def __init__(self):
        self.db_path = get_vectors_db()
        self.memory_base = get_memory_base()
        self.conn = None
        self._connect()
    
    def _connect(self):
        if Path(self.db_path).exists():
            self.conn = sqlite3.connect(str(self.db_path))
            self.conn.row_factory = sqlite3.Row
    
    def get_type_distribution(self) -> Dict[str, int]:
        """获取类型分布"""
        if not self.conn:
            return {}
        
        cursor = self.conn.execute("""
            SELECT type, COUNT(*) as count
            FROM l1_records
            GROUP BY type
            ORDER BY count DESC
        """)
        
        return {row['type'] or 'unknown': row['count'] for row in cursor.fetchall()}
    
    def get_priority_distribution(self) -> Dict[str, int]:
        """获取优先级分布"""
        if not self.conn:
            return {}
        
        cursor = self.conn.execute("""
            SELECT 
                CASE 
                    WHEN priority >= 90 THEN 'critical (90-100)'
                    WHEN priority >= 70 THEN 'high (70-89)'
                    WHEN priority >= 40 THEN 'normal (40-69)'
                    ELSE 'low (0-39)'
                END as level,
                COUNT(*) as count
            FROM l1_records
            GROUP BY level
            ORDER BY count DESC
        """)
        
        return {row['level']: row['count'] for row in cursor.fetchall()}
    
    def get_time_distribution(self, days: int = 30) -> Dict[str, int]:
        """获取时间分布（按天）"""
        if not self.conn:
            return {}
        
        cursor = self.conn.execute("""
            SELECT DATE(created_time) as date, COUNT(*) as count
            FROM l1_records
            WHERE created_time >= date('now', ?)
            GROUP BY DATE(created_time)
            ORDER BY date
        """, (f'-{days} days',))
        
        return {row['date']: row['count'] for row in cursor.fetchall()}
    
    def get_hour_distribution(self) -> Dict[int, int]:
        """获取小时分布"""
        if not self.conn:
            return {}
        
        cursor = self.conn.execute("""
            SELECT CAST(strftime('%H', created_time) AS INTEGER) as hour, COUNT(*) as count
            FROM l1_records
            WHERE created_time IS NOT NULL
            GROUP BY hour
            ORDER BY hour
        """)
        
        return {row['hour'] or 0: row['count'] for row in cursor.fetchall()}
    
    def get_growth_trend(self) -> List[Dict]:
        """获取增长趋势"""
        if not self.conn:
            return []
        
        cursor = self.conn.execute("""
            SELECT 
                DATE(created_time) as date,
                COUNT(*) as total_count,
                COUNT(DISTINCT type) as type_count,
                AVG(priority) as avg_priority
            FROM l1_records
            WHERE created_time >= date('now', '-30 days')
            GROUP BY DATE(created_time)
            ORDER BY date
        """)
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_content_stats(self) -> Dict:
        """获取内容统计"""
        if not self.conn:
            return {}
        
        cursor = self.conn.execute("""
            SELECT 
                COUNT(*) as total,
                AVG(LENGTH(content)) as avg_length,
                MAX(LENGTH(content)) as max_length,
                MIN(LENGTH(content)) as min_length
            FROM l1_records
            WHERE content IS NOT NULL
        """)
        
        row = cursor.fetchone()
        return {
            'total': row['total'] or 0,
            'avg_length': round(row['avg_length'] or 0, 1),
            'max_length': row['max_length'] or 0,
            'min_length': row['min_length'] or 0
        }
    
    def get_top_keywords(self, limit: int = 20) -> List[Tuple[str, int]]:
        """获取高频关键词"""
        if not self.conn:
            return []
        
        cursor = self.conn.execute("""
            SELECT content FROM l1_records LIMIT 500
        """)
        
        word_counter = Counter()
        
        for row in cursor.fetchall():
            content = row['content'] or ''
            # 简单分词
            words = content.split()
            # 过滤短词
            words = [w for w in words if len(w) >= 2]
            word_counter.update(words)
        
        return word_counter.most_common(limit)
    
    def calculate_health_score(self) -> Dict:
        """计算记忆健康度"""
        if not self.conn:
            return {'score': 0, 'status': '无数据'}
        
        # 基本指标
        cursor = self.conn.execute("SELECT COUNT(*) as total FROM l1_records")
        total = cursor.fetchone()['total']
        
        if total == 0:
            return {'score': 0, 'status': '无记忆'}
        
        scores = {}
        
        # 1. 数量健康度 (0-25)
        if total >= 100:
            scores['quantity'] = 25
        elif total >= 50:
            scores['quantity'] = 20
        elif total >= 20:
            scores['quantity'] = 15
        else:
            scores['quantity'] = max(5, total // 4)
        
        # 2. 类型多样性 (0-25)
        cursor = self.conn.execute("SELECT COUNT(DISTINCT type) as types FROM l1_records")
        types = cursor.fetchone()['types']
        scores['diversity'] = min(types * 5, 25)
        
        # 3. 优先级健康度 (0-25)
        cursor = self.conn.execute("SELECT AVG(priority) as avg FROM l1_records WHERE priority IS NOT NULL")
        avg_priority = cursor.fetchone()['avg'] or 50
        scores['priority'] = min(avg_priority // 4, 25)
        
        # 4. 内容完整度 (0-25)
        cursor = self.conn.execute("""
            SELECT AVG(LENGTH(content)) as avg_len FROM l1_records WHERE content IS NOT NULL
        """)
        avg_len = cursor.fetchone()['avg_len'] or 0
        if avg_len >= 100:
            scores['completeness'] = 25
        elif avg_len >= 50:
            scores['completeness'] = 20
        elif avg_len >= 20:
            scores['completeness'] = 15
        else:
            scores['completeness'] = 10
        
        total_score = sum(scores.values())
        
        # 状态判定
        if total_score >= 80:
            status = "优秀"
        elif total_score >= 60:
            status = "良好"
        elif total_score >= 40:
            status = "一般"
        else:
            status = "需优化"
        
        return {
            'score': total_score,
            'status': status,
            'details': scores
        }
    
    def generate_full_report(self) -> str:
        """生成完整统计报告"""
        lines = ["# 📊 记忆统计分析报告", ""]
        lines.append(f"**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append("")
        
        # 健康度
        health = self.calculate_health_score()
        lines.append(f"## 🏥 健康度：{health['score']}/100 （{health['status']}）")
        if 'details' in health:
            for k, v in health['details'].items():
                lines.append(f"- {k}：{v}/25")
        lines.append("")
        
        # 基本统计
        content_stats = self.get_content_stats()
        lines.append("## 📈 基本统计")
        lines.append(f"- 总记忆数：{content_stats['total']} 条")
        lines.append(f"- 平均长度：{content_stats['avg_length']} 字符")
        lines.append(f"- 最长：{content_stats['max_length']} 字符")
        lines.append(f"- 最短：{content_stats['min_length']} 字符")
        lines.append("")
        
        # 类型分布
        type_dist = self.get_type_distribution()
        if type_dist:
            lines.append("## 📂 类型分布")
            for t, count in sorted(type_dist.items(), key=lambda x: -x[1])[:10]:
                pct = count * 100 // max(content_stats['total'], 1)
                bar = "█" * pct + "░" * (20 - pct)
                lines.append(f"{t:12} │ {bar} {count} ({pct}%)")
            lines.append("")
        
        # 优先级分布
        priority_dist = self.get_priority_distribution()
        if priority_dist:
            lines.append("## ⚖️ 优先级分布")
            for level, count in priority_dist.items():
                pct = count * 100 // max(content_stats['total'], 1)
                bar = "█" * pct + "░" * (20 - pct)
                lines.append(f"{level:15} │ {bar} {count}")
            lines.append("")
        
        # 高频关键词
        keywords = self.get_top_keywords(15)
        if keywords:
            lines.append("## 🔑 高频关键词 TOP15")
            kw_str = "、".join([f"{w}({c})" for w, c in keywords[:15]])
            lines.append(kw_str)
            lines.append("")
        
        return "\n".join(lines)
    
    def close(self):
        if self.conn:
            self.conn.close()


def main():
    import argparse
    parser = argparse.ArgumentParser(description='记忆统计')
    parser.add_argument('--report', '-r', action='store_true', help='完整报告')
    parser.add_argument('--health', action='store_true', help='健康度')
    parser.add_argument('--types', action='store_true', help='类型分布')
    parser.add_argument('--keywords', '-k', action='store_true', help='高频关键词')
    args = parser.parse_args()
    
    stats = MemoryStats()
    
    if args.health:
        health = stats.calculate_health_score()
        print(f"# 🏥 健康度：{health['score']}/100 ({health['status']})")
        if 'details' in health:
            for k, v in health['details'].items():
                print(f"- {k}: {v}/25")
    elif args.types:
        dist = stats.get_type_distribution()
        print("# 📂 类型分布")
        for t, c in sorted(dist.items(), key=lambda x: -x[1]):
            print(f"- {t}: {c}")
    elif args.keywords:
        kws = stats.get_top_keywords()
        print("# 🔑 高频关键词")
        for w, c in kws[:20]:
            print(f"- {w}: {c}次")
    else:
        print(stats.generate_full_report())
    
    stats.close()


if __name__ == '__main__':
    main()
