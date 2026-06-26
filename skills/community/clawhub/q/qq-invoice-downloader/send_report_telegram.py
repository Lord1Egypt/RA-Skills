# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import os
import requests

# 配置
TOKEN = "8408048074:AAHRX5vogDUKZjdf-mL4ByJ8ukihRosqFpI"
REPORT_DIR = r"Z:\OpenClaw\InvoiceOC"
LATEST_REPORT_FILE = os.path.join(REPORT_DIR, "latest_report.txt")

def get_latest_report():
    """获取最新报告路径"""
    if os.path.exists(LATEST_REPORT_FILE):
        with open(LATEST_REPORT_FILE, 'r', encoding='utf-8') as f:
            return f.read().strip()
    return None

def get_chat_id():
    """获取Chat ID - 需要用户先给bot发送消息"""
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            updates = data.get('result', [])
            if updates:
                for u in reversed(updates):
                    if 'message' in u:
                        chat = u['message'].get('chat', {})
                        chat_id = chat.get('id')
                        if chat_id:
                            return chat_id
    except Exception as e:
        print(f"获取Chat ID失败: {e}")
    return None

def send_file(chat_id, file_path, caption):
    """发送文件到Telegram"""
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
        
        with open(file_path, 'rb') as f:
            files = {'document': f}
            data = {
                'chat_id': chat_id,
                'caption': caption
            }
            r = requests.post(url, data=data, files=files, timeout=60)
            
        if r.status_code == 200:
            result = r.json()
            if result.get('ok'):
                print("发送成功!")
                return True
            else:
                print(f"发送失败: {result}")
        else:
            print(f"HTTP错误: {r.status_code}")
    except Exception as e:
        print(f"发送异常: {e}")
    return False

def main():
    print("="*50)
    print("发票报告自动发送工具")
    print("="*50)
    
    # 1. 获取最新报告
    report_path = get_latest_report()
    if not report_path or not os.path.exists(report_path):
        print("未找到报告文件，尝试查找最新...")
        import glob
        xlsx_files = glob.glob(os.path.join(REPORT_DIR, "*", "发票目录.xlsx"))
        if xlsx_files:
            report_path = max(xlsx_files, key=os.path.getmtime)
            print(f"使用最新报告: {report_path}")
        else:
            print("没有报告文件")
            return
    
    # 2. 获取Chat ID
    print("获取Chat ID...")
    chat_id_file = os.path.join(REPORT_DIR, "telegram_chat_id.txt")
    
    # 先检查保存的chat_id
    chat_id = None
    if os.path.exists(chat_id_file):
        with open(chat_id_file, 'r') as f:
            chat_id = f.read().strip()
        print(f"使用已保存的Chat ID: {chat_id}")
    else:
        chat_id = get_chat_id()
        if not chat_id:
            print("无法获取Chat ID")
            print("请先给Telegram bot发送一条消息")
            return
        print(f"获取到Chat ID: {chat_id}")
    
    # 3. 发送文件
    caption = f"发票下载报告 - {os.path.basename(report_path)}"
    send_file(chat_id, report_path, caption)

if __name__ == "__main__":
    main()
