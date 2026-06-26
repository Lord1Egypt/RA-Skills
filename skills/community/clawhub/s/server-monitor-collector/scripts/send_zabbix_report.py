#!/usr/bin/env python3
"""
发送 Zabbix 监控报告邮件 + 飞书消息
"""
import os
import smtplib
import sys
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

HERMES_DIR = os.environ.get("HERMES_DIR", os.path.expanduser("~/.hermes"))
CSV_PATH = os.path.join(HERMES_DIR, "cron", "output", "zabbix_monitor.csv")
XLSX_PATH = os.path.join(HERMES_DIR, "cron", "output", "zabbix_monitor.xlsx")


def send_email(subject, html_body, attachments=None):
    smtp_host = os.environ.get("SMTP_HOST", "")
    smtp_port = os.environ.get("SMTP_PORT", "465")
    smtp_from = os.environ.get("SMTP_FROM", "")
    smtp_token = os.environ.get("SMTP_TOKEN", "")
    target = os.environ.get("TARGET_EMAIL", "")

    if not all([smtp_host, smtp_from, smtp_token, target]):
        print("邮件配置不完整，跳过发送")
        return False

    msg = MIMEMultipart()
    msg["From"] = smtp_from
    msg["To"] = target
    msg["Subject"] = subject

    msg.attach(MIMEText(html_body, "html", "utf-8"))

    # 附件
    for fpath in (attachments or []):
        if os.path.exists(fpath):
            with open(fpath, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
                encoders.encode_base64(part)
                fname = os.path.basename(fpath)
                part.add_header("Content-Disposition", f"attachment; filename={fname}")
                msg.attach(part)

    try:
        if smtp_port == "465":
            with smtplib.SMTP_SSL(smtp_host, int(smtp_port)) as server:
                server.login(smtp_from, smtp_token)
                server.sendmail(smtp_from, target, msg.as_string())
        else:
            with smtplib.SMTP(smtp_host, int(smtp_port)) as server:
                server.starttls()
                server.login(smtp_from, smtp_token)
                server.sendmail(smtp_from, target, msg.as_string())
        print(f"邮件已发送至 {target}")
        return True
    except Exception as e:
        print(f"邮件发送失败: {e}")
        return False


def build_html_body():
    """从 CSV 读取数据，生成 HTML 表格"""
    if not os.path.exists(CSV_PATH):
        return "<p>CSV 文件不存在</p>"

    import csv
    from collections import defaultdict

    groups = defaultdict(list)
    with open(CSV_PATH, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            groups[row["主机组"]].append(row)

    html = f"""
    <h2>服务器监控报告</h2>
    <p><b>采集时间：</b>{datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    """

    for gname, rows in sorted(groups.items()):
        html += f"<h3>{gname} ({len(rows)} 台)</h3>"
        html += "<table border='1' cellpadding='4' cellspacing='0' style='border-collapse:collapse;font-size:13px;'>"
        html += "<tr bgcolor='#4472C4' style='color:white;'>"
        for h in ["主机名", "IP", "内存总量(GB)", "内存可用(GB)", "内存占用率(%)", "CPU占用率(%)"]:
            html += f"<th>{h}</th>"
        html += "</tr>"

        for i, r in enumerate(rows):
            bg = "#EEF2FF" if i % 2 == 0 else "#FFFFFF"
            mem_pct = float(r["内存占用率(%)"]) if r["内存占用率(%)"] != "N/A" else 0
            cpu_pct = float(r["CPU占用率(%)"]) if r["CPU占用率(%)"] != "N/A" else 0

            mem_style = ""
            if mem_pct >= 80:
                mem_style = "background:#FF4444;color:white;"
            elif mem_pct >= 60:
                mem_style = "background:#FFAA44;"
            elif mem_pct >= 40:
                mem_style = "background:#FFEE88;"

            cpu_style = ""
            if cpu_pct >= 80:
                cpu_style = "background:#FF4444;color:white;"
            elif cpu_pct >= 60:
                cpu_style = "background:#FFAA44;"
            elif cpu_pct >= 40:
                cpu_style = "background:#FFEE88;"

            html += f"<tr bgcolor='{bg}'>"
            html += f"<td>{r['主机名']}</td>"
            html += f"<td>{r['IP']}</td>"
            html += f"<td>{r['内存总量(GB)']}</td>"
            html += f"<td>{r['内存可用(GB)']}</td>"
            html += f"<td style='{mem_style}'>{r['内存占用率(%)']}</td>"
            html += f"<td style='{cpu_style}'>{r['CPU占用率(%)']}</td>"
            html += "</tr>"
        html += "</table><br/>"

    return html


def main():
    print("开始发送报告...")

    # 1. 飞书消息（由 Hermes cron 自动发，这里只打印摘要）
    print("飞书消息已通过主脚本发送")

    # 2. 邮件
    subject = f"【监控报告】服务器巡检 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    html_body = build_html_body()

    attachments = []
    if os.path.exists(XLSX_PATH):
        attachments.append(XLSX_PATH)
    if os.path.exists(CSV_PATH):
        attachments.append(CSV_PATH)

    send_email(subject, html_body, attachments)


if __name__ == "__main__":
    main()
