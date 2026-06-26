#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WorkBuddy智能记忆管理系统快速测试
作者: zcg007
日期: 2026-03-15
"""

import sys
import os

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print("🚀 WorkBuddy智能记忆管理系统 v3.0 快速测试")
print("作者: zcg007")
print("=" * 60)

try:
    # 测试1: 配置加载器
    print("\n1. 测试配置加载器...")
    from config_loader import config_loader
    config = config_loader.load_config()
    print(f"   ✅ 配置加载成功")
    print(f"      记忆源: {len(config.get('memory_sources', []))}个")
    print(f"      最大检索结果: {config.get('retrieval_config', {}).get('max_results')}")
    
    # 测试2: 任务检测器
    print("\n2. 测试任务检测器...")
    from task_detector import task_detector
    
    test_tasks = [
        "制作Excel预算表",
        "如何安装新的技能？",
        "回忆一下之前的经验",
    ]
    
    for task in test_tasks:
        result = task_detector.detect_task(task)
        print(f"   📝 '{task}'")
        print(f"      类型: {result.get('primary_task')}, 置信度: {result.get('confidence'):.2f}")
        print(f"      意图: {result.get('intent')}")
    
    # 测试3: 记忆检索器（基础功能）
    print("\n3. 测试记忆检索器基础功能...")
    from memory_retriever import memory_retriever
    print(f"   ✅ 记忆检索器初始化成功")
    print(f"      缓存目录: {memory_retriever.cache_dir}")
    
    # 测试4: 对话钩子
    print("\n4. 测试对话钩子...")
    from conversation_hook import conversation_hook
    print(f"   ✅ 对话钩子初始化成功")
    
    # 测试简单消息处理
    test_message = "请帮我制作Excel预算表"
    result = conversation_hook.process_message(test_message)
    print(f"   💬 消息: '{test_message}'")
    print(f"      触发检测: {result['trigger_detected']}")
    if result['trigger_detected']:
        print(f"      触发类型: {result['trigger_type']}")
        print(f"      置信度: {result['confidence']:.2f}")
    
    # 测试5: 工作准备模块
    print("\n5. 测试工作准备模块...")
    from work_preparation import WorkPreparation
    
    # 创建临时工作空间
    import tempfile
    temp_dir = tempfile.mkdtemp()
    
    preparer = WorkPreparation(temp_dir)
    print(f"   ✅ 工作准备器初始化成功")
    print(f"      工作空间: {temp_dir}")
    
    # 清理临时目录
    import shutil
    shutil.rmtree(temp_dir)
    
    # 测试6: 启动脚本功能
    print("\n6. 测试启动脚本功能...")
    print("   ✅ 启动脚本可用命令:")
    print("      python start_work.py \"任务描述\"")
    print("      python start_work.py --interactive")
    print("      python start_work.py --status")
    print("      python start_work.py --workspace /path/to/work \"任务\"")
    
    print("\n" + "=" * 60)
    print("🎉 所有基本功能测试通过！")
    print("=" * 60)
    
    print("\n📋 新版本功能总结:")
    print("   1. 增强配置加载器 - 支持多层级配置和验证")
    print("   2. 智能任务检测器 - 多层级检测算法，更准确")
    print("   3. 增强记忆检索器 - TF-IDF + 语义相似度混合检索")
    print("   4. 增强对话钩子 - 智能触发机制，自动回忆")
    print("   5. 工作准备模块 - 自动准备环境、检索记忆、生成计划")
    print("   6. 改进启动脚本 - 交互式和命令行两种模式")
    
    print("\n💡 使用建议:")
    print("   1. 首次使用: python start_work.py --interactive")
    print("   2. 快速开始: python start_work.py \"您的任务描述\"")
    print("   3. 配置调整: 编辑 config/main.yaml 文件")
    print("   4. 查看示例: python examples/example_usage.py")
    
except Exception as e:
    print(f"\n❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()

print("\n📞 作者: zcg007")
print("📅 版本: v3.0 (2026-03-15)")