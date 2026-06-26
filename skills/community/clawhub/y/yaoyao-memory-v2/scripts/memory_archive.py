#!/usr/bin/env python3
"""
记忆归档模块 - 归档和清理旧记忆

功能：
- 自动归档旧记忆
- 归档策略配置
- 归档历史
- 归档恢复
- 定期清理
"""

import sys
import json
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent))
from paths import get_vectors_db, get_memory_base


class MemoryArchiver:
    """记忆归档器"""
    
    def __init__(self):
        self.db_path = get_vectors_db()
        self.memory_base = get_memory_base()
        self.archive_dir = self.memory_base / ".archive"
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        
        self.archive_meta_file = self.archive_dir / "archive_meta.json"
    
    def get_archive_policy(self) -> Dict:
        """获取归档策略"""
        return {
            'auto_archive_days': 90,      # 90天前自动归档
            'archive_high_priority_days': 365,  # 高优先级365天
            'keep_archive_days': 180,      # 归档保留180天
            'archive_types': ['info', 'task'],  # 归档这些类型
            'preserve_types': ['decision', 'preference', 'fact'],  # 永不归档这些
        }
    
    def should_archive(self, memory: Dict) -> Tuple[bool, str]:
        """判断是否应该归档"""
        policy = self.get_archive_policy()
        
        created = memory.get('created_time', '')
        if not created:
            return False, "无创建时间"
        
        try:
            created_date = datetime.fromisoformat(created)
            days_old = (datetime.now() - created_date).days
            memory_type = memory.get('type', 'info')
            priority = memory.get('priority', 50)
            
            # 永不归档的类型
            if memory_type in policy['preserve_types']:
                return False, "类型保护"
            
            # 高优先级保护
            if priority >= 80 and days_old < policy['archive_high_priority_days']:
                return False, "高优先级保护"
            
            # 超长等待归档
            if days_old >= policy['auto_archive_days']:
                return True, f"超过{days_old}天"
            
            return False, "未达到归档条件"
            
        except:
            return False, "日期解析错误"
    
    def archive_memory(self, record_id: str, reason: str = "") -> bool:
        """归档单条记忆"""
        try:
            import sqlite3
            conn = sqlite3.connect(str(self.db_path))
            conn.row_factory = sqlite3.Row
            
            cursor = conn.execute("""
                SELECT * FROM l1_records WHERE record_id = ?
            """, (record_id,))
            row = cursor.fetchone()
            
            if not row:
                conn.close()
                return False
            
            # 创建归档记录
            archive_record = {
                'record_id': row['record_id'],
                'content': row['content'],
                'type': row['type'],
                'priority': row['priority'],
                'created_time': row['created_time'],
                'archived_at': datetime.now().isoformat(),
                'reason': reason,
            }
            
            # 保存到归档文件
            archive_file = self.archive_dir / f"{record_id}.json"
            with open(archive_file, 'w') as f:
                json.dump(archive_record, f, ensure_ascii=False, indent=2)
            
            # 从数据库删除
            conn.execute("DELETE FROM l1_records WHERE record_id = ?", (record_id,))
            conn.commit()
            conn.close()
            
            # 更新归档元数据
            self._update_archive_meta(record_id, 'archive')
            
            return True
            
        except Exception as e:
            print(f"归档失败: {e}")
            return False
    
    def batch_archive(self, dry_run: bool = False) -> Dict:
        """批量归档"""
        try:
            import sqlite3
            conn = sqlite3.connect(str(self.db_path))
            conn.row_factory = sqlite3.Row
            
            # 获取所有记忆
            cursor = conn.execute("""
                SELECT record_id, content, type, priority, created_time
                FROM l1_records
                ORDER BY created_time ASC
            """)
            
            to_archive = []
            for row in cursor.fetchall():
                memory = dict(row)
                should, reason = self.should_archive(memory)
                if should:
                    to_archive.append((memory, reason))
            
            archived_count = 0
            if not dry_run:
                for memory, reason in to_archive:
                    if self.archive_memory(memory['record_id'], reason):
                        archived_count += 1
            else:
                archived_count = len(to_archive)
            
            conn.close()
            
            return {
                'total_checked': cursor.rowcount,
                'archived': archived_count,
                'dry_run': dry_run,
                'reasons': [r for _, r in to_archive]
            }
            
        except Exception as e:
            return {'error': str(e), 'archived': 0}
    
    def restore_memory(self, record_id: str) -> bool:
        """恢复归档的记忆"""
        try:
            archive_file = self.archive_dir / f"{record_id}.json"
            if not archive_file.exists():
                return False
            
            with open(archive_file) as f:
                record = json.load(f)
            
            import sqlite3
            conn = sqlite3.connect(str(self.db_path))
            
            conn.execute("""
                INSERT INTO l1_records (record_id, content, type, priority, created_time)
                VALUES (?, ?, ?, ?, ?)
            """, (
                record['record_id'],
                record['content'],
                record['type'],
                record['priority'],
                record['created_time']
            ))
            
            conn.commit()
            conn.close()
            
            # 删除归档文件
            archive_file.unlink()
            
            # 更新元数据
            self._update_archive_meta(record_id, 'restore')
            
            return True
            
        except Exception as e:
            print(f"恢复失败: {e}")
            return False
    
    def list_archived(self, limit: int = 50) -> List[Dict]:
        """列出归档的记忆"""
        archives = []
        
        for archive_file in sorted(self.archive_dir.glob("*.json"), reverse=True)[:limit]:
            try:
                with open(archive_file) as f:
                    record = json.load(f)
                archives.append(record)
            except:
                continue
        
        return archives
    
    def get_archive_stats(self) -> Dict:
        """获取归档统计"""
        archives = self.list_archived(limit=1000)
        
        by_month = {}
        by_type = {}
        total_size = 0
        
        for a in archives:
            date = a.get('archived_at', '')[:7]  # YYYY-MM
            by_month[date] = by_month.get(date, 0) + 1
            
            t = a.get('type', 'unknown')
            by_type[t] = by_type.get(t, 0) + 1
            
            total_size += len(json.dumps(a))
        
        return {
            'total_archived': len(archives),
            'by_month': by_month,
            'by_type': by_type,
            'total_size_bytes': total_size,
        }
    
    def cleanup_old_archives(self, days: int = 180) -> int:
        """清理过期的归档"""
        policy = self.get_archive_policy()
        max_age = min(days, policy['keep_archive_days'])
        
        cutoff = datetime.now() - timedelta(days=max_age)
        removed = 0
        
        for archive_file in self.archive_dir.glob("*.json"):
            try:
                with open(archive_file) as f:
                    record = json.load(f)
                
                archived_at = datetime.fromisoformat(record.get('archived_at', '2000-01-01'))
                
                if archived_at < cutoff:
                    archive_file.unlink()
                    removed += 1
                    
            except:
                continue
        
        return removed
    
    def _update_archive_meta(self, record_id: str, action: str):
        """更新归档元数据"""
        meta = {'archives': [], 'restores': []}
        
        if self.archive_meta_file.exists():
            try:
                with open(self.archive_meta_file) as f:
                    meta = json.load(f)
            except:
                pass
        
        entry = {
            'record_id': record_id,
            'action': action,
            'timestamp': datetime.now().isoformat()
        }
        
        if action == 'archive':
            meta['archives'].append(entry)
        else:
            meta['restores'].append(entry)
        
        with open(self.archive_meta_file, 'w') as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)
    
    def generate_archive_report(self) -> str:
        """生成归档报告"""
        stats = self.get_archive_stats()
        
        lines = ["# 📦 记忆归档报告", ""]
        
        lines.append(f"**归档总数**：{stats['total_archived']} 条")
        lines.append(f"**占用空间**：{stats['total_size_bytes'] / 1024:.1f} KB")
        lines.append("")
        
        if stats['by_month']:
            lines.append("## 📅 按月统计")
            for month, count in sorted(stats['by_month'].items(), reverse=True)[:6]:
                lines.append(f"- {month}：{count} 条")
            lines.append("")
        
        if stats['by_type']:
            lines.append("## 📂 按类型统计")
            for t, count in sorted(stats['by_type'].items(), key=lambda x: -x[1]):
                lines.append(f"- {t}：{count} 条")
        
        return "\n".join(lines)


def main():
    """CLI 入口"""
    import argparse
    parser = argparse.ArgumentParser(description='记忆归档')
    parser.add_argument('--list', '-l', action='store_true', help='列出归档')
    parser.add_argument('--archive', '-a', type=str, help='归档指定记忆')
    parser.add_argument('--restore', '-r', type=str, help='恢复归档')
    parser.add_argument('--batch', '-b', action='store_true', help='批量归档')
    parser.add_argument('--dry-run', action='store_true', help='试运行')
    parser.add_argument('--stats', '-s', action='store_true', help='归档统计')
    parser.add_argument('--cleanup', '-c', type=int, help='清理过期归档')
    args = parser.parse_args()
    
    archiver = MemoryArchiver()
    
    if args.list:
        archives = archiver.list_archived()
        print(f"# 📦 已归档记忆 ({len(archives)} 条)")
        for a in archives[:10]:
            print(f"\n## {a['record_id']}")
            print(f"类型: {a['type']} | 归档时间: {a.get('archived_at', 'unknown')}")
            print(f"原因: {a.get('reason', 'N/A')}")
            print(f"内容: {a['content'][:60]}...")
    
    elif args.archive:
        if archiver.archive_memory(args.archive):
            print(f"✅ 记忆 {args.archive} 已归档")
        else:
            print(f"❌ 归档失败")
    
    elif args.restore:
        if archiver.restore_memory(args.restore):
            print(f"✅ 记忆 {args.restore} 已恢复")
        else:
            print(f"❌ 恢复失败")
    
    elif args.batch:
        result = archiver.batch_archive(dry_run=args.dry_run)
        if 'error' in result:
            print(f"❌ 批量归档失败: {result['error']}")
        elif result['dry_run']:
            print(f"# 🔍 试运行结果")
            print(f"将归档 {result['archived']} 条记忆")
        else:
            print(f"✅ 批量归档完成，共归档 {result['archived']} 条")
    
    elif args.stats:
        print(archiver.generate_archive_report())
    
    elif args.cleanup:
        removed = archiver.cleanup_old_archives(args.cleanup)
        print(f"✅ 已清理 {removed} 个过期归档")
    
    else:
        print(archiver.generate_archive_report())


if __name__ == '__main__':
    main()
