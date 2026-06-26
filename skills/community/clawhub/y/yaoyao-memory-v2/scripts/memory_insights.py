#!/usr/bin/env python3
"""
记忆洞察模块 - 从记忆中提取洞见

功能：
- 从记忆中提取关键洞察
- 识别行为模式
- 发现知识缺口
- 生成洞见摘要
- 关联分析（跨记忆连接）
"""

import sys
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Tuple
from collections import Counter, defaultdict
import re

sys.path.insert(0, str(Path(__file__).parent.parent))
from paths import get_vectors_db, get_memory_base


class MemoryInsights:
    """记忆洞察提取器"""
    
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
    
    def extract_keywords(self, min_freq: int = 3) -> List[Tuple[str, int]]:
        """提取高频关键词"""
        if not self.conn:
            return []
        
        cursor = self.conn.execute("SELECT content FROM l1_records LIMIT 500")
        
        keywords = []
        for row in cursor.fetchall():
            content = row['content']
            # 提取中文词（2字以上）
            words = re.findall(r'[\u4e00-\u9fff]{2,}', content)
            keywords.extend(words)
        
        counter = Counter(keywords)
        return [(w, c) for w, c in counter.most_common(100) if c >= min_freq]
    
    def extract_entities(self) -> Dict[str, List[str]]:
        """提取实体（人名、地点、组织等）- 简化版"""
        if not self.conn:
            return {}
        
        cursor = self.conn.execute("SELECT content FROM l1_records LIMIT 200")
        
        entities = {
            'names': [],      # 假设的人名模式
            'places': [],     # 地点
            'projects': [],   # 项目名
            'tools': []      # 工具/技术
        }
        
        # 简化模式匹配
        name_pattern = re.compile(r'[\u4e00-\u9fff]{2,3}(?:同学|老师|先生|女士|老板|总)')
        place_pattern = re.compile(r'在([\u4e00-\u9fff]{2,}(?:公司|医院|学校|店|餐厅|酒店|机场|车站))')
        
        for row in cursor.fetchall():
            content = row['content']
            
            names = name_pattern.findall(content)
            entities['names'].extend(names)
            
            places = place_pattern.findall(content)
            entities['places'].extend(places)
        
        # 去重
        for key in entities:
            entities[key] = list(set(entities[key]))[:20]
        
        return entities
    
    def identify_patterns(self) -> List[Dict]:
        """识别行为模式"""
        if not self.conn:
            return []
        
        patterns = []
        
        # 时间模式
        cursor = self.conn.execute("""
            SELECT strftime('%H', created_time) as hour, COUNT(*) as count
            FROM l1_records
            GROUP BY hour
            ORDER BY count DESC
        """)
        
        peak_hours = []
        for row in cursor.fetchall():
            if row['count'] >= 5:  # 至少5条记忆
                peak_hours.append(f"{row['hour']}:00")
        
        if peak_hours:
            patterns.append({
                'type': 'time',
                'title': '活跃时间段',
                'description': f'你在 {", ".join(peak_hours[:3])} 比较活跃',
                'evidence': f'这些时段共有 {len(peak_hours)} 个记忆高峰'
            })
        
        # 类型模式
        cursor = self.conn.execute("""
            SELECT type, COUNT(*) as count
            FROM l1_records
            GROUP BY type
            ORDER BY count DESC
        """)
        
        primary_type = cursor.fetchone()
        if primary_type and primary_type['count'] >= 10:
            patterns.append({
                'type': 'content',
                'title': '主要记忆类型',
                'description': f'你主要记录 {primary_type["type"]} 类信息',
                'evidence': f'占总记忆的 {primary_type["count"]} 条'
            })
        
        return patterns
    
    def find_knowledge_gaps(self) -> List[Dict]:
        """发现知识缺口"""
        if not self.conn:
            return []
        
        gaps = []
        
        # 检查缺乏的领域
        cursor = self.conn.execute("SELECT type, COUNT(*) as count FROM l1_records GROUP BY type")
        existing_types = {row['type']: row['count'] for row in cursor.fetchall()}
        
        important_types = ['decision', 'learning', 'preference', 'fact']
        for t in important_types:
            if t not in existing_types or existing_types[t] < 3:
                gap_names = {
                    'decision': '决策记录',
                    'learning': '学习记录',
                    'preference': '偏好记录',
                    'fact': '事实性知识'
                }
                gaps.append({
                    'type': t,
                    'title': f'缺少 {gap_names.get(t, t)}',
                    'suggestion': f'建议记录更多 {gap_names.get(t, t)}，有助于 AI 更好地了解你'
                })
        
        return gaps
    
    def find_connections(self, keyword: str) -> List[Dict]:
        """发现与关键词相关的记忆连接"""
        if not self.conn:
            return []
        
        cursor = self.conn.execute("""
            SELECT id, content, type, importance
            FROM l1_records
            WHERE content LIKE ?
            ORDER BY importance DESC
            LIMIT 20
        """, (f'%{keyword}%',))
        
        connections = []
        for row in cursor.fetchall():
            connections.append({
                'id': row['id'],
                'content': row['content'][:100],
                'type': row['type'],
                'importance': row['importance']
            })
        
        return connections
    
    def generate_insights_summary(self) -> str:
        """生成洞察摘要"""
        lines = ["# 🧠 记忆洞察报告", ""]
        lines.append(f"**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append("")
        
        # 关键词
        keywords = self.extract_keywords(3)
        if keywords:
            lines.append("## 🔑 高频关键词 TOP20")
            top_keywords = [f"{w}({c}次)" for w, c in keywords[:20]]
            lines.append("、".join(top_keywords))
            lines.append("")
        
        # 实体
        entities = self.extract_entities()
        if entities:
            has_entities = False
            for key, values in entities.items():
                if values:
                    has_entities = True
                    break
            
            if has_entities:
                lines.append("## 👤 识别的实体")
                if entities['names']:
                    lines.append(f"- 人名：{', '.join(entities['names'][:5])}")
                if entities['places']:
                    lines.append(f"- 地点：{', '.join(entities['places'][:5])}")
                lines.append("")
        
        # 行为模式
        patterns = self.identify_patterns()
        if patterns:
            lines.append("## 📊 行为模式")
            for p in patterns:
                lines.append(f"### {p['title']}")
                lines.append(f"{p['description']}")
                lines.append(f"_{p['evidence']}_")
                lines.append("")
        
        # 知识缺口
        gaps = self.find_knowledge_gaps()
        if gaps:
            lines.append("## 💡 知识缺口建议")
            for g in gaps:
                lines.append(f"- **{g['title']}**：{g['suggestion']}")
            lines.append("")
        
        return "\n".join(lines)
    
    def get_memory_graph(self, max_nodes: int = 50) -> Dict:
        """生成记忆图谱数据（用于可视化）"""
        if not self.conn:
            return {}
        
        cursor = self.conn.execute("""
            SELECT id, content, type, importance
            FROM l1_records
            ORDER BY importance DESC
            LIMIT ?
        """, (max_nodes,))
        
        nodes = []
        edges = []
        
        for row in cursor.fetchall():
            node_id = str(row['id'])
            nodes.append({
                'id': node_id,
                'label': row['content'][:30],
                'type': row['type'],
                'importance': row['importance']
            })
        
        # 简单边：同一类型的连接
        type_groups = defaultdict(list)
        for n in nodes:
            type_groups[n['type']].append(n['id'])
        
        for t, ids in type_groups.items():
            for i in range(len(ids) - 1):
                edges.append({
                    'source': ids[i],
                    'target': ids[i+1]
                })
        
        return {
            'nodes': nodes,
            'edges': edges
        }
    
    def close(self):
        """关闭连接"""
        if self.conn:
            self.conn.close()


def main():
    """CLI 入口"""
    import argparse
    parser = argparse.ArgumentParser(description='记忆洞察提取')
    parser.add_argument('--keywords', '-k', action='store_true', help='显示高频关键词')
    parser.add_argument('--entities', '-e', action='store_true', help='显示识别的实体')
    parser.add_argument('--patterns', '-p', action='store_true', help='显示行为模式')
    parser.add_argument('--gaps', '-g', action='store_true', help='显示知识缺口')
    parser.add_argument('--connect', '-c', type=str, help='查找关联记忆')
    parser.add_argument('--graph', action='store_true', help='生成图谱数据')
    args = parser.parse_args()
    
    insights = MemoryInsights()
    
    if args.keywords:
        kws = insights.extract_keywords()
        print("# 🔑 高频关键词")
        for w, c in kws[:30]:
            print(f"- {w}: {c}次")
    
    elif args.entities:
        entities = insights.extract_entities()
        print("# 👤 识别的实体")
        if entities['names']:
            print(f"人名：{', '.join(entities['names'])}")
        if entities['places']:
            print(f"地点：{', '.join(entities['places'])}")
    
    elif args.patterns:
        patterns = insights.identify_patterns()
        print("# 📊 行为模式")
        for p in patterns:
            print(f"\n## {p['title']}")
            print(f"{p['description']}")
            print(f"_{p['evidence']}_")
    
    elif args.gaps:
        gaps = insights.find_knowledge_gaps()
        print("# 💡 知识缺口")
        for g in gaps:
            print(f"- **{g['title']}**：{g['suggestion']}")
    
    elif args.connect:
        conns = insights.find_connections(args.connect)
        print(f"# 🔗 关于「{args.connect}」的关联记忆 ({len(conns)} 条)")
        for c in conns[:10]:
            print(f"\n## [{c['type']}] {c['content']}...")
            print(f"重要性: {c['importance']}")
    
    elif args.graph:
        import json
        graph = insights.get_memory_graph()
        print(json.dumps(graph, ensure_ascii=False, indent=2))
    
    else:
        print(insights.generate_insights_summary())
    
    insights.close()


if __name__ == '__main__':
    main()
