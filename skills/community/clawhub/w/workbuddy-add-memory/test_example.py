#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
workbuddy-add-memory技能v3.0使用示例
作者: zcg007
日期: 2026-03-15
"""

import sys
import os
from pathlib import Path

# 添加技能目录到Python路径
skill_dir = Path(__file__).parent
sys.path.insert(0, str(skill_dir))

def test_memory_retrieval():
    """测试记忆检索功能"""
    print("🧠 测试记忆检索功能...")
    try:
        from memory_retriever import MemoryRetriever
        
        # 创建记忆检索器
        mr = MemoryRetriever()
        
        # 搜索Excel相关记忆
        results = mr.search("Excel处理", top_k=5)
        print(f"✅ 找到 {len(results)} 条Excel相关记忆")
        
        # 显示前3条
        for i, result in enumerate(results[:3], 1):
            print(f"    {i}. {result.get('title', '无标题')[:40]}... (相关性: {result.get('relevance_score', 0):.3f})")
        
        return True
    except Exception as e:
        print(f"❌ 记忆检索测试失败: {e}")
        return False

def test_task_detection():
    """测试任务检测功能"""
    print("🎯 测试任务检测功能...")
    try:
        from task_detector import TaskDetector
        
        # 创建任务检测器
        td = TaskDetector()
        
        # 测试不同任务类型
        test_cases = [
            "制作Excel预算表",
            "如何安装新的技能",
            "处理尤米教育财务报表",
            "回忆一下之前的经验"
        ]
        
        for task in test_cases:
            result = td.detect_task(task)
            print(f"    '{task}' -> 类型: {result.get('primary_task_type', 'None')}, 置信度: {result.get('confidence', 0):.2f}, 意图: {result.get('intent', 'unknown')}")
        
        return True
    except Exception as e:
        print(f"❌ 任务检测测试失败: {e}")
        return False

def test_conversation_hook():
    """测试对话钩子功能"""
    print("💬 测试对话钩子功能...")
    try:
        from conversation_hook import ConversationHook
        
        # 创建对话钩子
        ch = ConversationHook()
        
        # 测试不同对话
        test_messages = [
            "请帮我制作Excel预算表",
            "我要开始一个新的工作",
            "今天有什么任务",
            "你好"
        ]
        
        for message in test_messages:
            result = ch.process_message(message)
            if result.get("triggered", False):
                print(f"    '{message}' -> 触发类型: {result.get('task_type', 'unknown')}, 置信度: {result.get('confidence', 0):.2f}")
            else:
                print(f"    '{message}' -> 未触发")
        
        return True
    except Exception as e:
        print(f"❌ 对话钩子测试失败: {e}")
        return False

def test_config_loader():
    """测试配置加载功能"""
    print("⚙️  测试配置加载功能...")
    try:
        from config_loader import config_loader
        
        # 获取配置
        config = config_loader.get_retrieval_config()
        
        print(f"✅ 配置加载成功")
        print(f"    最大检索结果: {config.get('max_results', '未设置')}")
        print(f"    最小相关性: {config.get('min_relevance', '未设置')}")
        
        return True
    except Exception as e:
        print(f"❌ 配置加载测试失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("workbuddy-add-memory技能v3.0使用示例")
    print("作者: zcg007")
    print("=" * 60)
    print()
    
    # 运行所有测试
    tests = [
        ("配置加载", test_config_loader),
        ("任务检测", test_task_detection),
        ("对话钩子", test_conversation_hook),
        ("记忆检索", test_memory_retrieval),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}测试通过")
            else:
                print(f"❌ {test_name}测试失败")
        except Exception as e:
            print(f"❌ {test_name}测试异常: {e}")
        print()
    
    # 测试结果
    print("=" * 60)
    print(f"测试完成: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！workbuddy-add-memory v3.0 运行正常")
        print()
        print("使用方法:")
        print("  1. 命令行: python start_work.py \"任务描述\"")
        print("  2. 交互式: python start_work.py --interactive")
        print("  3. 检查状态: python start_work.py --status")
    else:
        print("⚠️ 部分测试失败，请检查技能安装和环境配置")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)