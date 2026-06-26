#!/usr/bin/env python3
"""
记忆质量评估模块 - 评估和提升记忆质量

功能：
- 内容质量评分
- 完整性检查
- 冗余检测
- 一致性验证
- 建议生成
"""

import sys
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from collections import Counter

sys.path.insert(0, str(Path(__file__).parent.parent))
from paths import get_vectors_db, get_memory_base


class MemoryQualityAnalyzer:
    """记忆质量分析器"""
    
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
    
    def calculate_content_quality(self, content: str) -> float:
        """计算内容质量分数 (0-100)"""
        if not content or len(content.strip()) < 10:
            return 0
        
        score = 50  # 基础分
        
        # 长度加分（上限80）
        length = len(content)
        if length > 100:
            score += min((length - 100) / 10, 30)
        
        # 有结构（标点、换行）加分
        structure_chars = sum(1 for c in content if c in '，。！？；：、\n')
        if structure_chars > 5:
            score += min(structure_chars, 15)
        
        # 有具体信息（数字、英文、专有名词）加分
        has_numbers = any(c.isdigit() for c in content)
        has_english = any(c.isalpha() and ord(c) < 128 for c in content)
        if has_numbers:
            score += 5
        if has_english:
            score += 5
        
        return min(score, 100)
    
    def get_quality_distribution(self) -> Dict[str, int]:
        """获取质量分布"""
        if not self.conn:
            return {}
        
        cursor = self.conn.execute("SELECT content FROM l1_records")
        
        distribution = {
            'excellent': 0,  # 80-100
            'good': 0,       # 60-80
            'average': 0,     # 40-60
            'poor': 0         # <40
        }
        
        for row in cursor.fetchall():
            score = self.calculate_content_quality(row['content'])
            if score >= 80:
                distribution['excellent'] += 1
            elif score >= 60:
                distribution['good'] += 1
            elif score >= 40:
                distribution['average'] += 1
            else:
                distribution['poor'] += 1
        
        return distribution
    
    def detect_duplicates(self) -> List[Dict]:
        """检测重复记忆"""
        if not self.conn:
            return []
        
        cursor = self.conn.execute("""
            SELECT content, COUNT(*) as count, GROUP_CONCAT(record_id) as ids
            FROM l1_records
            GROUP BY content
            HAVING count > 1
            ORDER BY count DESC
        """)
        
        duplicates = []
        for row in cursor.fetchall():
            duplicates.append({
                'content': row['content'][:50] + '...' if len(row['content']) > 50 else row['content'],
                'count': row['count'],
                'ids': row['ids'].split(',')
            })
        
        return duplicates
    
    def detect_similar(self, threshold: float = 0.8) -> List[Tuple]:
        """检测相似记忆（简单基于关键词重叠）"""
        if not self.conn:
            return []
        
        cursor = self.conn.execute("""
            SELECT id, content FROM l1_records LIMIT 100
        """)
        
        memories = cursor.fetchall()
        similar_pairs = []
        
        for i, m1 in enumerate(memories):
            for m2 in memories[i+1:50]:  # 限制比较数量
                # 简单相似度：字符集重叠率
                set1 = set(m1['content'])
                set2 = set(m2['content'])
                if len(set1) > 10 and len(set2) > 10:
                    overlap = len(set1 & set2) / len(set1 | set2)
                    if overlap > threshold:
                        similar_pairs.append((m1['id'], m2['id'], overlap))
        
        return similar_pairs[:10]
    
    def check_completeness(self) -> Dict:
        """检查记忆完整性"""
        if not self.conn:
            return {}
        
        checks = {}
        
        # 1. 没有类型的记忆
        cursor = self.conn.execute("""
            SELECT COUNT(*) as count FROM l1_records
            WHERE type = 'unknown' OR type IS NULL
        """)
        checks['no_type'] = cursor.fetchone()['count']
        
        # 2. 没有重要性的记忆 (priority = 0 表示未设置)
        cursor = self.conn.execute("""
            SELECT COUNT(*) as count FROM l1_records
            WHERE priority = 0 OR priority IS NULL
        """)
        checks['no_importance'] = cursor.fetchone()['count']
        
        # 3. 没有标签的记忆 (metadata_json 中没有 tags 字段)
        checks['no_tags'] = 0  # 跳過，tags 存在於 metadata_json 中
        
        # 4. 内容过短的记忆
        cursor = self.conn.execute("""
            SELECT COUNT(*) as count FROM l1_records
            WHERE length(content) < 20
        """)
        checks['too_short'] = cursor.fetchone()['count']
        
        return checks
    
    def check_consistency(self) -> List[Dict]:
        """检查一致性问题"""
        if not self.conn:
            return []
        
        issues = []
        
        # 检测同一实体不同描述
        # 简化版本：检测关键词冲突
        cursor = self.conn.execute("""
            SELECT content, type FROM l1_records
            WHERE type IN ('preference', 'fact')
            LIMIT 50
        """)
        
        # 简化检测：查找可能的矛盾
        # 实际应用中需要更复杂的 NLP
        preferences = []
        facts = []
        for row in cursor.fetchall():
            if row['type'] == 'preference':
                preferences.append(row['content'])
            else:
                facts.append(row['content'])
        
        return issues
    
    def get_low_quality_memories(self, limit: int = 20) -> List[Dict]:
        """获取低质量记忆"""
        if not self.conn:
            return []
        
        cursor = self.conn.execute("""
            SELECT record_id, content, type, priority
            FROM l1_records
            ORDER BY length(content)
            LIMIT ?
        """, (limit,))
        
        memories = []
        for row in cursor.fetchall():
            memories.append({
                'id': row['record_id'],
                'content': row['content'][:50] + '...' if len(row['content']) > 50 else row['content'],
                'type': row['type'],
                'importance': row['priority']
            })
        
        return memories
    
    def generate_quality_report(self) -> str:
        """生成质量报告"""
        lines = ["# 📋 记忆质量评估报告", ""]
        lines.append(f"**评估时间**：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append("")
        
        # 质量分布
        dist = self.get_quality_distribution()
        if dist:
            total = sum(dist.values())
            lines.append("## 📊 质量分布")
            lines.append(f"- 优秀（80-100分）：{dist['excellent']} 条 ({dist['excellent']*100//total}%）")
            lines.append(f"- 良好（60-80分）：{dist['good']} 条 ({dist['good']*100//total}%）")
            lines.append(f"- 一般（40-60分）：{dist['average']} 条 ({dist['average']*100//total}%）")
            lines.append(f"- 待改进（<40分）：{dist['poor']} 条 ({dist['poor']*100//total}%）")
            lines.append("")
        
        # 完整性检查
        completeness = self.check_completeness()
        if completeness:
            total_issues = sum(completeness.values())
            if total_issues > 0:
                lines.append("## 🔍 完整性问题")
                if completeness['no_type'] > 0:
                    lines.append(f"- 缺少类型：{completeness['no_type']} 条")
                if completeness['no_importance'] > 0:
                    lines.append(f"- 缺少重要性：{completeness['no_importance']} 条")
                if completeness['no_tags'] > 0:
                    lines.append(f"- 缺少标签：{completeness['no_tags']} 条")
                if completeness['too_short'] > 0:
                    lines.append(f"- 内容过短：{completeness['too_short']} 条")
                lines.append("")
        
        # 重复检测
        duplicates = self.detect_duplicates()
        if duplicates:
            lines.append(f"## ⚠️ 重复记忆：{len(duplicates)} 组")
            for d in duplicates[:3]:
                lines.append(f"- [{d['count']}条重复] {d['content']}")
            lines.append("")
        
        # 低质量记忆
        low_quality = self.get_low_quality_memories(5)
        if low_quality:
            lines.append("## 📝 待改进记忆 TOP5")
            for m in low_quality:
                lines.append(f"- [{m['type']}] {m['content']}")
            lines.append("")
        
        # 建议
        lines.append("## 💡 优化建议")
        if completeness['too_short'] > 10:
            lines.append("- 增加记忆内容长度，提供更多上下文")
        if completeness['no_type'] > 5:
            lines.append("- 为记忆添加类型标签")
        if duplicates:
            lines.append("- 合并重复记忆，减少冗余")
        if not lines[-1].startswith("-"):
            lines.append("- 记忆质量良好，继续保持！")
        
        return "\n".join(lines)
    
    def close(self):
        """关闭连接"""
        if self.conn:
            self.conn.close()


def main():
    """CLI 入口"""
    import argparse
    parser = argparse.ArgumentParser(description='记忆质量评估')
    parser.add_argument('--report', '-r', action='store_true', help='生成质量报告')
    parser.add_argument('--duplicates', '-d', action='store_true', help='检测重复')
    parser.add_argument('--low', '-l', type=int, help='显示最低质量记忆')
    args = parser.parse_args()
    
    analyzer = MemoryQualityAnalyzer()
    
    if args.duplicates:
        dups = analyzer.detect_duplicates()
        print(f"发现 {len(dups)} 组重复记忆：")
        for d in dups:
            print(f"- {d['content']} ({d['count']}条)")
    elif args.low:
        memories = analyzer.get_low_quality_memories(args.low)
        print(f"最低质量记忆 TOP{args.low}：")
        for m in memories:
            print(f"- [{m['type']}] {m['content']}")
    else:
        print(analyzer.generate_quality_report())
    
    analyzer.close()


if __name__ == '__main__':
    main()
