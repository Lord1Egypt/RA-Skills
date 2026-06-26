---
name: wecom-email
version: 1.0.0
description: >
  企业微信邮箱操作 - 使用专用邮箱发送邮件。
  支持读取会议纪要、业务文档等作为邮件内容发送。
author: SC
keywords: [email, mail, smtp, wecom, notification]
metadata:
  openclaw:
    emoji: "📧"
    category: productivity
---

# 📧 WeCom Email - 企业微信邮箱

使用专用邮箱发送工作邮件。

## 快速开始

### 1. 配置 SMTP

| 配置项 | 值 |
|--------|-----|
| SMTP服务器 | smtp.exmail.qq.com |
| SMTP端口 | 465 (SSL) |
| 邮箱账号 | YOUR_EMAIL@YOUR_DOMAIN.COM |
| 凭证文件 | ~/.openclaw/workspace/memory/sc-email-credentials.enc |

### 2. 发送邮件

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.exmail.qq.com"
SMTP_USER = "YOUR_EMAIL@YOUR_DOMAIN.COM"
SMTP_PASSWORD = "YOUR_PASSWORD"

msg = MIMEMultipart()
msg['From'] = SMTP_USER
msg['To'] = "recipient@example.com"
msg['Subject'] = "邮件主题"
msg.attach(MIMEText("邮件内容", 'plain', 'utf-8'))

server = smtplib.SMTP_SSL('smtp.exmail.qq.com', 465)
server.login(SMTP_USER, SMTP_PASSWORD)
server.sendmail(SMTP_USER, ["recipient@example.com"], msg.as_string())
server.quit()
```

## 安全规则

### 发送条件
- ✅ 需要用户明确指令才能发送
- ✅ 只能发送工作相关内容
- ✅ 使用专用邮箱账号

### 禁止发送
- ❌ 密码、token、密钥等鉴权信息
- ❌ 个人隐私信息
- ❌ 非工作相关内容

### 账号权限
- 专用邮箱: 仅授权用户可用
- SC代发邮箱: 需用户明确授权

## 使用示例

### 发送会议纪要

```python
# 读取会议纪要文件
with open("meeting-minutes.md", 'r') as f:
    content = f.read()

# 发送邮件
send_email(
    to=["colleague@example.com"],
    subject="会议纪要 - 日期",
    body=content
)
```

### 命令行发送

```bash
# 直接使用Python脚本发送
python3 scripts/send-email.py --to "xxx@example.com" --subject "主题" --body "内容"
```

## 凭证管理

- 凭证位置: ~/.openclaw/workspace/memory/sc-email-credentials.enc
- 编码方式: Base64 或 AES 加密
- 解码命令示例: `base64 -d ~/.openclaw/workspace/memory/sc-email-credentials.enc`

## 相关文件

- 邮箱列表: ~/.openclaw/workspace/memory/enmo-emails.enc
- 个人邮箱: ~/.openclaw/workspace/memory/email-credentials.enc (仅授权账号可用)

---

## 触发词

当用户提到以下内容时激活此Skill：
- "发送邮件"
- "发邮件"
- "邮件通知"
- "发送会议纪要"
- "用邮箱通知"
