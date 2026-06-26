#!/usr/bin/env python3
"""
探索同程旅行API的测试脚本
尝试不同的参数组合，找到返回航班数据的真实API
"""

import requests
import json
import re
import time
from urllib.parse import urlencode

def test_url_params():
    """测试不同的URL参数组合"""
    base_url = "https://wx.17u.cn/cheapflights/newcomparepriceV2/single"
    
    test_cases = [
        # 基础参数
        {'depcity': '北京', 'arrcity': '上海', 'date': '2026-03-16'},
        # 添加format参数
        {'depcity': '北京', 'arrcity': '上海', 'date': '2026-03-16', 'format': 'json'},
        {'depcity': '北京', 'arrcity': '上海', 'date': '2026-03-16', '_format': 'json'},
        # 添加cabin参数
        {'depcity': '北京', 'arrcity': '上海', 'date': '2026-03-16', 'cabin': 'Y'},
        {'depcity': '北京', 'arrcity': '上海', 'date': '2026-03-16', 'cabin': 'economy'},
        # 添加airline参数
        {'depcity': '北京', 'arrcity': '上海', 'date': '2026-03-16', 'airline': ''},
        # 添加flightno参数
        {'depcity': '北京', 'arrcity': '上海', 'date': '2026-03-16', 'flightno': ''},
        # 添加sort参数
        {'depcity': '北京', 'arrcity': '上海', 'date': '2026-03-16', 'sort': 'price'},
        {'depcity': '北京', 'arrcity': '上海', 'date': '2026-03-16', 'sort': 'departure'},
        # 尝试POST请求
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': 'https://wx.17u.cn/',
    }
    
    for i, params in enumerate(test_cases):
        print(f"\n{'='*60}")
        print(f"测试用例 {i+1}: {params}")
        
        try:
            response = requests.get(base_url, params=params, headers=headers, timeout=10)
            print(f"状态码: {response.status_code}")
            print(f"内容类型: {response.headers.get('content-type')}")
            print(f"内容长度: {len(response.text)} 字符")
            
            # 检查是否包含航班数据关键词
            text = response.text.lower()
            keywords = ['flight', '航班', 'price', '价格', 'airline', '航空公司', 'departure', '出发', 'arrival', '到达']
            found_keywords = [kw for kw in keywords if kw in text]
            print(f"找到关键词: {found_keywords}")
            
            # 尝试提取__INITIAL_STATE__
            match = re.search(r'window\.__INITIAL_STATE__\s*=\s*({.*?});', response.text, re.DOTALL)
            if match:
                json_str = match.group(1)
                print(f"找到__INITIAL_STATE__，长度: {len(json_str)}")
                
                # 尝试解析
                try:
                    # 修复常见的JSON问题
                    json_str = re.sub(r':\s*undefined', ': null', json_str, flags=re.IGNORECASE)
                    data = json.loads(json_str)
                    
                    # 检查是否有航班数据
                    flight_keys = []
                    for key in data:
                        if isinstance(data[key], dict) and any(k in key.lower() for k in ['flight', 'air', '航班', '机票']):
                            flight_keys.append(key)
                        elif isinstance(data[key], list) and len(data[key]) > 0:
                            # 检查列表元素是否包含航班信息
                            first_item = data[key][0]
                            if isinstance(first_item, dict):
                                if any(field in first_item for field in ['flightNo', 'flightNumber', 'flight_code']):
                                    flight_keys.append(key)
                    
                    if flight_keys:
                        print(f"找到疑似航班数据的键: {flight_keys}")
                        # 保存到文件以便分析
                        with open(f'/tmp/test_case_{i+1}.json', 'w', encoding='utf-8') as f:
                            json.dump(data, f, ensure_ascii=False, indent=2)
                        print(f"数据已保存到 /tmp/test_case_{i+1}.json")
                        
                        # 尝试提取航班信息
                        for key in flight_keys[:2]:  # 只检查前两个
                            print(f"分析键 '{key}':")
                            item = data[key]
                            if isinstance(item, list) and len(item) > 0:
                                print(f"  列表长度: {len(item)}")
                                sample = item[0]
                                if isinstance(sample, dict):
                                    print(f"  示例字段: {list(sample.keys())[:10]}")
                            elif isinstance(item, dict):
                                print(f"  字典键: {list(item.keys())[:10]}")
                    else:
                        print("未找到航班数据")
                        
                except json.JSONDecodeError as e:
                    print(f"JSON解析失败: {e}")
            else:
                print("未找到__INITIAL_STATE__")
            
            # 检查是否有其他JSON数据
            json_matches = re.findall(r'\{[^{}]*\}', response.text[:5000])
            if json_matches:
                print(f"找到其他JSON对象: {len(json_matches)}个")
            
            # 休眠避免过快请求
            time.sleep(1)
            
        except Exception as e:
            print(f"请求异常: {e}")
            import traceback
            traceback.print_exc()

def test_other_endpoints():
    """测试其他可能的API端点"""
    endpoints = [
        "https://wx.17u.cn/cheapflights/newcomparepriceV2/list",
        "https://wx.17u.cn/cheapflights/newcomparepriceV2/data",
        "https://wx.17u.cn/cheapflights/api/flights",
        "https://wx.17u.cn/api/flights",
        "https://wx.17u.cn/flights/api/search",
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
    }
    
    params = {'depcity': '北京', 'arrcity': '上海', 'date': '2026-03-16'}
    
    for endpoint in endpoints:
        print(f"\n{'='*60}")
        print(f"测试端点: {endpoint}")
        
        try:
            response = requests.get(endpoint, params=params, headers=headers, timeout=10)
            print(f"状态码: {response.status_code}")
            print(f"内容类型: {response.headers.get('content-type')}")
            
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                if 'json' in content_type:
                    try:
                        data = response.json()
                        print(f"JSON响应键: {list(data.keys()) if isinstance(data, dict) else type(data)}")
                        # 保存以便分析
                        import os
                        filename = f"/tmp/endpoint_{endpoint.split('/')[-1]}.json"
                        os.makedirs(os.path.dirname(filename), exist_ok=True)
                        with open(filename, 'w', encoding='utf-8') as f:
                            json.dump(data, f, ensure_ascii=False, indent=2)
                        print(f"保存到: {filename}")
                    except:
                        print(f"响应文本前500字符: {response.text[:500]}")
                else:
                    print(f"响应文本前500字符: {response.text[:500]}")
            else:
                print(f"响应文本: {response.text[:500]}")
                
            time.sleep(1)
            
        except Exception as e:
            print(f"请求异常: {e}")

def check_page_for_api_calls():
    """检查页面中是否包含API调用URL"""
    base_url = "https://wx.17u.cn/cheapflights/newcomparepriceV2/single"
    params = {'depcity': '北京', 'arrcity': '上海', 'date': '2026-03-16'}
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    }
    
    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=10)
        
        # 查找可能的API URL模式
        patterns = [
            r'https?://[^"\']+\.17u\.cn[^"\']+(api|data|search|query|flights)[^"\']*',
            r'https?://[^"\']+\.ly\.com[^"\']+(api|data|search|query|flights)[^"\']*',
            r'"/[^"\']+(api|data|search|query|flights)[^"\']*\.json"',
            r'fetch\([^)]+\)',
            r'axios\.get\([^)]+\)',
            r'\.ajax\([^)]+\)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, response.text, re.IGNORECASE)
            if matches:
                print(f"\n找到模式 '{pattern}':")
                for match in matches[:5]:  # 只显示前5个
                    print(f"  {match}")
        
        # 保存页面源代码以便手动分析
        with open('/tmp/page_source.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"\n页面源代码已保存到 /tmp/page_source.html")
        
    except Exception as e:
        print(f"请求异常: {e}")

def main():
    """主函数"""
    print("开始探索同程旅行API...")
    
    print("\n1. 测试URL参数组合")
    test_url_params()
    
    print("\n\n2. 测试其他端点")
    test_other_endpoints()
    
    print("\n\n3. 检查页面中的API调用")
    check_page_for_api_calls()
    
    print("\n\n探索完成!")

if __name__ == '__main__':
    main()