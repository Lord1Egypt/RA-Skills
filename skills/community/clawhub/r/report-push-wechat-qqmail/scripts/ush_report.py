import os
import argparse
import smtplib
import requests
import json
from email.mime.text import MIMEText
from email.header import Header

def send_qq_mail(title, content):
    sender = os.environ.get("QQ_MAIL_ACCOUNT")
    auth_code = os.environ.get("QQ_MAIL_AUTH_CODE")
    receiver = os.environ.get("TARGET_QQ_MAIL")
    
    if not all([sender, auth_code, receiver]):
        return False, "缺少QQ邮箱环境变量配置"

    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = Header("AI分析助手", 'utf-8')
    message['To'] = Header("订阅者", 'utf-8')
    message['Subject'] = Header(title, 'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL('smtp.qq.com', 465)
        smtpObj.login(sender, auth_code)
        smtpObj.sendmail(sender, [receiver], message.as_string())
        smtpObj.quit()
        return True, "成功"
    except Exception as e:
        return False, str(e)

def send_wechat(title, summary):
    token = os.environ.get("WECHAT_PUSH_KEY")
    if not token:
        return False, "缺少微信推送 Token (WECHAT_PUSH_KEY)"
    
    # 强制截断摘要至100字
    if len(summary) > 100:
        summary = summary[:97] + "..."

    url = 'http://www.pushplus.plus/send'
    data = {
        "token": token,
        "title": title,
        "content": summary,
        "template": "txt"
    }
    try:
        response = requests.post(url, json=data, timeout=10)
        if response.status_code == 200:
            return True, "成功"
        return False, f"HTTP状态码异常: {response.status_code}"
    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="推送报告脚本")
    parser.add_argument("--title", required=True, help="报告标题")
    parser.add_argument("--summary", required=True, help="微信摘要")
    parser.add_argument("--content", required=True, help="完整报告内容")
    parser.add_argument("--channel", default="both", choices=["both", "wechat", "email"], help="推送渠道")
    
    args = parser.parse_args()
    
    result = {
        "status": "completed",
        "wechat_status": "skipped",
        "email_status": "skipped",
        "details": {}
    }

    # 处理微信推送
    if args.channel in ["both", "wechat"]:
        success, msg = send_wechat(args.title, args.summary)
        result["wechat_status"] = "success" if success else "failed"
        result["details"]["wechat_error"] = msg if not success else None

    # 处理邮件推送
    if args.channel in ["both", "email"]:
        success, msg = send_qq_mail(args.title, args.content)
        result["email_status"] = "success" if success else "failed"
        result["details"]["email_error"] = msg if not success else None

    # 打印 JSON 结果供 Agent 解析
    print(json.dumps(result, ensure_ascii=False))