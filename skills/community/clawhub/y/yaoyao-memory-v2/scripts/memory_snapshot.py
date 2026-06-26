#!/usr/bin/env python3
"""
记忆快照模块 - 快速保存和恢复记忆状态

功能：
- 创建记忆快照（完整备份）
- 创建增量快照（差异备份）
- 恢复指定快照
- 快照列表管理
- 自动快照（定时/事件触发）
"""

import sys
import json
import sqlite3
import shutil
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import gzip
import tarfile

sys.path.insert(0, str(Path(__file__).parent.parent))
from paths import get_vectors_db, get_memory_base


class MemorySnapshot:
    """记忆快照管理器"""
    
    def __init__(self, snapshot_dir: Optional[Path] = None):
        self.db_path = Path(get_vectors_db())
        self.memory_base = Path(get_memory_base())
        
        if snapshot_dir is None:
            snapshot_dir = self.memory_base / ".snapshots"
        
        self.snapshot_dir = snapshot_dir
        self.snapshot_dir.mkdir(parents=True, exist_ok=True)
        
        self.conn = None
        self._connect()
    
    def _connect(self):
        """连接数据库"""
        if self.db_path.exists():
            self.conn = sqlite3.connect(str(self.db_path))
            self.conn.row_factory = sqlite3.Row
    
    def create_snapshot(self, name: Optional[str] = None, snapshot_type: str = "full") -> Dict:
        """创建快照"""
        if not name:
            name = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        snapshot_info = {
            "name": name,
            "created_at": datetime.now().isoformat(),
            "type": snapshot_type,
            "id": hashlib.md5(f"{name}_{time.time()}".encode()).hexdigest()[:12]
        }
        
        snapshot_path = self.snapshot_dir / f"{snapshot_info['id']}.tar.gz"
        
        try:
            with tarfile.open(snapshot_path, "w:gz") as tar:
                # 备份数据库
                if self.db_path.exists():
                    tar.add(str(self.db_path), arcname="vectors.db")
                
                # 备份记忆文件
                memory_files = list(self.memory_base.glob("*.md"))
                for f in memory_files:
                    tar.add(f, arcname=f"memory/{f.name}")
                
                # 备份配置
                config_dir = Path(__file__).parent.parent / "config"
                if config_dir.exists():
                    for f in config_dir.glob("*.json"):
                        if "llm_config" not in f.name and "embeddings" not in f.name:
                            tar.add(f, arcname=f"config/{f.name}")
            
            snapshot_info["path"] = str(snapshot_path)
            snapshot_info["size"] = snapshot_path.stat().st_size
            snapshot_info["status"] = "success"
            
            # 保存快照元数据
            self._save_snapshot_info(snapshot_info)
            
        except Exception as e:
            snapshot_info["status"] = "failed"
            snapshot_info["error"] = str(e)
        
        return snapshot_info
    
    def _save_snapshot_info(self, info: Dict):
        """保存快照元数据"""
        meta_file = self.snapshot_dir / "snapshots.json"
        
        snapshots = []
        if meta_file.exists():
            with open(meta_file) as f:
                snapshots = json.load(f)
        
        # 更新或添加
        existing_idx = None
        for i, s in enumerate(snapshots):
            if s.get("id") == info.get("id"):
                existing_idx = i
                break
        
        if existing_idx is not None:
            snapshots[existing_idx] = info
        else:
            snapshots.append(info)
        
        with open(meta_file, "w") as f:
            json.dump(snapshots, f, indent=2, ensure_ascii=False)
    
    def list_snapshots(self) -> List[Dict]:
        """列出所有快照"""
        meta_file = self.snapshot_dir / "snapshots.json"
        
        if not meta_file.exists():
            return []
        
        with open(meta_file) as f:
            snapshots = json.load(f)
        
        # 补充实际文件大小
        for s in snapshots:
            if "path" in s:
                p = Path(s["path"])
                if p.exists():
                    s["actual_size"] = p.stat().st_size
                else:
                    s["actual_size"] = 0
                    s["status"] = "missing"
        
        return sorted(snapshots, key=lambda x: x.get("created_at", ""), reverse=True)
    
    def restore_snapshot(self, snapshot_id: str) -> bool:
        """恢复指定快照"""
        snapshots = self.list_snapshots()
        
        target = None
        for s in snapshots:
            if s.get("id") == snapshot_id:
                target = s
                break
        
        if not target or "path" not in target:
            return False
        
        snapshot_path = Path(target["path"])
        if not snapshot_path.exists():
            return False
        
        try:
            # 创建当前状态备份（安全垫）
            current_backup = self.snapshot_dir / f"pre_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tar.gz"
            with tarfile.open(current_backup, "w:gz") as tar:
                if self.db_path.exists():
                    tar.add(self.db_path, arcname="vectors.db")
            
            # 解压恢复（安全：验证成员名称）
            with tarfile.open(snapshot_path, "r:gz") as tar:
                for member in tar.getmembers():
                    # 防止路径穿越攻击
                    member_name = member.name
                    if '..' in member_name or member_name.startswith('/'):
                        continue
                    # 安全提取
                    member.path = str(self.memory_base / member_name)
                    tar.extract(member, path=self.memory_base)
            
            return True
            
        except Exception as e:
            print(f"恢复失败: {e}")
            return False
    
    def delete_snapshot(self, snapshot_id: str) -> bool:
        """删除快照"""
        snapshots = self.list_snapshots()
        
        target_idx = None
        for i, s in enumerate(snapshots):
            if s.get("id") == snapshot_id:
                target_idx = i
                break
        
        if target_idx is None:
            return False
        
        target = snapshots[target_idx]
        
        # 删除文件
        if "path" in target:
            p = Path(target["path"])
            if p.exists():
                p.unlink()
        
        # 更新元数据
        snapshots.pop(target_idx)
        meta_file = self.snapshot_dir / "snapshots.json"
        with open(meta_file, "w") as f:
            json.dump(snapshots, f, indent=2, ensure_ascii=False)
        
        return True
    
    def auto_snapshot(self, max_snapshots: int = 10) -> Optional[Dict]:
        """自动快照（保留最近N个）"""
        # 检查是否需要快照（每天一次）
        snapshots = self.list_snapshots()
        
        if snapshots:
            latest = datetime.fromisoformat(snapshots[0]["created_at"])
            if datetime.now() - latest < timedelta(hours=6):
                return None  # 6小时内已快照
        
        # 创建快照
        result = self.create_snapshot(snapshot_type="auto")
        
        # 清理旧快照
        if len(snapshots) >= max_snapshots:
            for old in snapshots[max_snapshots:]:
                self.delete_snapshot(old["id"])
        
        return result
    
    def get_snapshot_diff(self, snapshot_id1: str, snapshot_id2: str) -> Dict:
        """比较两个快照的差异"""
        # 简化实现：只比较数据库记录数
        snapshots = {s["id"]: s for s in self.list_snapshots()}
        
        if snapshot_id1 not in snapshots or snapshot_id2 not in snapshots:
            return {}
        
        s1 = snapshots[snapshot_id1]
        s2 = snapshots[snapshot_id2]
        
        return {
            "snapshot1": {
                "created_at": s1.get("created_at"),
                "size": s1.get("size")
            },
            "snapshot2": {
                "created_at": s2.get("created_at"),
                "size": s2.get("size")
            },
            "time_diff": f"{(datetime.fromisoformat(s2['created_at']) - datetime.fromisoformat(s1['created_at'])).days} 天"
        }
    
    def close(self):
        """关闭连接"""
        if self.conn:
            self.conn.close()


def main():
    """CLI 入口"""
    import argparse
    parser = argparse.ArgumentParser(description='记忆快照管理')
    parser.add_argument('--create', '-c', nargs='?', const='auto', help='创建快照')
    parser.add_argument('--list', '-l', action='store_true', help='列出快照')
    parser.add_argument('--restore', '-r', type=str, help='恢复快照')
    parser.add_argument('--delete', '-d', type=str, help='删除快照')
    parser.add_argument('--diff', nargs=2, help='比较两个快照')
    args = parser.parse_args()
    
    snapshot_mgr = MemorySnapshot()
    
    if args.create is not None:
        name = args.create if args.create != 'auto' else None
        result = snapshot_mgr.create_snapshot(name)
        if result["status"] == "success":
            print(f"✅ 快照创建成功: {result['id']}")
            print(f"   大小: {result['size'] / 1024:.1f} KB")
        else:
            print(f"❌ 创建失败: {result.get('error')}")
    
    elif args.list:
        snapshots = snapshot_mgr.list_snapshots()
        print(f"# 📦 快照列表 ({len(snapshots)} 个)")
        for s in snapshots:
            size = s.get("actual_size", s.get("size", 0))
            print(f"\n## {s['id']}")
            print(f"- 创建时间: {s['created_at']}")
            print(f"- 类型: {s.get('type', 'unknown')}")
            print(f"- 大小: {size / 1024:.1f} KB")
            print(f"- 状态: {s.get('status', 'ok')}")
    
    elif args.restore:
        if snapshot_mgr.restore_snapshot(args.restore):
            print(f"✅ 快照 {args.restore} 已恢复")
        else:
            print(f"❌ 恢复失败")
    
    elif args.delete:
        if snapshot_mgr.delete_snapshot(args.delete):
            print(f"✅ 快照 {args.delete} 已删除")
        else:
            print(f"❌ 删除失败")
    
    elif args.diff:
        diff = snapshot_mgr.get_snapshot_diff(args.diff[0], args.diff[1])
        if diff:
            print(f"# 比较结果")
            print(f"快照1: {diff['snapshot1']['created_at']} ({diff['snapshot1']['size']} bytes)")
            print(f"快照2: {diff['snapshot2']['created_at']} ({diff['snapshot2']['size']} bytes)")
            print(f"时间差: {diff['time_diff']}")
        else:
            print("❌ 快照不存在")
    
    else:
        # 默认显示列表
        snapshots = snapshot_mgr.list_snapshots()
        print(f"# 📦 快照列表 ({len(snapshots)} 个)")
        for s in snapshots[:5]:
            print(f"- {s['id']} | {s['created_at']} | {s.get('type', 'unknown')}")
    
    snapshot_mgr.close()


if __name__ == '__main__':
    main()
