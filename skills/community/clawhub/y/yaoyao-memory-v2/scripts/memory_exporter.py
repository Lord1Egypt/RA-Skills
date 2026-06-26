#!/usr/bin/env python3
"""
记忆导出模块 - 导出记忆为各种格式

功能：
- 导出为 JSON
- 导出为 Markdown
- 导出为 CSV
- 导出为 HTML（可打印）
- 部分导出（按类型/时间/重要性）
"""

import sys
import json
import csv
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from io import StringIO

sys.path.insert(0, str(Path(__file__).parent.parent))
from paths import get_vectors_db, get_memory_base


class MemoryExporter:
    """记忆导出器"""
    
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
    
    def get_memories(self, filters: Optional[Dict] = None) -> List[Dict]:
        """获取记忆（可过滤）"""
        if not self.conn:
            return []
        
        query = "SELECT record_id, content, type, priority, created_time FROM l1_records WHERE 1=1"
        params = []
        
        if filters is not None:
            if 'type' in filters:
                query += " AND type = ?"
                params.append(filters['type'])
            if 'min_priority' in filters:
                query += " AND priority >= ?"
                params.append(filters['min_priority'])
            if 'days_ago' in filters:
                query += " AND created_time >= date('now', ?)"
                params.append(f"-{filters['days_ago']} days")
        
        query += " ORDER BY priority DESC, created_time DESC"
        
        if filters is not None and 'limit' in filters:
            query += " LIMIT ?"
            params.append(filters['limit'])
        
        cursor = self.conn.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def export_to_json(self, filters: Optional[Dict] = None, pretty: bool = True) -> str:
        """导出为 JSON"""
        memories = self.get_memories(filters)
        
        export_data = {
            'exported_at': datetime.now().isoformat(),
            'total_count': len(memories),
            'filters': filters or {},
            '_source': 'yaoyao-cloud-backup',
            '_export_version': '1.0',
            'memories': memories
        }
        
        if pretty:
            return json.dumps(export_data, ensure_ascii=False, indent=2)
        else:
            return json.dumps(export_data, ensure_ascii=False)
    
    def export_to_markdown(self, filters: Optional[Dict] = None) -> str:
        """导出为 Markdown"""
        memories = self.get_memories(filters)
        
        lines = ["# 记忆导出", ""]
        lines.append(f"**导出时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"**记忆总数**：{len(memories)} 条")
        lines.append("")
        
        if filters is not None:
            lines.append(f"**过滤条件**：{filters}")
            lines.append("")
        
        # 按类型分组
        by_type = {}
        for m in memories:
            t = m.get('type', 'unknown')
            if t not in by_type:
                by_type[t] = []
            by_type[t].append(m)
        
        for memory_type, items in sorted(by_type.items()):
            lines.append(f"## 📂 {memory_type} ({len(items)} 条)")
            lines.append("")
            
            for m in items:
                date = m.get('created_time', '')[:10]
                priority = m.get('priority', 50)
                content = m.get('content', '')
                
                lines.append(f"### {date} [P{priority}]")
                lines.append("")
                lines.append(content)
                lines.append("")
                lines.append("---")
                lines.append("")
        
        return "\n".join(lines)
    
    def export_to_csv(self, filters: Optional[Dict] = None) -> str:
        """导出为 CSV"""
        memories = self.get_memories(filters)
        
        output = StringIO()
        writer = csv.writer(output)
        
        # 标题行
        writer.writerow(['ID', '日期', '时间', '类型', '优先级', '内容'])
        
        for m in memories:
            created = m.get('created_time', '') or ''
            date = created[:10]
            time = created[11:19] if len(created) > 19 else ''
            
            writer.writerow([
                m.get('record_id', ''),
                date,
                time,
                m.get('type', ''),
                m.get('priority', 50),
                m.get('content', '').replace('\n', ' ')
            ])
        
        return output.getvalue()
    
    def export_to_html(self, filters: Optional[Dict] = None, title: str = "记忆导出") -> str:
        """导出为 HTML（可打印）"""
        memories = self.get_memories(filters)
        
        # 按类型分组
        by_type = {}
        for m in memories:
            t = m.get('type', 'unknown')
            if t not in by_type:
                by_type[t] = []
            by_type[t].append(m)
        
        html_parts = ["""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>""" + title + """</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        h1 { color: #333; border-bottom: 2px solid #667eea; padding-bottom: 10px; }
        h2 { color: #667eea; margin-top: 30px; }
        .meta { color: #666; font-size: 14px; margin-bottom: 20px; }
        .memory { background: #f8f9fa; border-radius: 8px; padding: 15px; margin: 15px 0; }
        .priority { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 12px; }
        .priority-high { background: #fee; color: #c00; }
        .priority-normal { background: #efe; color: #080; }
        .content { margin-top: 10px; line-height: 1.6; }
        .date { color: #888; font-size: 12px; }
        @media print { body { max-width: none; } }
    </style>
</head>
<body>
    <h1>""" + title + """</h1>
    <div class="meta">
        <p>导出时间：""" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
        <p>记忆总数：""" + str(len(memories)) + """ 条</p>
    </div>
"""]
        
        for memory_type, items in sorted(by_type.items()):
            html_parts.append(f'<h2>📂 {memory_type} ({len(items)} 条)</h2>')
            
            for m in items:
                priority = m.get('priority', 50)
                priority_class = 'priority-high' if priority >= 70 else 'priority-normal'
                date = m.get('created_time', '')[:10]
                content = m.get('content', '').replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br>')
                
                html_parts.append(f"""
    <div class="memory">
        <span class="priority {priority_class}">P{priority}</span>
        <span class="date">{date}</span>
        <div class="content">{content}</div>
    </div>
""")
        
        html_parts.append("""
</body>
</html>""")
        
        return "".join(html_parts)
    
    def export_to_ical(self, filters: Optional[Dict] = None) -> str:
        """导出为 iCal 格式（用于日历）"""
        memories = self.get_memories(filters)
        
        lines = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//yaoyao-memory//EN",
            "CALSCALE:GREGORIAN",
            "METHOD:PUBLISH"
        ]
        
        for m in memories:
            record_id = m.get('record_id', 'unknown')[:50]
            content = m.get('content', '')[:500].replace('\n', '\\n').replace(',', '\\,')
            created = m.get('created_time', '')
            
            if len(created) >= 10:
                date_str = created[:10].replace('-', '')
                
                lines.append("BEGIN:VEVENT")
                lines.append(f"UID:{record_id}@yaoyao-memory")
                lines.append(f"DTSTAMP:{date_str}T000000Z")
                lines.append(f"DTSTART:{date_str}")
                lines.append(f"SUMMARY:{content[:50]}")
                lines.append(f"DESCRIPTION:{content}")
                lines.append("END:VEVENT")
        
        lines.append("END:VCALENDAR")
        
        return "\n".join(lines)
    
    def save_export(self, format: str, filepath: str, filters: Optional[Dict] = None) -> bool:
        """保存导出文件"""
        try:
            if format == 'json':
                content = self.export_to_json(filters)
            elif format == 'md' or format == 'markdown':
                content = self.export_to_markdown(filters)
            elif format == 'csv':
                content = self.export_to_csv(filters)
            elif format == 'html':
                content = self.export_to_html(filters)
            elif format == 'ical':
                content = self.export_to_ical(filters)
            else:
                return False
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
            
        except Exception as e:
            print(f"导出失败: {e}")
            return False
    
    def close(self):
        """关闭连接"""
        if self.conn:
            self.conn.close()


def main():
    """CLI 入口"""
    import argparse
    parser = argparse.ArgumentParser(description='记忆导出')
    parser.add_argument('--format', '-f', choices=['json', 'md', 'csv', 'html', 'ical'], default='md', help='导出格式')
    parser.add_argument('--output', '-o', type=str, help='输出文件路径')
    parser.add_argument('--type', '-t', type=str, help='按类型过滤')
    parser.add_argument('--priority', '-p', type=int, help='最低优先级')
    parser.add_argument('--days', '-d', type=int, help='最近N天')
    parser.add_argument('--limit', '-l', type=int, help='限制数量')
    args = parser.parse_args()
    
    exporter = MemoryExporter()
    
    filters = {}
    if args.type:
        filters['type'] = args.type
    if args.priority:
        filters['min_priority'] = args.priority
    if args.days:
        filters['days_ago'] = args.days
    if args.limit:
        filters['limit'] = args.limit
    
    if args.output:
        if exporter.save_export(args.format, args.output, filters if filters else None):
            print(f"✅ 已导出到 {args.output}")
        else:
            print(f"❌ 导出失败")
    else:
        # 输出到 stdout
        if args.format == 'json':
            print(exporter.export_to_json(filters if filters else None))
        elif args.format == 'md':
            print(exporter.export_to_markdown(filters if filters else None))
        elif args.format == 'csv':
            print(exporter.export_to_csv(filters if filters else None))
        elif args.format == 'html':
            print(exporter.export_to_html(filters if filters else None))
        elif args.format == 'ical':
            print(exporter.export_to_ical(filters if filters else None))
    
    exporter.close()


if __name__ == '__main__':
    main()
