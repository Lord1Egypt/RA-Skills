---
name: smtp-mail-sender
description: "通用 SMTP 邮件发送工具。通过命令行脚本发送纯文本或 HTML 邮件，支持多收件人、多附件。首次使用时需交互式配置邮箱地址和密码/授权码，凭据持久化存储在 Windows 注册表中。内置常见邮箱服务商 SMTP 服务器自动匹配（电信、189、139、163、QQ、126、Outlook、Gmail 等）。触发场景：发邮件、发送报告、邮件通知、邮件提醒、定时发送邮件、批量发送邮件、send email、notify、email report、邮件附件、HTML邮件。"
agent_created: true
---

# SMTP 邮件发送工具

## Overview

提供通用的 SMTP 邮件发送能力，封装在 `scripts/send_email.py` 脚本中。支持纯文本和 HTML 正文、多收件人、多附件。首次使用需配置邮箱凭据，后续自动读取。

## 首次使用 — 配置邮箱凭据

检查是否已配置：

```bash
python <skill_dir>/scripts/send_email.py --check
```

如果输出"尚未配置邮箱凭据"，则需引导用户完成配置。有两种方式：

### 方式一：交互式配置（推荐）

```bash
python <skill_dir>/scripts/send_email.py --setup
```

脚本会提示用户输入邮箱地址和密码/授权码，自动识别 SMTP 服务器，并将凭据持久化到 Windows 注册表 `HKCU\Environment`。

### 方式二：手动设置环境变量

```bash
setx SMTP_MAIL_ADDR "your_email@domain.com"
setx SMTP_MAIL_PWD "your_password_or_auth_code"
```

注意：使用 QQ 邮箱、163 邮箱等需使用授权码而非登录密码。引导用户前往对应邮箱设置页面生成授权码。

## 发送邮件

### 发送纯文本邮件

```bash
python <skill_dir>/scripts/send_email.py \
  --to "person1@example.com,person2@example.com" \
  --subject "邮件主题" \
  --body "邮件正文内容"
```

### 发送 HTML 邮件（直接传 HTML 字符串）

```bash
python <skill_dir>/scripts/send_email.py \
  --to "person@example.com" \
  --subject "HTML 邮件" \
  --html-body "<h1>标题</h1><p>正文</p>"
```

### 发送 HTML 邮件（从 HTML 文件读取）

```bash
python <skill_dir>/scripts/send_email.py \
  --to "person@example.com" \
  --subject "报告邮件" \
  --html-file report.html
```

### 发送带附件的邮件

```bash
python <skill_dir>/scripts/send_email.py \
  --to "person1@example.com,person2@example.com" \
  --subject "带附件的邮件" \
  --body "请查收附件" \
  --attach report.csv \
  --attach data.xlsx
```

### 指定发件人显示名称

```bash
python <skill_dir>/scripts/send_email.py \
  --to "person@example.com" \
  --subject "邮件" \
  --body "正文" \
  --sender-name "运维团队"
```

### 指定自定义 SMTP 服务器

当邮箱域名不在自动匹配列表中时，手动指定：

```bash
python <skill_dir>/scripts/send_email.py \
  --to "person@example.com" \
  --subject "邮件" \
  --body "正文" \
  --smtp-server "smtp.example.com" \
  --smtp-port 465 \
  --smtp-mode ssl
```

## 在 Python 脚本中直接调用

除了命令行方式，也可在 Python 脚本中导入使用：

```python
import sys
sys.path.insert(0, '<skill_dir>/scripts')
from send_email import send_email

# 检查并引导配置
from send_email import get_credential
addr, pwd = get_credential()
if not addr or not pwd:
    print("邮箱未配置，请运行: python send_email.py --setup")
    sys.exit(1)

# 发送邮件
send_email(
    recipients=['a@b.com', 'c@d.com'],
    subject='邮件主题',
    body='纯文本正文',
    attachments=['report.csv', 'data.xlsx'],
)
```

发送 HTML 表格邮件示例：

```python
html = '''<html><body style="font-family: Microsoft YaHei, Arial, sans-serif; font-size: 14px;">
<p>各位好，</p>
<table style="border-collapse: collapse; width: 100%; margin: 10px 0;">
<thead><tr style="background-color: #4472C4; color: #fff;">
  <th style="border: 1px solid #ccc; padding: 6px 10px;">名称</th>
  <th style="border: 1px solid #ccc; padding: 6px 10px;">数值</th>
</tr></thead>
<tbody>
<tr style="background-color: #f5f7fa;">
  <td style="border: 1px solid #ddd; padding: 5px 10px;">项目A</td>
  <td style="border: 1px solid #ddd; padding: 5px 10px;">100</td>
</tr>
</tbody></table>
</body></html>'''

send_email(
    recipients='a@b.com,c@d.com',
    subject='数据报告',
    html_body=html,
    attachments=['report.csv'],
)
```

## 自动支持的 SMTP 服务器

以下邮箱域名可自动匹配 SMTP 服务器，无需手动指定：

| 邮箱域名 | SMTP 服务器 | 端口 | 加密方式 |
|----------|------------|------|---------|
| @chinatelecom.cn | smtp.chinatelecom.cn | 465 | SSL |
| @189.cn | smtp.189.cn | 465 | SSL |
| @139.com | smtp.139.com | 465 | SSL |
| @163.com | smtp.163.com | 465 | SSL |
| @126.com | smtp.126.com | 465 | SSL |
| @qq.com | smtp.qq.com | 465 | SSL |
| @foxmail.com | smtp.qq.com | 465 | SSL |
| @sina.com | smtp.sina.com | 465 | SSL |
| @sohu.com | smtp.sohu.com | 465 | SSL |
| @aliyun.com | smtp.qiye.aliyun.com | 465 | SSL |
| @outlook.com | smtp-mail.outlook.com | 587 | STARTTLS |
| @hotmail.com | smtp-mail.outlook.com | 587 | STARTTLS |
| @gmail.com | smtp.gmail.com | 465 | SSL |
| @yeah.net | smtp.yeah.net | 465 | SSL |
| @263.net | smtp.263.net | 465 | SSL |
| @wo.cn | smtp.wo.cn | 465 | SSL |

不在列表中的邮箱需通过 `--smtp-server`、`--smtp-port`、`--smtp-mode` 手动指定。

## 注意事项

- 密码/授权码存储在 Windows 注册表 `HKCU\Environment` 下，仅限当前用户可读
- QQ 邮箱、163 邮箱等使用授权码而非登录密码，需引导用户前往邮箱设置页面生成
- 附件文件名支持中文，自动进行 Base64 编码
- 多收件人逐个发送，每收件人单独建立 SMTP 连接
- `--check` 参数可随时检查当前配置状态
