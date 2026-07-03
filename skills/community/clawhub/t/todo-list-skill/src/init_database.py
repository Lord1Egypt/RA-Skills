#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""数据库初始化脚本（独立可执行）。

本模块提供一次性脚本用于初始化 SQLite 数据库。脚本是幂等的（可安全
多次运行），并通过插入和删除一条验证数据来执行自检。

使用方式：
    $ python3 -m src.init_database
    $ python3 src/init_database.py
    $ ./src/init_database.py  # 需可执行权限

技术决策：
    - 幂等：可多次运行，schema 加 IF NOT EXISTS
    - 自检：插入 + 删除一条数据验证数据库可用
    - 友好输出：每步打印进度（✅ / [info] 等）

参见：
    - SOUL.md 规则 15（数据源统一原则）
    - DESIGN.md §6.2（部署步骤）
    - schema/init_todos.sql（原始 schema）

License:
    MIT

Version:
    1.4.0

Author:
    月海巫师 (Chen Qing)
"""
from __future__ import annotations  # PEP 563：延后求值类型注解

import sys
from pathlib import Path

# 添加父目录到 path（方便直接运行）
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.store import TodosStore


def main():
    """初始化 todos 数据库"""
    print("🚀 初始化 todos 数据库...")
    print(f"   数据库路径: {Path(__file__).parent.parent / 'todos.db'}")

    store = TodosStore()
    store.init_db()

    # 验证：插入一条测试数据
    print("\n📋 验证：插入测试 TODO...")
    todo = store.add(
        content="数据库初始化验证",
        priority="low",
        source="init",
        raw_input=None,
    )
    print(f"   ✅ 创建成功：ID={todo['id']}, content={todo['content']}")

    # 清理测试数据
    store.delete(str(todo["id"]))
    print("   🧹 测试数据已清理")

    print("\n✅ 数据库初始化完成")
    print("   版本：v1.0")
    print("   表：todos / todos_archive / audit_log")


if __name__ == "__main__":
    main()