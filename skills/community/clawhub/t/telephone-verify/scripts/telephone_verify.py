#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手机号码三要素核验脚本
使用聚合数据 (Juhe) 运营商实名认证 API

Usage:
    python3 telephone_verify.py --mobile "13800000000" --name "张三" --idcard "44030419900101001X"
"""

import requests
import argparse
import json
import sys
import os
from pathlib import Path


def get_api_key():
    """从配置文件或环境变量获取 API Key"""
    workspace = Path.home() / ".openclaw" / "workspace"
    
    # 方法 1: 从 openclaw.json 读取
    config_file = Path.home() / ".openclaw" / "openclaw.json"
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                api_key = config.get('env', {}).get('vars', {}).get('JUHE_TELEPHONE_VERIFY_KEY')
                if api_key and api_key != "需要配置":
                    return api_key
        except Exception:
            pass
    
    # 方法 2: 从环境变量读取
    api_key = os.getenv('JUHE_TELEPHONE_VERIFY_KEY')
    if api_key:
        return api_key
    
    # 方法 3: 提示用户配置
    print("❌ 未找到 API Key 配置")
    print("\n请在以下位置之一配置 JUHE_TELEPHONE_VERIFY_KEY:")
    print("  1. ~/.openclaw/openclaw.json 的 env.vars 中")
    print("  2. 环境变量 JUHE_TELEPHONE_VERIFY_KEY")
    print("\n获取 API Key: https://www.juhe.cn/")
    sys.exit(1)


def verify_telecom(name: str, idcard: str, mobile: str) -> dict:
    """
    核验手机号码三要素
    
    Args:
        name: 真实姓名
        idcard: 身份证号码
        mobile: 手机号码
    
    Returns:
        核验结果字典
    """
    api_url = 'https://v.juhe.cn/telecom/query'
    api_key = get_api_key()
    
    # 请求参数
    params = {
        'key': api_key,
        'realname': name,
        'idcard': idcard,
        'mobile': mobile,
    }
    
    try:
        # 发起请求
        response = requests.get(api_url, params=params, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            return parse_result(result)
        else:
            return {
                'success': False,
                'error': f'HTTP 错误：{response.status_code}',
                'raw': None
            }
    
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': f'网络请求异常：{str(e)}',
            'raw': None
        }
    except json.JSONDecodeError as e:
        return {
            'success': False,
            'error': f'JSON 解析错误：{str(e)}',
            'raw': response.text if response else None
        }


def parse_result(result: dict) -> dict:
    """
    解析 API 响应结果
    
    Args:
        result: API 原始响应
    
    Returns:
        标准化结果
    """
    error_code = result.get('error_code', '')
    reason = result.get('reason', '')
    
    # 查询成功
    if error_code == 0:
        data = result.get('result', {})
        res = data.get('res', 0)
        resmsg = data.get('resmsg', '')
        
        # 根据 res 判断结果
        if res == 1:
            return {
                'success': True,
                'verified': True,
                'message': '✅ 三要素信息一致',
                'result': data
            }
        elif res == 2:
            return {
                'success': True,
                'verified': False,
                'message': '❌ 三要素信息不一致',
                'result': data
            }
        else:
            return {
                'success': True,
                'verified': None,
                'message': f'核验结果：{resmsg}',
                'result': data
            }
    
    # 其他错误
    error_map = {
        '220803': '查询无此记录',
        '220807': '参数错误：姓名不合法',
        '220808': '身份证号格式错误',
        '220809': '手机号格式错误',
        '400': '请求参数错误',
        '401': 'API Key 错误或无权限',
        '403': '无权限访问',
        '500': '服务器异常',
    }
    
    error_msg = error_map.get(str(error_code), reason or '未知错误')
    return {
        'success': False,
        'error': f'错误 {error_code}: {error_msg}',
        'code': error_code,
        'reason': reason
    }


def main():
    parser = argparse.ArgumentParser(
        description='手机号码三要素核验',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python3 telephone_verify.py --mobile "13800000000" --name "张三" --idcard "44030419900101001X"
        """
    )
    
    parser.add_argument('--mobile', '-m', required=True, help='手机号码')
    parser.add_argument('--name', '-n', required=True, help='真实姓名')
    parser.add_argument('--idcard', '-i', required=True, help='身份证号码')
    parser.add_argument('--json', action='store_true', help='以 JSON 格式输出结果')
    
    args = parser.parse_args()
    
    # 执行核验
    result = verify_telecom(args.name, args.idcard, args.mobile)
    
    # 输出结果
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if result['success']:
            print(result['message'])
            if result.get('result'):
                r = result['result']
                if r.get('type'):
                    print(f"运营商：{r['type']}")
                if r.get('province'):
                    print(f"省份：{r['province']}")
                if r.get('city'):
                    print(f"城市：{r['city']}")
        else:
            print(f"❌ {result.get('error', '核验失败')}")
        
        print(f"\n姓名：{args.name}")
        print(f"身份证号：{args.idcard}")
        print(f"手机号：{args.mobile}")


if __name__ == '__main__':
    main()
