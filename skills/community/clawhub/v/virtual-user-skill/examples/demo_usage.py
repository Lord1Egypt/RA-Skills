#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
虚拟用户 Skill 使用示例

展示如何在不同场景下使用虚拟用户技能
"""

import sys
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from main import VirtualUserSkill


def example_1_basic_usage():
    """示例 1：基本用法"""
    print("\n" + "=" * 60)
    print("示例 1: 基本用法 - 自动生成虚拟用户并对话")
    print("=" * 60)
    
    skill = VirtualUserSkill()
    
    # 运行技能（自动选择前 3 个用户类型）
    result = skill.run(
        "用户预订机票时最关心什么？",
        auto_select=True
    )
    
    print(f"\n✅ 执行完成")
    print(f"   生成用户类型：{len(result['user_types'])} 个")
    print(f"   对话轮数：{result['conversation_summary']['conversation_count']} 轮")


def example_2_custom_selection():
    """示例 2：自定义选择用户类型"""
    print("\n" + "=" * 60)
    print("示例 2: 自定义选择 - 手动选择特定用户类型")
    print("=" * 60)
    
    skill = VirtualUserSkill()
    
    # 阶段 1：生成用户类型
    scenarios = skill.search_engine.search("用户预订机票", top_k=20)
    user_types = skill.user_generator.generate_user_types(scenarios, top_n=10)
    
    print(skill.user_generator.format_user_list())
    
    # 阶段 2：用户选择（模拟）
    print("\n模拟用户选择：选择 1,3,5")
    skill.user_generator.select_all(selected=False)
    skill.user_generator.toggle_selection(1, True)
    skill.user_generator.toggle_selection(3, True)
    skill.user_generator.toggle_selection(5, True)
    
    selected_users = skill.user_generator.get_selected_users()
    print(f"✅ 已选择 {len(selected_users)} 个用户类型")
    
    # 阶段 3：对话
    skill.conversation_manager.start_session(selected_users)
    
    for i, user in enumerate(selected_users):
        skill.conversation_manager.set_current_user(i)
        response = skill.conversation_manager.generate_user_response(
            "你觉得在线预订机票方便吗？"
        )
        print(f"\n{user['type_name']}:")
        print(f"  回复：{response['response']}")


def example_3_product_evaluation():
    """示例 3：产品方案测评"""
    print("\n" + "=" * 60)
    print("示例 3: 产品测评 - 评估新的退改签方案")
    print("=" * 60)
    
    skill = VirtualUserSkill()
    
    # 生成虚拟用户
    result = skill.run(
        "评估新的机票退改签方案：起飞前 24 小时免费退改",
        auto_select=True
    )
    
    # 导出报告
    report_file = Path(__file__).parent.parent / "outputs" / "product_evaluation_report.md"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    
    skill.conversation_manager.export_report(str(report_file))
    print(f"\n📄 报告已保存：{report_file}")


def example_4_batch_interview():
    """示例 4：批量访谈"""
    print("\n" + "=" * 60)
    print("示例 4: 批量访谈 - 多个问题连续访谈")
    print("=" * 60)
    
    questions = [
        "用户选择机票时最看重什么？",
        "退改签流程有哪些痛点？",
        "对会员权益有什么期待？",
        "如何提升用户忠诚度？"
    ]
    
    all_results = []
    
    for i, question in enumerate(questions, 1):
        print(f"\n[{i}/{len(questions)}] 问题：{question}")
        
        skill = VirtualUserSkill()
        result = skill.run(question, auto_select=True)
        all_results.append(result)
    
    print(f"\n✅ 批量访谈完成，共 {len(all_results)} 个问题")


def main():
    """运行所有示例"""
    print("🎭 虚拟用户 Skill 使用示例")
    print("=" * 60)
    
    # 选择要运行的示例
    examples = {
        '1': example_1_basic_usage,
        '2': example_2_custom_selection,
        '3': example_3_product_evaluation,
        '4': example_4_batch_interview
    }
    
    print("\n可用示例：")
    for key, func in examples.items():
        print(f"  {key}. {func.__doc__.strip()}")
    
    choice = input("\n选择示例 (1-4，或回车运行全部): ").strip()
    
    if choice in examples:
        examples[choice]()
    else:
        # 运行全部
        for func in examples.values():
            try:
                func()
            except Exception as e:
                print(f"\n❌ 示例执行失败：{e}")
                print("   请确保已正确安装依赖并准备数据文件")


if __name__ == "__main__":
    main()
