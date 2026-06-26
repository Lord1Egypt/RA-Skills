#!/usr/bin/env python3
"""
Config Guardian - 配置健康检查与自动修复
检测配置异常，自动修复已知问题

用法:
    python3 check_config.py              # 健康检查
    python3 check_config.py --fix       # 自动修复
    python3 check_config.py --diff      # 对比版本差异
    python3 check_config.py --report    # 生成诊断报告
"""

import json
import os
import sys
import platform
import subprocess
from datetime import datetime
from pathlib import Path

# 导入备份模块（同一目录）
sys.path.insert(0, str(Path(__file__).parent))
from backup_config import (
    get_qclaw_version,
    get_config_path,
    get_backup_base_dir,
    get_openclaw_config_path,
    get_channel_defaults_path,
    get_channels_config,
    get_plugins_config,
    get_cron_jobs,
    check_version_change,
    backup_config,
)


# ============== 配置检查函数 ==============

def check_cron_jobs_health():
    """检查 cron 任务配置健康状态"""
    issues = []

    cron_jobs = get_cron_jobs()
    jobs = cron_jobs.get("jobs", [])

    for job in jobs:
        job_id = job.get("id", "unknown")
        name = job.get("name", "未命名")

        # 检查 delivery 配置
        delivery = job.get("delivery", {})

        # 问题 1: delivery 为空
        if not delivery:
            issues.append({
                "type": "missing_delivery",
                "job_id": job_id,
                "name": name,
                "severity": "high",
                "message": f"任务 '{name}' 缺少 delivery 配置",
                "fix": f"添加 delivery.channel 和 delivery.to"
            })
            continue

        # 问题 2: 有 delivery 但没有 channel
        channel = delivery.get("channel")
        if not channel:
            issues.append({
                "type": "missing_channel",
                "job_id": job_id,
                "name": name,
                "severity": "high",
                "message": f"任务 '{name}' delivery 缺少 channel 字段",
                "fix": "添加 delivery.channel"
            })

    return {
        "total_jobs": len(jobs),
        "issues": issues,
        "healthy": len(issues) == 0
    }


def check_channel_defaults():
    """检查 channel-defaults.json"""
    path = get_channel_defaults_path()

    if not path.exists():
        return {
            "exists": False,
            "message": "channel-defaults.json 不存在",
            "severity": "medium"
        }

    try:
        data = json.loads(path.read_text())
        return {
            "exists": True,
            "channels": list(data.keys()),
            "message": f"已配置 {len(data)} 个通道"
        }
    except Exception as e:
        return {
            "exists": True,
            "error": str(e),
            "message": "文件格式错误",
            "severity": "high"
        }


def check_version_health():
    """检查版本备份状态"""
    current = get_qclaw_version()
    last_version_file = get_backup_base_dir() / "last-version.txt"

    if not last_version_file.exists():
        return {
            "backed_up": False,
            "current": current,
            "message": "从未备份过配置",
            "severity": "high"
        }

    last = last_version_file.read_text().strip()

    if current != last:
        return {
            "backed_up": True,
            "current": current,
            "last": last,
            "changed": True,
            "message": f"版本已变化: {last} → {current}",
            "severity": "high"
        }

    return {
        "backed_up": True,
        "current": current,
        "last": last,
        "changed": False,
        "message": "配置已备份，版本一致"
    }


def get_all_health_checks():
    """执行所有健康检查"""
    return {
        "timestamp": datetime.now().isoformat(),
        "platform": platform.system(),
        "version": get_qclaw_version(),
        "checks": {
            "version": check_version_health(),
            "cron_jobs": check_cron_jobs_health(),
            "channel_defaults": check_channel_defaults(),
        }
    }


# ============== 修复函数 ==============

def suggest_fixes(health_report):
    """根据健康检查结果提供修复建议"""
    suggestions = []

    checks = health_report.get("checks", {})

    # 版本问题
    version_check = checks.get("version", {})
    if version_check.get("severity") == "high":
        suggestions.append({
            "action": "backup",
            "reason": "配置未备份或版本已变化",
            "command": "python3 backup_config.py"
        })

    # Cron 任务问题
    cron_check = checks.get("cron_jobs", {})
    for issue in cron_check.get("issues", []):
        if issue.get("type") in ["missing_delivery", "missing_channel"]:
            job_name = issue.get("name")
            suggestions.append({
                "action": "fix_cron",
                "job_id": issue.get("job_id"),
                "job_name": job_name,
                "reason": issue.get("message"),
                "fix": issue.get("fix"),
                # 智能建议
                "suggested_channel": get_default_channel_for_job(job_name)
            })

    return suggestions


def get_default_channel_for_job(job_name):
    """根据任务名称智能推荐通道"""
    name_lower = job_name.lower()

    # 微信相关任务
    if "微信" in job_name or "选股" in job_name or "会议室" in job_name:
        return "openclaw-weixin"

    # GitHub 相关
    if "github" in name_lower or "简报" in job_name:
        return "openclaw-weixin"

    # 学习任务
    if "学习" in job_name or "memory" in name_lower:
        return "openclaw-weixin"

    # 默认返回
    return "openclaw-weixin"


# ============== 输出函数 ==============

def print_health_report(health_report):
    """打印健康报告"""
    print("🔍 QClaw 配置健康检查")
    print("=" * 50)
    print()

    checks = health_report.get("checks", {})

    # 版本状态
    version_check = checks.get("version", {})
    status = "✅" if not version_check.get("changed") else "⚠️"
    print(f"{status} 版本状态")
    print(f"   当前: {version_check.get('current', '?')}")
    print(f"   备份: {version_check.get('last', '从未备份')}")
    print()

    # Cron 任务状态
    cron_check = checks.get("cron_jobs", {})
    status = "✅" if cron_check.get("healthy") else "❌"
    print(f"{status} Cron 任务 ({cron_check.get('total_jobs', 0)} 个)")
    for issue in cron_check.get("issues", [])[:3]:
        print(f"   - {issue.get('message')}")
    if len(cron_check.get("issues", [])) > 3:
        print(f"   ... 共 {len(cron_check.get('issues', []))} 个问题")
    print()

    # Channel defaults
    channel_check = checks.get("channel_defaults", {})
    status = "✅" if channel_check.get("exists") else "❌"
    print(f"{status} 通道默认配置")
    print(f"   {channel_check.get('message', '')}")
    print()


def print_fixes(suggestions):
    """打印修复建议"""
    if not suggestions:
        print("✅ 未发现问题，无需修复")
        return

    print("💡 修复建议")
    print("-" * 50)

    for i, s in enumerate(suggestions, 1):
        print(f"{i}. {s.get('reason')}")
        if s.get("action") == "backup":
            print(f"   执行: {s.get('command')}")
        elif s.get("action") == "fix_cron":
            print(f"   任务: {s.get('job_name')}")
            print(f"   修复: {s.get('fix')}")
            print(f"   建议: delivery.channel = \"{s.get('suggested_channel')}\"")
        print()


# ============== 主函数 ==============

def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1]

        if arg == "--fix":
            # 执行检查并尝试修复
            health = get_all_health_checks()
            suggestions = suggest_fixes(health)

            if not suggestions:
                print("✅ 配置健康，无需修复")
                return

            print_fixes(suggestions)

            # 自动备份
            print()
            print("正在自动备份...")
            backup_config()

            print()
            print("⚠️ 部分修复需要手动执行。请运行:")
            for s in suggestions:
                if s.get("action") == "fix_cron":
                    print(f"   openclaw cron update {s.get('job_id')} --channel {s.get('suggested_channel')}")
            return

        elif arg == "--report":
            # 生成 JSON 报告
            health = get_all_health_checks()
            suggestions = suggest_fixes(health)
            report = {
                "health": health,
                "suggestions": suggestions
            }
            print(json.dumps(report, indent=2, ensure_ascii=False))
            return

        elif arg == "--diff":
            # 版本对比
            result = check_version_change()
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return

        elif arg in ["--help", "-h"]:
            print(__doc__)
            return

    # 默认：健康检查
    health = get_all_health_checks()
    print_health_report(health)

    suggestions = suggest_fixes(health)
    print_fixes(suggestions)


if __name__ == "__main__":
    main()
