#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 wecom-task-manager 技能的所有 Python API
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 设置环境变量
os.environ["AGENT_ID"] = "da-yan"

from task_manager import (
    get_all_tasks,
    get_task_by_id,
    search_tasks,
    filter_tasks,
    get_statistics,
    check_due_tasks,
    check_overdue_tasks,
    get_in_progress_count
)

print("=" * 70)
print("🧪 WeCom Task Manager Python API 测试")
print("=" * 70)
print()

# 测试 1：获取所有任务
print("【测试 1】get_all_tasks()")
print("-" * 70)
tasks = get_all_tasks("da-yan")
print(f"✅ 获取到 {len(tasks)} 个任务")
print()

# 测试 2：查询单个任务
print("【测试 2】get_task_by_id('TASK-001')")
print("-" * 70)
task = get_task_by_id("TASK-001", "da-yan")
if task:
    print(f"✅ 找到任务：{task['values']['任务 ID'][0]['text']}")
    print(f"   名称：{task['values']['任务名称'][0]['text']}")
    print(f"   状态：{task['values']['状态'][0]['text']}")
else:
    print("❌ 未找到任务")
print()

# 测试 3：搜索任务
print("【测试 3】search_tasks('系统')")
print("-" * 70)
results = search_tasks("系统")
print(f"✅ 搜索到 {len(results)} 个任务")
print()

# 测试 4：过滤任务
print("【测试 4】filter_tasks(status='进行中', priority='P0')")
print("-" * 70)
results = filter_tasks(status="进行中", priority="P0")
print(f"✅ 过滤到 {len(results)} 个任务")
print()

# 测试 5：获取统计数据
print("【测试 5】get_statistics()")
print("-" * 70)
stats = get_statistics()
print(f"总任务数：{stats['总任务数']}")
print(f"已完成：{stats['已完成']}")
print(f"进行中：{stats['进行中']}")
print(f"按时完成率：{stats['按时完成率']}")
print()

# 测试 6：检查到期任务
print("【测试 6】check_due_tasks(days=7)")
print("-" * 70)
due_tasks = check_due_tasks(days=7)
print(f"✅ 找到 {len(due_tasks)} 个即将到期的任务")
print()

# 测试 7：检查超期任务
print("【测试 7】check_overdue_tasks()")
print("-" * 70)
overdue_tasks = check_overdue_tasks()
print(f"✅ 找到 {len(overdue_tasks)} 个超期任务")
print()

# 测试 8：获取进行中任务数
print("【测试 8】get_in_progress_count()")
print("-" * 70)
count = get_in_progress_count()
print(f"✅ 进行中任务数：{count}")
print()

print("=" * 70)
print("✅ 所有 Python API 测试完成")
print("=" * 70)
