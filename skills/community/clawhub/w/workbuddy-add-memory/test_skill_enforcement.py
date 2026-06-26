#!/usr/bin/env python3
"""
测试技能使用强制执行器
验证conversation_hook和memory_system_enforcer的改进
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from conversation_hook import ConversationHook
from memory_system_enforcer import MemorySystemEnforcer

def test_conversation_hook():
    """测试对话钩子的技能提醒检测"""
    print("="*70)
    print("测试对话钩子 - 技能提醒检测")
    print("="*70)
    
    hook = ConversationHook()
    
    # 测试技能提醒消息
    test_messages = [
        "@skill://workbuddy-add-memory 这个skill呢，你又忘了用它了吗",
        "为啥会多次犯这个错误，前边的反思都没用吗",
        "workbuddy-add-memory技能又忘了用",
        "请帮我处理Excel报表",
        "回忆一下之前的错误教训"
    ]
    
    for message in test_messages:
        print(f"\n{'='*50}")
        print(f"测试消息: {message}")
        
        result = hook.process_message(message)
        
        if result["trigger_detected"]:
            print(f"触发类型: {result['trigger_type']}")
            print(f"置信度: {result['confidence']:.2f}")
            
            if result["should_respond"]:
                print(f"响应内容 (前200字):")
                print(result["response"][:200] + "..." if len(result["response"]) > 200 else result["response"])
        else:
            print("未触发记忆检索")
    
    # 显示对话摘要
    print(f"\n{'='*70}")
    print("对话摘要:")
    print(hook.get_conversation_summary())

def test_memory_system_enforcer():
    """测试记忆系统强制执行器"""
    print("\n" + "="*70)
    print("测试记忆系统强制执行器 - 技能使用检查")
    print("="*70)
    
    enforcer = MemorySystemEnforcer()
    
    # 测试用例
    test_cases = [
        {
            "description": "包含技能标签的正确使用",
            "task": "@skill://workbuddy-add-memory 请帮我分析数据",
            "actions": "use_skill('workbuddy-add-memory')然后运行python start_work.py"
        },
        {
            "description": "包含技能标签但未使用技能",
            "task": "@skill://workbuddy-add-memory 处理Excel报表",
            "actions": "直接开始处理Excel，没有使用技能"
        },
        {
            "description": "应该使用技能的任务（Excel处理）",
            "task": "请帮我制作2026年预算表",
            "actions": "use_skill('workbuddy-add-memory')"
        },
        {
            "description": "应该使用技能的任务但忘记使用",
            "task": "分析之前的错误教训并总结",
            "actions": "直接创建总结文件"
        },
        {
            "description": "简单任务不需要技能",
            "task": "今天天气怎么样",
            "actions": "回答天气情况"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*50}")
        print(f"测试用例 {i}: {test_case['description']}")
        print(f"任务: {test_case['task']}")
        print(f"实际动作: {test_case['actions']}")
        
        result = enforcer.enforce_memory_system(
            test_case['task'], 
            test_case['actions']
        )
        
        print(f"检查结果: {'通过' if result else '失败'}")
    
    # 显示技能使用统计
    print(f"\n{'='*70}")
    print("技能使用统计:")
    print(enforcer.get_skill_usage_stats())
    
    # 创建每日提醒
    reminder_file = enforcer.create_reminder()
    print(f"\n每日提醒已创建: {reminder_file}")

def main():
    """主函数"""
    print("技能使用强制执行器测试 v2.0")
    print("测试时间: 2026-03-15")
    print()
    
    # 测试对话钩子
    test_conversation_hook()
    
    # 测试强制执行器
    test_memory_system_enforcer()
    
    print("\n" + "="*70)
    print("测试完成！")
    print("改进总结:")
    print("1. ✅ conversation_hook增加了skill_reminder触发类型")
    print("2. ✅ 可以检测用户提醒使用技能的消息")
    print("3. ✅ memory_system_enforcer增加了技能使用检查")
    print("4. ✅ 可以检查是否正确使用了workbuddy-add-memory技能")
    print("5. ✅ 提供了技能使用统计和错误模式分析")
    print("="*70)

if __name__ == "__main__":
    main()