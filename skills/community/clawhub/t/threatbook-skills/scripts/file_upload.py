#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微步在线文件上传分析
API文档: https://x.threatbook.com/v5/apiDocs#/file/upload
"""

import os
import sys
import argparse
import json
from pathlib import Path
import requests


def upload_file(file_path: str) -> dict:
    """
    上传文件到微步在线进行分析
    
    Args:
        file_path: 待分析的文件路径
    
    Returns:
        dict: API响应结果，包含文件hash和分析结果
    """
    # 获取API Key
    
    api_key = os.getenv("THREATBOOK_API_KEY")
    
    if not api_key:
        raise ValueError("缺少API Key配置，请先配置微步在线API凭证")
    
    # 检查文件是否存在
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    if not file_path.is_file():
        raise ValueError(f"路径不是文件: {file_path}")
    
    # 构建请求
    url = "https://api.threatbook.cn/v3/file/upload"
    headers = {
        "Authorization": api_key
    }
    
    try:
        # 读取文件内容
        with open(file_path, 'rb') as f:
            files = {
                'file': (file_path.name, f, 'application/octet-stream')
            }
            
            # 发起请求
            response = requests.post(
                url,
                headers=headers,
                files=files,
                timeout=60
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
        description="上传文件到微步在线进行威胁分析",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--file_path",
        required=True,
        help="待分析的文件路径"
    )
    
    args = parser.parse_args()
    
    try:
        result = upload_file(args.file_path)
        
        # 提取关键信息
        sha256 = result.get("sha256", "")
        md5 = result.get("md5", "")
        sha1 = result.get("sha1", "")
        
        print(f"文件上传成功！")
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
