"""Spirit butler: spirit, daily-report, weekly-report, health."""

from __future__ import annotations

import json
import re
import sys
from argparse import Namespace
from datetime import datetime

from agent_memory.cli._utils import get_memory

# Security: max command length and dangerous pattern blocklist
_MAX_COMMAND_LENGTH = 500
_DANGEROUS_PATTERNS = re.compile(
    r"(?:ignore\s+(?:previous|above|all)\s+instructions?"
    r"|system\s*:"
    r"|you\s+are\s+now"
    r"|new\s+rule\s*:",
    re.IGNORECASE,
)


def cmd_spirit(args):
    """自然语言指令 — 通过 Spirit 管家解析并执行"""
    command = args.command
    if not command or not command.strip():
        print(json.dumps({"error": "命令不能为空"}, ensure_ascii=False))
        return
    if len(command) > _MAX_COMMAND_LENGTH:
        print(json.dumps({"error": f"命令过长（最大 {_MAX_COMMAND_LENGTH} 字符）"}, ensure_ascii=False))
        return
    if _DANGEROUS_PATTERNS.search(command):
        print(json.dumps({"error": "命令包含不允许的模式"}, ensure_ascii=False))
        return
    mem = get_memory()
    try:
        result = mem.spirit.execute(args.command, confirm=True)
        if result.success:
            if result.output:
                print(result.output)
            else:
                print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
        else:
            if result.preview:
                print(f"📋 预览: {result.preview}")
            else:
                print(f"❌ {result.error or '执行失败'}")
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
    finally:
        mem.close()


def cmd_daily_report(args):
    """生成每日记忆报告"""
    mem = get_memory()
    try:
        date_ts = None
        if args.date:
            date_ts = int(datetime.strptime(args.date, "%Y-%m-%d").timestamp())
        report = mem.spirit.report(report_type='daily', date=date_ts, format='markdown')
        print(report)
    except ValueError:
        print(json.dumps({"error": f"日期格式错误: {args.date}，请使用 YYYY-MM-DD"}, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
    finally:
        mem.close()


def cmd_weekly_report(args):
    """生成每周记忆报告"""
    mem = get_memory()
    try:
        report = mem.spirit.report(report_type='weekly', format='markdown')
        print(report)
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
    finally:
        mem.close()


def cmd_health(args):
    """运行健康检查"""
    mem = get_memory()
    try:
        report = mem.spirit.check_health(fix=args.fix)
        status_icons = {
            'healthy': '✅',
            'healthy_with_notes': '⚠️',
            'warning': '⚠️',
            'critical': '🔴',
            'error': '❌',
        }
        icon = status_icons.get(report.overall_status, '❓')
        print(f"{icon} 系统状态: {report.overall_status} (评分: {report.score:.2f})")

        if report.issues:
            print(f"\n发现 {len(report.issues)} 个问题:")
            for i, issue in enumerate(report.issues, 1):
                sev_icon = {'critical': '🔴', 'warning': '⚠️', 'info': 'ℹ️'}.get(issue.severity, '❓')
                print(f"  {i}. {sev_icon} [{issue.category}] {issue.description}")
                if issue.suggestion:
                    print(f"     💡 {issue.suggestion}")

        if report.fix_results:
            print(f"\n自动修复结果:")
            for fr in report.fix_results:
                status_icon = '✅' if fr.get('status') == 'fixed' else '⚠️'
                print(f"  {status_icon} {fr.get('category', '')}: {fr.get('status', '')}")

        if not report.issues:
            print("系统运行正常，无异常。")
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
    finally:
        mem.close()
