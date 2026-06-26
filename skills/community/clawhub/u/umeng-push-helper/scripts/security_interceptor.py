#!/usr/bin/env python3
"""
友盟推送助手 - API 请求安全拦截器
用于检查和阻止禁止调用的敏感接口
"""

import sys
import re

# 禁止调用的接口列表（黑名单）
FORBIDDEN_APIS = [
    {
        'url': 'https://upush.umeng.com/hsf/push/sendMsg',
        'name': '发送推送消息',
        'risk': '高危',
        'reason': '此操作会向用户发送推送消息，可能导致误操作或骚扰用户'
    },
    {
        'url': 'https://upush.umeng.com/hsf/setting/updateApp',
        'name': '修改应用配置',
        'risk': '高危',
        'reason': '此操作会修改应用配置，可能影响正常业务'
    },
    {
        'url': 'https://upush.umeng.com/hsf/setting/updateChannelInfo',
        'name': '修改渠道信息',
        'risk': '高危',
        'reason': '此操作会修改渠道配置，可能影响数据统计'
    },
    {
        'url': 'https://upush.umeng.com/hsf/setting/saveReceipt',
        'name': '保存回执配置',
        'risk': '中危',
        'reason': '此操作会修改回执配置，需要通过官方后台执行'
    }
]

# 允许调用的接口列表（白名单）
ALLOWED_APIS = [
    'https://upush.umeng.com/hsf/home/listAll',
    'https://upush.umeng.com/hsf/push/messageOverview',
    'https://upush.umeng.com/hsf/push/diagnosisSummery',
    'https://upush.umeng.com/hsf/push/diagnosisReport',
]

def check_api_url(url):
    """
    检查 URL 是否在禁止列表中
    
    参数:
        url: 要检查的 API URL
        
    返回:
        tuple: (is_allowed: bool, message: str)
    """
    if not url:
        return False, "URL 不能为空"
    
    # 去除 URL 两端的空白字符
    url = url.strip()
    
    # 检查是否在禁止列表中
    for forbidden in FORBIDDEN_APIS:
        if forbidden['url'] in url:
            return False, format_forbidden_message(forbidden)
    
    # 检查是否在允许列表中（可选，提供额外确认）
    for allowed in ALLOWED_APIS:
        if allowed in url:
            return True, f"✓ URL 验证通过：{allowed}"
    
    # 如果既不在禁止列表也不在允许列表，默认允许（保持向后兼容）
    return True, "URL 未在禁止列表中，允许调用"

def format_forbidden_message(api_info):
    """
    格式化禁止调用的提示信息
    
    参数:
        api_info: 禁止的 API 信息字典
        
    返回:
        str: 格式化的提示消息
    """
    message = f"""
⚠️ 安全限制 - 禁止调用的接口

接口名称：{api_info['name']}
接口地址：{api_info['url']}
风险等级：{api_info['risk']}
禁止原因：{api_info['reason']}

抱歉，出于安全考虑，本技能禁止调用此接口。

建议您：
1. 登录友盟官方后台手动执行此操作：https://upush.umeng.com
2. 使用本技能的查询功能（只读操作）

本技能仅支持以下只读操作：
✅ 获取应用列表
✅ 查询推送数据
✅ 查看诊断报告
"""
    return message.strip()

def print_security_notice():
    """打印安全注意事项"""
    notice = """
================================================================================
🔒 API 调用安全注意事项

禁止调用的接口（4 个）：
  ❌ sendMsg - 发送推送消息
  ❌ updateApp - 修改应用配置
  ❌ updateChannelInfo - 修改渠道信息
  ❌ saveReceipt - 保存回执配置

允许调用的接口（只读操作）：
  ✅ listAll - 获取应用列表
  ✅ messageOverview - 消息概览
  ✅ diagnosisSummery - 诊断摘要
  ✅ diagnosisReport - 诊断报告

如需执行修改类操作，请访问：https://upush.umeng.com
================================================================================
"""
    print(notice)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "check":
            # 检查单个 URL
            if len(sys.argv) > 2:
                url = sys.argv[2]
                is_allowed, message = check_api_url(url)
                if is_allowed:
                    print(f"✓ 允许调用：{message}")
                    sys.exit(0)
                else:
                    print(f"✗ 禁止调用：{message}", file=sys.stderr)
                    sys.exit(1)
            else:
                print("用法：python security_interceptor.py check <url>")
                sys.exit(1)
        elif sys.argv[1] == "list":
            # 列出所有禁止和允许的接口
            print_security_notice()
        elif sys.argv[1] == "test":
            # 测试模式
            print("测试模式 - 检查所有禁止的接口...")
            for api in FORBIDDEN_APIS:
                is_allowed, message = check_api_url(api['url'])
                status = "❌ 禁止" if not is_allowed else "✅ 允许"
                print(f"{status} - {api['name']}: {api['url']}")
            
            print("\n测试模式 - 检查所有允许的接口...")
            for api in ALLOWED_APIS:
                is_allowed, message = check_api_url(api)
                status = "✅ 允许" if is_allowed else "❌ 禁止"
                print(f"{status} - {api}")
    else:
        print("用法：python security_interceptor.py <command> [arguments]")
        print("命令:")
        print("  check <url>  - 检查 URL 是否允许调用")
        print("  list         - 列出所有禁止和允许的接口")
        print("  test         - 测试模式")
