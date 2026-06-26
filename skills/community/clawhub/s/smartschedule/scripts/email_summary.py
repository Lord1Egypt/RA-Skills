#!/usr/bin/env python3
"""
邮件日程汇总脚本
每小时通过 SMTP 发送未来 24 小时内的日程摘要。
由 OpenClaw cron 定时调用。
"""

import json
import os
import smtplib
import sys
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "config.json")

sys.path.insert(0, SCRIPT_DIR)
from schedule_manager import init_db, get_upcoming

DATE_FMT = "%Y-%m-%d %H:%M"


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def format_schedule_list(schedules):
    if not schedules:
        return "未来 24 小时内没有日程安排。可以好好休息！"

    lines = []
    for i, s in enumerate(schedules, 1):
        start = s["start_time"]
        end = s["end_time"]
        loc = f"  📍 地点：{s['location']}" if s.get("location") else ""
        desc = f"  📝 备注：{s['description']}" if s.get("description") else ""
        lines.append(f"{i}. 📅 {s['title']}")
        lines.append(f"   ⏰ {start} ~ {end}")
        if loc:
            lines.append(loc)
        if desc:
            lines.append(desc)
        lines.append("")
    return "\n".join(lines)


def build_email(schedules, config):
    now = datetime.now()
    subject = f"📅 日程汇总 - {now.strftime('%Y-%m-%d %H:%M')}"

    body_text = format_schedule_list(schedules)

    html = f"""
    <html>
    <head><meta charset="utf-8"></head>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h2 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">
            📅 未来 24 小时日程汇总
        </h2>
        <p style="color: #7f8c8d;">生成时间：{now.strftime('%Y-%m-%d %H:%M')}</p>
    """

    if not schedules:
        html += '<p style="color: #27ae60; font-size: 16px;">✨ 未来 24 小时内没有日程安排，可以好好休息！</p>'
    else:
        html += f'<p style="color: #555;">共 <strong>{len(schedules)}</strong> 个日程：</p>'
        for i, s in enumerate(schedules, 1):
            loc_html = f'<br>📍 {s["location"]}' if s.get("location") else ""
            desc_html = f'<br><em style="color:#888">{s["description"]}</em>' if s.get("description") else ""
            html += f"""
            <div style="background:#f8f9fa; border-left:4px solid #3498db; padding:12px; margin:10px 0; border-radius:4px;">
                <strong style="font-size:15px;">{i}. {s['title']}</strong><br>
                ⏰ {s['start_time']} ~ {s['end_time']}
                {loc_html}{desc_html}
            </div>
            """

    html += """
        <hr style="border:none; border-top:1px solid #eee; margin-top:20px;">
        <p style="color:#aaa; font-size:12px;">此邮件由智能日程管理系统自动发送（OpenClaw）</p>
    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = config["smtp"]["sender_email"]
    msg["To"] = config["smtp"]["receiver_email"]
    msg.attach(MIMEText(body_text, "plain", "utf-8"))
    msg.attach(MIMEText(html, "html", "utf-8"))
    return msg


def send_email(msg, config):
    smtp_cfg = config["smtp"]
    if smtp_cfg.get("use_ssl"):
        server = smtplib.SMTP_SSL(smtp_cfg["server"], smtp_cfg["port"])
    else:
        server = smtplib.SMTP(smtp_cfg["server"], smtp_cfg["port"])
        server.starttls()

    server.login(smtp_cfg["sender_email"], smtp_cfg["password"])
    server.send_message(msg)
    server.quit()


def main():
    init_db()
    config = load_config()
    schedules = get_upcoming(hours=24)

    msg = build_email(schedules, config)

    try:
        send_email(msg, config)
        result = {
            "status": "success",
            "schedules_count": len(schedules),
            "sent_to": config["smtp"]["receiver_email"],
            "time": datetime.now().strftime(DATE_FMT),
        }
    except Exception as e:
        result = {
            "status": "error",
            "error": str(e),
            "time": datetime.now().strftime(DATE_FMT),
        }

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


if __name__ == "__main__":
    main()
