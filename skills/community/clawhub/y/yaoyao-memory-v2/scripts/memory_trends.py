#!/usr/bin/env python3
"""
记忆趋势分析模块 - 分析和可视化记忆变化趋势

功能：
- 记忆数量时间序列
- 记忆类型分布变化
- 重要性等级趋势
- 热度追踪（访问频率）
- 遗忘曲线分析
- 记忆健康度评分
"""

import sys
import json
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent))
from paths import get_vectors_db, get_memory_base


class MemoryTrends:
    """记忆趋势分析器"""
    
    def __init__(self, days: int = 30):
        self.days = days
        self.db_path = get_vectors_db()
        self.memory_base = get_memory_base()
        self.conn = None
        self._connect()
    
    def _connect(self):
        """连接数据库"""
        if Path(self.db_path).exists():
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
    
    def get_memory_count_timeline(self) -> List[Dict]:
        """获取记忆数量时间线"""
        if not self.conn:
            return []
        
        cursor = self.conn.execute("""
            SELECT DATE(created_time) as date, COUNT(*) as count
            FROM l1_records
            WHERE created_time >= date('now', ?)
            GROUP BY DATE(created_time)
            ORDER BY date
        """, (f'-{self.days} days',))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_type_distribution(self) -> Dict[str, int]:
        """获取记忆类型分布"""
        if not self.conn:
            return {}
        
        cursor = self.conn.execute("""
            SELECT type, COUNT(*) as count
            FROM l1_records
            WHERE created_time >= date('now', ?)
            GROUP BY type
        """, (f'-{self.days} days',))
        
        return {row['type']: row['count'] for row in cursor.fetchall()}
    
    def get_importance_distribution(self) -> Dict[str, int]:
        """获取重要性等级分布"""
        if not self.conn:
            return {}
        
        cursor = self.conn.execute("""
            SELECT importance, COUNT(*) as count
            FROM l1_records
            GROUP BY type
        """)
        
        return {row['type']: row['count'] for row in cursor.fetchall()}
    
    def get_access_frequency(self) -> List[Dict]:
        """获取访问频率（热度）"""
        if not self.conn:
            return []
        
        cursor = self.conn.execute("""
            SELECT content, priority, updated_time
            FROM l1_records
            WHERE priority > 0
            ORDER BY priority DESC
            LIMIT 20
        """)
        
        return [dict(row) for row in cursor.fetchall()]
    
    def calculate_forgetting_risk(self) -> List[Dict]:
        """计算遗忘风险（长时间未访问的记忆）"""
        if not self.conn:
            return []
        
        cursor = self.conn.execute("""
            SELECT id, content, updated_time,
                   julianday('now') - julianday(updated_time) as days_since_access
            FROM l1_records
            WHERE updated_time IS NOT NULL
            AND priority < 3
            AND julianday('now') - julianday(updated_time) > 7
            ORDER BY days_since_access DESC
            LIMIT 10
        """)
        
        return [dict(row) for row in cursor.fetchall()]
    
    def calculate_health_score(self) -> Dict:
        """计算记忆系统健康度"""
        if not self.conn:
            return {"score": 0, "status": "无数据"}
        
        # 基本统计
        cursor = self.conn.execute("SELECT COUNT(*) as total FROM l1_records")
        total = cursor.fetchone()['total']
        
        if total == 0:
            return {"score": 0, "status": "无记忆"}
        
        # 访问率
        cursor = self.conn.execute("""
            SELECT COUNT(*) as accessed
            FROM l1_records
            WHERE priority > 0
        """)
        accessed = cursor.fetchone()['accessed']
        access_rate = accessed / total
        
        # 有内容记忆比例
        cursor = self.conn.execute("""
            SELECT COUNT(*) as with_content
            FROM l1_records
            WHERE length(content) > 50
        """)
        with_content = cursor.fetchone()['with_content']
        content_rate = with_content / total
        
        # 分类率
        cursor = self.conn.execute("""
            SELECT COUNT(*) as categorized
            FROM l1_records
            WHERE type != 'unknown'
        """)
        categorized = cursor.fetchone()['categorized']
        category_rate = categorized / total
        
        # 综合评分
        score = (
            min(access_rate * 40, 40) +      # 访问率 0-40
            min(content_rate * 30, 30) +      # 内容完整率 0-30
            min(category_rate * 30, 30)       # 分类率 0-30
        )
        
        # 状态判定
        if score >= 80:
            status = "优秀"
        elif score >= 60:
            status = "良好"
        elif score >= 40:
            status = "一般"
        else:
            status = "需优化"
        
        return {
            "score": round(score, 1),
            "status": status,
            "details": {
                "total_memories": total,
                "access_rate": round(access_rate * 100, 1),
                "content_rate": round(content_rate * 100, 1),
                "category_rate": round(category_rate * 100, 1)
            }
        }
    
    def generate_trend_report(self) -> str:
        """生成趋势分析报告"""
        lines = ["# 📊 记忆趋势分析报告", ""]
        lines.append(f"**分析周期**：过去 {self.days} 天")
        lines.append(f"**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append("")
        
        # 健康度
        health = self.calculate_health_score()
        lines.append(f"## 🏥 健康度评分：{health['score']}/100 （{health['status']}）")
        if 'details' in health:
            d = health['details']
            lines.append(f"- 总记忆数：{d['total_memories']}")
            lines.append(f"- 访问率：{d['access_rate']}%")
            lines.append(f"- 内容完整率：{d['content_rate']}%")
            lines.append(f"- 分类率：{d['category_rate']}%")
        lines.append("")
        
        # 类型分布
        type_dist = self.get_type_distribution()
        if type_dist:
            lines.append("## 📈 类型分布")
            for t, count in sorted(type_dist.items(), key=lambda x: -x[1]):
                lines.append(f"- {t}：{count}")
            lines.append("")
        
        # 重要性分布
        imp_dist = self.get_importance_distribution()
        if imp_dist:
            lines.append("## ⚖️ 重要性分布")
            for level in ['critical', 'high', 'normal', 'low']:
                count = imp_dist.get(level, 0)
                lines.append(f"- {level}：{count}")
            lines.append("")
        
        # 热度排行
        hot_memories = self.get_access_frequency()[:5]
        if hot_memories:
            lines.append("## 🔥 热度排行 TOP5")
            for i, m in enumerate(hot_memories, 1):
                content = m['content'][:30] + "..." if len(m['content']) > 30 else m['content']
                lines.append(f"{i}. {content} （访问 {m['priority']} 次）")
            lines.append("")
        
        # 遗忘风险
        forgetting_risk = self.get_forgetting_risk()
        if forgetting_risk:
            lines.append("## ⚠️ 遗忘风险提醒")
            for m in forgetting_risk[:3]:
                days = int(m['days_since_access'])
                content = m['content'][:25] + "..." if len(m['content']) > 25 else m['content']
                lines.append(f"- [{days}天未访问] {content}")
            lines.append("")
        
        return "\n".join(lines)
    
    def close(self):
        """关闭连接"""
        if self.conn:
            self.conn.close()


def main():
    """CLI 入口"""
    import argparse
    parser = argparse.ArgumentParser(description='记忆趋势分析')
    parser.add_argument('--days', '-d', type=int, default=30, help='分析天数')
    parser.add_argument('--format', '-f', choices=['text', 'json'], default='text', help='输出格式')
    parser.add_argument('--timeline', '-t', action='store_true', help='显示时间线')
    parser.add_argument('--health', action='store_true', help='显示健康度')
    args = parser.parse_args()
    
    trends = MemoryTrends(days=args.days)
    
    if args.health:
        result = trends.calculate_health_score()
        if args.format == 'json':
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"🏥 健康度：{result['score']}/100 （{result['status']}）")
            if 'details' in result:
                for k, v in result['details'].items():
                    print(f"  {k}：{v}")
    elif args.timeline:
        timeline = trends.get_memory_count_timeline()
        if args.format == 'json':
            print(json.dumps(timeline, ensure_ascii=False, indent=2))
        else:
            print("# 📅 记忆数量时间线")
            for item in timeline:
                print(f"{item['date']}：{item['count']} 条")
    else:
        print(trends.generate_trend_report())
    
    trends.close()


if __name__ == '__main__':
    main()
