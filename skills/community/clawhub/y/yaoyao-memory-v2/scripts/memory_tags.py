#!/usr/bin/env python3
"""
记忆标签系统 - 自动和手动标签管理

功能：
- 自动提取标签
- 标签建议
- 标签统计分析
- 基于标签的智能分类
- 标签云生成
"""

import sys
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Set, Tuple
from collections import Counter, defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent))
from paths import get_vectors_db, get_memory_base


class TagExtractor:
    """标签提取器"""
    
    def __init__(self):
        self.db_path = get_vectors_db()
        self.memory_base = get_memory_base()
        self.conn = None
        self._connect()
        
        # 内置标签规则
        self.tag_patterns = {
            '技术': ['Python', 'JavaScript', 'API', 'Git', '代码', '编程', '开发', '系统', '数据库', 'SQL', 'Linux'],
            '工作': ['会议', '报告', '客户', '同事', '项目', '任务', 'deadline', '周报', '月报'],
            '学习': ['课程', '读书', '学习', '考试', '练习', '作业', '论文', '研究'],
            '生活': ['吃饭', '睡觉', '运动', '休息', '购物', '旅行', '朋友', '家人'],
            '财务': ['预算', '报销', '工资', '投资', '股票', '支出', '收入', '账单'],
            '健康': ['医生', '医院', '药', '锻炼', '运动', '饮食', '睡眠', '减肥'],
            '重要': ['紧急', '重要', '关键', '必须', '优先', 'critical', 'urgent'],
            '决定': ['决定', '选择', '方案', '结论', '确定', '采纳'],
        }
        
        # 自定义标签
        self.custom_tags = set()
    
    def _connect(self):
        """连接数据库"""
        if Path(self.db_path).exists():
            self.conn = sqlite3.connect(str(self.db_path))
            self.conn.row_factory = sqlite3.Row
    
    def extract_tags(self, content: str) -> List[str]:
        """从内容中提取标签"""
        tags = set()
        
        content_lower = content.lower()
        
        for tag, keywords in self.tag_patterns.items():
            for keyword in keywords:
                if keyword.lower() in content_lower:
                    tags.add(tag)
                    break
        
        # 提取 #标签
        hash_tags = re.findall(r'#(\w+)', content)
        tags.update(hash_tags)
        
        # 提取 @人名
        mentions = re.findall(r'@(\w+)', content)
        for m in mentions:
            tags.add(f'@{m}')
        
        return list(tags)
    
    def get_all_tags(self) -> Dict[str, int]:
        """获取所有标签及其出现次数"""
        if not self.conn:
            return {}
        
        cursor = self.conn.execute("SELECT content FROM l1_records LIMIT 500")
        
        tag_counts = Counter()
        
        for row in cursor.fetchall():
            tags = self.extract_tags(row['content'])
            for tag in tags:
                tag_counts[tag] += 1
        
        return dict(tag_counts.most_common(50))
    
    def suggest_tags_for_content(self, content: str, limit: int = 5) -> List[Tuple[str, float]]:
        """为内容推荐标签"""
        tags = self.extract_tags(content)
        
        # 计算置信度
        tag_scores = []
        content_lower = content.lower()
        
        for tag in tags:
            score = 0.5  # 基础分
            
            # 根据出现次数加分
            if tag in self.tag_patterns:
                for keyword in self.tag_patterns[tag]:
                    if keyword.lower() in content_lower:
                        score += 0.1
            
            tag_scores.append((tag, min(score, 1.0)))
        
        tag_scores.sort(key=lambda x: x[1], reverse=True)
        return tag_scores[:limit]
    
    def get_memories_by_tag(self, tag: str, limit: int = 20) -> List[Dict]:
        """获取带有指定标签的记忆"""
        if not self.conn:
            return []
        
        # 构建搜索模式
        pattern = f'%{tag}%'
        
        cursor = self.conn.execute("""
            SELECT record_id, content, type, priority, created_time
            FROM l1_records
            WHERE content LIKE ?
            ORDER BY priority DESC, created_time DESC
            LIMIT ?
        """, (pattern, limit))
        
        memories = []
        for row in cursor.fetchall():
            memories.append({
                'id': row['record_id'],
                'content': row['content'],
                'type': row['type'],
                'priority': row['priority'],
                'date': row['created_time']
            })
        
        return memories
    
    def get_tag_network(self) -> Dict:
        """获取标签网络（哪些标签经常一起出现）"""
        if not self.conn:
            return {}
        
        cursor = self.conn.execute("SELECT content FROM l1_records LIMIT 200")
        
        cooccurrence = defaultdict(Counter)
        all_tags = set()
        
        for row in cursor.fetchall():
            tags = self.extract_tags(row['content'])
            all_tags.update(tags)
            
            for t1 in tags:
                for t2 in tags:
                    if t1 != t2:
                        cooccurrence[t1][t2] += 1
        
        return {
            'nodes': [{'id': t, 'count': len(all_tags)} for t in all_tags],
            'links': [
                {'source': t1, 'target': t2, 'weight': c}
                for t1, counter in cooccurrence.items()
                for t2, c in counter.items()
                if c >= 2
            ][:50]  # 限制链接数量
        }
    
    def generate_tag_cloud(self, min_count: int = 2) -> str:
        """生成标签云 ASCII"""
        tag_counts = self.get_all_tags()
        
        if not tag_counts:
            return "# 🏷️ 标签云\n\n（暂无标签）"
        
        # 过滤低频标签
        filtered = {t: c for t, c in tag_counts.items() if c >= min_count}
        
        if not filtered:
            return "# 🏷️ 标签云\n\n（标签出现次数过低）"
        
        lines = ["# 🏷️ 标签云", ""]
        lines.append(f"共 {len(filtered)} 个标签，总计 {sum(filtered.values())} 次使用")
        lines.append("")
        
        # 按频率排序
        sorted_tags = sorted(filtered.items(), key=lambda x: x[1], reverse=True)
        
        # 分组显示
        high_freq = [(t, c) for t, c in sorted_tags if c >= 5]
        mid_freq = [(t, c) for t, c in sorted_tags if 2 <= c < 5]
        
        if high_freq:
            lines.append("## 🔥 高频标签")
            tags_line = " ".join(f"[{t}]({c})" for t, c in high_freq[:15])
            lines.append(tags_line)
            lines.append("")
        
        if mid_freq:
            lines.append("## 📊 中频标签")
            tags_line = " ".join(f"[{t}]({c})" for t, c in mid_freq[:20])
            lines.append(tags_line)
        
        return "\n".join(lines)
    
    def update_memory_tags(self, record_id: str, tags: List[str]) -> bool:
        """更新记忆的标签"""
        if not self.conn:
            return False
        
        try:
            # 将标签转为 JSON 存储在 metadata
            import json
            cursor = self.conn.execute("""
                SELECT metadata_json FROM l1_records WHERE record_id = ?
            """, (record_id,))
            row = cursor.fetchone()
            
            metadata = json.loads(row['metadata_json'] or '{}') if row else {}
            metadata['tags'] = tags
            
            self.conn.execute("""
                UPDATE l1_records 
                SET metadata_json = ?
                WHERE record_id = ?
            """, (json.dumps(metadata), record_id))
            
            self.conn.commit()
            return True
        except:
            return False
    
    def close(self):
        """关闭连接"""
        if self.conn:
            self.conn.close()


# 需要导入 sqlite3
import sqlite3


def main():
    """CLI 入口"""
    import argparse
    parser = argparse.ArgumentParser(description='记忆标签系统')
    parser.add_argument('--cloud', '-c', action='store_true', help='显示标签云')
    parser.add_argument('--suggest', '-s', type=str, help='为内容推荐标签')
    parser.add_argument('--tag', '-t', type=str, help='按标签搜索')
    parser.add_argument('--stats', action='store_true', help='标签统计')
    args = parser.parse_args()
    
    extractor = TagExtractor()
    
    if args.cloud:
        print(extractor.generate_tag_cloud())
    elif args.suggest:
        tags = extractor.suggest_tags_for_content(args.suggest)
        print(f"# 🏷️ 标签推荐")
        for t, score in tags:
            print(f"- {t}: {score:.2f}")
    elif args.tag:
        memories = extractor.get_memories_by_tag(args.tag)
        print(f"# 🔍 标签「{args.tag}」相关记忆 ({len(memories)} 条)")
        for m in memories[:10]:
            print(f"\n## {m['id']} [P{m['priority']}]")
            print(f"{m['content'][:100]}...")
    elif args.stats:
        tag_counts = extractor.get_all_tags()
        print("# 📊 标签统计")
        for t, c in list(tag_counts.items())[:20]:
            print(f"- {t}: {c} 次")
    else:
        print(extractor.generate_tag_cloud())
    
    extractor.close()


if __name__ == '__main__':
    main()
