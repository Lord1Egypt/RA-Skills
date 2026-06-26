#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///
"""
Heartbeat Check - 心跳检查

功能:
- 工作时间内的定期检查
- 全部正常时静默（回复 HEARTBEAT_OK）
- 有问题时输出告警摘要

使用方式:
    python scripts/heartbeat.py
    python scripts/heartbeat.py --force  # 强制输出（非工作时间也检查）
"""

import json
import os
import sys
import time
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent))
from i18n import get_i18n

# 导入 L2 检查函数
from l2_hourly_check import load_config, run_l2_check

# ============== 配置 ==============

DEFAULT_CONFIG = Path.home() / ".openclaw" / "skills" / "system-healthcheck" / "config" / "default_config.yaml"

WORK_HOURS_START = 9   # 9:00
WORK_HOURS_END = 18    # 18:00


def is_work_hours(start: int, end: int) -> bool:
    """检查当前是否在工作时间内"""
    current_hour = time.localtime().tm_hour
    return start <= current_hour < end


def run_heartbeat_check(config: dict, force: bool = False) -> dict:
    """执行心跳检查
    
    Args:
        config: 配置字典
        force: 强制检查（忽略工作时间）
    
    Returns:
        {
            "should_output": bool,
            "is_work_hours": bool,
            "health": dict,  # L2 检查结果
            "message": str
        }
    """
    i18n = get_i18n()
    
    work_start = config.get("work_hours_start", WORK_HOURS_START)
    work_end = config.get("work_hours_end", WORK_HOURS_END)
    quiet_on_ok = config.get("quiet_on_ok", True)
    
    in_work_hours = is_work_hours(work_start, work_end)
    
    result = {
        "is_work_hours": in_work_hours,
        "should_output": force or in_work_hours,
        "health": None,
        "message": ""
    }
    
    # 非工作时间且不强制 → 跳过
    if not result["should_output"]:
        result["message"] = i18n.t("heartbeat.suppressed")
        return result
    
    # 执行健康检查
    health = run_l2_check(config)
    result["health"] = health
    
    # 决定输出
    if quiet_on_ok and health["success"]:
        # 全部正常 → 静默
        result["should_output"] = False
        result["message"] = "HEARTBEAT_OK"
    else:
        # 有问题 → 输出
        result["should_output"] = True
        if health["success"]:
            result["message"] = i18n.t("summary.all_ok")
        elif health["error_count"] > 0:
            result["message"] = i18n.t("summary.has_errors", count=health["error_count"])
        else:
            result["message"] = i18n.t("summary.has_warnings", count=health["warning_count"])
    
    return result


def format_heartbeat_output(result: dict) -> str:
    """格式化心跳输出"""
    i18n = get_i18n()
    
    lines = []
    lines.append(f"{i18n.t('heartbeat.title')} · {time.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    
    if result["health"]:
        # 输出健康检查详情（复用 L2 格式）
        from l2_hourly_check import format_output
        lines.append(format_output(result["health"], 0))
    else:
        lines.append(result["message"])
    
    return "\n".join(lines)


def main():
    """主函数"""
    # 加载配置
    config = load_config()
    
    # 解析命令行参数
    force = "--force" in sys.argv
    json_output = "--json" in sys.argv
    
    # 执行检查
    result = run_heartbeat_check(config, force)
    
    # 输出
    if json_output:
        print(json.dumps(result, indent=2))
    elif result["should_output"]:
        print(format_heartbeat_output(result))
        # 如果有错误，返回非零退出码
        if result["health"] and not result["health"]["success"]:
            sys.exit(1)
    else:
        # 静默模式
        if result["message"] == "HEARTBEAT_OK":
            print("HEARTBEAT_OK")
        sys.exit(0)


if __name__ == "__main__":
    main()
