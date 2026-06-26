#!/usr/bin/env python3
"""
订单到期检查模块
- 通过 getorderexpiretime API 获取到期时间
- 计算剩余天数
- 多级提醒
"""

import os
import sys
import requests
from datetime import datetime, timedelta
from pathlib import Path

# 导入配置管理
try:
    from config_manager import load_config, is_configured, get_credentials
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from config_manager import load_config, is_configured, get_credentials


def get_order_expire_time(retry_count=0):
    """
    获取订单到期时间
    
    接口: GET https://dev.kdlapi.com/api/getorderexpiretime
    参数: secret_id, signature (secret_token)
    
    Returns:
        dict: {"success": bool, "expire_time": str, "days_left": int}
    """
    if not is_configured():
        return {
            "success": False,
            "error": "请先配置API密钥（使用 set_config）"
        }
    
    # 获取认证信息
    creds = get_credentials()
    if "error" in creds:
        return {"success": False, "error": creds["error"]}
    
    config = load_config()
    max_retry = config.get("max_retry", 3)
    timeout = config.get("timeout", 10)
    
    secret_id = creds["secret_id"]
    signature = creds["signature"]
    
    # 调用API
    api_url = "https://dev.kdlapi.com/api/getorderexpiretime"
    params = {
        "secret_id": secret_id,
        "signature": signature
    }
    
    try:
        print(f"[API] 获取订单到期时间 (尝试 {retry_count + 1}/{max_retry})")
        
        response = requests.get(api_url, params=params, timeout=timeout)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get("code") != 0:
            return {
                "success": False,
                "error": f"API错误: {result.get('msg', '未知错误')}"
            }
        
        expire_time = result.get("data", {}).get("expire_time", "")
        
        return {
            "success": True,
            "expire_time": expire_time,
            "raw": result
        }
        
    except requests.exceptions.Timeout:
        if retry_count < max_retry - 1:
            print(f"[重试] 请求超时...")
            import time
            time.sleep(2)
            return get_order_expire_time(retry_count + 1)
        return {"success": False, "error": "请求超时"}
    
    except requests.exceptions.RequestException as e:
        if retry_count < max_retry - 1:
            print(f"[重试] 网络错误: {e}")
            import time
            time.sleep(2)
            return get_order_expire_time(retry_count + 1)
        return {"success": False, "error": f"网络错误: {str(e)}"}


def parse_expire_time(expire_str):
    """解析到期时间字符串"""
    if not expire_str:
        return None
    
    formats = [
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%d',
        '%Y/%m/%d %H:%M:%S',
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(expire_str, fmt)
        except ValueError:
            continue
    
    return None


def calculate_days_left(expire_time):
    """计算剩余天数"""
    if isinstance(expire_time, str):
        expire_time = parse_expire_time(expire_time)
    
    if not expire_time:
        return None, "无法解析到期时间"
    
    now = datetime.now()
    delta = expire_time - now
    days_left = delta.days
    hours_left = delta.seconds // 3600
    
    return days_left, hours_left, expire_time


def get_expiry_status(days_left):
    """获取到期状态"""
    if days_left is None:
        return "unknown", "无法确定"
    
    if days_left <= 0:
        return "expired", "已过期"
    elif days_left < 1:
        return "critical", "紧急（即将过期）"
    elif days_left < 3:
        return "warning", "警告（3天内过期）"
    elif days_left < 5:
        return "attention", "注意（5天内过期）"
    else:
        return "normal", "正常"


def check_expiry():
    """检查订单到期情况"""
    # 获取到期时间
    result = get_order_expire_time()
    
    if not result["success"]:
        return result
    
    expire_str = result["expire_time"]
    
    if not expire_str:
        return {
            "success": True,
            "status": "unknown",
            "message": "无法获取到期时间"
        }
    
    # 计算剩余时间
    calc_result = calculate_days_left(expire_str)
    days_left, hours_left, expire_datetime = calc_result
    
    if days_left is None:
        return {
            "success": True,
            "status": "unknown",
            "message": f"到期时间格式异常: {expire_str}"
        }
    
    status, status_text = get_expiry_status(days_left)
    
    # 构建响应
    response = {
        "success": True,
        "status": status,
        "status_text": status_text,
        "expire_time": expire_str,
        "days_left": days_left,
        "hours_left": hours_left,
        "renew_link": "https://www.kuaidaili.com/uc/order-list/"
    }
    
    # 状态处理
    if status == "expired":
        response["action"] = "停止使用"
        response["message"] = f"订单已过期 {abs(days_left)} 天，请立即续费"
    
    elif status == "critical":
        response["action"] = "紧急续费"
        response["message"] = f"订单将在 {hours_left} 小时内过期，请立即续费"
    
    elif status == "warning":
        response["action"] = "尽快续费"
        response["message"] = f"订单将在 {days_left} 天后过期（3天内）"
    
    elif status == "attention":
        response["action"] = "建议续费"
        response["message"] = f"订单将在 {days_left} 天后过期（5天内）"
    
    else:
        response["action"] = "正常使用"
        response["message"] = f"订单有效期充足，剩余 {days_left} 天"
    
    return response


# 命令行入口
if __name__ == '__main__':
    # 设置控制台编码
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')
    
    result = check_expiry()
    
    if result["success"]:
        print(f"\n[到期检查结果]")
        print(f"  状态: {result['status_text']}")
        print(f"  到期时间: {result['expire_time']}")
        print(f"  剩余天数: {result['days_left']} 天")
        
        if result['hours_left'] and result['days_left'] < 1:
            print(f"  剩余时间: {result['hours_left']} 小时")
        
        print(f"  建议: {result['message']}")
        print(f"  续费链接: {result['renew_link']}")
        
        if result['status'] == 'expired':
            print(f"\n[警告] 订单已过期，请立即续费！")
    else:
        print(f"[错误] {result['error']}")