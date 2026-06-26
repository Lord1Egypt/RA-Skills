#!/usr/bin/env python3
"""
友盟推送助手 - 查询应用数据
调用三个 API 接口获取应用的消息概览、诊断摘要和诊断报告
"""

import json
import os
import sys
import urllib.request
import urllib.error

COOKIE_FILE = os.path.expanduser("~/.qoderwork/skills/umeng-push-helper/cookie.txt")

def load_cookie():
    """从文件加载 Cookie"""
    if not os.path.exists(COOKIE_FILE):
        return None
    with open(COOKIE_FILE, 'r') as f:
        return f.read().strip()

def extract_ctoken(cookie):
    """从 Cookie 字符串中提取 ctoken 值"""
    for item in cookie.split(';'):
        item = item.strip()
        if item.startswith('ctoken='):
            return item.split('=', 1)[1]
    return None

def make_request(url, data):
    """发起 HTTP POST 请求"""
    cookie = load_cookie()
    if not cookie:
        print("ERROR: 未找到 Cookie，请先登录并保存 Cookie", file=sys.stderr)
        sys.exit(1)
    
    # 提取 ctoken 用于 x-csrf-token 头
    ctoken = extract_ctoken(cookie)
    
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "Cookie": cookie,
        "x-csrf-token": ctoken if ctoken else ""
    }
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return {
                'success': True,
                'data': result
            }
                
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else ''
        return {
            'success': False,
            'error': f'HTTP {e.code}',
            'message': error_body
        }
    except urllib.error.URLError as e:
        return {
            'success': False,
            'error': '网络错误',
            'message': str(e.reason)
        }
    except Exception as e:
        return {
            'success': False,
            'error': '未知错误',
            'message': str(e)
        }

def query_message_overview(appkey):
    """查询消息概览 - 接口 1"""
    url = "https://upush.umeng.com/hsf/push/messageOverview"
    data = {
        "appkey": appkey,
        "dateType": "7d"
    }
    
    print(f"\n📊 正在查询消息概览...")
    result = make_request(url, data)
    
    if result['success']:
        print("✅ 消息概览查询成功")
        response_data = result['data']
        
        if 'data' in response_data and 'list' in response_data['data']:
            data_list = response_data['data']['list']
            print("\n消息概览数据：")
            for item in data_list:
                name = item.get('name', 'N/A')
                value = item.get('value', 'N/A')
                print(f"  • {name}: {value}")
        else:
            print("⚠️  未找到 list 数据")
            print(json.dumps(response_data, indent=2, ensure_ascii=False))
        
        return response_data.get('data', {})
    else:
        print(f"❌ 查询失败：{result['error']} - {result['message']}")
        return None

def query_diagnosis_summary(appkey):
    """查询诊断摘要 - 接口 2"""
    url = "https://upush.umeng.com/hsf/push/diagnosisSummery"
    data = {
        "appkey": appkey,
        "dateType": "7d"
    }
    
    print(f"\n📋 正在查询诊断摘要...")
    result = make_request(url, data)
    
    if result['success']:
        print("✅ 诊断摘要查询成功")
        response_data = result['data']
        
        if 'data' in response_data:
            summary_data = response_data['data']
            print("\n诊断摘要数据：")
            print(json.dumps(summary_data, indent=2, ensure_ascii=False))
            return summary_data
        else:
            print("⚠️  未找到 data 数据")
            print(json.dumps(response_data, indent=2, ensure_ascii=False))
            return {}
    else:
        print(f"❌ 查询失败：{result['error']} - {result['message']}")
        return None

def query_diagnosis_report(appkey):
    """查询诊断报告 - 接口 3"""
    url = "https://upush.umeng.com/hsf/push/diagnosisReport"
    data = {
        "appkey": appkey,
        "dateType": "7d"
    }
    
    print(f"\n📑 正在查询诊断报告...")
    result = make_request(url, data)
    
    if result['success']:
        print("✅ 诊断报告查询成功")
        response_data = result['data']
        
        # 提取 data 值
        report_data = response_data.get('data', None)
        
        print("\n诊断报告分析：")
        if report_data is not None:
            # 简单分析报告数据
            if isinstance(report_data, dict):
                print("\n报告数据结构：")
                print(json.dumps(report_data, indent=2, ensure_ascii=False))
                
                # 尝试进行简单分析
                print("\n📈 简单分析：")
                if 'score' in report_data:
                    print(f"  • 健康得分：{report_data['score']}")
                if 'issues' in report_data or 'problems' in report_data:
                    issues = report_data.get('issues', report_data.get('problems', []))
                    if issues:
                        print(f"  • 发现问题数：{len(issues)}")
                        for i, issue in enumerate(issues[:5], 1):
                            print(f"    {i}. {issue}")
                if 'suggestions' in report_data or 'recommendations' in report_data:
                    suggestions = report_data.get('suggestions', report_data.get('recommendations', []))
                    if suggestions:
                        print(f"  • 建议数量：{len(suggestions)}")
                        for i, suggestion in enumerate(suggestions[:3], 1):
                            print(f"    {i}. {suggestion}")
            else:
                print(f"报告数据：{report_data}")
        else:
            print("⚠️  data 值为空")
            print("\n完整响应：")
            print(json.dumps(response_data, indent=2, ensure_ascii=False))
        
        return report_data
    else:
        print(f"❌ 查询失败：{result['error']} - {result['message']}")
        return None

def main():
    if len(sys.argv) < 2:
        print("使用方法：python query_app_data.py <appkey>")
        print("示例：python query_app_data.py EXAMPLE_APPKEY_004")
        sys.exit(1)
    
    appkey = sys.argv[1]
    
    print("=" * 60)
    print(f"友盟推送数据查询")
    print(f"AppKey: {appkey}")
    print(f"时间范围：最近 7 天 (7d)")
    print("=" * 60)
    
    # 依次调用三个接口
    overview_data = query_message_overview(appkey)
    summary_data = query_diagnosis_summary(appkey)
    report_data = query_diagnosis_report(appkey)
    
    print("\n" + "=" * 60)
    print("✅ 所有查询完成")
    print("=" * 60)

if __name__ == "__main__":
    main()
