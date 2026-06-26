#!/usr/bin/env python3
"""
订单到期提醒脚本
- 检查到期时间
- 根据剩余天数生成提醒
- 输出提醒信息（不发送通知）
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# 设置控制台编码
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 导入其他模块
try:
    from expiry_checker import get_order_expire_time, calculate_days_left, get_expiry_status
    from config_manager import is_configured
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from expiry_checker import get_order_expire_time, calculate_days_left, get_expiry_status
    from config_manager import is_configured


# 提醒阈值
REMIND_DAYS = [5, 3, 1]  # 5天、3天、1天提醒


def check_expiry_reminder():
    """
    检查到期时间并生成提醒
    
    Returns:
        dict: 包含提醒信息，不发送通知
    """
    
    if not is_configured():
        return {
            "need_notify": False,
            "error": "未配置代理API，请先使用 set_config 配置"
        }
    
    # 获取到期时间
    result = get_order_expire_time()
    
    if not result["success"]:
        return {
            "need_notify": False,
            "error": result["error"]
        }
    
    expire_str = result["expire_time"]
    
    if not expire_str:
        return {
            "need_notify": False,
            "error": "无法获取到期时间"
        }
    
    # 计算剩余天数
    calc_result = calculate_days_left(expire_str)
    days_left, hours_left, expire_datetime = calc_result
    
    if days_left is None:
        return {
            "need_notify": False,
            "error": "无法解析到期时间"
        }
    
    # 获取状态
    status, status_text = get_expiry_status(days_left)
    
    # 判断是否需要提醒
    need_notify = days_left in REMIND_DAYS or days_left <= 0
    
    # 生成通知内容
    output = {
        "need_notify": need_notify,
        "days_left": days_left,
        "expire_time": expire_str,
        "status": status,
        "status_text": status_text,
        "renew_link": "https://www.kuaidaili.com/uc/order-list/"
    }
    
    if need_notify:
        # 确定提醒级别
        if days_left <= 0:
            notify_level = "expired"
            emoji = "🚨"
            urgency = "紧急"
            message = f"快代理订单已过期 {abs(days_left)} 天，请立即续费！"
        elif days_left == 1:
            notify_level = "critical"
            emoji = "🚨"
            urgency = "紧急"
            message = f"快代理订单将在明天到期，请立即续费！"
        elif days_left == 3:
            notify_level = "warning"
            emoji = "⚠️"
            urgency = "警告"
            message = f"快代理订单将在3天后到期，请尽快续费。"
        else:  # days_left == 5
            notify_level = "attention"
            emoji = "📅"
            urgency = "提醒"
            message = f"快代理订单将在5天后到期，请安排续费。"
        
        output["notify_level"] = notify_level
        output["emoji"] = emoji
        output["urgency"] = urgency
        output["message"] = message
        
        # 格式化的通知文本
        output["notification_text"] = (
            f"{emoji}【快代理订单到期{urgency}】\n\n"
            f"{message}\n\n"
            f"到期时间：{expire_str}\n"
            f"剩余天数：{days_left} 天\n"
            f"续费链接：{output['renew_link']}"
        )
    else:
        output["notify_level"] = ""
        output["notification_text"] = (
            f"ℹ️ 快代理订单状态正常\n\n"
            f"到期时间：{expire_str}\n"
            f"剩余天数：{days_left} 天"
        )
    
    return output


# 命令行入口
if __name__ == '__main__':
    result = check_expiry_reminder()
    
    # 输出JSON结果
    print(json.dumps(result, ensure_ascii=False, indent=2))