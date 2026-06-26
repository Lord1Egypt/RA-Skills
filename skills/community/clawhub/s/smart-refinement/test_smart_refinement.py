"""
Smart Refinement System 测试脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from smart_refinement_system import SmartRefinementSystem, refine_prompt, match_skills


def test_basic_functionality():
    """测试基本功能"""
    print("=" * 60)
    print("Smart Refinement System 基本功能测试")
    print("=" * 60)
    
    # 初始化系统
    system = SmartRefinementSystem()
    
    # 测试用例
    test_cases = [
        {
            "message": "Help me process that file",
            "context": {"active_project": "data-processing", "last_operation": "created CSV file"},
            "description": "模糊文件处理请求"
        },
        {
            "message": "Write a Python script to analyze data",
            "context": {"programming_language": "Python", "data_source": "CSV files"},
            "description": "明确的代码生成请求"
        },
        {
            "message": "搜索AI行业趋势信息",
            "context": {"language": "zh", "topic": "人工智能"},
            "description": "中文搜索请求"
        },
        {
            "message": "Analyze sales data and generate report",
            "context": {"data_type": "sales", "report_format": "PDF"},
            "description": "数据分析与报告生成"
        },
        {
            "message": "Setup monitoring for the server",
            "context": {"server_type": "Linux", "monitoring_tool": "Prometheus"},
            "description": "系统操作请求"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'─' * 40}")
        print(f"测试用例 #{i}: {test_case['description']}")
        print(f"{'─' * 40}")
        
        # 处理消息
        result = system.process_message(
            test_case["message"], 
            test_case["context"]
        )
        
        # 显示结果
        print(f"原始消息: {test_case['message']}")
        print(f"需要优化: {result['needs_refinement']}")
        print(f"优化置信度: {result['refinement_confidence']:.1%}")
        print(f"意图类型: {result['intent']['intent_type']}")
        print(f"处理时间: {result['processing_time_ms']:.2f} ms")
        
        # 显示技能匹配
        if result['skill_matches']:
            print(f"\n技能匹配 (前3个):")
            for match in result['skill_matches'][:3]:
                print(f"  - {match['skill_type']}: {match['match_score']:.1%}")
        
        # 显示建议动作
        if result['suggested_actions']:
            print(f"\n建议动作:")
            for j, action in enumerate(result['suggested_actions'][:3], 1):
                print(f"  {j}. {action}")
        
        # 显示优化后的提示（如果需要）
        if result['needs_refinement']:
            print(f"\n优化后提示:")
            print("-" * 40)
            print(result['refined_prompt'][:200] + "..." if len(result['refined_prompt']) > 200 else result['refined_prompt'])
            print("-" * 40)


def test_simplified_api():
    """测试简化API"""
    print("\n" + "=" * 60)
    print("简化API测试")
    print("=" * 60)
    
    # 测试 refine_prompt
    test_messages = [
        "帮我处理那个文件",
        "Write code for data processing",
        "Check system status"
    ]
    
    for i, msg in enumerate(test_messages, 1):
        print(f"\n测试 #{i}: {msg}")
        refined = refine_prompt(msg)
        print(f"优化结果: {refined[:100]}..." if len(refined) > 100 else f"优化结果: {refined}")
    
    # 测试 match_skills
    print(f"\n{'─' * 40}")
    print("技能匹配测试")
    print(f"{'─' * 40}")
    
    skill_test_messages = [
        "Create a web scraper in Python",
        "Read data from file and analyze",
        "Search for latest news"
    ]
    
    for i, msg in enumerate(skill_test_messages, 1):
        print(f"\n消息 #{i}: {msg}")
        skills = match_skills(msg)
        if skills:
            for skill in skills[:2]:
                print(f"  - {skill['skill_type']} ({skill['match_score']:.1%})")


def test_performance():
    """性能测试"""
    print("\n" + "=" * 60)
    print("性能测试")
    print("=" * 60)
    
    system = SmartRefinementSystem()
    
    # 测试消息
    test_message = "Process data and generate report with charts"
    
    # 预热
    for _ in range(10):
        system.process_message(test_message)
    
    # 正式测试
    import time
    iterations = 100
    start_time = time.time()
    
    for _ in range(iterations):
        system.process_message(test_message)
    
    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / iterations * 1000  # 转换为毫秒
    
    print(f"迭代次数: {iterations}")
    print(f"总时间: {total_time:.3f} 秒")
    print(f"平均时间: {avg_time:.3f} ms")
    print(f"吞吐量: {iterations / total_time:.0f} 次/秒")
    
    # 显示统计信息
    stats = system.get_stats()
    print(f"\n系统统计:")
    print(f"  优化次数: {stats['refinements']}")
    print(f"  向量匹配次数: {stats['vector_matches']}")
    print(f"  平均处理时间: {stats['avg_processing_time']:.2f} ms")


def test_integration():
    """集成测试"""
    print("\n" + "=" * 60)
    print("集成功能测试")
    print("=" * 60)
    
    system = SmartRefinementSystem()
    
    # 测试上下文集成
    print("测试上下文集成:")
    context = {
        "project": "数据分析平台",
        "user": "屠哥",
        "last_tasks": ["数据清洗", "特征工程"],
        "current_phase": "模型训练"
    }
    
    result = system.process_message("继续下一步", context)
    print(f"集成上下文: {result.get('integrated_context', {})}")
    
    # 测试配置保存
    print(f"\n测试配置管理:")
    config_path = "./test_config.json"
    system.save_config(config_path)
    
    if os.path.exists(config_path):
        print(f"配置已保存到: {config_path}")
        
        # 测试从配置初始化
        system2 = SmartRefinementSystem(config_path)
        print("从配置文件初始化成功")
        
        # 清理测试文件
        os.remove(config_path)
        print("测试配置文件已清理")
    
    # 测试数据导出
    print(f"\n测试数据导出:")
    skill_data = system.export_skill_data()
    print(f"导出数据包含: {len(skill_data.get('skills_database', {}))} 个技能")
    print(f"系统版本: {skill_data.get('version')}")
    print(f"时间戳: {skill_data.get('timestamp')}")


def main():
    """主测试函数"""
    print("Smart Refinement System 综合测试")
    print("=" * 60)
    
    try:
        # 运行所有测试
        test_basic_functionality()
        test_simplified_api()
        test_performance()
        test_integration()
        
        print("\n" + "=" * 60)
        print("所有测试完成!")
        print("=" * 60)
        
        # 显示最终统计
        system = SmartRefinementSystem()
        stats = system.get_stats()
        print(f"\n最终系统统计:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
            
    except Exception as e:
        print(f"\n测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)