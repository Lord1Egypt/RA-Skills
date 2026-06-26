#!/usr/bin/env python3
"""
订单信息模块
- 通过 dev.kdlapi.com 获取完整订单信息
- 解析订单详情
- 生成代理连接信息
"""

import os
import sys
import requests
from datetime import datetime
from pathlib import Path

# 导入配置管理
try:
    from config_manager import load_config, is_configured, get_credentials, mask_secret
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from config_manager import load_config, is_configured, get_credentials, mask_secret


def get_order_info_from_api(retry_count=0):
    """
    获取订单详细信息
    
    接口: GET https://dev.kdlapi.com/api/getorderinfo
    参数: secret_id, signature (secret_token)
    
    Returns:
        dict: 订单详细信息
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
    
    # 调用订单信息API
    url = "https://dev.kdlapi.com/api/getorderinfo"
    params = {
        "secret_id": secret_id,
        "signature": signature
    }
    
    try:
        print(f"[API] 获取订单信息 (尝试 {retry_count + 1}/{max_retry})")
        
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get("code") != 0:
            return {
                "success": False,
                "error": f"API错误: {result.get('msg', '未知错误')}",
                "code": result.get("code")
            }
        
        # 解析订单数据
        data = result.get("data", {})
        order_info = parse_order_data(data)
        
        return {
            "success": True,
            "order_info": order_info,
            "raw": data
        }
        
    except requests.exceptions.Timeout:
        if retry_count < max_retry - 1:
            print(f"[重试] 请求超时，等待后重试...")
            import time
            time.sleep(2)
            return get_order_info_from_api(retry_count + 1)
        return {"success": False, "error": "请求超时，请检查网络"}
    
    except requests.exceptions.RequestException as e:
        if retry_count < max_retry - 1:
            print(f"[重试] 网络错误: {e}")
            import time
            time.sleep(2)
            return get_order_info_from_api(retry_count + 1)
        return {"success": False, "error": f"网络错误: {str(e)}"}


def parse_order_data(data):
    """
    解析订单数据
    
    字段映射:
    - orderid → order_id
    - product → product_type
    - status → status
    - tunnel_req → max_concurrency
    - tunnel_bandwidth → bandwidth
    - tunnel_host → proxy_host
    - tunnel_port_http → proxy_port
    - tunnel_username → username
    - tunnel_password → password
    """
    order_info = {
        "order_id": data.get("orderid", "未知"),
        "pay_type": data.get("pay_type", "未知"),
        "product_type": data.get("product", "未知"),
        "status": data.get("status", "未知"),
        "expire_time": data.get("expire_time", ""),
        "is_auto_renew": data.get("is_auto_renew", False),
        "freeze_amount": data.get("freeze_amount", "0"),
        "unit_price": data.get("unit_price", "0"),
        
        # 代理连接信息
        "proxy_host": data.get("tunnel_host", ""),
        "proxy_port": data.get("tunnel_port_http", ""),
        "proxy_port_socks": data.get("tunnel_port_socks", ""),
        "username": data.get("tunnel_username", ""),
        "password": data.get("tunnel_password", ""),
        
        # 性能参数
        "max_concurrency": data.get("tunnel_req", 0),
        "bandwidth": data.get("tunnel_bandwidth", 0),
    }
    
    # 生成完整代理地址
    if order_info["username"] and order_info["password"]:
        order_info["proxy_address"] = f"http://{order_info['username']}:{order_info['password']}@{order_info['proxy_host']}:{order_info['proxy_port']}"
    else:
        order_info["proxy_address"] = f"http://{order_info['proxy_host']}:{order_info['proxy_port']}"
    
    return order_info


def format_order_report(order_info):
    """格式化订单报告"""
    lines = ["\n[订单信息]"]
    
    lines.append(f"  订单ID: {order_info['order_id']}")
    lines.append(f"  产品类型: {order_info['product_type']}")
    lines.append(f"  订单状态: {order_info['status']}")
    lines.append(f"  付费方式: {order_info['pay_type']}")
    
    # 根据付费方式显示不同信息
    if order_info['pay_type'] == 'POST_PAY':
        lines.append(f"  单价: ¥{order_info['unit_price']}/GB")
        if order_info['freeze_amount'] != "0":
            lines.append(f"  冻结金额: ¥{order_info['freeze_amount']}")
    elif order_info['expire_time']:
        lines.append(f"  到期时间: {order_info['expire_time']}")
        if order_info.get('is_auto_renew'):
            lines.append(f"  自动续费: 已开启")
    
    lines.append(f"\n[代理配置]")
    lines.append(f"  并发上限: {order_info['max_concurrency']}")
    lines.append(f"  带宽: {order_info['bandwidth']} Mbps")
    
    lines.append(f"\n[代理连接]")
    lines.append(f"  主机: {order_info['proxy_host']}")
    lines.append(f"  HTTP端口: {order_info['proxy_port']}")
    if order_info['proxy_port_socks']:
        lines.append(f"  SOCKS端口: {order_info['proxy_port_socks']}")
    
    # 脱敏显示代理地址
    if order_info.get('password'):
        masked_address = order_info['proxy_address'].replace(order_info['password'], '***')
        lines.append(f"  代理地址: {masked_address}")
    else:
        lines.append(f"  代理地址: {order_info['proxy_address']}")
    
    return "\n".join(lines)


# 命令行入口
if __name__ == '__main__':
    # 设置控制台编码
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')
    
    result = get_order_info_from_api()
    
    if result["success"]:
        print(format_order_report(result["order_info"]))
    else:
        print(f"[错误] {result['error']}")