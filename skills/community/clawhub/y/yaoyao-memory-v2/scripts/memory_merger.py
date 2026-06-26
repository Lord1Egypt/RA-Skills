#!/usr/bin/env python3
"""
记忆合并模块 - 合并相似或重复的记忆

功能：
- 检测相似记忆
- 合并重复记忆
- 智能去重
- 合并历史追踪
"""

import sys
import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Set, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent))
from paths import get_vectors_db, get_memory_base


class MemoryMerger:
    """记忆合并器"""
    
    def __init__(self):
        self.db_path = get_vectors_db()
        self.memory_base = get_memory_base()
        self.conn = None
        self._connect()
    
    def _connect(self):
        if Path(self.db_path).exists():
            self.conn = sqlite3.connect(str(self.db_path))
            self.conn.row_factory = sqlite3.Row
    
    def calculate_similarity(self, content1: str, content2: str) -> float:
        """计算两段内容的相似度"""
        if not content1 or not content2:
            return 0.0
        
        # 简单词集合相似度
        words1 = set(content1.lower().split())
        words2 = set(content2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0
    
    def find_duplicates(self, threshold: float = 0.8) -> List[Tuple[str, str, float]]:
        """查找重复记忆"""
        if not self.conn:
            return []
        
        cursor = self.conn.execute("""
            SELECT record_id, content, type, priority, created_time
            FROM l1_records
            ORDER BY created_time DESC
            LIMIT 200
        """)
        
        memories = [dict(row) for row in cursor.fetchall()]
        duplicates = []
        
        checked = set()
        
        for i, m1 in enumerate(memories):
            for m2 in memories[i+1:100]:
                pair_key = f"{m1['record_id']}-{m2['record_id']}"
                if pair_key in checked:
                    continue
                
                similarity = self.calculate_similarity(m1['content'], m2['content'])
                
                if similarity >= threshold:
                    duplicates.append((m1['record_id'], m2['record_id'], similarity))
                    checked.add(pair_key)
        
        return duplicates
    
    def merge_memories(self, keep_id: str, remove_id: str, create_link: bool = True) -> bool:
        """合并两条记忆"""
        try:
            cursor = self.conn.execute("""
                SELECT record_id, content, type, priority, created_time, metadata_json
                FROM l1_records WHERE record_id IN (?, ?)
            """, (keep_id, remove_id))
            
            rows = {row['record_id']: dict(row) for row in cursor.fetchall()}
            
            if keep_id not in rows or remove_id not in rows:
                return False
            
            keep_row = rows[keep_id]
            remove_row = rows[remove_id]
            
            # 保留优先级更高的
            if (remove_row.get('priority', 0) or 0) > (keep_row.get('priority', 0) or 0):
                keep_id, remove_id = remove_id, keep_id
                keep_row, remove_row = remove_row, keep_row
            
            # 合并内容（保留更长的）
            if len(remove_row['content'] or '') > len(keep_row['content'] or ''):
                new_content = remove_row['content']
            else:
                new_content = keep_row['content']
            
            # 更新保留的记忆
            self.conn.execute("""
                UPDATE l1_records
                SET content = ?, priority = MAX(priority, ?), updated_time = ?
                WHERE record_id = ?
            """, (new_content, remove_row.get('priority', 50), datetime.now().isoformat(), keep_id))
            
            # 记录合并历史
            merge_record = {
                'merged_from': remove_id,
                'merged_to': keep_id,
                'merged_at': datetime.now().isoformat(),
                'original_content': remove_row['content'][:100]
            }
            
            # 如果需要创建链接，更新 metadata
            if create_link:
                import json
                cursor = self.conn.execute("""
                    SELECT metadata_json FROM l1_records WHERE record_id = ?
                """, (keep_id,))
                row = cursor.fetchone()
                metadata = json.loads(row['metadata_json'] or '{}') if row else {}
                
                if 'merged_from' not in metadata:
                    metadata['merged_from'] = []
                metadata['merged_from'].append({
                    'id': remove_id,
                    'at': datetime.now().isoformat()
                })
                
                self.conn.execute("""
                    UPDATE l1_records SET metadata_json = ? WHERE record_id = ?
                """, (json.dumps(metadata), keep_id))
            
            # 删除被合并的记忆
            self.conn.execute("DELETE FROM l1_records WHERE record_id = ?", (remove_id,))
            
            self.conn.commit()
            return True
            
        except Exception as e:
            print(f"合并失败: {e}")
            return False
    
    def batch_merge_duplicates(self, threshold: float = 0.85, dry_run: bool = True) -> Dict:
        """批量合并重复记忆"""
        duplicates = self.find_duplicates(threshold)
        
        merged_count = 0
        skipped_count = 0
        
        for keep_id, remove_id, similarity in duplicates:
            if dry_run:
                merged_count += 1
            else:
                if self.merge_memories(keep_id, remove_id):
                    merged_count += 1
                else:
                    skipped_count += 1
        
        return {
            'duplicates_found': len(duplicates),
            'merged': merged_count,
            'skipped': skipped_count,
            'dry_run': dry_run
        }
    
    def get_merge_candidates(self, limit: int = 20) -> List[Dict]:
        """获取推荐合并的候选记忆"""
        if not self.conn:
            return []
        
        # 获取高相似度记忆对
        cursor = self.conn.execute("""
            SELECT record_id, content, type, priority, created_time
            FROM l1_records
            ORDER BY priority DESC
            LIMIT 100
        """)
        
        memories = [dict(row) for row in cursor.fetchall()]
        candidates = []
        
        for i, m1 in enumerate(memories):
            for m2 in memories[i+1:50]:
                similarity = self.calculate_similarity(m1['content'], m2['content'])
                
                if 0.6 <= similarity < 1.0:  # 中等相似度，可能需要合并
                    candidates.append({
                        'memory1': m1,
                        'memory2': m2,
                        'similarity': round(similarity, 2)
                    })
        
        # 按相似度排序
        candidates.sort(key=lambda x: x['similarity'], reverse=True)
        return candidates[:limit]
    
    def close(self):
        if self.conn:
            self.conn.close()


def main():
    import argparse
    parser = argparse.ArgumentParser(description='记忆合并')
    parser.add_argument('--find', '-f', action='store_true', help='查找重复')
    parser.add_argument('--merge', '-m', nargs=2, metavar=('KEEP', 'REMOVE'), help='合并两条记忆')
    parser.add_argument('--batch', '-b', action='store_true', help='批量合并')
    parser.add_argument('--dry-run', action='store_true', help='试运行')
    parser.add_argument('--candidates', '-c', action='store_true', help='显示推荐合并')
    args = parser.parse_args()
    
    merger = MemoryMerger()
    
    if args.find:
        dups = merger.find_duplicates()
        print(f"# 🔍 发现 {len(dups)} 对重复记忆")
        for keep, remove, sim in dups[:10]:
            print(f"- [{sim:.2f}] {keep} ← {remove}")
    
    elif args.merge:
        if merger.merge_memories(args.merge[0], args.merge[1]):
            print(f"✅ {args.merge[1]} 已合并到 {args.merge[0]}")
        else:
            print("❌ 合并失败")
    
    elif args.batch:
        result = merger.batch_merge_duplicates(dry_run=args.dry_run)
        if result['dry_run']:
            print(f"# 🔍 试运行结果：可合并 {result['duplicates_found']} 对")
        else:
            print(f"✅ 合并完成：{result['merged']} 对")
    
    elif args.candidates:
        candidates = merger.get_merge_candidates()
        print(f"# 💡 推荐合并候选 ({len(candidates)} 对)")
        for c in candidates[:10]:
            print(f"\n## [{c['similarity']}]")
            print(f"记忆1: {c['memory1']['content'][:50]}...")
            print(f"记忆2: {c['memory2']['content'][:50]}...")
    
    merger.close()


if __name__ == '__main__':
    main()
