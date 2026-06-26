# QQ邮箱邮件发送技能 | Email Sender Skill

## 概述 | Overview

这是一个专为 OpenClaw AI Agent 设计的邮件自动发送和接收技能。通过 SMTP/POP3 协议实现邮件收发，支持附件、抄送等功能。

This is an email automation skill designed for OpenClaw AI Agents. It enables email sending and receiving via SMTP/POP3 protocols, with support for attachments and CC.

---

## 解决的问题 | Problem Solving

### 多 OpenClaw 协作痛点 | Multi-Agent Collaboration Pain Points

**使用飞书的局限：**
- ❌ Agent 群聊消息容易丢失
- ❌ 云文档沟通效率低，经常出现空白内容
- ❌ 消息同步不及时，无法追踪任务状态

**Limitations of using Feishu (Lark):**
- ❌ Group chat messages between agents are often lost
- ❌ Cloud document communication is inefficient with frequent blank content
- ❌ Message sync is not timely, making task tracking difficult

**邮件协作的优势：**
- ✅ 消息100%可靠传输，不会丢失
- ✅ 完整的对话历史记录，便于追溯
- ✅ 支持附件传输，方便文件共享
- ✅ 跨平台兼容，任何邮件客户端都能接收

**Advantages of Email Collaboration:**
- ✅ 100% reliable message delivery, never lost
- ✅ Complete conversation history for easy tracking
- ✅ Supports file attachments for easy sharing
- ✅ Cross-platform compatibility, works with any email client

---

## 核心功能 | Core Features

| 功能 | Feature | 说明 |
|------|---------|------|
| 发送邮件 | Send Email | 支持纯文本、HTML格式 |
| 附件发送 | Attachments | 支持PDF、图片、文档等 |
| 抄送功能 | CC/BCC | 支持多人抄送 |
| 邮件接收 | Receive Email | 定时检查收件箱 |
| 自动回复 | Auto Reply | 可配置自动回复规则 |

---

## 使用场景 | Use Cases

### 1. 多 Agent 任务协作 | Multi-Agent Task Collaboration
```python
# Agent A 完成任务后通知 Agent B
send_email(
    to="agent_b@company.com",
    subject="任务完成: 数据分析",
    body="已完成数据分析，结果见附件"
)
```

### 2. 定时报告推送 | Scheduled Report Delivery
```python
# 每日自动发送报告
send_email(
    to="team@company.com", 
    subject="每日工作报告",
    attachment="/path/to/report.pdf"
)
```

### 3. 跨平台文件传输 | Cross-Platform File Transfer
```python
# 文件在不同设备间传输
send_email(
    to="another_device@email.com",
    attachment="/large/file.zip"
)
```

---

## 技术配置 | Technical Configuration

### QQ邮箱配置 | QQ Mail Configuration

| 配置项 | Config | 值 | Value |
|--------|--------|-----|-------|
| SMTP服务器 | SMTP Server | smtp.qq.com | |
| SMTP端口 | SMTP Port | 465 (SSL) / 587 (TLS) | |
| POP3服务器 | POP3 Server | pop.qq.com | |
| POP3端口 | POP3 Port | 995 (SSL) | |
| 用户名 | Username | your@qq.com | |
| 密码 | Password | 授权码（非QQ密码）| |

### 获取授权码 | Get Authorization Code
1. 登录 mail.qq.com
2. 进入设置 → 账户
3. 开启 POP3/SMTP 服务
4. 获取授权码

---

## 安装依赖 | Installation

```bash
pip install python-docx
```

---

## 示例代码 | Sample Code

### 发送简单邮件 | Send Simple Email
```python
import smtplib
import ssl
from email.mime.text import MIMEText

smtp_server = "smtp.qq.com"
smtp_port = 465
username = "your@qq.com"
password = "授权码"

msg = MIMEText("邮件内容", "plain", "utf-8")
msg["Subject"] = "邮件标题"
msg["From"] = username
msg["To"] = "receiver@example.com"

ctx = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, smtp_port, context=ctx) as server:
    server.login(username, password)
    server.send_message(msg)
```

### 发送带附件的邮件 | Send Email with Attachment
```python
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

msg = MIMEMultipart()
msg["From"] = username
msg["To"] = "receiver@example.com"
msg["Subject"] = "带附件的邮件"

msg.attach(MIMEText("邮件正文", "plain", "utf-8"))

# 添加附件
with open("file.pdf", "rb") as f:
    part = MIMEBase("application", "pdf")
    part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", "attachment", filename="file.pdf")
    msg.attach(part)

ctx = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, smtp_port, context=ctx) as server:
    server.login(username, password)
    server.send_message(msg)
```

### 接收邮件 | Receive Email
```python
import poplib
import ssl

pop_server = "pop.qq.com"
pop_port = 995
username = "your@qq.com"
password = "授权码"

ctx = ssl.create_default_context()
server = poplib.POP3_SSL(pop_server, pop_port, context=ctx)
server.user(username)
server.pass_(password)

# 获取邮件数量
num = len(server.list()[1])
print(f"收件箱: {num} 封邮件")

# 获取最新邮件
msg = server.retr(num)[1]
server.quit()
```

---

## 适用人群 | Target Users

- 🤖 使用 OpenClaw 的 AI Agent 开发者
- 👥 需要多 Agent 协作的团队
- 📧 需要可靠消息传递的场景
- 📁 需要传输大文件的用户

---

## 版本 | Version

- v1.0.0 - 初始版本 | Initial version

---

## 作者 | Author

OpenClaw Community

---

## 许可 | License

MIT License
