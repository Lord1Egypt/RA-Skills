#!/usr/bin/env python3
"""
小龙虾工作流 MVP 演示脚本

这是一个最小可行版本的演示，展示完整工作流程：
1. 任务分析 → 2. 项目创建 → 3. 文档生成
"""

import os
import sys
import argparse
from pathlib import Path

# 添加脚本路径
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from task_analyzer import TaskAnalyzer
from project_manager import ProjectManager
from step_decomposer import StepDecomposer
from step_executor import StepExecutor
from error_classifier import ErrorClassifier
from template_engine import TemplateEngine
from email_sender import EmailSender
from backup_manager import BackupManager


def print_banner():
    """打印横幅"""
    banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║        小龙虾分层任务工作流 MVP v0.1.0 演示              ║
    ║        Xiaolongxia Hierarchical Task Workflow           ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(banner)


def run_workflow(task_description: str, config_path: str = None, execute: bool = False):
    """
    运行完整工作流
    
    Args:
        task_description: 任务描述
        config_path: 配置文件路径
    """
    print("🚀 开始小龙虾工作流...")
    print(f"任务描述: {task_description[:100]}...")
    
    # 步骤1: 任务分析
    print("\n" + "="*60)
    print("步骤1: 任务分析")
    print("="*60)
    
    analyzer = TaskAnalyzer(config_path)
    summary = analyzer.analyze(task_description)
    
    print(f"✅ 任务分析完成")
    print(f"   任务ID: {summary.task_id}")
    print(f"   复杂度: {summary.complexity_score}/10")
    print(f"   预计耗时: {summary.estimated_hours} 小时")
    print(f"   需要分层: {'是' if summary.requires_decomposition else '否'}")
    
    # 步骤2: 项目创建
    print("\n" + "="*60)
    print("步骤2: 项目创建")
    print("="*60)
    
    manager = ProjectManager(summary, config_path)
    project_dir = manager.create_project()
    
    print(f"✅ 项目创建完成")
    print(f"   项目目录: {project_dir}")
    
    # 步骤3: 显示项目信息
    print("\n" + "="*60)
    print("步骤3: 项目信息")
    print("="*60)
    
    info = manager.get_project_info()
    
    print(f"📁 项目文件:")
    for name, path in info['files'].items():
        exists = "✅" if os.path.exists(path) else "❌"
        print(f"   {exists} {name}: {os.path.basename(path)}")
    
    # 步骤4: 步骤分解
    print("\n" + "="*60)
    print("步骤4: 步骤分解")
    print("="*60)
    
    if summary.requires_decomposition:
        print("任务需要分层处理，开始步骤分解...")
        decomposer = StepDecomposer(config_path)
        phases = decomposer.decompose(summary)
        
        # 保存分解结果
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
        
        # 更新项目信息
        info['files']['decomposition_summary'] = str(project_dir / "steps" / "decomposition_summary.md")
    else:
        print("任务不需要分层处理，跳过步骤分解")
    
    # 步骤5: 步骤执行
    print("\n" + "="*60)
    print("步骤5: 步骤执行")
    print("="*60)
    
    if summary.requires_decomposition and executable_steps:
        if execute:
            print("开始执行步骤（模拟模式）...")
            executor = StepExecutor(config_path)
            # 加载可执行步骤
            loaded_steps = executor.load_steps_from_project(project_dir)
            
            if loaded_steps:
                print(f"加载了 {len(loaded_steps)} 个可执行步骤")
                results = executor.execute_steps(loaded_steps, project_dir)
                
                # 生成报告
                report = executor.generate_execution_report(project_dir)
                
                print(f"✅ 步骤执行完成")
                print(f"   执行步骤: {len(results)}")
                print(f"   成功步骤: {sum(1 for r in results.values() if r.success)}")
                print(f"   失败步骤: {sum(1 for r in results.values() if not r.success)}")
                
                # 更新项目信息
                info['files']['execution_report'] = str(project_dir / "execution_report.md")
            else:
                print("⚠️  没有加载到可执行步骤")
        else:
            print("跳过步骤执行（未启用 --execute 标志）")
            print("提示: 使用 --execute 参数启用步骤执行")
    else:
        if not summary.requires_decomposition:
            print("任务不需要分层处理，跳过步骤执行")
        elif not executable_steps:
            print("没有可执行步骤，跳过步骤执行")
    
    # 显示建议
    print("\n" + "="*60)
    print("执行建议")
    print("="*60)
    
    if summary.complexity_score >= 7:
        print("📋 建议采用完整分层工作流:")
        print("   1. 阅读 top_level_plan.md 了解阶段划分")
        print("   2. 细化每个阶段的详细步骤")
        print("   3. 按照计划逐步执行")
    elif summary.complexity_score >= 4:
        print("📋 建议采用简化分层流程:")
        print("   1. 阅读 top_level_plan.md 了解主要步骤")
        print("   2. 为每个步骤制定详细计划")
        print("   3. 按顺序执行")
    else:
        print("📋 建议直接执行:")
        print("   1. 理解任务要求")
        print("   2. 直接调用API或执行命令")
        print("   3. 检查结果质量")
    
    # 显示下一步操作
    print("\n" + "="*60)
    print("下一步操作")
    print("="*60)
    print(f"1. 查看任务概要: cat '{project_dir}/task_summary.md' | head -20")
    print(f"2. 查看顶层方案: cat '{project_dir}/top_level_plan.md' | head -30")
    print(f"3. 查看项目配置: cat '{project_dir}/project_config.json'")
    print(f"4. 进入项目目录: cd '{project_dir}'")
    
    return {
        'success': True,
        'task_id': summary.task_id,
        'project_dir': str(project_dir),
        'complexity': summary.complexity_score,
        'requires_decomposition': summary.requires_decomposition,
        'files': info['files']
    }


def test_workflow():
    """测试工作流"""
    print("🧪 运行测试工作流...")
    
    test_tasks = [
        "设计一个简单的用户登录系统，包含前端界面和后端API",
        "分析当前股票市场趋势，生成投资建议报告",
        "编写一个Python脚本，自动备份指定目录到云存储"
    ]
    
    for i, task in enumerate(test_tasks):
        print(f"\n{'#'*60}")
        print(f"测试 {i+1}: {task[:50]}...")
        
        try:
            result = run_workflow(task, execute=False)
            if result['success']:
                print(f"✅ 测试 {i+1} 成功")
            else:
                print(f"❌ 测试 {i+1} 失败")
        except Exception as e:
            print(f"❌ 测试 {i+1} 异常: {e}")
    
    print(f"\n{'#'*60}")
    print("测试完成")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='小龙虾分层任务工作流 MVP')
    parser.add_argument('task', nargs='?', help='任务描述')
    parser.add_argument('--config', '-c', help='配置文件路径')
    parser.add_argument('--test', '-t', action='store_true', help='运行测试')
    parser.add_argument('--interactive', '-i', action='store_true', help='交互模式')
    parser.add_argument('--execute', '-e', action='store_true', help='启用步骤执行')
    
    args = parser.parse_args()
    
    print_banner()
    
    if args.test:
        test_workflow()
        return
    
    if args.interactive:
        print("💬 交互模式")
        print("请输入您的任务描述（输入空行结束）:")
        
        lines = []
        while True:
            line = input("> ")
            if not line.strip():
                break
            lines.append(line)
        
        task_description = '\n'.join(lines)
        
        if not task_description.strip():
            print("❌ 任务描述不能为空")
            return
    elif args.task:
        task_description = args.task
    else:
        parser.print_help()
        print("\n示例:")
        print("  python run_workflow.py \"设计一个电商网站后端系统\"")
        print("  python run_workflow.py --test")
        print("  python run_workflow.py --interactive")
        return
    
    try:
        result = run_workflow(task_description, args.config, execute=args.execute)
        
        print("\n" + "="*60)
        print("🎉 工作流执行完成！")
        print("="*60)
        print(f"任务ID: {result['task_id']}")
        print(f"项目目录: {result['project_dir']}")
        print(f"复杂度: {result['complexity']}/10")
        print(f"\n下一步: 进入项目目录开始详细规划")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  用户中断")
    except Exception as e:
        print(f"\n❌ 工作流执行失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()