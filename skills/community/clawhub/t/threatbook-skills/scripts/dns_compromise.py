#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微步在线失陷检测
API文档: https://x.threatbook.com/v5/apiDocs#/scene/dns
"""

import os
import sys
import argparse
import json
import re
import requests


def check_dns_compromise(resource: str) -> dict:
    """
    检测域名或IP是否存在失陷风险
    
    Args:
        resource: 域名或IP地址
    
    Returns:
        dict: 失陷检测结果
    """
    # 获取API Key
    
    api_key = os.getenv("THREATBOOK_API_KEY")
    
    if not api_key:
        raise ValueError("缺少API Key配置，请先配置微步在线API凭证")
    
    # 验证资源
    resource = resource.strip()
    if not resource:
        raise ValueError("域名或IP地址不能为空")
    
    # 构建请求
    url = "https://api.threatbook.cn/v3/scene/dns"
    headers = {
        "Authorization": api_key
    }
    params = {
        "resource": resource
    }
    
    try:
        # 发起请求
        response = requests.get(
            url,
            headers=headers,
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
        description="检测域名或IP是否存在失陷风险",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--resource",
        required=True,
        help="待检测的域名或IP地址"
    )
    
    args = parser.parse_args()
    
    try:
        result = check_dns_compromise(args.resource)
        
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
        
        print(f"失陷检测报告")
        print(f"=" * 50)
        print(f"检测目标: {args.resource}")
        print(f"威胁等级: {threat_level_desc} ({threat_level})")
        print(f"置信度: {confidence}")
        
        if tags:
            print(f"标签: {', '.join(tags)}")
        
        if judgments:
            print(f"\n判断依据:")
            for judgment in judgments:
                print(f"  - {judgment}")
        
        # 显示DNS相关信息
        if "dns_records" in result:
            print(f"\nDNS记录:")
            dns_records = result["dns_records"]
            if isinstance(dns_records, list):
                for record in dns_records:
                    print(f"  - {record}")
        
        # 显示关联信息
        if "related_samples" in result:
            print(f"\n关联样本:")
            samples = result["related_samples"]
            if isinstance(samples, list):
                for sample in samples[:5]:  # 只显示前5个
                    print(f"  - {sample}")
        
        # 显示威胁类型
        if "threat_types" in result:
            print(f"\n威胁类型:")
            threat_types = result["threat_types"]
            if isinstance(threat_types, list):
                for threat_type in threat_types:
                    print(f"  - {threat_type}")
        
        print(f"\n完整结果:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
