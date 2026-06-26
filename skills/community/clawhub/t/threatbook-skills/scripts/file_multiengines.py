#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微步在线文件反病毒引擎检测报告
API文档: https://x.threatbook.com/v5/apiDocs#/file/report_multiengines
"""

import os
import sys
import argparse
import json
import requests


def get_multiengines_report(hash_value: str) -> dict:
    """
    查询文件的多引擎反病毒检测报告
    
    Args:
        hash_value: 文件的sha256/md5/sha1值
    
    Returns:
        dict: 多引擎检测报告
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
    url = "https://api.threatbook.cn/v3/file/report/multiengines"
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
        description="查询文件的多引擎反病毒检测报告",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--hash_value",
        required=True,
        help="文件的sha256/md5/sha1值"
    )
    
    args = parser.parse_args()
    
    try:
        result = get_multiengines_report(args.hash_value)
        
        # 提取关键信息
        multiengines = result.get("multiengines", {})
        if isinstance(multiengines, dict):
            # 统计检测结果
            total = len(multiengines)
            detected = sum(1 for v in multiengines.values() if v and v.get("detected", False))
            
            print(f"多引擎反病毒检测报告")
            print(f"=" * 50)
            print(f"检测引擎总数: {total}")
            print(f"检测为恶意的引擎数: {detected}")
            print(f"检测率: {detected}/{total} ({detected*100//total if total > 0 else 0}%)")
            
            # 显示各引擎结果
            if multiengines:
                print(f"\n各引擎检测结果:")
                for engine, detail in multiengines.items():
                    if isinstance(detail, dict):
                        detected_status = "恶意" if detail.get("detected", False) else "clean"
                        malware_name = detail.get("result", "")
                        print(f"  - {engine}: {detected_status} {malware_name}")
        
        print(f"\n完整结果:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
