#!/usr/bin/env python3
"""
vector_extension_manager.py - 向量扩展管理器

功能：
- 自动检测 sqlite-vec 扩展
- 支持 FTS5 回退
- 向量搜索性能优化
- 扩展健康检查

用法：
    python3 vector_extension_manager.py status    # 查看状态
    python3 vector_extension_manager.py enable   # 启用向量扩展
    python3 vector_extension_manager.py disable  # 禁用向量扩展
    python3 vector_extension_manager.py test     # 测试向量功能
"""

import json
import sqlite3
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class VectorExtensionManager:
    """向量扩展管理器"""
    
    # 扩展搜索路径
    SEARCH_PATHS = [
        Path.home() / ".openclaw" / "extensions" / "memory-tencentdb" / "node_modules" / "sqlite-vec-linux-x64",
        Path.home() / ".openclaw" / "extensions" / "memory-tencentdb" / "node_modules" / "sqlite-vec",
        Path.home() / ".openclaw" / "extensions" / "sqlite-vec",
        Path("/usr/lib"),
        Path("/usr/local/lib"),
    ]
    
    # 扩展候选名称
    EXT_NAMES = ["vec0", "sqlite-vec", "sqlite_vec"]
    
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or (Path.home() / ".openclaw" / "memory-tdai" / "vectors.db")
        self.conn = None
        self.extension_path = None
        self.extension_loaded = False
        self.fts_available = True
    
    def find_extension(self) -> Optional[Path]:
        """查找向量扩展"""
        for search_path in self.SEARCH_PATHS:
            if not search_path.exists():
                continue
            
            for ext_file in search_path.rglob("*"):
                if ext_file.is_file():
                    # 检查是否是共享库
                    if ext_file.suffix in (".so", ".dylib", ".dll"):
                        for name in self.EXT_NAMES:
                            if name in ext_file.stem.lower():
                                return ext_file
        
        return None
    
    def load_extension(self, ext_path: Path) -> bool:
        """加载向量扩展"""
        if not ext_path.exists():
            print(f"   ❌ 扩展文件不存在: {ext_path}")
            return False
        
        try:
            self.conn.enable_load_extension(True)
            self.conn.load_extension(str(ext_path))
            self.extension_loaded = True
            self.extension_path = ext_path
            print(f"   ✅ 成功加载扩展: {ext_path.name}")
            return True
        except Exception as e:
            print(f"   ❌ 加载扩展失败: {e}")
            self.extension_loaded = False
            return False
    
    def check_fts5(self) -> bool:
        """检查 FTS5 支持"""
        try:
            cursor = self.conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='l1_fts'")
            result = cursor.fetchone()
            if result:
                print("   ✅ FTS5 索引已存在")
                return True
            
            # 尝试创建 FTS5 表
            self.conn.execute("CREATE VIRTUAL TABLE IF NOT EXISTS l1_fts USING fts5(content)")
            print("   ✅ FTS5 可用")
            return True
        except Exception as e:
            print(f"   ❌ FTS5 不可用: {e}")
            return False
    
    def check_vector_tables(self) -> Dict[str, int]:
        """检查向量相关表"""
        tables = {}
        try:
            cursor = self.conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
            for row in cursor.fetchall():
                name = row[0]
                if "vec" in name.lower() or "fts" in name.lower():
                    # 统计行数
                    try:
                        count = self.conn.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
                        tables[name] = count
                    except:
                        tables[name] = -1
        except Exception as e:
            print(f"   ❌ 查询表失败: {e}")
        
        return tables
    
    def get_status(self) -> dict:
        """获取状态"""
        status = {
            "extension_path": str(self.extension_path) if self.extension_path else None,
            "extension_loaded": self.extension_loaded,
            "fts_available": self.fts_available,
            "tables": {},
        }
        
        if self.conn:
            status["tables"] = self.check_vector_tables()
        
        return status
    
    def connect(self) -> bool:
        """连接数据库"""
        try:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            self.conn = sqlite3.connect(str(self.db_path))
            self.conn.row_factory = sqlite3.Row
            print(f"   ✅ 连接数据库: {self.db_path}")
            return True
        except Exception as e:
            print(f"   ❌ 数据库连接失败: {e}")
            return False
    
    def close(self):
        """关闭连接"""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def enable(self) -> bool:
        """启用向量扩展"""
        print("🚀 启用向量扩展...\n")
        
        # 连接数据库
        if not self.connect():
            return False
        
        # 查找扩展
        ext_path = self.find_extension()
        if ext_path:
            print(f"📦 找到扩展: {ext_path}")
            if self.load_extension(ext_path):
                return True
        
        # 回退到 FTS5
        print("\n⚠️  向量扩展不可用，使用 FTS5 回退")
        return self.check_fts5()
    
    def disable(self):
        """禁用向量扩展"""
        print("📦 禁用向量扩展（使用纯 FTS5）...")
        if self.connect():
            self.check_fts5()
    
    def test_vector_search(self, limit: int = 10) -> Tuple[bool, float]:
        """测试向量搜索性能"""
        if not self.conn:
            self.connect()
        
        print(f"\n🧪 测试向量搜索（前 {limit} 条）...")
        
        try:
            # 测试 FTS5 搜索
            start = time.time()
            cursor = self.conn.execute(
                "SELECT record_id, content FROM l1_fts ORDER BY rank LIMIT ?",
                (limit,)
            )
            results = cursor.fetchall()
            elapsed = (time.time() - start) * 1000  # ms
            
            print(f"   FTS5 搜索: {len(results)} 条结果, 耗时 {elapsed:.2f}ms")
            return True, elapsed
        except Exception as e:
            print(f"   ❌ FTS5 搜索失败: {e}")
            return False, 0
    
    def benchmark(self) -> dict:
        """性能基准测试"""
        print("\n📊 向量系统性能基准测试\n")
        
        if not self.connect():
            return {}
        
        # 获取状态
        status = self.get_status()
        
        # 统计
        print("📈 表统计:")
        for table, count in status["tables"].items():
            print(f"   {table}: {count} 条")
        
        print()
        
        # 搜索测试
        success, elapsed = self.test_vector_search(100)
        
        # 总结
        print("\n" + "=" * 40)
        print("📋 基准测试总结:")
        print(f"   向量扩展: {'✅ 已加载' if self.extension_loaded else '❌ 未加载'}")
        print(f"   FTS5: {'✅ 可用' if self.fts_available else '❌ 不可用'}")
        print(f"   搜索延迟: {elapsed:.2f}ms")
        print("=" * 40)
        
        return {
            "extension_loaded": self.extension_loaded,
            "fts_available": self.fts_available,
            "search_latency_ms": elapsed,
            "tables": status["tables"],
        }
    
    def status(self) -> dict:
        """查看状态"""
        print("\n📊 向量扩展状态\n")
        
        if not self.connect():
            return {}
        
        # 扩展检查
        print("🔍 扩展检查:")
        ext_path = self.find_extension()
        if ext_path:
            print(f"   ✅ 找到扩展: {ext_path}")
        else:
            print("   ❌ 未找到向量扩展")
        
        if self.extension_loaded:
            print(f"   ✅ 已加载: {self.extension_path}")
        else:
            print("   ℹ️  未加载（使用 FTS5）")
        
        # FTS5 检查
        print("\n🔍 FTS5 检查:")
        if self.check_fts5():
            print("   ✅ FTS5 可用")
        else:
            print("   ❌ FTS5 不可用")
        
        # 表统计
        print("\n📈 数据统计:")
        tables = self.check_vector_tables()
        if tables:
            for table, count in tables.items():
                print(f"   {table}: {count} 条")
        else:
            print("   ℹ️  无数据")
        
        return self.get_status()


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="向量扩展管理器")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # status 命令
    subparsers.add_parser("status", help="查看状态")
    
    # enable 命令
    subparsers.add_parser("enable", help="启用向量扩展")
    
    # disable 命令
    subparsers.add_parser("disable", help="禁用向量扩展")
    
    # test 命令
    subparsers.add_parser("test", help="测试向量功能")
    
    # benchmark 命令
    subparsers.add_parser("benchmark", help="性能基准测试")
    
    # find 命令
    subparsers.add_parser("find", help="查找扩展文件")
    
    args = parser.parse_args()
    
    manager = VectorExtensionManager()
    
    if args.command == "status":
        manager.status()
    elif args.command == "enable":
        manager.enable()
    elif args.command == "disable":
        manager.disable()
    elif args.command == "test":
        manager.connect()
        manager.test_vector_search()
    elif args.command == "benchmark":
        manager.benchmark()
    elif args.command == "find":
        ext_path = manager.find_extension()
        if ext_path:
            print(f"✅ 找到扩展: {ext_path}")
            print(f"   大小: {ext_path.stat().st_size / 1024:.1f} KB")
        else:
            print("❌ 未找到扩展")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
