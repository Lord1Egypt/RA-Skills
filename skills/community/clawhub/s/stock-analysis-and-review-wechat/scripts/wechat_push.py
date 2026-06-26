#!/usr/bin/env python3
"""
微信推送辅助脚本 - 股市复盘报告推送
支持微信插件版本检查和报告格式化
"""

import json
import sys
import re
from datetime import datetime

def check_wechat_version():
    """
    检查微信插件版本
    返回: (bool, str) - (是否OK, 版本信息或错误信息)
    """
    # 实际调用时可通过 exec 运行 openclaw status 获取
    # 这里返回模拟值，实际使用时替换为真实检查逻辑
    return (True, "openclaw-weixin@1.2.3")

def format_for_wechat(markdown_content):
    """
    将Markdown格式转换为微信友好格式
    
    转换规则:
    1. 表格转换为列表
    2. 简化标题层级
    3. 确保emoji兼容
    """
    lines = markdown_content.split('\n')
    result = []
    in_table = False
    table_header = None
    
    for line in lines:
        stripped = line.strip()
        
        # 跳过空行
        if not stripped:
            result.append('')
            continue
        
        # 处理表格
        if stripped.startswith('|'):
            parts = [p.strip() for p in stripped.split('|')[1:-1]]
            
            # 跳过分隔线
            if '---' in stripped:
                continue
            
            # 表头
            if '标的' in stripped or '名称' in stripped:
                table_header = parts
                result.append('📊 持仓详情:')
                continue
            
            # 表格内容
            if table_header and len(parts) >= 3:
                # 格式化为列表项
                name = parts[0] if len(parts) > 0 else '-'
                price = parts[2] if len(parts) > 2 else '-'
                change = parts[3] if len(parts) > 3 else ''
                status = parts[6] if len(parts) > 6 else ''
                
                item = f"• {name}: {price} {change} {status}".strip()
                result.append(item)
            continue
        
        # 处理标题
        if stripped.startswith('#'):
            # 减少标题层级
            level = len(stripped) - len(stripped.lstrip('#'))
            if level > 2:
                stripped = '##' + stripped[level:]
            result.append(stripped)
            continue
        
        # 普通文本直接保留
        result.append(stripped)
    
    return '\n'.join(result)

def generate_delivery_config(user_id, account_id):
    """
    生成微信推送配置
    
    Args:
        user_id: 用户微信ID (不含@im.wechat后缀)
        account_id: 机器人账号ID
    
    Returns:
        dict: delivery配置
    """
    return {
        "mode": "announce",
        "channel": "openclaw-weixin",
        "to": f"{user_id}@im.wechat",
        "accountId": account_id
    }

def push_report(report_content, user_id, account_id, check_version=True):
    """
    推送复盘报告到微信
    
    Args:
        report_content: 报告内容（Markdown格式）
        user_id: 用户微信ID
        account_id: 机器人账号ID
        check_version: 是否检查微信插件版本
    
    Returns:
        tuple: (success, message)
    """
    
    # 1. 版本检查
    if check_version:
        version_ok, version_info = check_wechat_version()
        if not version_ok:
            return (False, f"⚠️ 微信插件检查失败: {version_info}")
        print(f"✅ 微信插件版本: {version_info}")
    
    # 2. 参数验证
    if not user_id:
        return (False, "❌ 缺少用户ID (user_id)")
    if not account_id:
        return (False, "❌ 缺少账号ID (account_id)")
    
    # 3. 格式化报告
    formatted_report = format_for_wechat(report_content)
    
    # 4. 生成推送配置
    delivery = generate_delivery_config(user_id, account_id)
    
    # 5. 输出结果（供OpenClaw解析）
    output = {
        "report": formatted_report,
        "delivery": delivery,
        "timestamp": datetime.now().isoformat()
    }
    
    return (True, output)

if __name__ == "__main__":
    # 命令行用法
    if len(sys.argv) < 4:
        print("Usage: python wechat_push.py <report_file> <user_id> <account_id>")
        print("Example: python wechat_push.py report.md user_xxx account_xxx")
        sys.exit(1)
    
    report_file = sys.argv[1]
    user_id = sys.argv[2]
    account_id = sys.argv[3]
    
    # 读取报告
    try:
        with open(report_file, 'r', encoding='utf-8') as f:
            report_content = f.read()
    except FileNotFoundError:
        print(f"❌ 报告文件不存在: {report_file}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 读取报告失败: {e}")
        sys.exit(1)
    
    # 推送
    success, result = push_report(report_content, user_id, account_id)
    
    if success:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"❌ 推送失败: {result}")
        sys.exit(1)
