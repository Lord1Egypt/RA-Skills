#!/usr/bin/env python3
"""
智能并发调度模块
- 基于成功率动态调整并发
- 失败保护机制
- 推荐请求频率
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import json

# 导入其他模块
try:
    from api_client import get_order_info, is_configured
    from health_checker import check_ip_health
    from stats_tracker import get_recent_stats
    from config_manager import load_config, STATS_DIR
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from api_client import get_order_info, is_configured
    from health_checker import check_ip_health
    from stats_tracker import get_recent_stats
    from config_manager import load_config, STATS_DIR


# 连续失败计数器
FAIL_COUNTER_FILE = STATS_DIR / "fail_counter.json"


def load_fail_counter():
    """加载连续失败计数"""
    if FAIL_COUNTER_FILE.exists():
        with open(FAIL_COUNTER_FILE, 'r') as f:
            return json.load(f)
    return {"consecutive_fails": 0, "last_updated": None}


def save_fail_counter(counter):
    """保存失败计数"""
    STATS_DIR.mkdir(parents=True, exist_ok=True)
    with open(FAIL_COUNTER_FILE, 'w') as f:
        json.dump(counter, f)


def calculate_base_concurrency(max_concurrency):
    """计算基础并发（80%）"""
    return int(max_concurrency * 0.8)


def adjust_by_success_rate(base, success_rate):
    """根据成功率调整并发"""
    if success_rate >= 95:
        return base
    elif success_rate >= 80:
        return int(base * 0.7)
    elif success_rate >= 60:
        return int(base * 0.5)
    elif success_rate >= 50:
        return int(base * 0.3)
    else:
        return int(base * 0.2)  # 最低保护


def apply_fail_protection(current_concurrency, consecutive_fails, success_rate):
    """应用失败保护机制"""
    # 连续失败 > 10，并发降低50%
    if consecutive_fails > 10:
        return int(current_concurrency * 0.5), True

    # 成功率 < 50%，并发降至最低
    if success_rate < 50:
        return 1, True  # 最小并发

    return current_concurrency, False


def get_concurrency(force_health_check=False):
    """获取推荐并发配置"""
    if not is_configured():
        return {
            "success": False,
            "error": "请先配置代理API链接（使用 set_config）"
        }

    # 获取订单信息（并发上限）
    try:
        from order_info import get_order_info_from_api
        order_result = get_order_info_from_api()
        
        if not order_result["success"]:
            return order_result
        
        max_concurrency = order_result["order_info"].get("max_concurrency", 0)
    except:
        # 如果订单API失败，使用默认值
        max_concurrency = 5  # 默认并发

    if max_concurrency == 0:
        return {
            "success": False,
            "error": "订单并发上限为0，可能已过期"
        }

    # 获取成功率
    success_rate = None

    if force_health_check:
        # 强制健康检测
        health_result = check_ip_health(sample_size=3)
        if health_result["success"]:
            success_rate = health_result["summary"]["success_rate"]
    else:
        # 使用最近统计
        stats = get_recent_stats(days=1)
        if stats and stats.get("today"):
            success_rate = stats["today"].get("success_rate", 0)

    # 如果没有成功率数据，使用默认值
    if success_rate is None:
        success_rate = 85  # 默认假设良好

    # 计算并发
    base = calculate_base_concurrency(max_concurrency)
    adjusted = adjust_by_success_rate(base, success_rate)

    # 失败保护
    counter = load_fail_counter()
    final_concurrency, protection_active = apply_fail_protection(
        adjusted,
        counter.get("consecutive_fails", 0),
        success_rate
    )

    # 计算请求频率
    request_interval = calculate_request_interval(final_concurrency)

    return {
        "success": True,
        "recommendation": {
            "max_concurrency": max_concurrency,
            "recommended_concurrency": final_concurrency,
            "current_success_rate": success_rate,
            "base_concurrency": base,
            "protection_active": protection_active,
            "consecutive_fails": counter.get("consecutive_fails", 0)
        },
        "request_config": {
            "concurrent_requests": final_concurrency,
            "request_interval_ms": request_interval,
            "batch_size": min(final_concurrency, 10)
        },
        "advice": generate_advice(success_rate, final_concurrency, protection_active)
    }


def calculate_request_interval(concurrency):
    """计算请求间隔"""
    # 根据并发数计算推荐间隔
    if concurrency >= 50:
        return 100  # 高并发，短间隔
    elif concurrency >= 20:
        return 200
    elif concurrency >= 10:
        return 500
    else:
        return 1000  # 低并发，长间隔


def generate_advice(success_rate, concurrency, protection_active):
    """生成调度建议"""
    if protection_active:
        return "失败保护已激活，建议暂停或检查代理状态"

    if success_rate >= 95:
        return "状态优秀，可保持当前并发或适当提高"
    elif success_rate >= 80:
        return "状态良好，建议保持当前并发"
    elif success_rate >= 60:
        return "状态一般，建议降低并发或检查代理质量"
    else:
        return "状态较差，建议暂停并检查代理配置"


def record_request_result(success):
    """记录请求结果（用于失败计数）"""
    counter = load_fail_counter()

    if success:
        counter["consecutive_fails"] = 0
    else:
        counter["consecutive_fails"] += 1

    counter["last_updated"] = datetime.now().isoformat()
    save_fail_counter(counter)


# 命令行入口
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='智能并发调度')
    parser.add_argument('--check', action='store_true', help='强制健康检测')
    parser.add_argument('--record-success', action='store_true', help='记录成功')
    parser.add_argument('--record-fail', action='store_true', help='记录失败')
    args = parser.parse_args()

    if args.record_success:
        record_request_result(True)
        print("[OK] 记录成功请求")

    elif args.record_fail:
        record_request_result(False)
        print("[警告] 记录失败请求")

    else:
        result = get_concurrency(force_health_check=args.check)

        if result["success"]:
            print(f"\n[并发调度建议]")
            r = result["recommendation"]
            print(f"  并发上限: {r['max_concurrency']}")
            print(f"  基础并发: {r['base_concurrency']} (80%)")
            print(f"  推荐并发: {r['recommended_concurrency']}")
            print(f"  当前成功率: {r['current_success_rate']}%")

            if r['protection_active']:
                print(f"  [警告] 失败保护已激活")
                print(f"  连续失败: {r['consecutive_fails']}")

            c = result["request_config"]
            print(f"\n[请求配置]")
            print(f"  并发请求: {c['concurrent_requests']}")
            print(f"  请求间隔: {c['request_interval_ms']}ms")
            print(f"  批次大小: {c['batch_size']}")

            print(f"\n[建议] {result['advice']}")
        else:
            print(f"[错误] {result['error']}")