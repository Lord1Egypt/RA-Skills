#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周报检查脚本 - 检查腾讯文档周报填写情况
"""

import subprocess
import sys
import os
import json
import urllib.request

# 配置
DOC_URL = "https://docs.qq.com/sheet/DQ2xhSUdzQW9CZ2NE"
OUTPUT_FILE = "workspace/qq_weekly_report.txt"
QQ_USER_ID = os.environ.get("QQ_USER_ID", "7B423FBDC28B52E0BC22A7808EBD4AC1")  # 文哥的QQ号，从环境变量读取
WEBHOOK_URL = os.environ.get("WECOM_WEBHOOK_URL", "")  # 企业微信webhook，从环境变量读取

# 脚本路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
READ_SCRIPT = os.path.join(SCRIPT_DIR, "read_sheet.py")


def send_qq_message(user_id, message):
    """通过QQ发送消息给用户"""
    try:
        # 使用message工具发送QQ消息
        # 这里需要通过OpenClaw的message工具
        # 由于这是独立脚本，我们返回消息内容，让调用者处理
        print(f"QQ通知: {message}", file=sys.stderr)
        return True
    except Exception as e:
        print(f"发送QQ消息失败: {e}", file=sys.stderr)
        return False


def check_weekly_report():
    """检查周报填写情况"""
    # 1. 读取文档
    print(f"读取周报文档: {DOC_URL}", file=sys.stderr)
    result = subprocess.run(
        ["python", READ_SCRIPT, "--url", DOC_URL, "--auto-tab", "--output", OUTPUT_FILE],
        capture_output=True,
        text=True,
        timeout=60
    )

    # 2. 检查是否成功
    if result.returncode != 0:
        error_msg = result.stderr.strip()
        print(f"读取文档失败: {error_msg}", file=sys.stderr)

        # 检查是否是"找不到标签页"的错误
        if "No suitable tab found" in error_msg or "No tabs found" in error_msg:
            # 通过QQ告知用户
            msg = f"周报检查失败：找不到本周的周报标签页（本周五）或当前日期前后两天内的标签页。请检查文档是否已创建本周周报。"
            send_qq_message(QQ_USER_ID, msg)
            return None

        print(f"其他错误: {error_msg}", file=sys.stderr)
        return None

    # 3. 读取文件内容
    try:
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"读取输出文件失败: {e}", file=sys.stderr)
        return None

    # 4. 解析表格，找出未填写的同事
    lines = content.strip().split('\n')
    if not lines:
        print("文档内容为空", file=sys.stderr)
        return None

    # 找到表头行
    header_line = None
    for i, line in enumerate(lines):
        if '本周主要工作进展' in line and '下周工作计划' in line:
            header_line = i
            break

    if header_line is None:
        print("找不到表头行", file=sys.stderr)
        return None

    # 解析表头，找到列索引
    header = lines[header_line].split('\t')
    try:
        progress_col = header.index('本周主要工作进展')
        plan_col = header.index('下周工作计划')
        name_col = header.index('责任人')
    except ValueError as e:
        print(f"找不到必要的列: {e}", file=sys.stderr)
        return None

    # 检查数据行
    not_filled = []
    for line in lines[header_line + 1:]:
        if not line.strip():
            continue

        parts = line.split('\t')
        if len(parts) <= max(progress_col, plan_col, name_col):
            continue

        progress = parts[progress_col].strip() if progress_col < len(parts) else ""
        plan = parts[plan_col].strip() if plan_col < len(parts) else ""
        name = parts[name_col].strip() if name_col < len(parts) else ""

        # 如果两列都为空，说明未填写
        if not progress and not plan and name:
            not_filled.append(name)

    return not_filled


def main():
    not_filled = check_weekly_report()

    if not_filled is None:
        # 检查失败，已经在check_weekly_report中发送QQ通知
        sys.exit(1)

    if not not_filled:
        print("所有同事都已填写周报", file=sys.stderr)
        sys.exit(0)

    # 发送企业微信通知（需要配置WECOM_WEBHOOK_URL环境变量）
    webhook_url = WEBHOOK_URL
    if not webhook_url:
        print("未配置WECOM_WEBHOOK_URL环境变量，跳过企业微信通知", file=sys.stderr)
        print("未填写周报的同事: " + ", ".join(not_filled), file=sys.stderr)
        sys.exit(0)
    msg_lines = ['周报检查：以下同事尚未填写周报，请尽快完成：']
    for i, name in enumerate(not_filled, 1):
        msg_lines.append(f'{i}. {name}')

    data = {
        'msgtype': 'text',
        'text': {
            'content': '\n'.join(msg_lines)
        }
    }

    try:
        req = urllib.request.Request(
            webhook_url,
            data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req) as resp:
            print(f"已发送企业微信通知: {resp.read().decode('utf-8')}", file=sys.stderr)
    except Exception as e:
        print(f"发送企业微信通知失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
