#!/usr/bin/env python3
"""
记忆系统初始化脚本 - 参考 OpenClaw 初始化模式

用法：
    python3 init_memory.py          # 交互式初始化
    python3 init_memory.py --force  # 强制重新初始化
    python3 init_memory.py --check  # 仅检查状态
    python3 init_memory.py --fix    # 自动修复问题
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# 路径配置
SKILL_DIR = Path(__file__).parent.parent
WORKSPACE = Path.home() / ".openclaw" / "workspace"
MEMORY_DIR = WORKSPACE / "memory"
MEM_DB_DIR = Path.home() / ".openclaw" / "memory-tdai"
CONFIG_DIR = SKILL_DIR / "config"

# 记忆文件模板
MEMORY_MD_TEMPLATE = """# MEMORY.md - 长期核心记忆

> 此文件存储30天+的核心知识、身份认同、重要决策。

---

## 📌 记忆索引

| 标签 | 说明 |
|------|------|
| #用户 | 用户信息、偏好 |
| #技术 | 技术决策、经验 |
| #决策 | 重要决策及理由 |
| #错误 | 错误教训 |

---

## 👤 用户档案

> 从对话中自动更新

- **语言**：中文
- **时区**：Asia/Shanghai

---

## 🏛️ 系统配置

> 配置文件参考 BOOTSTRAP.md

---
"""

DAILY_TEMPLATE = """# {date} 日记

> 每日对话记录，7-30天后自动清理或升级

---

## 📋 今日事项

-

---

## 💬 对话摘要



---

"""

CONFIG_TEMPLATE = {
    "version": "3.9.5",
    "features": {
        "vector_search": True,
        "fts_search": True,
        "auto_backup": False,
        "ima_sync": False,
        "meo_push": True,
    },
    "paths": {
        "memory_dir": str(MEMORY_DIR),
        "memory_db": str(MEM_DB_DIR),
    },
    "limits": {
        "max_memory_items": 200,
        "max_precomputed": 50,
        "cache_ttl_hours": 24,
    }
}


def check_environment():
    """检查环境"""
    print("🔍 检查环境...\n")
    
    checks = []
    
    # Python 版本
    v = sys.version_info[:2]
    checks.append(("Python", v >= (3, 8), f"{v[0]}.{v[1]}"))
    
    # SQLite
    try:
        import sqlite3
        ver = sqlite3.sqlite_version
        checks.append(("SQLite", True, ver))
    except:
        checks.append(("SQLite", False, "N/A"))
    
    # 目录
    checks.append(("记忆目录", MEMORY_DIR.exists(), str(MEMORY_DIR)))
    checks.append(("数据库目录", MEM_DB_DIR.exists(), str(MEM_DB_DIR)))
    checks.append(("配置目录", CONFIG_DIR.exists(), str(CONFIG_DIR)))
    
    # 打印结果
    for name, ok, detail in checks:
        status = "✅" if ok else "❌"
        print(f"  {status} {name}: {detail}")
    
    return all(ok for _, ok, _ in checks)


def create_directories():
    """创建目录结构"""
    print("\n📁 创建目录...\n")
    
    dirs = [
        MEMORY_DIR,
        MEM_DB_DIR,
        MEM_DB_DIR / ".cache" / "embeddings",
        CONFIG_DIR,
    ]
    
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        print(f"  ✅ {d.relative_to(Path.home())}")
    
    print()


def create_config():
    """创建配置文件"""
    print("⚙️ 创建配置...\n")
    
    config_file = CONFIG_DIR / "unified_config.json"
    
    if config_file.exists():
        print(f"  ℹ️  配置文件已存在: {config_file.name}")
        # 合并配置
        try:
            existing = json.loads(config_file.read_text())
            # 更新新配置
            for k, v in CONFIG_TEMPLATE.items():
                if k not in existing:
                    existing[k] = v
            config_file.write_text(json.dumps(existing, indent=2, ensure_ascii=False))
            print(f"  ✅ 配置已更新")
        except:
            config_file.write_text(json.dumps(CONFIG_TEMPLATE, indent=2, ensure_ascii=False))
            print(f"  ✅ 配置已重建")
    else:
        config_file.write_text(json.dumps(CONFIG_TEMPLATE, indent=2, ensure_ascii=False))
        print(f"  ✅ {config_file.name}")


def create_memory_files():
    """创建记忆文件"""
    print("📝 创建记忆文件...\n")
    
    # MEMORY.md
    memory_file = MEMORY_DIR / "MEMORY.md"
    if not memory_file.exists():
        memory_file.write_text(MEMORY_MD_TEMPLATE, encoding="utf-8")
        print(f"  ✅ MEMORY.md")
    else:
        print(f"  ℹ️  MEMORY.md 已存在")
    
    # 今日记忆
    today = datetime.now().strftime("%Y-%m-%d")
    today_file = MEMORY_DIR / f"{today}.md"
    if not today_file.exists():
        content = DAILY_TEMPLATE.format(date=today)
        today_file.write_text(content, encoding="utf-8")
        print(f"  ✅ {today}.md")
    
    # 索引文件
    index_file = MEM_DB_DIR / ".cache" / "index.json"
    if not index_file.exists():
        index_file.parent.mkdir(parents=True, exist_ok=True)
        index_file.write_text(json.dumps({"version": "1.0", "updated": today}))
        print(f"  ✅ index.json")


def initialize_database():
    """初始化数据库"""
    print("🗄️ 初始化数据库...\n")
    
    import sqlite3
    
    db_path = MEM_DB_DIR / "vectors.db"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # 创建表
    tables = [
        """CREATE TABLE IF NOT EXISTS l1_records (
            record_id TEXT PRIMARY KEY,
            content TEXT,
            type TEXT,
            priority INTEGER,
            scene_name TEXT,
            session_key TEXT,
            session_id TEXT,
            timestamp_str TEXT,
            timestamp_start TEXT,
            timestamp_end TEXT,
            created_time TEXT,
            updated_time TEXT,
            metadata_json TEXT
        )""",
        "CREATE INDEX IF NOT EXISTS idx_l1_type ON l1_records(type)",
        "CREATE INDEX IF NOT EXISTS idx_l1_session_key ON l1_records(session_key)",
    ]
    
    for sql in tables:
        cursor.execute(sql)
    
    conn.commit()
    conn.close()
    
    print(f"  ✅ vectors.db 已就绪")
    print(f"     路径: {db_path}")


def run_health_check():
    """运行健康检查"""
    print("\n🏥 运行健康检查...\n")
    
    try:
        import subprocess
        result = subprocess.run(
            [sys.executable, str(SKILL_DIR / "scripts" / "health_check.py")],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print("  ✅ 健康检查通过")
            return True
        else:
            print("  ⚠️  健康检查有警告")
            return False
    except Exception as e:
        print(f"  ⚠️  健康检查失败: {e}")
        return False


def print_summary():
    """打印摘要"""
    print("\n" + "=" * 50)
    print("📊 初始化完成")
    print("=" * 50)
    print()
    print("下一步：")
    print("  1. AI 会自动管理记忆，无需手动操作")
    print("  2. 查看新手教程: cat QUICKSTART.md")
    print("  3. 运行测试: python3 scripts/benchmark.py")
    print()
    print("文档：")
    print("  📖 QUICKSTART.md - 小白入门")
    print("  🔧 ADVANCED.md  - 高级配置")
    print("  📋 FUNCTIONS.md - 功能清单")
    print()


def main():
    parser = argparse.ArgumentParser(description="记忆系统初始化")
    parser.add_argument("--force", "-f", action="store_true", help="强制重新初始化")
    parser.add_argument("--check", "-c", action="store_true", help="仅检查状态")
    parser.add_argument("--fix", action="store_true", help="自动修复问题")
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("🦞 摇摇记忆系统初始化")
    print("=" * 50)
    print()
    
    if args.check:
        check_environment()
        return
    
    if args.fix:
        print("🔧 自动修复模式\n")
        create_directories()
        create_config()
        create_memory_files()
        initialize_database()
        run_health_check()
        print_summary()
        return
    
    # 标准初始化
    print("🚀 开始初始化...\n")
    
    env_ok = check_environment()
    if not env_ok and not args.force:
        print("\n❌ 环境检查失败，请先解决上述问题")
        print("   或使用 --force 强制继续")
        return
    
    create_directories()
    create_config()
    create_memory_files()
    initialize_database()
    run_health_check()
    print_summary()


if __name__ == "__main__":
    main()
