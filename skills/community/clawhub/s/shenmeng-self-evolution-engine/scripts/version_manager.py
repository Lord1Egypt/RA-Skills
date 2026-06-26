#!/usr/bin/env python3
"""
版本管理器 - 管理Skill的版本演进和回滚

用法:
    # 创建版本快照
    python version_manager.py --skill my-skill --snapshot --message "添加新功能"
    
    # 查看版本历史
    python version_manager.py --skill my-skill --history
    
    # 回滚到指定版本
    python version_manager.py --skill my-skill --rollback v1.2.0
"""

import argparse
import json
import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import hashlib


class VersionManager:
    """版本管理器"""
    
    def __init__(self, skill_name: str, workspace_dir: str = "/root/.openclaw/workspace/skills"):
        self.skill_name = skill_name
        self.skill_dir = Path(workspace_dir) / skill_name
        self.versions_dir = self.skill_dir / ".versions"
        self.versions_dir.mkdir(exist_ok=True)
        
        self.manifest_file = self.versions_dir / "manifest.json"
        self.manifest = self._load_manifest()
    
    def _load_manifest(self) -> Dict:
        """加载版本清单"""
        if self.manifest_file.exists():
            with open(self.manifest_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"versions": [], "current": None}
    
    def _save_manifest(self):
        """保存版本清单"""
        with open(self.manifest_file, 'w', encoding='utf-8') as f:
            json.dump(self.manifest, f, indent=2, ensure_ascii=False)
    
    def _get_next_version(self) -> str:
        """获取下一个版本号"""
        if not self.manifest['versions']:
            return "v1.0.0"
        
        # 解析最新版本
        latest = self.manifest['versions'][-1]['version']
        parts = latest.replace('v', '').split('.')
        major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
        
        # 自动增加patch版本
        patch += 1
        return f"v{major}.{minor}.{patch}"
    
    def _calculate_checksum(self, filepath: Path) -> str:
        """计算文件校验和"""
        hasher = hashlib.md5()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    
    def create_snapshot(self, message: str = "") -> Dict:
        """创建版本快照"""
        version = self._get_next_version()
        snapshot_dir = self.versions_dir / version
        snapshot_dir.mkdir(exist_ok=True)
        
        # 收集文件
        files_info = []
        
        for pattern in ["*.py", "*.md", "*.json", "*.txt", "*.yaml", "*.yml"]:
            for file in self.skill_dir.rglob(pattern):
                # 跳过版本控制目录
                if any(skip in str(file) for skip in ['.versions', '.evolutions', '.backups', '__pycache__', '.git']):
                    continue
                
                rel_path = file.relative_to(self.skill_dir)
                dest = snapshot_dir / rel_path
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file, dest)
                
                files_info.append({
                    "path": str(rel_path),
                    "checksum": self._calculate_checksum(file),
                    "size": file.stat().st_size
                })
        
        # 创建版本记录
        version_record = {
            "version": version,
            "created_at": datetime.now().isoformat(),
            "message": message,
            "files_count": len(files_info),
            "files": files_info
        }
        
        self.manifest['versions'].append(version_record)
        self.manifest['current'] = version
        self._save_manifest()
        
        return version_record
    
    def get_history(self) -> List[Dict]:
        """获取版本历史"""
        return self.manifest.get('versions', [])
    
    def rollback(self, version: str, confirmed: bool = False) -> Dict:
        """回滚到指定版本"""
        if not confirmed:
            return {
                "status": "pending",
                "message": f"⚠️ 即将回滚到 {version}",
                "warning": "当前未保存的修改将丢失",
                "action_required": "添加 --confirm 参数确认回滚"
            }
        
        # 检查版本是否存在
        version_exists = any(v['version'] == version for v in self.manifest['versions'])
        if not version_exists:
            return {"status": "error", "message": f"版本 {version} 不存在"}
        
        snapshot_dir = self.versions_dir / version
        if not snapshot_dir.exists():
            return {"status": "error", "message": f"版本 {version} 的快照不存在"}
        
        # 先创建当前状态的备份
        current_backup = self.create_snapshot("自动备份：回滚前")
        
        # 恢复文件
        restored_files = []
        for file_path in snapshot_dir.rglob("*"):
            if file_path.is_file():
                rel_path = file_path.relative_to(snapshot_dir)
                dest = self.skill_dir / rel_path
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file_path, dest)
                restored_files.append(str(rel_path))
        
        # 更新当前版本
        self.manifest['current'] = version
        self._save_manifest()
        
        return {
            "status": "success",
            "rolled_back_to": version,
            "backup_created": current_backup['version'],
            "restored_files": len(restored_files)
        }
    
    def compare_versions(self, v1: str, v2: str) -> Dict:
        """比较两个版本"""
        # 获取版本信息
        v1_record = next((v for v in self.manifest['versions'] if v['version'] == v1), None)
        v2_record = next((v for v in self.manifest['versions'] if v['version'] == v2), None)
        
        if not v1_record or not v2_record:
            return {"error": "版本不存在"}
        
        # 比较文件
        v1_files = {f['path']: f for f in v1_record['files']}
        v2_files = {f['path']: f for f in v2_record['files']}
        
        added = []
        removed = []
        modified = []
        
        for path, info in v2_files.items():
            if path not in v1_files:
                added.append(path)
            elif v1_files[path]['checksum'] != info['checksum']:
                modified.append(path)
        
        for path in v1_files:
            if path not in v2_files:
                removed.append(path)
        
        return {
            "from": v1,
            "to": v2,
            "added": added,
            "removed": removed,
            "modified": modified,
            "summary": f"+{len(added)} -{len(removed)} ~{len(modified)}"
        }
    
    def get_diff(self, version: str) -> str:
        """获取与上一版本的差异"""
        versions = self.manifest['versions']
        current_idx = next((i for i, v in enumerate(versions) if v['version'] == version), -1)
        
        if current_idx <= 0:
            return "这是第一个版本，无差异可比较"
        
        prev_version = versions[current_idx - 1]['version']
        comparison = self.compare_versions(prev_version, version)
        
        lines = [f"## {prev_version} → {version}", ""]
        
        if comparison['added']:
            lines.append(f"### 新增文件 (+{len(comparison['added'])})")
            for f in comparison['added']:
                lines.append(f"  + {f}")
            lines.append("")
        
        if comparison['removed']:
            lines.append(f"### 删除文件 (-{len(comparison['removed'])})")
            for f in comparison['removed']:
                lines.append(f"  - {f}")
            lines.append("")
        
        if comparison['modified']:
            lines.append(f"### 修改文件 (~{len(comparison['modified'])})")
            for f in comparison['modified']:
                lines.append(f"  ~ {f}")
            lines.append("")
        
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='版本管理器')
    parser.add_argument('--skill', type=str, required=True, help='Skill名称')
    parser.add_argument('--snapshot', action='store_true', help='创建版本快照')
    parser.add_argument('--message', type=str, default='', help='版本说明')
    parser.add_argument('--history', action='store_true', help='查看版本历史')
    parser.add_argument('--rollback', type=str, help='回滚到指定版本')
    parser.add_argument('--confirm', action='store_true', help='确认回滚')
    parser.add_argument('--compare', nargs=2, metavar=('V1', 'V2'), help='比较两个版本')
    parser.add_argument('--diff', type=str, help='查看版本差异')
    
    args = parser.parse_args()
    
    manager = VersionManager(args.skill)
    
    if args.snapshot:
        record = manager.create_snapshot(args.message)
        print(f"[OK] 已创建版本: {record['version']}")
        print(f"  文件数: {record['files_count']}")
        print(f"  说明: {record['message']}")
    
    elif args.history:
        history = manager.get_history()
        print(f"[*] 版本历史 ({len(history)} 个版本)")
        print("-" * 60)
        for v in history:
            marker = " ← 当前" if v['version'] == manager.manifest.get('current') else ""
            print(f"{v['version']}{marker}")
            print(f"  时间: {v['created_at'][:10]}")
            print(f"  文件: {v['files_count']} 个")
            print(f"  说明: {v['message'] or '无'}")
            print()
    
    elif args.rollback:
        result = manager.rollback(args.rollback, args.confirm)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.compare:
        comparison = manager.compare_versions(args.compare[0], args.compare[1])
        print(json.dumps(comparison, indent=2, ensure_ascii=False))
    
    elif args.diff:
        diff = manager.get_diff(args.diff)
        print(diff)
    
    else:
        print(f"[*] 版本管理器已初始化: {args.skill}")
        print("[*] 当前版本:", manager.manifest.get('current', '无'))
        print("[*] 使用 --snapshot 创建新版本")
        print("[*] 使用 --history 查看历史")


if __name__ == '__main__':
    main()
