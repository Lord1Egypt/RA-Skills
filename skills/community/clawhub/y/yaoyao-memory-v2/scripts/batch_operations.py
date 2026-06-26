#!/usr/bin/env python3
"""
batch_operations.py - 批量记忆操作工具
支持批量导入/导出/删除/更新
"""
import json
import sqlite3
import csv
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
MEMORY_DB = MEMORY_DIR / "memory.db"
EXPORT_DIR = MEMORY_DIR / "exports"


class BatchOperations:
    """批量操作管理器"""
    
    def __init__(self):
        self.db_path = MEMORY_DB
    
    def _connect(self):
        """连接数据库"""
        return sqlite3.connect(self.db_path)
    
    def export_to_json(self, output_path: str = None, type_filter: str = None) -> int:
        """导出到JSON"""
        if not output_path:
            EXPORT_DIR.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = EXPORT_DIR / f"memory_export_{timestamp}.json"
        
        conn = self._connect()
        
        query = "SELECT id, type, content, importance, tags, created_at, updated_at FROM memories"
        params = []
        if type_filter:
            query += " WHERE type = ?"
            params.append(type_filter)
        
        cursor = conn.execute(query, params)
        rows = cursor.fetchall()
        
        memories = []
        for row in rows:
            memories.append({
                "id": row[0],
                "type": row[1],
                "content": row[2],
                "importance": row[3],
                "tags": json.loads(row[4]) if row[4] else [],
                "created_at": row[5],
                "updated_at": row[6]
            })
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(memories, f, ensure_ascii=False, indent=2)
        
        conn.close()
        return len(memories)
    
    def export_to_csv(self, output_path: str = None) -> int:
        """导出到CSV"""
        if not output_path:
            EXPORT_DIR.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = EXPORT_DIR / f"memory_export_{timestamp}.csv"
        
        conn = self._connect()
        cursor = conn.execute(
            "SELECT id, type, content, importance, tags, created_at FROM memories"
        )
        rows = cursor.fetchall()
        
        with open(output_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "type", "content", "importance", "tags", "created_at"])
            for row in rows:
                writer.writerow(row)
        
        conn.close()
        return len(rows)
    
    def import_from_json(self, input_path: str, update_existing: bool = True) -> Dict:
        """从JSON导入"""
        with open(input_path, "r", encoding="utf-8") as f:
            memories = json.load(f)
        
        conn = self._connect()
        imported = 0
        updated = 0
        skipped = 0
        
        for mem in memories:
            # 检查是否已存在
            cursor = conn.execute("SELECT id FROM memories WHERE id = ?", (mem["id"],))
            exists = cursor.fetchone()
            
            if exists:
                if update_existing:
                    conn.execute("""
                        UPDATE memories 
                        SET content = ?, type = ?, importance = ?, tags = ?, updated_at = ?
                        WHERE id = ?
                    """, (
                        mem["content"],
                        mem.get("type", "info"),
                        mem.get("importance", "normal"),
                        json.dumps(mem.get("tags", [])),
                        datetime.now().isoformat(),
                        mem["id"]
                    ))
                    updated += 1
                else:
                    skipped += 1
            else:
                conn.execute("""
                    INSERT INTO memories (id, type, content, importance, tags, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    mem["id"],
                    mem.get("type", "info"),
                    mem["content"],
                    mem.get("importance", "normal"),
                    json.dumps(mem.get("tags", [])),
                    mem.get("created_at", datetime.now().isoformat()),
                    datetime.now().isoformat()
                ))
                imported += 1
        
        conn.commit()
        conn.close()
        
        return {
            "imported": imported,
            "updated": updated,
            "skipped": skipped,
            "total": imported + updated + skipped
        }
    
    def batch_delete(self, ids: List[str]) -> int:
        """批量删除"""
        if not ids:
            return 0
        
        conn = self._connect()
        placeholders = ",".join("?" * len(ids))
        conn.execute(f"DELETE FROM memories WHERE id IN ({placeholders})", ids)
        deleted = conn.rowcount
        conn.commit()
        conn.close()
        
        return deleted
    
    def batch_update_importance(self, updates: Dict[str, str]) -> int:
        """批量更新重要性"""
        if not updates:
            return 0
        
        conn = self._connect()
        updated = 0
        for id, importance in updates.items():
            conn.execute(
                "UPDATE memories SET importance = ?, updated_at = ? WHERE id = ?",
                (importance, datetime.now().isoformat(), id)
            )
            updated += 1
        
        conn.commit()
        conn.close()
        return updated
    
    def find_duplicates(self) -> List[Dict]:
        """查找重复记忆（基于内容hash）"""
        import hashlib
        
        conn = self._connect()
        cursor = conn.execute("""
            SELECT id, type, content, importance, created_at 
            FROM memories 
            ORDER BY created_at DESC
        """)
        rows = cursor.fetchall()
        
        seen = {}
        duplicates = []
        
        for row in rows:
            content_hash = hashlib.md5(row[2].encode()).hexdigest()
            
            if content_hash in seen:
                duplicates.append({
                    "original_id": seen[content_hash],
                    "duplicate_id": row[0],
                    "content_preview": row[2][:100],
                    "created_at": row[4]
                })
            else:
                seen[content_hash] = row[0]
        
        conn.close()
        return duplicates
    
    def cleanup_duplicates(self, keep: str = "newest") -> int:
        """清理重复记忆"""
        duplicates = self.find_duplicates()
        
        if not duplicates:
            return 0
        
        ids_to_delete = []
        for dup in duplicates:
            if keep == "newest":
                ids_to_delete.append(dup["original_id"])
            else:
                ids_to_delete.append(dup["duplicate_id"])
        
        return self.batch_delete(ids_to_delete)


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("""📦 批量记忆操作
    
用法:
    batch_operations.py export_json [类型]   # 导出JSON
    batch_operations.py export_csv          # 导出CSV
    batch_operations.py import_json <文件>  # 导入JSON
    batch_operations.py duplicates          # 查找重复
    batch_operations.py cleanup_dup         # 清理重复
    batch_operations.py batch_delete <ids>  # 批量删除""")
        return
    
    cmd = sys.argv[1]
    batch = BatchOperations()
    
    if cmd == "export_json":
        type_filter = sys.argv[2] if len(sys.argv) > 2 else None
        count = batch.export_to_json(type_filter=type_filter)
        print(f"✅ 导出成功: {count} 条记忆")
    
    elif cmd == "export_csv":
        count = batch.export_to_csv()
        print(f"✅ 导出成功: {count} 条记忆")
    
    elif cmd == "import_json":
        if len(sys.argv) < 3:
            print("❌ 请指定导入文件")
            return
        result = batch.import_from_json(sys.argv[2])
        print(f"✅ 导入完成:")
        print(f"   新增: {result['imported']}")
        print(f"   更新: {result['updated']}")
        print(f"   跳过: {result['skipped']}")
    
    elif cmd == "duplicates":
        dups = batch.find_duplicates()
        if not dups:
            print("✅ 无重复记忆")
        else:
            print(f"⚠️ 发现 {len(dups)} 组重复:")
            for dup in dups[:10]:
                print(f"   {dup['original_id']} <-> {dup['duplicate_id']}")
    
    elif cmd == "cleanup_dup":
        count = batch.cleanup_duplicates()
        print(f"✅ 已清理 {count} 条重复记忆")
    
    elif cmd == "batch_delete":
        if len(sys.argv) < 3:
            print("❌ 请指定ID列表（逗号分隔）")
            return
        ids = sys.argv[2].split(",")
        count = batch.batch_delete(ids)
        print(f"✅ 已删除 {count} 条记忆")


if __name__ == "__main__":
    main()
