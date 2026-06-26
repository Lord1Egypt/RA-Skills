#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能编程助手 - 使用示例

演示如何使用智能编程助手技能完成各种编程任务
"""

import sys
import os

# 添加脚本目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

from model_router import route_task, TaskType


def demo_task_routing():
    """演示任务路由功能"""
    print("\n" + "="*70)
    print("智能编程助手 - 任务路由演示")
    print("="*70 + "\n")
    
    test_cases = [
        "用 Python 写一个快速排序算法",
        "审查这段代码的安全隐患",
        "这个函数为什么返回空值？帮我调试一下",
        "优化这个数据库查询的性能",
        "重构这个模块，提高可维护性",
        "为这个类生成单元测试",
        "解释一下 React 的虚拟 DOM 原理",
        "给这个 API 写文档",
        "设计一个支持百万并发的消息队列系统",
        "这段代码是什么意思？"
    ]
    
    for i, task in enumerate(test_cases, 1):
        print(f"\n[任务 {i}/{len(test_cases)}]")
        print(f"任务：{task}")
        print("-" * 70)
        
        result = route_task(task, verbose=False)
        
        print(f"任务类型：{result['task_type']}")
        print(f"置信度：{result['confidence']:.2f}")
        print(f"推荐模型：{result['recommended_model']}")
        print(f"协作模式：{'是' if result['collaboration_mode'] else '否'}")
        
        if result['collaboration_mode']:
            print(f"   工作流程：{' -> '.join(result['collaboration_plan'])}")
        
        print(f"模型特点：{result['model_profile']['special_notes']}")
    
    print("\n" + "="*70)
    print("演示完成")
    print("="*70 + "\n")


def demo_model_comparison():
    """演示模型对比"""
    from model_router import MODEL_PROFILES
    
    print("\n" + "="*70)
    print("模型能力对比")
    print("="*70 + "\n")
    
    print(f"{'模型':<20} {'速度':<8} {'质量':<8} {'成本':<8} {'优势场景':<30}")
    print("-" * 70)
    
    for name, profile in MODEL_PROFILES.items():
        strengths = ", ".join([s.value.split('_')[0] for s in profile.strengths[:2]])
        print(f"{name:<20} {profile.speed:<8} {profile.quality:<8} {profile.cost:<8} {strengths:<30}")
    
    print("\n")


def demo_collaboration_workflow():
    """演示协作工作流"""
    print("\n" + "="*70)
    print("多模型协作工作流演示")
    print("="*70 + "\n")
    
    task = "重构这个用户管理模块，并添加完整的单元测试"
    
    print(f"任务：{task}\n")
    
    result = route_task(task, verbose=False)
    
    print("路由决策:")
    print(f"   任务类型：{result['task_type']}")
    print(f"   协作模式：{'启用' if result['collaboration_mode'] else '禁用'}")
    
    if result['collaboration_mode']:
        print(f"\n协作流程:\n")
        
        workflow_steps = {
            1: ("架构分析", "分析当前代码结构，识别问题"),
            2: ("重构设计", "设计重构方案，应用设计模式"),
            3: ("代码实现", "实施重构，优化代码结构"),
            4: ("测试生成", "生成单元测试，覆盖边界情况"),
            5: ("最终审查", "审查代码质量，提出改进建议")
        }
        
        for i, model in enumerate(result['collaboration_plan'], 1):
            step_name, step_desc = workflow_steps.get(i, ("处理", "执行任务"))
            print(f"   步骤{i}: {model}")
            print(f"           {step_name} - {step_desc}")
            print()
    
    print("预估成本：0.50-1.00 元")
    print("预估时间：10-15 分钟")
    print("\n")


def demo_best_practices():
    """演示最佳实践"""
    print("\n" + "="*70)
    print("最佳实践建议")
    print("="*70 + "\n")
    
    practices = [
        ("推荐做法", [
            "任务拆分：大任务拆成小步骤",
            "明确约束：给出技术栈、性能要求",
            "迭代优化：生成 -> 优化 -> 审查",
            "质量优先：重要代码必须审查",
            "记录反馈：持续优化路由策略"
        ]),
        ("避免做法", [
            "模糊描述：'写个代码'",
            "一步到位：复杂任务期望一次成功",
            "忽略审查：重要代码直接上线",
            "单一模型：所有任务用同一个模型",
            "不记录反馈：重复犯同样的错误"
        ]),
        ("成本优化", [
            "简单任务用 qwen-turbo（节省 60-80%）",
            "启用代码缓存（节省 30-50%）",
            "批量处理任务（节省 20-40%）",
            "合理选择模型（节省 40-60%）"
        ])
    ]
    
    for title, items in practices:
        print(f"[{title}]")
        for item in items:
            print(f"   {item}")
        print()


def main():
    """主函数"""
    print("\n" + "="*70)
    print("  智能编程助手技能 - 使用示例")
    print("="*70 + "\n")
    
    # 演示任务路由
    demo_task_routing()
    
    # 演示模型对比
    demo_model_comparison()
    
    # 演示协作工作流
    demo_collaboration_workflow()
    
    # 演示最佳实践
    demo_best_practices()
    
    print("\n" + "="*70)
    print("更多信息请查看:")
    print("   - SKILL.md: 技能主文档")
    print("   - references/model-profiles.md: 模型能力画像")
    print("   - references/task-taxonomy.md: 任务分类体系")
    print("   - references/best-practices.md: 最佳实践案例")
    print("   - README.md: 完整使用指南")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
