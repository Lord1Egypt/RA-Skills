#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WorkBuddy智能记忆管理系统使用示例
作者: zcg007
日期: 2026-03-15
"""

import sys
from pathlib import Path

# 添加技能目录到Python路径
skill_dir = Path(__file__).parent.parent
sys.path.insert(0, str(skill_dir))

# 导入技能模块
from config_loader import config_loader
from task_detector import task_detector
from memory_retriever import memory_retriever
from conversation_hook import conversation_hook
from work_preparation import WorkPreparation, prepare_for_work


def example_config_loader():
    """配置加载器示例"""
    print("=" * 60)
    print("示例 1: 配置加载器")
    print("=" * 60)
    
    # 加载配置
    config = config_loader.load_config()
    
    print(f"✅ 配置加载成功")
    print(f"   记忆源数量: {len(config.get('memory_sources', []))}")
    print(f"   最大检索结果: {config.get('retrieval_config', {}).get('max_results')}")
    print(f"   最小相关性阈值: {config.get('retrieval_config', {}).get('min_relevance')}")
    
    # 获取特定配置
    memory_sources = config_loader.get_memory_sources()
    retrieval_config = config_loader.get_retrieval_config()
    
    print(f"\n📚 记忆源:")
    for source in memory_sources[:3]:
        print(f"   - {source}")
    
    print(f"\n🔍 检索配置:")
    for key, value in retrieval_config.items():
        print(f"   - {key}: {value}")


def example_task_detector():
    """任务检测器示例"""
    print("\n" + "=" * 60)
    print("示例 2: 任务检测器")
    print("=" * 60)
    
    test_messages = [
        "请帮我制作一个Excel预算表",
        "如何安装新的技能？",
        "我遇到了Excel处理错误",
        "回忆一下之前的记忆管理经验",
    ]
    
    for message in test_messages:
        print(f"\n📝 输入: {message}")
        
        result = task_detector.detect_task(message)
        
        print(f"   🎯 主要任务: {result.get('primary_task')}")
        print(f"   📊 置信度: {result.get('confidence'):.2f}")
        print(f"   🎯 意图: {result.get('intent')}")
        
        keywords = [k['keyword'] for k in result.get('keywords_found', [])]
        if keywords:
            print(f"   🔑 关键词: {keywords}")
        
        suggestions = result.get('suggested_actions', [])
        if suggestions:
            print(f"   💡 建议: {suggestions[0]}")


def example_memory_retriever():
    """记忆检索器示例"""
    print("\n" + "=" * 60)
    print("示例 3: 记忆检索器")
    print("=" * 60)
    
    # 加载记忆库
    memory_sources = config_loader.get_memory_sources()
    memory_retriever.load_memories(memory_sources)
    memory_retriever.build_index()
    
    test_queries = [
        "Excel处理",
        "技能安装",
        "记忆管理",
    ]
    
    for query in test_queries:
        print(f"\n🔍 查询: {query}")
        
        memories = memory_retriever.search(query, top_k=3)
        
        if memories:
            print(f"   ✅ 找到 {len(memories)} 条相关记忆:")
            for i, memory in enumerate(memories, 1):
                title = memory.get('title', '无标题')
                relevance = memory.get('relevance_score', 0)
                category = memory.get('category', 'general')
                
                print(f"      {i}. {title}")
                print(f"          相关性: {relevance:.3f}, 类别: {category}")
        else:
            print(f"   ⚠️  未找到相关记忆")


def example_conversation_hook():
    """对话钩子示例"""
    print("\n" + "=" * 60)
    print("示例 4: 对话钩子")
    print("=" * 60)
    
    test_messages = [
        "请帮我制作一个Excel预算表",
        "我遇到了问题，怎么办？",
        "回忆一下之前的经验",
    ]
    
    for message in test_messages:
        print(f"\n💬 用户消息: {message}")
        
        result = conversation_hook.process_message(message)
        
        if result['trigger_detected']:
            print(f"   ✅ 触发类型: {result['trigger_type']}")
            print(f"   📊 置信度: {result['confidence']:.2f}")
            print(f"   📚 检索到记忆: {len(result['memories_retrieved'])}条")
            
            if result['should_respond']:
                # 显示响应预览
                response = result['response']
                if len(response) > 200:
                    response = response[:197] + "..."
                print(f"   💡 响应预览: {response[:100]}...")
        else:
            print(f"   ⚠️  未触发记忆检索")


def example_work_preparation():
    """工作准备示例"""
    print("\n" + "=" * 60)
    print("示例 5: 工作准备")
    print("=" * 60)
    
    test_tasks = [
        "制作Excel预算表",
        "安装新技能",
    ]
    
    for task in test_tasks:
        print(f"\n🚀 开始工作: {task}")
        
        result = prepare_for_work(task)
        
        if "error" in result:
            print(f"   ❌ 错误: {result['error']}")
            continue
        
        analysis = result['task_analysis']
        memories = result['memory_results']
        plan = result['work_plan']
        
        print(f"   📊 任务分析:")
        print(f"      类型: {analysis.get('primary_task_type')}")
        print(f"      复杂度: {analysis.get('complexity')}")
        print(f"      预估时间: {analysis.get('estimated_time', {}).get('estimated_range')}")
        
        print(f"   📚 相关记忆: {len(memories)}条")
        
        print(f"   📅 工作计划:")
        print(f"      阶段: {len(plan.get('phases', []))}个")
        print(f"      建议操作: {len(plan.get('suggested_actions', []))}条")
        
        status = result['preparation_status']
        print(f"   ⏱️  准备时间: {status.get('elapsed_seconds', 0):.1f}秒")


def example_start_work_script():
    """启动脚本示例"""
    print("\n" + "=" * 60)
    print("示例 6: 启动脚本使用")
    print("=" * 60)
    
    print("命令行使用:")
    print("  python start_work.py \"制作Excel预算表\"")
    print("  python start_work.py --interactive")
    print("  python start_work.py --status")
    print("  python start_work.py --workspace /path/to/work \"分析数据\"")
    
    print("\n交互式模式:")
    print("  1. 运行: python start_work.py --interactive")
    print("  2. 输入任务描述")
    print("  3. 系统自动分析任务、检索记忆、生成计划")
    print("  4. 查看准备结果和建议")
    
    print("\n输出文件:")
    print("  - 工作准备报告 (.md格式)")
    print("  - 准备数据 (.json格式)")
    print("  - 系统日志 (.log格式)")


def main():
    """主函数"""
    print("WorkBuddy智能记忆管理系统 v3.0 - 使用示例")
    print("作者: zcg007")
    print("=" * 60)
    
    try:
        # 运行所有示例
        example_config_loader()
        example_task_detector()
        example_memory_retriever()
        example_conversation_hook()
        example_work_preparation()
        example_start_work_script()
        
        print("\n" + "=" * 60)
        print("✅ 所有示例运行完成！")
        print("=" * 60)
        
        print("\n💡 提示:")
        print("  1. 使用 start_work.py 开始新工作")
        print("  2. 所有配置可在 config/ 目录中自定义")
        print("  3. 记忆源可在配置文件中添加")
        print("  4. 详细文档请参考 SKILL.md")
        
    except Exception as e:
        print(f"\n❌ 示例运行失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()