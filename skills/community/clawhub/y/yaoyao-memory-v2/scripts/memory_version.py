#!/usr/bin/env python3
"""
记忆版本控制模块 - v1.0.0
追踪记忆的历史变更

功能：
1. 记录每次记忆修改的快照
2. 查看历史版本
3. 回滚到指定版本
4. 查看修改历史
"""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
VERSIONS_DIR = MEMORY_DIR / ".versions"

class MemoryVersion:
    """记忆版本控制器"""
    
    def __init__(self):
        self.memory_dir = MEMORY_DIR
        self.versions_dir = VERSIONS_DIR
        self.versions_dir.mkdir(parents=True, exist_ok=True)
    
    def save_version(self, filename: str, reason: str = "") -> bool:
        """
        保存记忆的当前版本
        - filename: 记忆文件名
        - reason: 修改原因（可选）
        """
        file_path = self.memory_dir / filename
        if not file_path.exists():
            return False
        
        try:
            content = file_path.read_text(encoding="utf-8")
            
            # 创建版本文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            version_filename = f"{filename}.v{timestamp}.json"
            version_path = self.versions_dir / version_filename
            
            # 保存版本快照
            version_data = {
                "filename": filename,
                "timestamp": datetime.now().isoformat(),
                "reason": reason,
                "content": content,
                "size": len(content)
            }
            
            version_path.write_text(
                json.dumps(version_data, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            
            # 更新索引
            self._update_index(filename, version_filename)
            
            return True
        except Exception as e:
            print(f"保存版本失败: {e}")
            return False
    
    def _update_index(self, filename: str, version_filename: str):
        """更新版本索引"""
        index_file = self.versions_dir / f"{filename}.index.json"
        
        index = {}
        if index_file.exists():
            try:
                index = json.loads(index_file.read_text(encoding="utf-8"))
            except:
                pass
        
        if filename not in index:
            index[filename] = []
        
        index[filename].append(version_filename)
        
        index_file.write_text(
            json.dumps(index, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
    
    def get_versions(self, filename: str) -> List[Dict]:
        """获取记忆的所有版本"""
        index_file = self.versions_dir / f"{filename}.index.json"
        
        if not index_file.exists():
            return []
        
        try:
            index = json.loads(index_file.read_text(encoding="utf-8"))
            version_files = index.get(filename, [])
            
            versions = []
            for vf in reversed(version_files[-10:]):  # 最近10个版本
                version_path = self.versions_dir / vf
                if version_path.exists():
                    data = json.loads(version_path.read_text(encoding="utf-8"))
                    versions.append({
                        "version_file": vf,
                        "timestamp": data["timestamp"],
                        "reason": data.get("reason", ""),
                        "size": data["size"]
                    })
            
            return versions
        except:
            return []
    
    def get_version_content(self, version_filename: str) -> Optional[str]:
        """获取指定版本的内容"""
        version_path = self.versions_dir / version_filename
        
        if not version_path.exists():
            return None
        
        try:
            data = json.loads(version_path.read_text(encoding="utf-8"))
            return data["content"]
        except:
            return None
    
    def rollback(self, filename: str, version_filename: str) -> bool:
        """
        回滚记忆到指定版本
        """
        content = self.get_version_content(version_filename)
        if content is None:
            return False
        
        try:
            # 先保存当前版本
            self.save_version(filename, f"回滚前备份")
            
            # 写入回滚版本
            file_path = self.memory_dir / filename
            file_path.write_text(content, encoding="utf-8")
            
            return True
        except:
            return False
    
    def diff(self, filename: str, version1: str, version2: str) -> Dict:
        """
        对比两个版本的差异
        """
        content1 = self.get_version_content(version1)
        content2 = self.get_version_content(version2)
        
        if content1 is None or content2 is None:
            return {"error": "版本不存在"}
        
        # 简单统计差异
        lines1 = content1.splitlines()
        lines2 = content2.splitlines()
        
        return {
            "filename": filename,
            "version1": version1,
            "version2": version2,
            "lines_added": len(lines2) - len(lines1),
            "chars_added": len(content2) - len(content1),
            "size1": len(content1),
            "size2": len(content2)
        }
    
    def report(self) -> str:
        """生成版本报告"""
        index_files = list(self.versions_dir.glob("*.index.json"))
        
        total_versions = 0
        memories_with_versions = set()
        
        for idx_file in index_files:
            try:
                index = json.loads(idx_file.read_text(encoding="utf-8"))
                for filename, versions in index.items():
                    memories_with_versions.add(filename)
                    total_versions += len(versions)
            except:
                pass
        
        lines = [
            "📜 记忆版本控制报告",
            "=" * 40,
            f"版本化记忆: {len(memories_with_versions)}",
            f"总版本数: {total_versions}",
            "",
        ]
        
        if memories_with_versions:
            lines.append("已版本化的记忆:")
            for mem in sorted(memories_with_versions)[:5]:
                lines.append(f"  • {mem}")
        
        return "\n".join(lines)


if __name__ == "__main__":
    vctrl = MemoryVersion()
    
    # 测试保存版本
    print("=== 保存版本测试 ===")
    test_file = "2026-04-07.md"
    if (vctrl.memory_dir / test_file).exists():
        result = vctrl.save_version(test_file, "测试保存")
        print(f"保存结果: {result}")
    
    print("\n=== 版本报告 ===")
    print(vctrl.report())
    
    print("\n=== 获取版本列表 ===")
    versions = vctrl.get_versions(test_file)
    print(f"版本数: {len(versions)}")
