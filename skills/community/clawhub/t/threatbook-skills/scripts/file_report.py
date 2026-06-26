#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微步在线文件信誉报告查询
API文档: https://x.threatbook.com/v5/apiDocs#/file/report
"""

import os
import sys
import argparse
import json
import requests


def get_file_report(hash_value: str) -> dict:
    """
    查询文件的威胁情报报告
    
    Args:
        hash_value: 文件的sha256/md5/sha1值
    
    Returns:
        dict: 文件威胁情报报告
    """
    # 获取API Key
    
    api_key = os.getenv("THREATBOOK_API_KEY")
    
    if not api_key:
        raise ValueError("缺少API Key配置，请先配置微步在线API凭证")
    
    # 验证hash值
    hash_value = hash_value.strip().lower()
    if not hash_value:
        raise ValueError("hash值不能为空")
    
    hash_len = len(hash_value)
    if hash_len not in [32, 40, 64]:
        raise ValueError(f"无效的hash长度: {hash_len}，应为32(md5)、40(sha1)或64(sha256)")
    
    # 构建请求
    url = "https://api.threatbook.cn/v3/file/report"
    headers = {
        "Authorization": api_key
    }
    params = {
        "hash": hash_value
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
        description="查询文件的威胁情报报告",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--hash_value",
        required=True,
        help="文件的sha256/md5/sha1值"
    )
    
    args = parser.parse_args()
    
    try:
        result = get_file_report(args.hash_value)
        
        # 提取关键信息
        threat_level = result.get("threat_level", "unknown")
        threat_level_desc = {
            "malicious": "恶意",
            "suspicious": "可疑",
            "benign": " benign",
            "unknown": "未知"
        }.get(threat_level, threat_level)
        
        sha256 = result.get("sha256", "")
        md5 = result.get("md5", "")
        sha1 = result.get("sha1", "")
        
        print(f"文件威胁情报报告")
        print(f"=" * 50)
        print(f"威胁等级: {threat_level_desc} ({threat_level})")
        print(f"SHA256: {sha256}")
        print(f"MD5: {md5}")
        print(f"SHA1: {sha1}")
        print(f"\n完整结果:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
