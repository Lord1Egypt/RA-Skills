#!/usr/bin/env python3
"""
safe_extension_loader.py - 安全的 SQLite 扩展加载器

功能：
- SHA256 哈希验证扩展文件完整性
- 用户确认机制
- 扩展文件路径自动发现
- 回退到纯 Python 实现

用法：
    from safe_extension_loader import safe_load_extension
    conn = safe_load_extension(sqlite_conn, "vec0")
"""

import hashlib
import os
import sqlite3
import sys
from pathlib import Path
from typing import Optional, List, Tuple

# 信任的扩展哈希表（生产环境应使用硬编码哈希）
TRUSTED_EXTENSIONS = {
    "vec0": {
        "linux-x64": "sha256:754b46a02b3caba9b1c75aeaeb8f8177a61f527b531151f7de5324ba4c10d444",
    },
    "sqlite-vec": {
        "linux-x64": "sha256:754b46a02b3caba9b1c75aeaeb8f8177a61f527b531151f7de5324ba4c10d444",  # vec0.so v0.1.0
    }
}

# 扩展搜索路径
EXTENSION_SEARCH_PATHS = [
    Path.home() / ".openclaw" / "extensions" / "memory-tencentdb" / "node_modules" / "sqlite-vec-linux-x64",
    Path.home() / ".openclaw" / "extensions" / "memory-tencentdb" / "node_modules" / "sqlite-vec",
    Path("/usr/lib"),
    Path("/usr/local/lib"),
    Path.home() / ".local" / "lib",
]


class SafeExtensionLoader:
    """安全的扩展加载器"""
    
    def __init__(self, interactive: bool = True):
        self.interactive = interactive
        self.loaded_extensions = {}
        self.failed_extensions = {}
    
    def find_extension(self, ext_name: str) -> Optional[Path]:
        """查找扩展文件路径"""
        # 可能的扩展文件名
        possible_names = [
            ext_name,
            f"lib{ext_name}.so",
            f"{ext_name}.dylib",
            f"{ext_name}.dll",
            f"vec0.so",  # sqlite-vec 的常见文件名
        ]
        
        for search_path in EXTENSION_SEARCH_PATHS:
            if not search_path.exists():
                continue
            
            # 递归搜索
            for ext_file in search_path.rglob("*"):
                if ext_file.is_file():
                    for name in possible_names:
                        if ext_file.name == name or ext_file.stem == name:
                            return ext_file
        
        return None
    
    def compute_sha256(self, file_path: Path) -> str:
        """计算文件的 SHA256 哈希"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
    
    def verify_extension(self, ext_path: Path, ext_name: str) -> Tuple[bool, str]:
        """验证扩展文件的完整性"""
        if not ext_path.exists():
            return False, f"扩展文件不存在: {ext_path}"
        
        # 计算实际哈希
        actual_hash = self.compute_sha256(ext_path)
        hash_str = f"sha256:{actual_hash}"
        
        # 检查是否在信任列表中
        if ext_name in TRUSTED_EXTENSIONS:
            trusted = TRUSTED_EXTENSIONS[ext_name]
            for platform, trusted_hash in trusted.items():
                if trusted_hash == hash_str:
                    return True, "验证通过（信任列表）"
            
            # 哈希不匹配
            return False, f"哈希不匹配！期望: {list(trusted.values())}, 实际: {hash_str}"
        
        # 不在信任列表中，需要用户确认
        if self.interactive:
            return self._interactive_verify(ext_path, ext_name, hash_str)
        
        return False, "扩展不在信任列表中（非交互模式）"
    
    def _interactive_verify(self, ext_path: Path, ext_name: str, hash_str: str) -> Tuple[bool, str]:
        """交互式验证扩展"""
        print(f"\n⚠️ 安全警告：扩展 '{ext_name}' 不在信任列表中")
        print(f"   文件: {ext_path}")
        print(f"   哈希: {hash_str}")
        print(f"   大小: {ext_path.stat().st_size / 1024:.1f} KB")
        
        # 检查文件权限
        mode = ext_path.stat().st_mode
        if mode & 0o100:  # 任何人都可执行
            print(f"   ⚠️ 警告：文件具有执行权限！")
        
        response = input("\n是否信任此扩展并加载？（输入 'yes' 确认）：").strip().lower()
        
        if response in ("yes", "y", "是", "确认"):
            return True, "用户确认信任"
        
        return False, "用户拒绝加载"
    
    def load(self, conn: sqlite3.Connection, ext_name: str, 
             enable_foreign_keys: bool = True) -> Tuple[bool, str]:
        """
        安全加载扩展
        
        Args:
            conn: SQLite 连接
            ext_name: 扩展名（如 "vec0", "sqlite-vec"）
            enable_foreign_keys: 是否启用外键约束
        
        Returns:
            (成功标志, 消息)
        """
        # 如果已加载，直接返回
        if ext_name in self.loaded_extensions:
            return True, f"扩展已加载: {ext_name}"
        
        # 查找扩展
        ext_path = self.find_extension(ext_name)
        if not ext_path:
            # 回退到纯 Python 实现
            return False, f"未找到扩展 '{ext_name}'，使用纯 Python 回退"
        
        # 验证扩展
        verified, msg = self.verify_extension(ext_path, ext_name)
        if not verified:
            self.failed_extensions[ext_name] = msg
            return False, f"扩展验证失败: {msg}"
        
        # 启用扩展加载
        conn.enable_load_extension(True)
        
        try:
            conn.load_extension(str(ext_path))
            self.loaded_extensions[ext_name] = ext_path
            return True, f"成功加载: {ext_path}"
        except Exception as e:
            self.failed_extensions[ext_name] = str(e)
            return False, f"加载失败: {e}"
    
    def get_status(self) -> dict:
        """获取加载状态"""
        return {
            "loaded": list(self.loaded_extensions.keys()),
            "failed": self.failed_extensions,
        }


def safe_load_extension(conn: sqlite3.Connection, ext_name: str) -> Tuple[bool, str]:
    """
    便捷函数：安全加载扩展
    
    用法：
        success, msg = safe_load_extension(conn, "vec0")
    """
    loader = SafeExtensionLoader(interactive=False)
    return loader.load(conn, ext_name)


# CLI 入口
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="安全的 SQLite 扩展加载器")
    parser.add_argument("--check", "-c", help="检查扩展是否存在", metavar="NAME")
    parser.add_argument("--verify", "-v", help="验证扩展哈希", metavar="PATH")
    parser.add_argument("--list", "-l", action="store_true", help="列出所有可用扩展")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互式模式")
    
    args = parser.parse_args()
    
    loader = SafeExtensionLoader(interactive=args.interactive)
    
    if args.check:
        ext_path = loader.find_extension(args.check)
        if ext_path:
            print(f"✅ 找到扩展: {ext_path}")
            verified, msg = loader.verify_extension(ext_path, args.check)
            print(f"   验证: {msg}")
        else:
            print(f"❌ 未找到扩展: {args.check}")
    
    elif args.verify:
        ext_path = Path(args.verify)
        if ext_path.exists():
            verified, msg = loader.verify_extension(ext_path, "manual")
            print(f"验证: {msg}")
            print(f"哈希: sha256:{loader.compute_sha256(ext_path)}")
        else:
            print(f"❌ 文件不存在: {ext_path}")
    
    elif args.list:
        print("🔍 搜索可用扩展...\n")
        found = []
        for search_path in EXTENSION_SEARCH_PATHS:
            if search_path.exists():
                print(f"📁 搜索: {search_path}")
                for ext_file in search_path.rglob("*.so"):
                    found.append(ext_file)
                    print(f"   ✅ {ext_file.relative_to(search_path)}")
        
        if not found:
            print("❌ 未找到任何扩展")
        else:
            print(f"\n📊 共找到 {len(found)} 个扩展文件")
    
    else:
        parser.print_help()
