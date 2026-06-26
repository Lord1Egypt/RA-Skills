#!/usr/bin/env python3
"""
工作流引擎集成测试脚本

测试项目:
1. Hook 服务健康检查
2. 工作流消息处理
3. 非工作流消息放行
4. 多轮对话状态保持
5. 会话超时清理
"""

import json
import sys
import time
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# 配置
HOOK_URL = "http://127.0.0.1:8765"
HOOK_TOKEN = "6fb57eb806f64da4e70b1b7a8c41f6b97a4788dc9f6b15430cdfedc0b61c75b1"

def make_request(endpoint, data=None):
    """发送 HTTP 请求"""
    url = f"{HOOK_URL}{endpoint}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {HOOK_TOKEN}',
    }
    
    if data:
        req = Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')
    else:
        req = Request(url, headers=headers, method='GET')
    
    try:
        with urlopen(req, timeout=5) as response:
            return json.loads(response.read().decode('utf-8'))
    except HTTPError as e:
        return {'error': f'HTTP {e.code}', 'body': e.read().decode('utf-8')}
    except URLError as e:
        return {'error': f'URL Error: {e.reason}'}
    except Exception as e:
        return {'error': str(e)}


def test_health():
    """测试 1: 健康检查"""
    print("\n📋 测试 1: 健康检查")
    print("-" * 50)
    
    result = make_request('/health')
    
    if 'error' in result:
        print(f"❌ 失败：{result['error']}")
        return False
    
    if result.get('status') == 'healthy':
        print(f"✅ 通过：服务健康，活跃会话数：{result.get('active_sessions', 0)}")
        return True
    else:
        print(f"❌ 失败：服务状态异常 {result}")
        return False


def test_workflow_message():
    """测试 2: 工作流消息处理"""
    print("\n📋 测试 2: 工作流消息处理（帮我开机）")
    print("-" * 50)
    
    data = {
        'event': 'inbound_message',
        'channel': 'openclaw-weixin',
        'from': 'test_user_workflow@im.wechat',
        'to': 'bot@im.wechat',
        'text': '帮我开机',
        'timestamp': int(time.time())
    }
    
    result = make_request('/hook', data)
    
    if 'error' in result:
        print(f"❌ 失败：{result['error']}")
        return False
    
    if result.get('handled') == True:
        response_text = result.get('response', '')
        print(f"✅ 通过：工作流已处理")
        print(f"   回复预览：{response_text[:100]}...")
        return True
    else:
        print(f"❌ 失败：工作流未匹配，reason={result.get('reason')}")
        return False


def test_non_workflow_message():
    """测试 3: 非工作流消息放行"""
    print("\n📋 测试 3: 非工作流消息放行（你好）")
    print("-" * 50)
    
    data = {
        'event': 'inbound_message',
        'channel': 'openclaw-weixin',
        'from': 'test_user_non_workflow@im.wechat',
        'to': 'bot@im.wechat',
        'text': '你好，今天天气怎么样？',
        'timestamp': int(time.time())
    }
    
    result = make_request('/hook', data)
    
    if 'error' in result:
        print(f"❌ 失败：{result['error']}")
        return False
    
    if result.get('handled') == False:
        print(f"✅ 通过：消息已放行给 AI")
        print(f"   reason: {result.get('reason')}")
        return True
    else:
        print(f"❌ 失败：非工作流消息被错误处理")
        return False


def test_multi_turn_conversation():
    """测试 4: 多轮对话状态保持"""
    print("\n📋 测试 4: 多轮对话状态保持")
    print("-" * 50)
    
    session_id = f'test_multi_turn_{int(time.time())}@im.wechat'
    
    # 第一轮：启动工作流
    print("  第 1 轮：启动添加设备工作流")
    data1 = {
        'event': 'inbound_message',
        'channel': 'openclaw-weixin',
        'from': session_id,
        'to': 'bot@im.wechat',
        'text': '添加网络唤醒',
        'timestamp': int(time.time())
    }
    result1 = make_request('/hook', data1)
    
    if not result1.get('handled'):
        print(f"❌ 失败：第一轮未启动工作流")
        return False
    
    response1 = result1.get('response', '')
    if '第一步' in response1 and '设备名称' in response1:
        print(f"  ✅ 第一轮通过：{response1[:50]}...")
    else:
        print(f"❌ 失败：第一轮回复异常：{response1}")
        return False
    
    # 第二轮：输入设备名称
    print("  第 2 轮：输入设备名称")
    data2 = {
        'event': 'inbound_message',
        'channel': 'openclaw-weixin',
        'from': session_id,
        'to': 'bot@im.wechat',
        'text': '测试电脑',
        'timestamp': int(time.time())
    }
    result2 = make_request('/hook', data2)
    
    if not result2.get('handled'):
        print(f"❌ 失败：第二轮工作流中断")
        return False
    
    response2 = result2.get('response', '')
    if '第二步' in response2 and 'MAC' in response2:
        print(f"  ✅ 第二轮通过：{response2[:50]}...")
    else:
        print(f"❌ 失败：第二轮回复异常：{response2}")
        return False
    
    # 第三轮：输入 MAC 地址
    print("  第 3 轮：输入 MAC 地址")
    data3 = {
        'event': 'inbound_message',
        'channel': 'openclaw-weixin',
        'from': session_id,
        'to': 'bot@im.wechat',
        'text': 'AA:BB:CC:DD:EE:FF',
        'timestamp': int(time.time())
    }
    result3 = make_request('/hook', data3)
    
    if not result3.get('handled'):
        print(f"❌ 失败：第三轮工作流中断")
        return False
    
    response3 = result3.get('response', '')
    if '第三步' in response3 or '备注' in response3 or '成功' in response3:
        print(f"  ✅ 第三轮通过：{response3[:50]}...")
    else:
        print(f"❌ 失败：第三轮回复异常：{response3}")
        return False
    
    print(f"✅ 通过：多轮对话状态保持正常")
    return True


def test_exit_command():
    """测试 5: 退出命令"""
    print("\n📋 测试 5: 退出命令")
    print("-" * 50)
    
    session_id = f'test_exit_{int(time.time())}@im.wechat'
    
    # 启动工作流
    data1 = {
        'event': 'inbound_message',
        'channel': 'openclaw-weixin',
        'from': session_id,
        'to': 'bot@im.wechat',
        'text': '添加网络唤醒',
        'timestamp': int(time.time())
    }
    make_request('/hook', data1)
    
    # 发送退出命令
    print("  发送退出命令")
    data2 = {
        'event': 'inbound_message',
        'channel': 'openclaw-weixin',
        'from': session_id,
        'to': 'bot@im.wechat',
        'text': '退出',
        'timestamp': int(time.time())
    }
    result2 = make_request('/hook', data2)
    
    if result2.get('handled'):
        response = result2.get('response', '')
        if '退出' in response:
            print(f"  ✅ 通过：退出命令已处理：{response}")
            return True
    
    print(f"❌ 失败：退出命令未正确处理")
    return False


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("工作流引擎集成测试")
    print("=" * 60)
    
    tests = [
        ("健康检查", test_health),
        ("工作流消息处理", test_workflow_message),
        ("非工作流消息放行", test_non_workflow_message),
        ("多轮对话状态保持", test_multi_turn_conversation),
        ("退出命令", test_exit_command),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"\n💥 {name} 测试异常：{e}")
            results.append((name, False))
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{status}: {name}")
    
    print("-" * 60)
    print(f"总计：{passed_count}/{total_count} 通过")
    
    if passed_count == total_count:
        print("\n🎉 所有测试通过！集成成功！")
        return True
    else:
        print(f"\n⚠️  {total_count - passed_count} 个测试失败，请检查日志。")
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
