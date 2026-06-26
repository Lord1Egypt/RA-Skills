#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram报告发送工具
"""

import requests
import json

# 配置
TOKEN = "8408048074:AAHRX5vogDUKZjdf-mL4ByJ8ukihRosqFpI"

def send_report(round_num, success, failed, total, elapsed, failed_details=None):
    """发送报告到Telegram"""
    msg = f"📊 *发票下载第{round_num}轮报告*\n\n"
    msg += f"⏱️ 耗时: {elapsed:.1f}秒\n"
    msg += f"✅ 成功: {success}\n"
    msg += f"❌ 失败: {failed}\n"
    msg += f"📁 总附件: {total}\n"
    
    if failed > 0:
        msg += f"\n⚠️ 失败详情:\n"
        if failed_details:
            for detail in failed_details[:3]:
                msg += f"  • {detail}\n"
    else:
        msg += f"\n🎉 全部完成!"
    
    try:
        # 先尝试获取chat列表
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            updates = data.get('result', [])
            if updates:
                for u in updates[-5:]:
                    msg_data = u.get('message', u.get('edited_message', {}))
                    chat = msg_data.get('chat', {})
                    chat_id = chat.get('id')
                    if chat_id:
                        # 发送消息
                        send_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                        send_data = {"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}
                        send_r = requests.post(send_url, json=send_data, timeout=10)
                        if send_r.status_code == 200:
                            print(f"✅ 报告已发送到 Chat ID: {chat_id}")
                            return True
        
        print("⚠️ 无法获取chat ID，请先给bot发送一条消息")
        return False
    except Exception as e:
        print(f"❌ 发送失败: {e}")
        return False

if __name__ == "__main__":
    # 测试
    send_report(1, 15, 2, 37, 120.5, ["和运国际下载失败", "诺诺网超时"])
