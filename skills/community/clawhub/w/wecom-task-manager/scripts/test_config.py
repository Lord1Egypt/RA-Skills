#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试配置文件加载
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入配置加载函数
import importlib.util
spec = importlib.util.spec_from_file_location("task_manager", "task_manager.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

print("=" * 70)
print("📋 WeCom Task Manager 配置文件测试")
print("=" * 70)
print()

# 测试配置加载
print("📄 加载的配置文件:")
print(f"  路径：{module.Path(__file__).parent.parent / 'config.json'}")
print()

print("⚙️  企业微信配置:")
print(f"  DOCID: {module.DOCID[:50]}...")
print(f"  SHEET_ID: {module.SHEET_ID}")
print()

print("🔐 访问控制配置:")
print(f"  启用：{module.ACCESS_CONTROL_ENABLED}")
print(f"  白名单 agents: {', '.join(module.ALLOWED_AGENTS)}")
print()

print("⚡ 并发控制配置:")
print(f"  最大并发数：{module.MAX_CONCURRENT_TASKS}")
print()

print("🔄 重试配置:")
print(f"  启用：{module.RETRY_ENABLED}")
print(f"  最大重试次数：{module.MAX_RETRIES}")
print(f"  退避时间：{module.BACKOFF_SECONDS}秒")
print()

print("=" * 70)
print("✅ 配置加载测试完成")
print("=" * 70)
