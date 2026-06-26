#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工作启动脚本 v3.0
作者: zcg007
日期: 2026-03-15

开始新工作前自动回忆相关记忆，提供智能建议
"""

import os
import sys
import argparse
import json
from pathlib import Path
from datetime import datetime
import logging

# 添加技能目录到Python路径
skill_dir = Path(__file__).parent
sys.path.insert(0, str(skill_dir))

# 导入技能模块
try:
    from work_preparation import WorkPreparation, prepare_for_work
    from config_loader import config_loader
    from task_detector import task_detector
    from memory_retriever import memory_retriever
    from conversation_hook import conversation_hook
except ImportError as e:
    print(f"导入技能模块失败: {e}")
    print("请确保所有依赖模块都已正确安装")
    sys.exit(1)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(skill_dir / 'workbuddy_add_memory.log')
    ]
)

logger = logging.getLogger(__name__)


def print_banner() -> None:
    """打印启动横幅"""
    banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║               WorkBuddy智能记忆管理系统 v3.0             ║
    ║                   作者: zcg007                           ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_section(title: str) -> None:
    """打印章节标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def format_memory_result(memory: dict, index: int) -> str:
    """格式化记忆结果"""
    title = memory.get('title', '无标题')
    relevance = memory.get('relevance_score', 0)
    category = memory.get('category', 'general')
    importance = memory.get('importance', 'normal')
    
    # 格式化内容预览
    content = memory.get('content', '')[:200]
    if len(memory.get('content', '')) > 200:
        content += "..."
    
    formatted = [
        f"{index}. {title}",
        f"   相关性: {relevance:.3f} | 类别: {category} | 重要性: {importance}",
        f"   {content}",
        ""
    ]
    
    return "\n".join(formatted)


def format_task_analysis(analysis: dict) -> str:
    """格式化任务分析"""
    formatted = [
        f"任务类型: {analysis.get('primary_task_type', '未知')}",
        f"置信度: {analysis.get('confidence', 0):.2f}",
        f"复杂度: {analysis.get('complexity', '未知')}",
        f"预估时间: {analysis.get('estimated_time', {}).get('estimated_range', '未知')}",
        f"意图: {analysis.get('intent', '未知')}",
    ]
    
    return " | ".join(formatted)


def format_work_plan(plan: dict) -> str:
    """格式化工作计划"""
    formatted = []
    
    # 工作阶段
    if plan.get('phases'):
        formatted.append("工作阶段:")
        for i, phase in enumerate(plan['phases'], 1):
            formatted.append(f"  {i}. {phase.get('name')}: {phase.get('description')}")
    
    # 建议操作
    if plan.get('suggested_actions'):
        formatted.append("\n建议操作:")
        for i, action in enumerate(plan['suggested_actions'][:5], 1):
            formatted.append(f"  {i}. {action}")
    
    return "\n".join(formatted)


def start_work_interactive() -> None:
    """交互式启动工作"""
    print_banner()
    
    print_section("欢迎使用WorkBuddy智能记忆管理系统")
    print("请描述您要开始的工作任务:")
    print("（例如：制作Excel预算表、安装新技能、分析工作流程等）")
    print("\n输入 'quit' 或 'exit' 退出")
    print("-" * 40)
    
    while True:
        try:
            task_input = input("\n📝 任务描述: ").strip()
            
            if task_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 再见！祝您工作顺利！")
                break
            
            if not task_input:
                print("⚠️  请输入任务描述")
                continue
            
            print(f"\n⏳ 正在为您准备: {task_input}")
            
            # 开始工作准备
            result = prepare_for_work(task_input)
            
            # 显示结果
            print_section("任务分析结果")
            print(format_task_analysis(result['task_analysis']))
            
            print_section("相关记忆检索")
            memories = result['memory_results']
            if memories:
                print(f"找到 {len(memories)} 条相关记忆:\n")
                for i, memory in enumerate(memories[:5], 1):
                    print(format_memory_result(memory, i))
            else:
                print("⚠️  未找到相关记忆")
            
            print_section("工作计划建议")
            print(format_work_plan(result['work_plan']))
            
            print_section("准备状态")
            status = result['preparation_status']
            print(f"✅ 记忆库加载: {'完成' if status.get('memory_loaded') else '未完成'}")
            print(f"✅ 索引构建: {'完成' if status.get('index_built') else '未完成'}")
            print(f"✅ 环境检查: {'完成' if status.get('environment_checked') else '未完成'}")
            print(f"✅ 计划生成: {'完成' if status.get('plan_generated') else '未完成'}")
            print(f"⏱️  准备时间: {status.get('elapsed_seconds', 0):.1f}秒")
            
            print_section("输出文件")
            output_files = result.get('output_files', [])
            if output_files:
                for file_path in output_files[:3]:
                    print(f"📄 {file_path}")
            else:
                print("📝 报告已生成在内存中")
            
            # 询问是否继续
            print("\n" + "="*60)
            choice = input("是否开始新任务？ (y/n): ").strip().lower()
            if choice not in ['y', 'yes', '是']:
                print("\n👋 工作准备完成！祝您工作顺利！")
                break
            
            print("\n" + "="*60)
            print("开始新任务...")
            
        except KeyboardInterrupt:
            print("\n\n👋 用户中断，退出程序")
            break
        except Exception as e:
            print(f"\n❌ 发生错误: {e}")
            logger.error(f"交互式工作启动失败: {e}", exc_info=True)
            
            choice = input("是否重试？ (y/n): ").strip().lower()
            if choice not in ['y', 'yes', '是']:
                print("\n👋 退出程序")
                break


def start_work_command_line(task_description: str, workspace_dir: str = None) -> dict:
    """
    命令行启动工作
    
    Args:
        task_description: 任务描述
        workspace_dir: 工作空间目录
        
    Returns:
        准备结果
    """
    print_banner()
    print_section(f"开始工作: {task_description}")
    
    try:
        # 创建工作准备器
        if workspace_dir:
            preparer = WorkPreparation(workspace_dir)
        else:
            preparer = WorkPreparation()
        
        # 开始工作准备
        result = preparer.prepare_for_work(task_description)
        
        # 显示关键信息
        print(f"📊 任务分析: {format_task_analysis(result['task_analysis'])}")
        print(f"📚 相关记忆: {len(result['memory_results'])}条")
        print(f"📅 工作阶段: {len(result['work_plan']['phases'])}个")
        print(f"💡 建议操作: {len(result['work_plan']['suggested_actions'])}条")
        print(f"⏱️  准备时间: {result['preparation_status']['elapsed_seconds']:.1f}秒")
        
        # 显示输出文件
        output_files = result.get('output_files', [])
        if output_files:
            print(f"📄 输出文件: {len(output_files)}个")
            for file_path in output_files[:2]:
                print(f"   - {file_path}")
        
        print_section("工作准备完成")
        print("✅ 现在可以开始工作了！")
        
        return result
        
    except Exception as e:
        print(f"❌ 工作准备失败: {e}")
        logger.error(f"命令行工作启动失败: {e}", exc_info=True)
        return {"error": str(e)}


def check_system_status() -> dict:
    """检查系统状态"""
    print_section("系统状态检查")
    
    status = {
        "skill_directory": str(skill_dir),
        "python_version": sys.version,
        "modules_loaded": False,
        "memory_sources": [],
        "config_loaded": False,
    }
    
    try:
        # 检查模块加载
        status["modules_loaded"] = all([
            'config_loader' in sys.modules,
            'task_detector' in sys.modules,
            'memory_retriever' in sys.modules,
            'work_preparation' in sys.modules,
        ])
        
        # 检查配置
        try:
            config = config_loader.load_config()
            status["config_loaded"] = True
            status["memory_sources"] = config.get("memory_sources", [])
        except Exception as e:
            status["config_error"] = str(e)
        
        # 显示状态
        print(f"📁 技能目录: {status['skill_directory']}")
        print(f"🐍 Python版本: {status['python_version'].split()[0]}")
        print(f"📦 模块加载: {'✅ 成功' if status['modules_loaded'] else '❌ 失败'}")
        print(f"⚙️  配置加载: {'✅ 成功' if status['config_loaded'] else '❌ 失败'}")
        
        if status["memory_sources"]:
            print(f"📚 记忆源: {len(status['memory_sources'])}个")
            for source in status["memory_sources"][:3]:
                print(f"   - {source}")
        
        return status
        
    except Exception as e:
        print(f"❌ 系统状态检查失败: {e}")
        return {"error": str(e)}


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="WorkBuddy智能记忆管理系统 - 工作启动脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  %(prog)s "制作Excel预算表"            # 启动特定工作
  %(prog)s --interactive               # 交互式模式
  %(prog)s --status                    # 检查系统状态
  %(prog)s --workspace /path/to/work   # 指定工作空间
        """
    )
    
    parser.add_argument(
        "task",
        nargs="?",
        help="任务描述（例如：制作Excel预算表）"
    )
    
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="交互式模式"
    )
    
    parser.add_argument(
        "-s", "--status",
        action="store_true",
        help="检查系统状态"
    )
    
    parser.add_argument(
        "-w", "--workspace",
        help="指定工作空间目录"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="输出文件路径（JSON格式）"
    )
    
    args = parser.parse_args()
    
    try:
        # 检查系统状态
        if args.status:
            check_system_status()
            return 0
        
        # 交互式模式
        if args.interactive:
            start_work_interactive()
            return 0
        
        # 命令行模式
        if args.task:
            result = start_work_command_line(args.task, args.workspace)
            
            # 保存输出到文件
            if args.output and result:
                output_path = Path(args.output)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                
                print(f"\n📄 结果已保存到: {output_path}")
            
            return 0 if "error" not in result else 1
        
        # 没有参数时显示帮助
        print_banner()
        parser.print_help()
        print("\n💡 提示: 使用 --interactive 进入交互式模式")
        return 0
        
    except KeyboardInterrupt:
        print("\n\n👋 用户中断，退出程序")
        return 0
    except Exception as e:
        print(f"\n❌ 程序执行失败: {e}")
        logger.error(f"主程序执行失败: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())