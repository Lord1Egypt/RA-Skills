#!/usr/bin/env python3
"""
记忆提醒器 - 主动提醒用户重要记忆

功能：
- 基于时间的提醒（定期复习、重要日期）
- 基于事件的提醒（临近的决策复查）
- 遗忘曲线复习提醒
- 习惯养成追踪提醒
"""

import sys
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent.parent))
from paths import get_vectors_db


class MemoryReminder:
    """记忆提醒器"""
    
    def __init__(self):
        self.db_path = get_vectors_db()
        self.conn = None
        self._connect()
    
    def _connect(self):
        if Path(self.db_path).exists():
            self.conn = sqlite3.connect(str(self.db_path))
            self.conn.row_factory = sqlite3.Row
    
    def check_due_reminders(self) -> List[Dict]:
        """检查到期提醒"""
        reminders = []
        
        # 检查标记了 reminder_time 的记忆
        cursor = self.conn.execute("""
            SELECT record_id, content, type, priority, created_time
            FROM l1_records
            WHERE content LIKE '%提醒%' OR content LIKE '%截止%' OR content LIKE '%deadline%'
            AND created_time > datetime('now', '-30 days')
            ORDER BY created_time DESC
            LIMIT 10
        """)
        
        for row in cursor.fetchall():
            content = row['content'] or ''
            # 简单检查是否包含时间相关词汇
            if any(word in content.lower() for word in ['今天', '明天', '本周', '截止', 'deadline', '提醒']):
                reminders.append({
                    'record_id': row['record_id'],
                    'content': content[:100],
                    'type': row['type'],
                    'priority': row['priority'],
                    'created_time': row['created_time'],
                    'reminder_type': 'time_based'
                })
        
        return reminders
    
    def check_review_needed(self, days_since_access: int = 7, min_priority: int = 60) -> List[Dict]:
        """检查需要复习的记忆"""
        cursor = self.conn.execute("""
            SELECT record_id, content, type, priority, created_time
            FROM l1_records
            WHERE priority >= ?
            AND created_time < datetime('now', '-30 days')
            ORDER BY priority DESC
            LIMIT 10
        """, (min_priority,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def check_recurring_memories(self) -> List[Dict]:
        """检查周期性记忆（习惯追踪）"""
        # 查找可能是习惯/周期性的记忆
        cursor = self.conn.execute("""
            SELECT record_id, content, type, priority, created_time
            FROM l1_records
            WHERE (type = 'habit' OR type = 'routine' OR content LIKE '%每天%' OR content LIKE '%习惯%')
            AND created_time > datetime('now', '-30 days')
            ORDER BY priority DESC
            LIMIT 10
        """)
        
        return [dict(row) for row in cursor.fetchall()]
    
    def check_important_dates(self) -> List[Dict]:
        """检查重要日期（纪念日、截止日期等）"""
        # 查找包含日期的记忆
        cursor = self.conn.execute("""
            SELECT record_id, content, type, priority, created_time
            FROM l1_records
            WHERE (
                content LIKE '%月%日%' 
                OR content LIKE '%周年%'
                OR content LIKE '%截止%'
                OR content LIKE '%deadline%'
            )
            AND created_time > datetime('now', '-90 days')
            ORDER BY priority DESC
            LIMIT 10
        """)
        
        return [dict(row) for row in cursor.fetchall()]
    
    def generate_reminder_report(self) -> str:
        """生成提醒报告"""
        lines = ["# 🔔 记忆提醒报告", ""]
        lines.append(f"**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        # 到期提醒
        lines.append("## ⏰ 到期提醒")
        due = self.check_due_reminders()
        if due:
            for item in due:
                lines.append(f"- **[{item['type']}]** {item['content'][:60]}...")
        else:
            lines.append("✅ 暂无到期提醒")
        lines.append("")
        
        # 复习提醒
        lines.append("## 📚 复习提醒")
        review = self.check_review_needed()
        if review:
            for item in review:
                lines.append(f"- **[{item['type']}]** (优先级{item['priority']}) {item['content'][:50]}...")
            lines.append(f"\n共 {len(review)} 条记忆需要复习")
        else:
            lines.append("✅ 暂无需要复习的记忆")
        lines.append("")
        
        # 习惯追踪
        lines.append("## 🔄 习惯追踪")
        recurring = self.check_recurring_memories()
        if recurring:
            for item in recurring:
                lines.append(f"- **[{item['type']}]** {item['content'][:60]}...")
        else:
            lines.append("ℹ️ 暂无周期性习惯记录")
        lines.append("")
        
        # 重要日期
        lines.append("## 📅 重要日期")
        dates = self.check_important_dates()
        if dates:
            for item in dates:
                lines.append(f"- **[{item['type']}]** {item['content'][:60]}...")
        else:
            lines.append("ℹ️ 暂无重要日期记录")
        
        return "\n".join(lines)
    
    def close(self):
        if self.conn:
            self.conn.close()


def main():
    reminder = MemoryReminder()
    print(reminder.generate_reminder_report())
    reminder.close()


if __name__ == '__main__':
    main()
