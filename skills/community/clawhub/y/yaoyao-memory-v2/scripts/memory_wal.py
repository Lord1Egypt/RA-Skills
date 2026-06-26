#!/usr/bin/env python3
"""
memory_wal.py - WAL模式管理
SQLite WAL模式优化，提升并发读写性能
"""
import sqlite3
import os
from pathlib import Path


MEMORY_DB = Path.home() / ".openclaw" / "workspace" / "memory" / "memory.db"


def enable_wal_mode():
    """启用WAL模式"""
    if not MEMORY_DB.exists():
        print(f"❌ 数据库不存在: {MEMORY_DB}")
        return False
    
    conn = sqlite3.connect(MEMORY_DB)
    cursor = conn.cursor()
    
    # 检查当前模式
    cursor.execute("PRAGMA journal_mode")
    current_mode = cursor.fetchone()[0]
    
    if current_mode.upper() == "WAL":
        print(f"✅ WAL模式已是启用状态")
        conn.close()
        return True
    
    # 启用WAL
    cursor.execute("PRAGMA journal_mode=WAL")
    new_mode = cursor.fetchone()[0]
    
    # 设置WAL参数
    cursor.execute("PRAGMA synchronous=NORMAL")  # 平衡安全性和性能
    cursor.execute("PRAGMA wal_autocheckpoint=1000")  # 1000页自动检查点
    cursor.execute("PRAGMA cache_size=-64000")  # 64MB缓存
    
    conn.commit()
    conn.close()
    
    if new_mode.upper() == "WAL":
        print(f"✅ WAL模式启用成功!")
        print(f"   旧模式: {current_mode}")
        print(f"   新模式: {new_mode}")
        return True
    else:
        print(f"❌ WAL模式启用失败，当前模式: {new_mode}")
        return False


def disable_wal_mode():
    """禁用WAL模式（切回DELETE模式）"""
    if not MEMORY_DB.exists():
        print(f"❌ 数据库不存在: {MEMORY_DB}")
        return False
    
    conn = sqlite3.connect(MEMORY_DB)
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA journal_mode=DELETE")
    new_mode = cursor.fetchone()[0]
    
    conn.commit()
    conn.close()
    
    if new_mode.upper() == "DELETE":
        print(f"✅ 已切换回DELETE模式")
        return True
    else:
        print(f"❌ 切换失败，当前模式: {new_mode}")
        return False


def get_wal_info():
    """获取WAL状态信息"""
    if not MEMORY_DB.exists():
        return None
    
    conn = sqlite3.connect(MEMORY_DB)
    cursor = conn.cursor()
    
    # 获取模式
    cursor.execute("PRAGMA journal_mode")
    mode = cursor.fetchone()[0]
    
    # 获取数据库大小
    db_size = MEMORY_DB.stat().st_size
    
    # 获取WAL文件大小
    wal_path = MEMORY_DB.with_suffix(".db-wal")
    wal_size = wal_path.stat().st_size if wal_path.exists() else 0
    
    # 获取SHM文件大小
    shm_path = MEMORY_DB.with_suffix(".db-shm")
    shm_size = shm_path.stat().st_size if shm_path.exists() else 0
    
    # 获取页面大小
    cursor.execute("PRAGMA page_size")
    page_size = cursor.fetchone()[0]
    
    # 获取页面数量
    cursor.execute("PRAGMA page_count")
    page_count = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        "mode": mode,
        "db_size": db_size,
        "wal_size": wal_size,
        "shm_size": shm_size,
        "page_size": page_size,
        "page_count": page_count,
        "total_overhead": wal_size + shm_size
    }


def checkpoint():
    """执行检查点，将WAL内容写回主数据库"""
    if not MEMORY_DB.exists():
        print(f"❌ 数据库不存在")
        return False
    
    conn = sqlite3.connect(MEMORY_DB)
    cursor = conn.cursor()
    
    # 执行检查点
    cursor.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    result = cursor.fetchone()
    
    conn.commit()
    conn.close()
    
    # result: (busy, log_pages, marked, checkpointed)
    if result[0] == 0:
        print(f"✅ 检查点执行成功")
        print(f"   写入页数: {result[3]}")
        return True
    else:
        print(f"⚠️ 检查点被延迟执行")
        return False


def main():
    import sys
    
    print("📊 WAL模式管理")
    print("=" * 40)
    
    if len(sys.argv) < 2:
        print("""用法:
    python3 memory_wal.py status    # 查看状态
    python3 memory_wal.py enable    # 启用WAL
    python3 memory_wal.py disable   # 禁用WAL
    python3 memory_wal.py checkpoint# 执行检查点""")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "status":
        info = get_wal_info()
        if info:
            print(f"\n📋 WAL状态:")
            print(f"   模式: {info['mode']}")
            print(f"   数据库大小: {info['db_size'] / 1024 / 1024:.2f} MB")
            print(f"   WAL大小: {info['wal_size'] / 1024 / 1024:.2f} MB")
            print(f"   SHM大小: {info['shm_size'] / 1024 / 1024:.2f} MB")
            print(f"   总开销: {info['total_overhead'] / 1024 / 1024:.2f} MB")
            print(f"   页面大小: {info['page_size']} bytes")
            print(f"   页面数: {info['page_count']}")
    
    elif cmd == "enable":
        enable_wal_mode()
    
    elif cmd == "disable":
        disable_wal_mode()
    
    elif cmd == "checkpoint":
        checkpoint()


if __name__ == "__main__":
    main()
