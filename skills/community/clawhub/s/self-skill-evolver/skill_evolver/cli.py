#!/usr/bin/env python3
"""
Skill Evolver CLI

命令行接口，用于查看技能分析报告、健康度评分等
"""

import sys
import argparse
import json
from typing import Optional
from pathlib import Path

# 添加父目录到路径以便导入
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.models import Database
from skill_evolver.monitor import SkillMonitor, log_skill_usage
from skill_evolver.analyzer import SkillAnalyzer
from skill_evolver.reporter import SkillReporter


def cmd_analyze(args):
    """分析技能代码"""
    analyzer = SkillAnalyzer(args.skills_dir)
    
    if args.all:
        print("正在分析所有技能...\n")
        results = analyzer.analyze_all_skills()
        
        for result in results:
            print_skill_analysis(result, args.verbose)
    else:
        result = analyzer.analyze_skill(args.skill)
        print_skill_analysis(result, args.verbose)


def print_skill_analysis(result, verbose: bool = False):
    """打印技能分析结果"""
    status_emoji = "✅" if result.score >= 80 else "⚠️" if result.score >= 60 else "❌"
    
    print(f"\n{status_emoji} {result.skill_name}")
    print(f"   评分：{result.score}/100")
    
    if result.exists:
        print(f"   路径：{result.skill_path}")
    else:
        print(f"   状态：目录不存在")
        return
    
    if result.issues:
        print(f"   问题：{len(result.issues)} 个")
        if verbose:
            for issue in result.issues[:5]:  # 只显示前 5 个
                severity_icon = {"critical": "🔴", "warning": "🟡", "info": "ℹ️"}.get(issue.severity, "⚪")
                print(f"      {severity_icon} [{issue.category}] {issue.message}")
            if len(result.issues) > 5:
                print(f"      ... 还有 {len(result.issues) - 5} 个问题")
    
    if result.suggestions:
        print(f"   建议：")
        for suggestion in result.suggestions[:3]:
            print(f"      • {suggestion}")


def cmd_report(args):
    """生成健康度报告"""
    db = Database()
    reporter = SkillReporter(db, args.skills_dir)
    
    if args.all:
        print("正在生成所有技能的报告...\n")
        report = reporter.generate_full_report()
        
        # 打印摘要
        summary = report["summary"]
        print(f"📊 技能健康度总览")
        print(f"   技能总数：{summary['total_skills']}")
        print(f"   健康：{summary['healthy_skills']} 🟢")
        print(f"   警告：{summary['warning_skills']} 🟡")
        print(f"   严重：{summary['critical_skills']} 🔴")
        print(f"   平均评分：{summary['average_score']}/100")
        print(f"   总调用次数：{summary['total_usage']}")
        
        if args.output:
            reporter.export_report(report, args.output, args.format)
            print(f"\n报告已导出到：{args.output}")
    
    else:
        report = reporter.generate_health_report(args.skill)
        
        status_emoji = {"healthy": "🟢", "warning": "🟡", "critical": "🔴"}.get(report["status"], "⚪")
        
        print(f"\n{status_emoji} {report['skill_name']} 健康度报告")
        print(f"   总体评分：{report['overall_score']}/100")
        print(f"   状态：{report['status']}")
        print()
        print("   详细评分:")
        print(f"      可靠性：{report['scores']['reliability']}/100")
        print(f"      性能：{report['scores']['performance']}/100")
        print(f"      代码质量：{report['scores']['code_quality']}/100")
        print(f"      用户满意度：{report['scores']['user_satisfaction']}/100")
        print()
        print("   使用情况 (过去 30 天):")
        print(f"      总调用：{report['usage']['total_calls']}")
        print(f"      成功率：{report['usage']['success_rate']}%")
        print(f"      平均耗时：{report['usage']['avg_duration_ms']}ms")
        print()
        print("   改进建议:")
        for i, rec in enumerate(report["recommendations"][:5], 1):
            print(f"      {i}. {rec}")
        
        if args.output:
            reporter.export_report(report, args.output, args.format)
            print(f"\n报告已导出到：{args.output}")


def cmd_log(args):
    """记录技能使用"""
    db = Database()
    
    if args.list:
        skills = db.get_all_skills()
        print("已记录的技能:")
        for skill in skills:
            print(f"  - {skill}")
        return
    
    log_skill_usage(
        skill_name=args.skill,
        action=args.action,
        status=args.status,
        duration_ms=args.duration,
        error_message=args.error
    )
    print(f"✓ 已记录技能使用：{args.skill}/{args.action} ({args.status})")


def cmd_feedback(args):
    """添加用户反馈"""
    db = Database()
    from database.models import Feedback
    
    feedback = Feedback(
        skill_name=args.skill,
        rating=args.rating,
        comment=args.comment,
        user_id=args.user_id
    )
    
    db.add_feedback(feedback)
    print(f"✓ 已添加反馈：{args.skill} - {args.rating}⭐")


def cmd_health(args):
    """查看健康度评分"""
    db = Database()
    
    if args.all:
        scores = db.get_all_health_scores()
        if not scores:
            print("暂无健康度记录")
            return
        
        print("技能健康度排行:\n")
        for i, score in enumerate(scores, 1):
            status = "🟢" if score.score >= 80 else "🟡" if score.score >= 60 else "🔴"
            print(f"{i}. {status} {score.skill_name}: {score.score}/100")
            print(f"   成功率：{score.success_rate:.1f}% | 调用：{score.usage_count}次")
    else:
        score = db.get_health_score(args.skill)
        if score:
            print(f"{args.skill} 健康度:")
            print(f"   评分：{score.score}/100")
            print(f"   成功率：{score.success_rate:.1f}%")
            print(f"   平均耗时：{score.avg_duration_ms:.0f}ms")
            print(f"   调用次数：{score.usage_count}")
            if score.issues:
                print(f"   建议：{', '.join(score.issues[:3])}")
        else:
            print(f"暂无 {args.skill} 的健康度记录")


def cmd_init(args):
    """初始化数据库"""
    db = Database()
    print(f"✓ 数据库已初始化：{db.db_path}")


def cmd_clear(args):
    """清理旧数据"""
    db = Database()
    db.clear_old_data(args.days)
    print(f"✓ 已清理 {args.days} 天前的数据")


def main():
    parser = argparse.ArgumentParser(
        prog="skill-evolver",
        description="Skill Evolver - 自动分析和优化 Agent Skill 的工具"
    )
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # analyze 命令
    analyze_parser = subparsers.add_parser("analyze", help="分析技能代码")
    analyze_parser.add_argument("skill", nargs="?", help="技能名称")
    analyze_parser.add_argument("--all", action="store_true", help="分析所有技能")
    analyze_parser.add_argument("--skills-dir", default=None, help="技能目录")
    analyze_parser.add_argument("-v", "--verbose", action="store_true", help="显示详细信息")
    analyze_parser.set_defaults(func=cmd_analyze)
    
    # report 命令
    report_parser = subparsers.add_parser("report", help="生成健康度报告")
    report_parser.add_argument("skill", nargs="?", help="技能名称")
    report_parser.add_argument("--all", action="store_true", help="生成所有技能报告")
    report_parser.add_argument("--skills-dir", default=None, help="技能目录")
    report_parser.add_argument("-o", "--output", help="输出文件路径")
    report_parser.add_argument("-f", "--format", choices=["json", "markdown", "html"], default="json")
    report_parser.set_defaults(func=cmd_report)
    
    # log 命令
    log_parser = subparsers.add_parser("log", help="记录技能使用")
    log_parser.add_argument("skill", nargs="?", help="技能名称")
    log_parser.add_argument("action", nargs="?", help="执行的动作")
    log_parser.add_argument("--status", choices=["success", "failed", "timeout"], default="success")
    log_parser.add_argument("--duration", type=int, default=0, help="耗时 (ms)")
    log_parser.add_argument("--error", help="错误信息")
    log_parser.add_argument("--list", action="store_true", help="列出所有技能")
    log_parser.set_defaults(func=cmd_log)
    
    # feedback 命令
    feedback_parser = subparsers.add_parser("feedback", help="添加用户反馈")
    feedback_parser.add_argument("skill", help="技能名称")
    feedback_parser.add_argument("rating", type=int, choices=[1, 2, 3, 4, 5], help="评分 (1-5)")
    feedback_parser.add_argument("--comment", help="评论")
    feedback_parser.add_argument("--user-id", help="用户 ID")
    feedback_parser.set_defaults(func=cmd_feedback)
    
    # health 命令
    health_parser = subparsers.add_parser("health", help="查看健康度评分")
    health_parser.add_argument("skill", nargs="?", help="技能名称")
    health_parser.add_argument("--all", action="store_true", help="显示所有技能")
    health_parser.set_defaults(func=cmd_health)
    
    # init 命令
    init_parser = subparsers.add_parser("init", help="初始化数据库")
    init_parser.set_defaults(func=cmd_init)
    
    # clear 命令
    clear_parser = subparsers.add_parser("clear", help="清理旧数据")
    clear_parser.add_argument("--days", type=int, default=90, help="保留天数")
    clear_parser.set_defaults(func=cmd_clear)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(0)
    
    try:
        args.func(args)
    except KeyboardInterrupt:
        print("\n中断")
        sys.exit(1)
    except Exception as e:
        print(f"错误：{e}", file=sys.stderr)
        if hasattr(args, "verbose") and args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
