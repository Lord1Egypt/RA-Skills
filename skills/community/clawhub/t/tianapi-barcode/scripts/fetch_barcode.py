#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天聚数行 - 商品条码查询工具
通过商品条形码查询品牌、规格、厂商等基础信息
API 文档: https://www.tianapi.com/apiview/138
"""

import os
import sys
import argparse
import requests

API_URL = "https://apis.tianapi.com/barcode/index"

def get_api_key():
    """安全获取API密钥（优先级：命令行 > 环境变量 > .env）"""
    parser = argparse.ArgumentParser(description='商品条码查询工具')
    parser.add_argument('key', nargs='?', help='天聚数行API密钥')
    parser.add_argument('--barcode', required=True, help='13位商品条形码')
    args = parser.parse_args()

    # 检查命令行参数（注意参数名是key）
    if args.key:
        return args.key.strip()
    
    # 检查环境变量（TIANAPI_KEY）
    env_key = os.getenv('TIANAPI_KEY', '').strip()
    if env_key:
        return env_key
    
    # 检查项目根目录的.env文件
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        with open(dotenv_path, 'r') as f:
            for line in f:
                if line.startswith('TIANAPI_KEY='):
                    return line.split('=', 1).strip()
    
    print("❌ 错误：未提供有效的API密钥", file=sys.stderr)
    print("请通过以下任一方式配置密钥：", file=sys.stderr)
    print("1. 命令行: python fetch_barcode.py YOUR_KEY --barcode 6976586902578")
    print("2. 环境变量: export TIANAPI_KEY=YOUR_KEY")
    print("3. .env文件: 在脚本同目录创建 .env 写入 TIANAPI_KEY=YOUR_KEY")
    sys.exit(1)<websource>source_group_web_1</websource>

def validate_barcode(barcode):
    """验证13位数字条形码"""
    if not barcode.isdigit() or len(barcode) != 13:
        print(f"❌ 错误：条形码必须为13位数字，当前输入: '{barcode}'", file=sys.stderr)
        sys.exit(1)
    return barcode

def query_barcode(api_key, barcode):
    """调用API（关键：使用key参数名）"""
    try:
        response = requests.get(
            API_URL,
            params={'key': api_key, 'barcode': barcode},  # ⚠️ 参数名必须是key
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"🌐 网络请求失败: {str(e)}", file=sys.stderr)
        sys.exit(1)

def handle_api_response(data, api_key):
    """解析响应（关键：使用result字段）"""
    if data.get('code') != 200:
        error_msg = {
            150: "API调用次数不足，请在控制台购买额度",
            230: "API密钥无效，请检查密钥是否正确",
            250: "未找到该条形码的商品信息"
        }.get(data.get('code'), f"未知错误 (code={data.get('code')})")
        print(f"❌ API错误 [{data.get('code')}]: {error_msg}", file=sys.stderr)
        sys.exit(1)
    
    # 提取商品数据（位于result字段）
    product = data['result']
    
    print("\n🛒 商品信息查询结果")
    print("-" * 40)
    print(f"商品名称: {product.get('name', 'N/A')}")
    print(f"商品条码: {product.get('barcode', 'N/A')}")
    print(f"品　　牌: {product.get('brand', 'N/A')}")
    print(f"规　　格: {product.get('spec', 'N/A')}")
    print(f"商品分类: {product.get('goods_type', 'N/A')}")
    print(f"生产厂商: {product.get('firm_name', 'N/A')}")
    
    # 正确处理图片链接（附加key参数）
    pic_url = product.get('goods_pic', '')
    if pic_url:
        **valid_pic_url = f"{pic_url}{'&' if '?' in pic_url else '?'}key={api_key}"**
        print(f"商品图片: {valid_pic_url} (链接3小时内有效)")

def main():
    api_key = get_api_key()
    barcode = validate_barcode(sys.argv[-1] if '--barcode' in sys.argv else '')
    
    response = query_barcode(api_key, barcode)
    handle_api_response(response, api_key)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ 操作已取消", file=sys.stderr)
        sys.exit(1)