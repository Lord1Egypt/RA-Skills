---
name: qq-mail-read-send
description: 读取和发送QQ邮箱邮件。使用IMAP协议读取，SMTP协议发送。支持多种编码解析。触发场景：用户要求查看邮箱、读取邮件、查看最近邮件、筛选特定邮件、发送邮件等
homepage: https://service.mail.qq.com/cgi-bin/help?subtype=1&&id=28&&no=1001256
metadata:
  {
    "openclaw": {
      "emoji": "📧",
      "requires": {
        "env": ["MAIL_USER", "MAIL_PASS"],
        "config": ["~/.openclaw/secrets/mail_qq.env"]
      },
      "install": []
    }
  }
---

# QQ邮箱读取和发送
通过 IMAP 协议读取 QQ 邮箱邮件
## 触发条件

用户提到以下场景时使用：
- "查看邮箱"
- "读取邮件"
- "查看最近邮件"
- "查看当天邮件"
- "搜索邮件"
- "有新的邮件吗"

## 配置

需要提前配置QQ 邮箱 IMAP：
1. 在 QQ 邮箱设置中开启 IMAP 服务
2. 创建授权码（不是登录密码）
3. 配置 secrets 文件：`~/.openclaw/secrets/mail_qq.env`
   ```
   MAIL_USER=your_email@qq.com
   MAIL_PASS=your_auth_code
   ```

### 安全注意事项
- 凭据文件必须设置权限为 `600`（仅所有者可读），防止其他用户读取敏感信息
- `~/.openclaw/secrets/` 目录默认已经加入.gitignore，不会被提交到版本控制
- 不要将授权码提交到代码仓库或分享给他人
## 使用方法

### 1. 连接邮箱

```python
import imaplib
import email
from email.header import decode_header

IMAP_HOST = 'imap.qq.com'
IMAP_PORT = 993

def connect_mail(user, password):
    mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
    mail.login(user, password)
    mail.select('INBOX')
    return mail
```

### 2. 搜索邮件

```python
# 搜索最近7天的邮件
week_ago = (datetime.now() - timedelta(days=7)).strftime('%d-%b-%Y')
typ, msg_ids = mail.search(None, f'SINCE {week_ago}')
```

### 3. 解析邮件

```python
def decode_header_value(header_value):
    """兼容多种编码的解码"""
    if not header_value:
        return ""
    decoded_parts = []
    for content, encoding in decode_header(header_value):
        if isinstance(content, bytes):
            try:
                decoded = content.decode(encoding if encoding else 'utf-8')
            except:
                # 尝试其他常见编码
                for enc in ['gbk', 'gb2312', 'utf-8', 'big5', 'latin1']:
                    try:
                        decoded = content.decode(enc)
                        break
                    except:
                        decoded = content.decode('utf-8', errors='ignore')
        else:
            decoded = str(content)
        decoded_parts.append(decoded)
    return ''.join(decoded_parts)
```

### 4. 提取正文

邮件正文可能包含 HTML，需要清理：

```python
import re

def get_text_body(msg):
    body = ''
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/html':
                payload = part.get_payload(decode=True)
                encoding = part.get_content_charset() or 'utf-8'
                body = payload.decode(encoding, errors='ignore')
                break
    else:
        payload = msg.get_payload(decode=True)
        encoding = msg.get_content_charset() or 'utf-8'
        body = payload.decode(encoding, errors='ignore')
    
    # 清理HTML标签
    text = re.sub(r'<[^>]+>', ' ', body)
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&amp;', '&')
    text = re.sub(r'\s+', ' ', text)
    return text
```

## 邮件过滤

根据用户需求过滤邮件，常见关键词类型：
- 通知类：通知、提醒、公告
- 业务类：订单、发货、支付
- 职位类：面试、邀请、邀约（仅当用户明确需要时）
## 注意事项

1. QQ 邮箱必须使用授权码登录，非登录密码
2. 邮件编码可能为GBK/GB2312/UTF-8 等，需要多种编码尝试
3. IMAP 搜索不支持中文，使用 SINCE 获取所有邮件后本地过滤

## 发送邮件
通过 QQ 邮箱 SMTP 服务发送邮件，使用相同的授权码进行认证
### 配置
发送邮件使用与读取邮件相同的凭据文件 `~/.openclaw/secrets/mail_qq.env`
```
MAIL_USER=your_email@qq.com
MAIL_PASS=your_auth_code
```

### SMTP 设置
- 主机为 `smtp.qq.com`
- 端口为 465 (SSL) 或 587 (STARTTLS)
- 授权码： 与 IMAP 相同的授权码（非登录密码）
### 使用方法

#### 1. 使用 Python 模块发送邮件
新建 `qq_mail_sender.py` 模块提供了发送邮件的功能
```python
from qq_mail_sender import send_email

send_email(
    to="recipient@example.com",
    subject="测试邮件主题",
    body="这是一封测试邮件正文"
)
```

#### 2. 命令行方式
```bash
python qq_mail_sender.py recipient@example.com "测试邮件主题" "这是一封测试邮件正文"
```

#### 3. 详细代码示例（在 qq_mail_sender.py 中）

```python
import smtplib
import ssl
from email.message import EmailMessage
from email.header import Header
import os

def load_credentials(env_path=r"C:\Users\Administrator\.openclaw\secrets\mail_qq.env"):
    """从env文件加载MAIL_USER和MAIL_PASS"""
    creds = {}
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        k, v = line.split('=', 1)
                        creds[k.strip()] = v.strip()
    return creds

def build_message(sender, to, subject, body, cc=None, bcc=None):
    """构建带有适当编码的EmailMessage"""
    msg = EmailMessage()
    msg['From'] = sender
    msg['To'] = to
    if cc:
        msg['Cc'] = cc
    if bcc:
        msg['Bcc'] = bcc
    msg['Subject'] = Header(subject, 'utf-8')
    msg.set_content(body, charset='utf-8')
    return msg

def send_email(to, subject, body, cc=None, bcc=None):
    """
    通过QQ SMTP发送邮件
    使用SSL连接端口465
    """
    creds = load_credentials()
    user = creds.get('MAIL_USER')
    password = creds.get('MAIL_PASS')
    if not user or not password:
        raise ValueError("凭据文件中缺少MAIL_USER或MAIL_PASS")

    msg = build_message(user, to, subject, body, cc, bcc)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.qq.com', 465, context=context) as server:
        server.login(user, password)
        server.send_message(msg)
    print(f"邮件已发送至 {to}")
```

### 安全注意事项
- 凭据文件必须设置权限为 `600`（仅所有者可读），防止其他用户读取敏感信息
- `~/.openclaw/secrets/` 目录默认已经加入.gitignore，不会被提交到版本控制
- 不要将授权码提交到代码仓库或分享给他人
- 建议先用少量收件人进行测试
### 参考文档
详细的发送邮件参考请参见：`references/message-sending.md`