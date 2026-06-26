#!/usr/bin/env python3
"""
记忆备份/恢复模块 - v1.0.0
支持记忆的导出、导入和迁移

功能：
1. 导出记忆到 JSON 文件
2. 从 JSON 文件导入记忆
3. 增量备份（只备份新增/修改的）
4. 记忆迁移（跨环境）
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import hashlib

# 配置
MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
BACKUP_DIR = MEMORY_DIR / "backups"
EXCLUDE_FILES = {".meta.json", ".heat_data.json", "archive", ".DS_Store"}

class BackupRestore:
    """记忆备份/恢复器"""
    
    def __init__(self):
        self.memory_dir = MEMORY_DIR
        self.backup_dir = BACKUP_DIR
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_file_hash(self, file_path: Path) -> str:
        """计算文件哈希（用于检测变更）"""
        try:
            content = file_path.read_text(encoding="utf-8")
            return hashlib.md5(content.encode()).hexdigest()
        except:
            return ""
    
    def export_all(self, output_path: str = None, include_stats: bool = True) -> Dict:
        """
        导出所有记忆
        - output_path: 输出文件路径
        - include_stats: 是否包含热度等统计信息
        """
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.backup_dir / f"backup_{timestamp}.json"
        else:
            output_path = Path(output_path)
        
        memories = []
        stats = {}
        
        # 遍历所有记忆文件
        for f in self.memory_dir.glob("*.md"):
            if f.name in EXCLUDE_FILES or "合并版" in f.name:
                continue
            
            try:
                content = f.read_text(encoding="utf-8")
                memories.append({
                    "filename": f.name,
                    "content": content,
                    "size": len(content),
                    "modified": datetime.fromtimestamp(f.stat().st_mtime).isoformat()
                })
            except:
                pass
        
        # 导出统计信息
        if include_stats:
            heat_file = self.memory_dir / ".heat_data.json"
            if heat_file.exists():
                try:
                    stats = json.loads(heat_file.read_text(encoding="utf-8"))
                except:
                    pass
        
        # 构建导出数据
        export_data = {
            "version": "1.0",
            "export_time": datetime.now().isoformat(),
            "memory_count": len(memories),
            "memories": memories,
            "stats": stats
        }
        
        # 保存
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(export_data, ensure_ascii=False, indent=2), 
            encoding="utf-8"
        )
        
        return {
            "success": True,
            "output_path": str(output_path),
            "memory_count": len(memories),
            "size_bytes": len(json.dumps(export_data))
        }
    
    def import_memories(self, input_path: str, mode: str = "merge") -> Dict:
        """
        导入记忆
        - input_path: 导入文件路径
        - mode: merge(合并) | replace(替换) | skip(跳过已存在)
        """
        input_path = Path(input_path)
        if not input_path.exists():
            return {"success": False, "error": f"文件不存在: {input_path}"}
        
        try:
            data = json.loads(input_path.read_text(encoding="utf-8"))
        except Exception as e:
            return {"success": False, "error": f"JSON解析失败: {e}"}
        
        memories = data.get("memories", [])
        if not memories:
            return {"success": False, "error": "没有记忆数据"}
        
        imported = 0
        skipped = 0
        errors = []
        
        for mem in memories:
            filename = mem.get("filename", "")
            content = mem.get("content", "")
            
            if not filename or not content:
                errors.append(f"跳过无效记录: {filename}")
                continue
            
            target_path = self.memory_dir / filename
            
            # 检查是否已存在
            if target_path.exists():
                if mode == "skip":
                    skipped += 1
                    continue
                elif mode == "replace":
                    pass  # 继续覆盖
                elif mode == "merge":
                    # 合并：追加内容
                    existing = target_path.read_text(encoding="utf-8")
                    # 简单合并：时间戳分隔
                    content = existing + f"\n\n---\n# 合并导入 {datetime.now().isoformat()} ---\n\n" + content
            
            try:
                target_path.write_text(content, encoding="utf-8")
                imported += 1
            except Exception as e:
                errors.append(f"写入失败 {filename}: {e}")
        
        return {
            "success": True,
            "imported": imported,
            "skipped": skipped,
            "errors": errors,
            "total": len(memories)
        }
    
    def list_backups(self) -> List[Dict]:
        """列出所有备份文件"""
        backups = []
        for f in sorted(self.backup_dir.glob("backup_*.json"), reverse=True):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                backups.append({
                    "filename": f.name,
                    "path": str(f),
                    "size": f.stat().st_size,
                    "memory_count": data.get("memory_count", 0),
                    "export_time": data.get("export_time", "")
                })
            except:
                pass
        return backups
    
    def incremental_backup(self) -> Dict:
        """增量备份（只备份有变更的文件）"""
        manifest_file = self.backup_dir / ".backup_manifest.json"
        
        # 读取上次备份的清单
        last_hashes = {}
        if manifest_file.exists():
            try:
                last_hashes = json.loads(manifest_file.read_text())
            except:
                pass
        
        # 计算当前文件的哈希
        current_hashes = {}
        changed_files = []
        
        for f in self.memory_dir.glob("*.md"):
            if f.name in EXCLUDE_FILES or "合并版" in f.name:
                continue
            
            file_hash = self._get_file_hash(f)
            current_hashes[f.name] = file_hash
            
            if f.name not in last_hashes or last_hashes[f.name] != file_hash:
                changed_files.append(f.name)
        
        if not changed_files:
            return {
                "success": True,
                "changed_count": 0,
                "message": "没有变更的文件"
            }
        
        # 只备份有变更的文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = self.backup_dir / f"incremental_{timestamp}.json"
        
        memories = []
        for f in self.memory_dir.glob("*.md"):
            if f.name in changed_files:
                try:
                    memories.append({
                        "filename": f.name,
                        "content": f.read_text(encoding="utf-8"),
                        "modified": datetime.fromtimestamp(f.stat().st_mtime).isoformat()
                    })
                except:
                    pass
        
        export_data = {
            "version": "1.0",
            "type": "incremental",
            "export_time": datetime.now().isoformat(),
            "changed_files": changed_files,
            "memories": memories
        }
        
        output_path.write_text(
            json.dumps(export_data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        
        # 更新清单
        manifest_file.write_text(json.dumps(current_hashes))
        
        return {
            "success": True,
            "output_path": str(output_path),
            "changed_count": len(changed_files),
            "changed_files": changed_files
        }


if __name__ == "__main__":
    br = BackupRestore()
    
    # 测试导出
    print("=== 导出测试 ===")
    result = br.export_all()
    print(f"导出结果: {result}")
    
    # 列出备份
    print("\n=== 备份列表 ===")
    backups = br.list_backups()
    for b in backups[:3]:
        print(f"  - {b['filename']} ({b['memory_count']}条记忆)")
