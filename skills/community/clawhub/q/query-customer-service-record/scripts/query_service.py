#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
霍小钉客户服务记录查询脚本
调用客户搜索接口和服务小计查询接口
"""

import json
import sys
import io
import requests
from datetime import datetime

# Windows 控制台 UTF-8 编码支持
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def search_customer(base_url, customer_name):
    """
    搜索客户，返回匹配的客户列表
    
    Args:
        base_url: API 基础 URL (如 https://hxd.ahdingtalk.com:8843)
        customer_name: 客户名称
    
    Returns:
        tuple: (success, data_or_error)
            - success=True: data_or_error 是客户名称列表
            - success=False: data_or_error 是错误信息
    """
    url = f"{base_url}/hxd/customerInfo/search"
    payload = {"customerName": customer_name}
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        if result.get("code") == 0:
            return True, result.get("data", [])
        else:
            return False, f"搜索失败：{result.get('message', '未知错误')}"
    except requests.exceptions.RequestException as e:
        return False, f"网络请求失败：{str(e)}"
    except json.JSONDecodeError as e:
        return False, f"响应解析失败：{str(e)}"

def search_service_records(base_url, customer_name, start_time, end_time):
    """
    查询客户服务小计记录
    
    Args:
        base_url: API 基础 URL
        customer_name: 客户名称
        start_time: 开始时间 (YYYY-MM-DD)
        end_time: 结束时间 (YYYY-MM-DD)
    
    Returns:
        tuple: (success, data_or_error)
            - success=True: data_or_error 是服务记录列表
            - success=False: data_or_error 是错误信息
    """
    url = f"{base_url}/hxd/sales_server_record/search"
    payload = {
        "customerName": customer_name,
        "startTime": start_time,
        "endTime": end_time
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        if result.get("code") == 0:
            return True, result.get("data", [])
        else:
            return False, f"查询失败：{result.get('message', '未知错误')}"
    except requests.exceptions.RequestException as e:
        return False, f"网络请求失败：{str(e)}"
    except json.JSONDecodeError as e:
        return False, f"响应解析失败：{str(e)}"

def format_service_summary(records):
    """
    格式化服务记录摘要
    
    Args:
        records: 服务记录列表
    
    Returns:
        str: 格式化的摘要文本
    """
    if not records:
        return "暂无服务记录"
    
    summary_lines = [f"共找到 {len(records)} 条服务记录："]
    
    for record in records:
        # 支持多种字段名（接口可能返回 createTime 或 time）
        time = record.get("createTime") or record.get("time") or "未知时间"
        sales = record.get("createName") or record.get("salesName") or "未知销售"
        server_type = record.get("serverType") or record.get("type") or ""
        content = record.get("serverContent") or record.get("content") or "无内容"
        
        # 格式化服务方式（如果有）
        type_str = f" [{server_type}]" if server_type else ""
        summary_lines.append(f"• {time} - {sales}{type_str}: {content}")
    
    return "\n".join(summary_lines)

def main():
    """
    主函数：处理命令行参数并执行查询
    
    用法:
        python query_service.py <action> <base_url> <customer_name> [start_time] [end_time]
    
    action: "search" 或 "records"
        - search: 搜索客户
        - records: 查询服务记录
    """
    if len(sys.argv) < 4:
        print(json.dumps({"success": False, "error": "参数不足"}))
        sys.exit(1)
    
    action = sys.argv[1]
    base_url = sys.argv[2].rstrip('/')
    customer_name = sys.argv[3]
    
    if action == "search":
        success, result = search_customer(base_url, customer_name)
        if success:
            print(json.dumps({"success": True, "data": result}, ensure_ascii=False))
        else:
            print(json.dumps({"success": False, "error": result}, ensure_ascii=False))
    
    elif action == "records":
        if len(sys.argv) < 6:
            # 默认查询当天
            today = datetime.now().strftime("%Y-%m-%d")
            start_time = today
            end_time = today
        else:
            start_time = sys.argv[4]
            end_time = sys.argv[5]
        
        success, result = search_service_records(base_url, customer_name, start_time, end_time)
        if success:
            summary = format_service_summary(result)
            print(json.dumps({
                "success": True,
                "data": result,
                "summary": summary
            }, ensure_ascii=False))
        else:
            print(json.dumps({"success": False, "error": result}, ensure_ascii=False))
    
    else:
        print(json.dumps({"success": False, "error": f"未知操作：{action}"}))
        sys.exit(1)

if __name__ == "__main__":
    main()
