#!/usr/bin/env python3
"""
集成演示 - 小龙虾工作流 v0.2.0 完整功能演示

演示完整的端到端流程：
1. 任务分析
2. 项目创建
3. 步骤分解
4. 步骤执行（带错误分类和恢复）
5. 报告生成
"""

import os
import sys
import json
from pathlib import Path

# 添加脚本目录到路径
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from task_analyzer import TaskAnalyzer
from project_manager import ProjectManager
from step_decomposer import StepDecomposer
from step_executor import StepExecutor
from error_classifier import ErrorClassifier
from template_engine import TemplateEngine


def print_header(text):
    """打印标题"""
    print("\n" + "="*70)
    print(f" {text}")
    print("="*70)


def demo_full_workflow():
    """演示完整工作流"""
    print_header("小龙虾分层任务工作流 v0.2.0 集成演示")
    
    # 测试任务
    test_task = "创建一个个人博客网站，包含文章管理、评论系统和用户认证功能"
    
    print(f"测试任务: {test_task}")
    
    # 1. 任务分析
    print_header("1. 任务分析")
    analyzer = TaskAnalyzer()
    summary = analyzer.analyze(test_task)
    
    print(f"✅ 任务分析完成")
    print(f"   任务ID: {summary.task_id}")
    print(f"   复杂度: {summary.complexity_score}/10")
    print(f"   预计耗时: {summary.estimated_hours} 小时")
    print(f"   需要分层: {'是' if summary.requires_decomposition else '否'}")
    
    # 2. 项目创建
    print_header("2. 项目创建")
    manager = ProjectManager(summary)
    project_dir = manager.create_project()
    
    print(f"✅ 项目创建完成")
    print(f"   项目目录: {project_dir}")
    
    # 显示项目文件
    info = manager.get_project_info()
    print(f"📁 项目文件:")
    for name, path in info['files'].items():
        exists = "✅" if os.path.exists(path) else "❌"
        print(f"   {exists} {name}: {os.path.basename(path)}")
    
    # 3. 步骤分解（如果需要）
    if summary.requires_decomposition:
        print_header("3. 步骤分解")
        decomposer = StepDecomposer()
        phases = decomposer.decompose(summary)
        decomposer.save_decomposition(phases, project_dir)
        
        # 统计信息
        total_phases = len(phases)
        all_steps = []
        executable_steps = []
        for phase in phases:
            all_steps.extend(phase.get_all_descendants())
            executable_steps.extend(phase.get_executable_leaves())
        
        print(f"✅ 步骤分解完成")
        print(f"   创建了 {total_phases} 个阶段")
        print(f"   总步骤数: {len(all_steps) + total_phases}")
        print(f"   可执行步骤: {len(executable_steps)}")
    else:
        print("⏭️  任务不需要分层处理，跳过步骤分解")
        executable_steps = []
    
    # 4. 错误分类器演示
    print_header("4. 错误分类器演示")
    classifier = ErrorClassifier()
    
    # 模拟一些错误
    error_cases = [
        ("请求频率超过限制，请稍后再试", 429),
        ("服务器内部错误", 500),
        ("请求超时，请检查网络连接", None),
        ("输入内容过长，超过限制", None),
    ]
    
    print("错误分类测试:")
    for error_msg, http_code in error_cases:
        error_info = classifier.classify(error_msg, http_code)
        strategies = classifier.get_recovery_strategies(error_info)
        best_strategy = classifier.recommend_strategy(error_info)
        
        print(f"\n  🐛 错误: {error_msg}")
        print(f"    类型: {error_info.error_type.value}")
        print(f"    严重度: {error_info.severity.value}")
        print(f"    推荐策略: {best_strategy.name if best_strategy else '无'}")
        print(f"    成功率: {best_strategy.success_probability if best_strategy else 0}")
    
    # 5. 步骤执行演示（如果可执行步骤）
    print_header("5. 步骤执行演示")
    
    if executable_steps:
        print(f"找到 {len(executable_steps)} 个可执行步骤，执行前3个作为演示...")
        
        executor = StepExecutor()
        loaded_steps = executor.load_steps_from_project(project_dir)
        
        if loaded_steps:
            # 只执行前3个步骤作为演示
            demo_steps = loaded_steps[:3]
            print(f"执行 {len(demo_steps)} 个演示步骤...")
            
            for i, step in enumerate(demo_steps):
                print(f"\n  🔧 步骤 {i+1}: {step.name}")
                print(f"     描述: {step.description[:50]}...")
                print(f"     预计耗时: {step.estimated_hours} 小时")
                
                # 执行步骤（模拟模式）
                result = executor.execute_step(step, project_dir)
                
                if result.success:
                    print(f"     ✅ 执行成功")
                    print(f"     实际耗时: {result.actual_hours:.3f} 小时")
                else:
                    print(f"     ❌ 执行失败")
                    print(f"     错误: {result.error_message}")
                    
                    # 使用错误分类器分析
                    error_info = classifier.classify(
                        result.error_message or "执行失败",
                        context={'input_size': step.expected_input_size}
                    )
                    strategies = classifier.get_recovery_strategies(error_info)
                    
                    if strategies:
                        print(f"     建议恢复策略: {strategies[0].name}")
                        print(f"     成功率: {strategies[0].success_probability}")
            
            # 生成执行报告
            print(f"\n📊 生成执行报告...")
            report = executor.generate_execution_report(project_dir)
            print(f"✅ 执行报告已生成")
        else:
            print("⚠️  没有加载到可执行步骤，跳过执行演示")
    else:
        print("⏭️  没有可执行步骤，跳过执行演示")
    
    # 6. 模板引擎演示
    print_header("6. 模板引擎演示")
    engine = TemplateEngine()
    
    # 创建演示数据
    demo_data = {
        'task_id': summary.task_id,
        'task_name': '个人博客网站开发',
        'task_description': test_task,
        'complexity_score': summary.complexity_score,
        'estimated_hours': summary.estimated_hours,
        'phases': [
            {
                'phase_number': 1,
                'phase_name': '需求分析与设计',
                'phase_goal': '明确需求，设计系统架构',
                'estimated_hours': 8,
                'deliverables': '需求文档、架构图',
                'dependencies': '无'
            },
            {
                'phase_number': 2,
                'phase_name': '核心功能开发',
                'phase_goal': '实现文章管理和用户认证',
                'estimated_hours': 20,
                'deliverables': '功能模块、API接口',
                'dependencies': '阶段1'
            },
            {
                'phase_number': 3,
                'phase_name': '界面与部署',
                'phase_goal': '开发用户界面，部署上线',
                'estimated_hours': 12,
                'deliverables': '网站界面、部署文档',
                'dependencies': '阶段2'
            }
        ],
        'total_hours': 40,
        'phase_count': 3,
        'milestones': '需求确认、核心功能完成、上线发布',
        'risks': [
            {
                'risk_name': '需求变更',
                'risk_description': '客户需求可能中途变更',
                'mitigation': '定期沟通，敏捷开发'
            },
            {
                'risk_name': '技术难点',
                'risk_description': '可能遇到未预见的开发难题',
                'mitigation': '技术预研，预留缓冲时间'
            }
        ],
        'success_criteria': [
            '功能完整，符合需求文档',
            '性能稳定，响应迅速',
            '代码质量高，易于维护',
            '用户界面友好，体验良好'
        ]
    }
    
    # 渲染模板
    rendered = engine.render('top_level_plan', demo_data)
    
    if rendered:
        # 保存演示输出
        demo_output = project_dir / "demo_top_level_plan.md"
        with open(demo_output, 'w', encoding='utf-8') as f:
            f.write(rendered)
        
        print(f"✅ 模板渲染演示完成")
        print(f"   输出文件: {demo_output}")
        
        # 显示模板列表
        templates = engine.get_available_templates()
        print(f"\n📋 可用模板 ({len(templates)} 个):")
        for t in templates:
            print(f"   - {t}")
    else:
        print("⚠️  模板渲染失败，可能模板不存在")
    
    # 7. 总结
    print_header("7. 演示总结")
    print("✅ 小龙虾工作流 v0.2.0 演示完成")
    print(f"\n📁 项目目录: {project_dir}")
    print("📋 包含文件:")
    
    for root, dirs, files in os.walk(project_dir):
        level = root.replace(str(project_dir), '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files[:5]:  # 只显示前5个文件
            print(f"{subindent}{file}")
        if len(files) > 5:
            print(f"{subindent}... 还有 {len(files) - 5} 个文件")
    
    print(f"\n🚀 下一步建议:")
    print("   1. 查看项目文件，了解工作流输出")
    print("   2. 运行完整工作流: python run_workflow.py \"你的任务描述\"")
    print("   3. 启用步骤执行: python run_workflow.py --execute \"你的任务描述\"")
    print("   4. 查看技能文档: cat SKILL.md | head -50")
    
    return {
        'success': True,
        'project_dir': str(project_dir),
        'task_id': summary.task_id,
        'components_tested': ['task_analyzer', 'project_manager', 'step_decomposer', 
                              'step_executor', 'error_classifier', 'template_engine']
    }


if __name__ == "__main__":
    try:
        result = demo_full_workflow()
        if result['success']:
            print("\n🎉 演示成功完成！")
            sys.exit(0)
        else:
            print("\n❌ 演示失败")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ 演示异常: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)