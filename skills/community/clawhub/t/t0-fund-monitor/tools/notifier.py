#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通知推送模块
"""

import requests
import json
import sys
from datetime import datetime

def send_dingtalk(webhook: str, title: str, text: str) -> bool:
    """发送钉钉通知"""
    try:
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": text
            }
        }
        response = requests.post(webhook, headers=headers, data=json.dumps(data), timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"钉钉通知发送失败：{e}", file=sys.stderr)
        return False

def send_wechat(key: str, title: str, content: str) -> bool:
    """发送企业微信通知"""
    try:
        url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}"
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": f"### {title}\n{content}"
            }
        }
        response = requests.post(url, json=data, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"企业微信通知发送失败：{e}", file=sys.stderr)
        return False

def send_terminal(signal: dict, sound: bool = True):
    """终端通知"""
    from signals import format_signal
    
    print("\n" + "=" * 60)
    print(format_signal(signal))
    print("=" * 60)
    
    if sound:
        # 播放提示音
        try:
            print('\a', end='')  # 终端蜂鸣
        except:
            pass

def notify(signal: dict, config: dict):
    """发送通知"""
    notify_cfg = config.get('notify', {})
    
    title = f"{'🟢 买入' if signal['type'] == 'BUY' else '🔴 卖出'}信号 - {signal['code']}"
    text = f"""
## {title}

**代码**: {signal['code']} ({signal['name']})  
**价格**: {signal['price']:.3f}  
**原因**: {signal['reason']}  
**时间**: {signal['time']}  
**置信度**: {signal['confidence']}
"""
    
    # 钉钉
    if notify_cfg.get('dingtalk', {}).get('enabled'):
        webhook = notify_cfg['dingtalk'].get('webhook', '')
        if webhook:
            send_dingtalk(webhook, title, text)
    
    # 企业微信
    if notify_cfg.get('wechat', {}).get('enabled'):
        key = notify_cfg['wechat'].get('key', '')
        if key:
            send_wechat(key, title, text)
    
    # 终端
    if notify_cfg.get('terminal', {}).get('enabled', True):
        send_terminal(signal, notify_cfg.get('terminal', {}).get('sound', True))

if __name__ == '__main__':
    print("通知模块测试")
