#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
友盟异常点检测接口封装
用于获取应用异动点的简要信息和归因报告链接

认证信息获取优先级：
1. 直接传入的参数（api_key, api_security）
2. umeng-config.json 配置文件
3. 环境变量（UMENG_API_KEY, UMENG_API_SECURITY）
"""

import os
import sys
import requests
import json
from datetime import datetime

# 导入配置管理模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from umeng_config import get_umeng_credentials


def get_umeng_outlier_points(appkey, ds, api_key=None, api_security=None):
    """
    获取友盟应用异常点数据
    
    Args:
        appkey (str): 应用唯一标识符
        ds (str): 查询日期，格式：YYYYMMDD
        api_key (str, optional): 友盟 OpenAPI Key（优先级最高）
        api_security (str, optional): 友盟 OpenAPI Security（优先级最高）
        
    Returns:
        dict: 异常点数据，包含 shareUrl（异动归因报告地址）
        
    Raises:
        ValueError: 认证信息未找到
        Exception: API 调用失败或认证错误
    """
    # 获取认证信息（按优先级：参数 > 配置文件 > 环境变量）
    try:
        creds = get_umeng_credentials(api_key, api_security)
        api_key = creds['apiKey']
        api_security = creds['apiSecurity']
    except ValueError as e:
        raise ValueError(str(e))
    
    # 构建请求 URL
    base_url = "https://mobile.umeng.com/ht/api/v3/ai/getOutlierPoints"
    params = {
        "ak": api_key,
        "sk": api_security,
        "appkey": appkey,
        "ds": ds
    }
    
    try:
        # 发送 GET 请求
        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()
        
        # 解析响应
        result = response.json()
        
        # 检查 API 响应状态
        if not result.get("status", False):
            raise Exception(f"API call failed: {result.get('msg', 'Unknown error')}")
        
        # 提取应用数据
        app_data = result.get("data", {}).get(appkey, {})
        if not app_data:
            raise Exception(f"No data found for appkey: {appkey}")
        
        return {
            "appKey": app_data.get("appKey"),
            "shareUrl": app_data.get("shareUrl"),
            "id": app_data.get("id"),
            "category": app_data.get("category"),
            "type": app_data.get("type"),
            "ds": app_data.get("ds"),
            "status": app_data.get("status"),
            "raw_response": result  # 保留原始响应供调试
        }
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"HTTP request failed: {str(e)}")
    except json.JSONDecodeError as e:
        raise Exception(f"Invalid JSON response: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to get outlier points: {str(e)}")


def format_outlier_report(outlier_data):
    """
    格式化异常点报告信息
    
    Args:
        outlier_data (dict): get_umeng_outlier_points 返回的数据
        
    Returns:
        str: 格式化的报告字符串
    """
    if not outlier_data:
        return "No outlier data available"
    
    report = f"""友盟异常点检测报告
==================

应用标识：{outlier_data.get('appKey', 'N/A')}
检测日期：{outlier_data.get('ds', 'N/A')}
异常类别：{outlier_data.get('category', 'N/A')}
异常级别：{outlier_data.get('type', 'N/A')}
报告状态：{'有效' if outlier_data.get('status') == 1 else '无效'}

📊 完整归因报告：{outlier_data.get('shareUrl', 'N/A')}

报告 ID: {outlier_data.get('id', 'N/A')}
"""
    return report


# 使用示例
if __name__ == "__main__":
    try:
        # 查询指定应用和日期的异常点
        appkey = "59892f08310c9307b60023d0"
        ds = "20260322"  # YYYYMMDD 格式
        
        outlier_data = get_umeng_outlier_points(appkey, ds)
        print(format_outlier_report(outlier_data))
        
    except Exception as e:
        print(f"Error: {e}")
