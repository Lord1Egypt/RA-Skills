#!/usr/bin/env python3
"""
API调用封装模块
- 超时控制
- 自动重试
- 错误处理
- 脱敏日志
"""

import os
import sys
import json
import time
import requests
from datetime import datetime
from pathlib import Path

# 导入配置管理
try:
    from config_manager import load_config, is_configured, get_credentials, mask_secret, STATS_DIR
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from config_manager import load_config, is_configured, get_credentials, mask_secret, STATS_DIR


MAX_RETRY = 3
DEFAULT_TIMEOUT = 15

# 代理API端点
PROXY_API_URLS = {
    "TPS": "https://tps.kdlapi.com/api/gettps",
    "DPS": "https://dps.kdlapi.com/api/getdps",
    "KPS": "https://kps.kdlapi.com/api/getkps",
    "FPS": "https://fps.kdlapi.com/api/getfps",
    "SFPS": "https://dev.kdlapi.com/api/getsfps"
}

# 当前IP查询API
CURRENT_IP_URLS = {
    "TPS_PRO": "https://tps.kdlapi.com/api/tpsprocurrentip",
    "TPS": "https://tps.kdlapi.com/api/tpscurrentip"
}


def call_api(product_type="TPS", params=None, retry_count=0):
    """
    调用代理API获取IP列表
    
    Args:
        product_type: 产品类型 (TPS/DPS/KPS)
        params: 额外参数 (如 num, format, sep 等)
        retry_count: 重试次数
    
    Returns:
        dict: {"success": bool, "data": dict}
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
    timeout = config.get("timeout", DEFAULT_TIMEOUT)
    
    # 构建API URL
    api_url = PROXY_API_URLS.get(product_type, PROXY_API_URLS["TPS"])
    
    # 构建请求参数
    request_params = {
        "secret_id": creds["secret_id"],
        "signature": creds["signature"],
        "num": 1,
        "format": "text",
        "sep": "1"
    }
    
    # 合并额外参数
    if params:
        request_params.update(params)
    
    try:
        # 脱敏日志
        masked_params = f"secret_id={mask_secret(creds['secret_id'])}&signature={mask_secret(creds['signature'])}"
        print(f"[API调用] {api_url}?{masked_params} (尝试 {retry_count + 1}/{MAX_RETRY})")
        
        response = requests.get(api_url, params=request_params, timeout=timeout)
        response.raise_for_status()
        
        # 检查响应类型
        content_type = response.headers.get('content-type', '')
        
        if 'text/plain' in content_type or 'text' in content_type:
            # 文本格式解析（快代理隧道代理格式：host:port:username:password）
            text = response.text.strip()
            if ':' in text:
                parts = text.split(':')
                if len(parts) >= 4:
                    proxy = {
                        "host": parts[0],
                        "port": parts[1],
                        "username": parts[2],
                        "password": parts[3],
                        "full_address": f"http://{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}"
                    }
                    return {
                        "success": True,
                        "data": {
                            "ip_list": [proxy],
                            "order_info": {}
                        },
                        "raw_text": text
                    }
            
            return {
                "success": True,
                "data": {
                    "ip_list": [],
                    "order_info": {},
                    "raw_text": text
                }
            }
        
        # JSON格式解析
        data = response.json()
        
        # 验证返回数据
        if not data or 'data' not in data:
            return {
                "success": False,
                "error": "API返回数据异常，请联系服务提供方"
            }
        
        # 解析代理列表
        proxy_list = parse_proxy_data(data)
        
        return {
            "success": True,
            "data": proxy_list,
            "raw": data
        }
    
    except requests.exceptions.Timeout:
        if retry_count < MAX_RETRY - 1:
            print(f"[重试] 超时，等待后重试...")
            time.sleep(2)
            return call_api(product_type, params, retry_count + 1)
        return {
            "success": False,
            "error": "代理API调用超时，请检查网络或API状态"
        }
    
    except requests.exceptions.RequestException as e:
        if retry_count < MAX_RETRY - 1:
            print(f"[重试] 网络错误: {e}")
            time.sleep(2)
            return call_api(product_type, params, retry_count + 1)
        return {
            "success": False,
            "error": f"代理API调用失败: {str(e)}"
        }
    
    except json.JSONDecodeError:
        return {
            "success": False,
            "error": "API返回数据格式异常，请联系服务提供方"
        }


def parse_proxy_data(data):
    """解析API返回的代理数据"""
    result = {
        "ip_list": [],
        "order_info": {}
    }
    
    # 解析IP列表
    if 'data' in data and 'proxy_list' in data['data']:
        for proxy in data['data']['proxy_list']:
            ip_entry = {
                "host": proxy.get('ip', ''),
                "port": proxy.get('port', ''),
                "username": proxy.get('username', ''),
                "password": proxy.get('password', ''),
                "full_address": f"http://{proxy.get('username', '')}:{proxy.get('password', '')}@{proxy.get('ip', '')}:{proxy.get('port', '')}"
            }
            result["ip_list"].append(ip_entry)
    
    # 解析订单信息
    order_data = data.get('data', {})
    result["order_info"] = {
        "max_concurrency": order_data.get('max_concurrency', 0),
        "expire_time": order_data.get('expire_time', ''),
        "bandwidth": order_data.get('bandwidth', ''),
        "order_id": order_data.get('order_id', '')
    }
    
    return result


def record_stat(success, latency=None):
    """记录调用统计"""
    today = datetime.now().strftime('%Y-%m-%d')
    stats_file = STATS_DIR / f"{today}.json"
    
    # 加载今日统计
    if stats_file.exists():
        with open(stats_file, 'r') as f:
            stats = json.load(f)
    else:
        stats = {
            "total_requests": 0,
            "success_count": 0,
            "fail_count": 0,
            "latencies": []
        }
    
    # 更新统计
    stats["total_requests"] += 1
    if success:
        stats["success_count"] += 1
        if latency:
            stats["latencies"].append(latency)
    else:
        stats["fail_count"] += 1
    
    # 保存统计
    STATS_DIR.mkdir(parents=True, exist_ok=True)
    with open(stats_file, 'w') as f:
        json.dump(stats, f)


def get_order_info():
    """获取订单信息"""
    result = call_api()
    
    if not result["success"]:
        return result
    
    order = result["data"]["order_info"]
    ip_count = len(result["data"]["ip_list"])
    
    return {
        "success": True,
        "order_info": {
            "order_id": order.get("order_id", "未知"),
            "max_concurrency": order.get("max_concurrency", 0),
            "expire_time": order.get("expire_time", "未知"),
            "bandwidth": order.get("bandwidth", "未知"),
            "ip_count": ip_count
        },
        "ip_list_sample": result["data"]["ip_list"][:3] if result["data"]["ip_list"] else []
    }


def get_proxy_ip(product_type="TPS", num=1):
    """
    获取代理IP
    
    Args:
        product_type: 产品类型 (TPS/DPS/KPS/FPS/SFPS)
        num: 提取数量（仅私密代理DPS支持）
    
    Returns:
        dict: {"success": bool, "data": {"ip_list": [...]}, "error": str}
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
    timeout = config.get("timeout", DEFAULT_TIMEOUT)
    
    # 选择API URL
    if product_type in CURRENT_IP_URLS:
        # 隧道代理当前IP
        api_url = CURRENT_IP_URLS[product_type]
        request_params = {
            "secret_id": creds["secret_id"],
            "signature": creds["signature"]
        }
    elif product_type in PROXY_API_URLS:
        # 其他代理类型
        api_url = PROXY_API_URLS[product_type]
        request_params = {
            "secret_id": creds["secret_id"],
            "signature": creds["signature"]
        }
        # 私密代理支持num参数
        if product_type == "DPS":
            request_params["num"] = num
    else:
        return {"success": False, "error": f"不支持的产品类型: {product_type}"}
    
    try:
        # 脱敏日志
        masked_params = f"secret_id={mask_secret(creds['secret_id'])}&signature={mask_secret(creds['signature'])}"
        print(f"[API调用] {api_url}?{masked_params}")
        
        response = requests.get(api_url, params=request_params, timeout=timeout)
        response.raise_for_status()
        
        # 检查响应类型
        content_type = response.headers.get('content-type', '')
        
        if 'text/plain' in content_type or 'text' in content_type:
            # 文本格式解析
            text = response.text.strip()
            ip_list = []
            
            # 快代理隧道代理格式：host:port:username:password
            if ':' in text:
                parts = text.split(':')
                if len(parts) >= 4:
                    ip_list.append({
                        "host": parts[0],
                        "port": parts[1],
                        "username": parts[2],
                        "password": parts[3],
                        "full_address": f"http://{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}"
                    })
                elif len(parts) == 2:
                    # 单IP格式
                    ip_list.append({
                        "ip": parts[0],
                        "port": parts[1],
                        "full_address": f"{parts[0]}:{parts[1]}"
                    })
            
            return {
                "success": True,
                "data": {
                    "ip_list": ip_list,
                    "raw_text": text
                }
            }
        
        # JSON格式解析
        data = response.json()
        
        if data.get("code") != 0:
            return {
                "success": False,
                "error": data.get("msg", "API返回错误")
            }
        
        # 解析代理列表
        ip_list = []
        if "data" in data:
            # 私密代理格式
            if "proxy_list" in data["data"]:
                for proxy in data["data"]["proxy_list"]:
                    ip_list.append({
                        "host": proxy.get("ip", ""),
                        "port": proxy.get("port", ""),
                        "username": proxy.get("username", ""),
                        "password": proxy.get("password", ""),
                        "full_address": f"http://{proxy.get('username', '')}:{proxy.get('password', '')}@{proxy.get('ip', '')}:{proxy.get('port', '')}"
                    })
            # 隧道IP格式
            elif "ip" in data["data"]:
                ip_list.append({
                    "ip": data["data"]["ip"],
                    "full_address": data["data"]["ip"]
                })
        
        return {
            "success": True,
            "data": {
                "ip_list": ip_list
            },
            "raw": data
        }
    
    except requests.exceptions.Timeout:
        return {"success": False, "error": "API调用超时"}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"API调用失败: {str(e)}"}
    except json.JSONDecodeError:
        return {"success": False, "error": "API返回数据格式异常"}


# 命令行入口
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='代理API调用工具')
    parser.add_argument('command', choices=['get', 'order', 'get_ip'], help='命令类型')
    parser.add_argument('--product', default='TPS', help='产品类型 (TPS/DPS/KPS/FPS/SFPS/TPS_PRO)')
    parser.add_argument('--num', type=int, default=1, help='提取数量（仅DPS）')
    args = parser.parse_args()
    
    if args.command == 'get':
        result = call_api(args.product)
        if result["success"]:
            print(f"[OK] 获取到 {len(result['data']['ip_list'])} 个代理IP")
            for ip in result['data']['ip_list'][:5]:
                print(f"  {ip['full_address']}")
        else:
            print(f"[错误] {result['error']}")
    
    elif args.command == 'order':
        result = get_order_info()
        if result["success"]:
            print("[订单信息]")
            info = result["order_info"]
            print(f"  订单ID: {info['order_id']}")
            print(f"  并发上限: {info['max_concurrency']}")
            print(f"  到期时间: {info['expire_time']}")
            print(f"  带宽: {info['bandwidth']}")
            print(f"  IP数量: {info['ip_count']}")
        else:
            print(f"[错误] {result['error']}")
    
    elif args.command == 'get_ip':
        result = get_proxy_ip(args.product, args.num)
        if result["success"]:
            ip_list = result["data"]["ip_list"]
            print(f"[OK] 获取到 {len(ip_list)} 个代理IP")
            for ip in ip_list:
                print(f"  {ip.get('full_address', ip)}")
        else:
            print(f"[错误] {result['error']}")