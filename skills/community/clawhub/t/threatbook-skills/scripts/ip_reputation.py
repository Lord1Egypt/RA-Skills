#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微步在线IP信誉查询
API文档: https://x.threatbook.com/v5/apiDocs#/ip/reputation
"""

import os
import sys
import argparse
import json
import re
import requests


def get_ip_reputation(ip: str, api_key: str) -> dict:
    """
    查询IP地址的威胁情报信息
    
    Args:
        ip: IP地址（IPv4或IPv6）
        api_key: 微步在线API Key
    
    Returns:
        dict: IP威胁情报信息
    """
    # 验证IP地址
    ip = ip.strip()
    if not ip:
        raise ValueError("IP地址不能为空")
    
    # 简单的IP格式验证
    ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if not re.match(ipv4_pattern, ip):
        # 可能是IPv6，不做严格验证
        pass
    else:
        # 验证IPv4各段范围
        parts = ip.split('.')
        if not all(0 <= int(part) <= 255 for part in parts):
            raise ValueError(f"无效的IPv4地址: {ip}")
    
    # 构建请求
    url = "https://api.threatbook.cn/v3/scene/ip_reputation"
    params = {
        "apikey": api_key,
        "resource": ip
    }
    
    try:
        # 发起请求
        response = requests.get(
            url,
            params=params,
            timeout=30
        )
        
        # 检查HTTP状态码
        if response.status_code >= 400:
            raise Exception(f"HTTP请求失败: 状态码 {response.status_code}, 响应内容: {response.text}")
        
        # 解析响应
        data = response.json()
        
        # 检查API响应码
        response_code = data.get("response_code", -1)
        if response_code != 0:
            error_msg = data.get("verbose_msg", "未知错误")
            raise Exception(f"API错误[{response_code}]: {error_msg}")
        
        return data
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"网络请求失败: {str(e)}")
    except json.JSONDecodeError as e:
        raise Exception(f"响应解析失败: {str(e)}")


def main():
    parser = argparse.ArgumentParser(
        description="查询IP地址的威胁情报信息",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--ip",
        required=True,
        help="待查询的IP地址"
    )
    parser.add_argument(
        "--api_key",
        required=True,
        help="微步在线API Key"
    )
    
    args = parser.parse_args()
    
    try:
        result = get_ip_reputation(args.ip, args.api_key)
        
        # 提取关键信息
        threat_level = result.get("threat_level", "unknown")
        threat_level_desc = {
            "malicious": "恶意",
            "suspicious": "可疑",
            "benign": "安全",
            "unknown": "未知"
        }.get(threat_level, threat_level)
        
        confidence = result.get("confidence", 0)
        tags = result.get("tags", [])
        judgments = result.get("judgments", [])
        
        print(f"IP威胁情报报告")
        print(f"=" * 50)
        print(f"IP地址: {args.ip}")
        print(f"威胁等级: {threat_level_desc} ({threat_level})")
        print(f"置信度: {confidence}")
        
        if tags:
            print(f"标签: {', '.join(tags)}")
        
        if judgments:
            print(f"\n判断依据:")
            for judgment in judgments:
                print(f"  - {judgment}")
        
        # 显示详细信息
        if "summary" in result:
            print(f"\n摘要: {result['summary']}")
        
        print(f"\n完整结果:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
