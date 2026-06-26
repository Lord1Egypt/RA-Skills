#!/usr/bin/env python3
"""
记忆图谱模块 - 生成记忆关系可视化

功能：
- 基于类型的记忆聚类
- 基于时间的记忆timeline
- 基于重要性的记忆分层
- 生成 ASCII 图谱
- 生成 JSON 图谱数据（用于 D3.js 可视化）
"""

import sys
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Tuple
from collections import defaultdict, Counter

sys.path.insert(0, str(Path(__file__).parent.parent))
from paths import get_vectors_db, get_memory_base


class MemoryGraph:
    """记忆图谱生成器"""
    
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
    
    def get_type_clusters(self, max_per_type: int = 20) -> Dict[str, List[Dict]]:
        """获取基于类型的记忆聚类"""
        if not self.conn:
            return {}
        
        clusters = defaultdict(list)
        
        cursor = self.conn.execute("""
            SELECT record_id, content, type, priority, created_time
            FROM l1_records
            ORDER BY created_time DESC
        """)
        
        for row in cursor.fetchall():
            memory_type = row['type'] or 'unknown'
            if len(clusters[memory_type]) < max_per_type:
                clusters[memory_type].append({
                    'id': row['record_id'],
                    'content': row['content'][:50],
                    'priority': row['priority'],
                    'created': row['created_time']
                })
        
        return dict(clusters)
    
    def get_timeline_data(self, days: int = 7) -> List[Dict]:
        """获取时间线数据"""
        if not self.conn:
            return []
        
        cursor = self.conn.execute("""
            SELECT DATE(created_time) as date, type, COUNT(*) as count
            FROM l1_records
            WHERE created_time >= date('now', ?)
            GROUP BY DATE(created_time), type
            ORDER BY date
        """, (f'-{days} days',))
        
        timeline = []
        for row in cursor.fetchall():
            timeline.append({
                'date': row['date'],
                'type': row['type'],
                'count': row['count']
            })
        
        return timeline
    
    def get_importance_hierarchy(self) -> Dict[str, List[Dict]]:
        """获取基于重要性的记忆分层"""
        if not self.conn:
            return {}
        
        hierarchy = {
            'critical': [],
            'high': [],
            'normal': [],
            'low': []
        }
        
        # priority > 80 为 critical/high
        cursor = self.conn.execute("""
            SELECT record_id, content, priority, created_time
            FROM l1_records
            ORDER BY priority DESC, created_time DESC
            LIMIT 50
        """)
        
        for row in cursor.fetchall():
            p = row['priority']
            if p >= 90:
                level = 'critical'
            elif p >= 70:
                level = 'high'
            elif p >= 40:
                level = 'normal'
            else:
                level = 'low'
            
            hierarchy[level].append({
                'id': row['record_id'],
                'content': row['content'][:40],
                'priority': p
            })
        
        return hierarchy
    
    def get_keyword_network(self, max_keywords: int = 30) -> Dict:
        """获取关键词网络（用于可视化）"""
        if not self.conn:
            return {}
        
        # 提取关键词
        cursor = self.conn.execute("""
            SELECT content FROM l1_records LIMIT 200
        """)
        
        import re
        word_counts = Counter()
        memory_words = defaultdict(list)
        
        for row in cursor.fetchall():
            content = row['content']
            # 提取中文词
            words = re.findall(r'[\u4e00-\u9fff]{2,}', content)
            for w in set(words):
                if len(w) >= 2:
                    word_counts[w] += 1
                    memory_words[w].append(content[:30])
        
        top_keywords = [w for w, c in word_counts.most_common(max_keywords)]
        
        # 构建节点和边
        nodes = []
        links = []
        
        for i, kw in enumerate(top_keywords):
            nodes.append({
                'id': f'kw_{i}',
                'name': kw,
                'count': word_counts[kw],
                'size': min(word_counts[kw] * 2, 20)
            })
        
        return {
            'nodes': nodes,
            'links': links
        }
    
    def generate_ascii_graph(self) -> str:
        """生成 ASCII 图谱"""
        lines = ["# 🕸️ 记忆图谱", ""]
        
        # 类型聚类
        clusters = self.get_type_clusters(max_per_type=10)
        if clusters:
            lines.append("## 📊 类型聚类")
            for memory_type, items in sorted(clusters.items()):
                count = len(items)
                bar = "█" * min(count, 20)
                lines.append(f"{memory_type:12} │ {bar} ({count})")
            lines.append("")
        
        # 时间线
        timeline = self.get_timeline_data(days=7)
        if timeline:
            lines.append("## 📅 7天时间线")
            by_date = defaultdict(list)
            for item in timeline:
                by_date[item['date']].append(item['count'])
            
            for date, counts in sorted(by_date.items()):
                total = sum(counts)
                bar = "▓" * min(total, 20)
                lines.append(f"{date} │ {bar} ({total})")
            lines.append("")
        
        # 重要性分层
        hierarchy = self.get_importance_hierarchy()
        if hierarchy:
            lines.append("## ⚖️ 重要性分层")
            for level, items in hierarchy.items():
                if items:
                    lines.append(f"{level:8} │ {len(items):3} 条")
                    for item in items[:3]:
                        lines.append(f"         └─ {item['content']}...")
                    if len(items) > 3:
                        lines.append(f"         ... 还有 {len(items)-3} 条")
            lines.append("")
        
        return "\n".join(lines)
    
    def generate_json_graph(self) -> Dict:
        """生成 JSON 图谱数据（用于 D3.js 可视化）"""
        clusters = self.get_type_clusters(max_per_type=15)
        hierarchy = self.get_importance_hierarchy()
        
        nodes = []
        links = []
        
        # 类型节点
        type_nodes = {}
        for i, memory_type in enumerate(clusters.keys()):
            node_id = f'type_{memory_type}'
            type_nodes[memory_type] = node_id
            nodes.append({
                'id': node_id,
                'name': memory_type,
                'type': 'cluster',
                'size': len(clusters[memory_type])
            })
        
        # 记忆节点
        for memory_type, items in clusters.items():
            parent_id = type_nodes[memory_type]
            for item in items:
                node_id = f'mem_{item["id"]}'
                nodes.append({
                    'id': node_id,
                    'name': item['content'],
                    'type': 'memory',
                    'parent': parent_id,
                    'priority': item['priority']
                })
                links.append({
                    'source': node_id,
                    'target': parent_id
                })
        
        return {
            'nodes': nodes,
            'links': links,
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'cluster_count': len(clusters),
                'total_nodes': len(nodes)
            }
        }
    
    def close(self):
        """关闭连接"""
        if self.conn:
            self.conn.close()


def main():
    """CLI 入口"""
    import argparse
    parser = argparse.ArgumentParser(description='记忆图谱')
    parser.add_argument('--ascii', '-a', action='store_true', help='ASCII 图谱')
    parser.add_argument('--json', '-j', action='store_true', help='JSON 数据')
    parser.add_argument('--clusters', '-c', action='store_true', help='类型聚类')
    parser.add_argument('--timeline', '-t', action='store_true', help='时间线')
    parser.add_argument('--hierarchy', '-H', action='store_true', help='重要性分层')
    args = parser.parse_args()
    
    graph = MemoryGraph()
    
    if args.clusters:
        clusters = graph.get_type_clusters()
        print("# 📊 记忆类型聚类")
        for t, items in clusters.items():
            print(f"\n## {t} ({len(items)} 条)")
            for item in items[:5]:
                print(f"- {item['content']}...")
    elif args.timeline:
        timeline = graph.get_timeline_data()
        print("# 📅 记忆时间线")
        for item in timeline:
            print(f"{item['date']} [{item['type']}]: {item['count']} 条")
    elif args.hierarchy:
        hierarchy = graph.get_importance_hierarchy()
        print("# ⚖️ 重要性分层")
        for level, items in hierarchy.items():
            print(f"\n## {level} ({len(items)} 条)")
            for item in items[:5]:
                print(f"- [P{item['priority']}] {item['content']}...")
    elif args.json:
        import json
        data = graph.generate_json_graph()
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(graph.generate_ascii_graph())
    
    graph.close()


if __name__ == '__main__':
    main()
