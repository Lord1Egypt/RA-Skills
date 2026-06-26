#!/usr/bin/env python3
"""
IP健康检测模块
- 代理可用性测试
- 响应延迟测量
- 质量评分计算
"""

import os
import sys
import time
import requests
from datetime import datetime
from pathlib import Path

# 导入其他模块
try:
    from api_client import call_api, record_stat, is_configured
    from config_manager import load_config, STATS_DIR
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from api_client import call_api, record_stat, is_configured
    from config_manager import load_config, STATS_DIR


def test_single_proxy(proxy, test_url, timeout):
    """测试单个代理IP"""
    proxy_address = proxy.get("full_address", "")

    if not proxy_address:
        return {"success": False, "error": "代理地址无效"}

    proxies = {
        "http": proxy_address,
        "https": proxy_address
    }

    start_time = time.time()

    try:
        response = requests.get(test_url, proxies=proxies, timeout=timeout)
        latency = (time.time() - start_time) * 1000  # ms

        return {
            "success": True,
            "status_code": response.status_code,
            "latency_ms": round(latency, 2),
            "response": response.json() if 'json' in response.headers.get('content-type', '') else response.text[:200]
        }

    except requests.exceptions.Timeout:
        return {"success": False, "error": "timeout", "latency_ms": timeout * 1000}

    except requests.exceptions.ProxyError:
        return {"success": False, "error": "proxy_error"}

    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}


def calculate_latency_score(latency_ms):
    """计算延迟评分"""
    latency_sec = latency_ms / 1000

    if latency_sec < 1:
        return 100
    elif latency_sec <= 3:
        return 80
    else:
        return 50


def calculate_quality_score(success_rate, avg_latency_ms):
    """计算IP质量评分"""
    # success_rate 权重 70%
    # latency_score 权重 30%

    latency_score = calculate_latency_score(avg_latency_ms)

    score = success_rate * 0.7 + latency_score * 0.3

    return round(score, 2)


def check_ip_health(sample_size=5):
    """检查IP健康状态"""
    if not is_configured():
        return {
            "success": False,
            "error": "请先配置代理API链接（使用 set_config）"
        }

    config = load_config()
    test_url = config.get("test_url", "https://httpbin.org/ip")
    timeout = config.get("timeout", 5)

    # 获取代理IP列表
    api_result = call_api()

    if not api_result["success"]:
        return api_result

    ip_list = api_result["data"]["ip_list"]

    if not ip_list:
        return {
            "success": False,
            "error": "API返回的IP列表为空"
        }

    # 测试样本
    test_ips = ip_list[:min(sample_size, len(ip_list))]

    print(f"[健康检测] 测试 {len(test_ips)} 个IP，目标: {test_url}")

    results = []
    success_count = 0
    fail_count = 0
    latencies = []

    for i, proxy in enumerate(test_ips):
        print(f"  [{i+1}/{len(test_ips)}] 测试 {proxy.get('host', 'unknown')}...")

        result = test_single_proxy(proxy, test_url, timeout)
        results.append({
            "proxy": proxy.get("host", ""),
            "port": proxy.get("port", ""),
            "result": result
        })

        if result["success"]:
            success_count += 1
            latencies.append(result["latency_ms"])
            print(f"    [OK] 响应 {result['latency_ms']}ms")
            record_stat(True, result["latency_ms"])
        else:
            fail_count += 1
            print(f"    [失败] {result.get('error', 'unknown')}")
            record_stat(False)

    # 计算指标
    success_rate = (success_count / len(test_ips)) * 100 if test_ips else 0
    avg_latency = sum(latencies) / len(latencies) if latencies else 0
    quality_score = calculate_quality_score(success_rate, avg_latency)

    return {
        "success": True,
        "summary": {
            "total_tested": len(test_ips),
            "success_count": success_count,
            "fail_count": fail_count,
            "success_rate": round(success_rate, 2),
            "avg_latency_ms": round(avg_latency, 2),
            "quality_score": quality_score
        },
        "details": results,
        "test_url": test_url,
        "check_time": datetime.now().isoformat()
    }


def get_health_status(quality_score):
    """根据评分获取健康状态"""
    if quality_score >= 80:
        return "excellent", "优秀"
    elif quality_score >= 60:
        return "good", "良好"
    elif quality_score >= 40:
        return "fair", "一般"
    else:
        return "poor", "较差"


# 命令行入口
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='IP健康检测')
    parser.add_argument('--sample', type=int, default=5, help='测试样本数量')
    args = parser.parse_args()

    result = check_ip_health(args.sample)

    if result["success"]:
        print(f"\n[健康检测报告]")
        s = result["summary"]
        print(f"  测试数量: {s['total_tested']}")
        print(f"  成功: {s['success_count']} | 失败: {s['fail_count']}")
        print(f"  成功率: {s['success_rate']}%")
        print(f"  平均延迟: {s['avg_latency_ms']}ms")
        print(f"  质量评分: {s['quality_score']}")

        status, status_text = get_health_status(s['quality_score'])
        print(f"  健康状态: {status_text}")

        # 输出详细结果
        print(f"\n[详细结果]")
        for d in result["details"]:
            status_icon = "[OK]" if d["result"]["success"] else "[失败]"
            print(f"  {status_icon} {d['proxy']}:{d['port']} - {d['result'].get('latency_ms', 'N/A')}ms")
    else:
        print(f"[错误] {result['error']}")