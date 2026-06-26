---
name: simple-email
description: 简单易用的 IMAP/SMTP 邮件技能。支持收发邮件、查看未读邮件、搜索、标记已读/未读、下载附件。兼容 Gmail、QQ 邮箱、163、新浪等所有标准 IMAP/SMTP 服务。
homepage: https://github.com/openclaw/skills
metadata:
  openclaw:
    emoji: "📧"
    requires:
      env:
        - IMAP_HOST
        - IMAP_USER
        - IMAP_PASS
        - SMTP_HOST
        - SMTP_USER
        - SMTP_PASS
      bins:
        - node
        - npm
    primaryEnv: SMTP_PASS
---

# Simple Email - 简单易用的邮件技能

通过 IMAP 协议接收和管理邮件，通过 SMTP 协议发送邮件。支持所有标准 IMAP/SMTP 邮件服务，包括 Gmail、QQ 邮箱、163、新浪、Outlook 等。

## 🚀 快速开始

### 1. 安装依赖

```bash
cd skills/simple-email
npm install
```

### 2. 配置邮箱

复制配置模板并填写你的邮箱信息：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的邮箱配置：

```bash
# IMAP 配置（接收邮件）
IMAP_HOST=imap.sina.cn
IMAP_PORT=993
IMAP_USER=makerprogram@sina.cn
IMAP_PASS=your_password_or_auth_code
IMAP_TLS=true

# SMTP 配置（发送邮件）
SMTP_HOST=smtp.sina.cn
SMTP_PORT=465
SMTP_SECURE=true
SMTP_USER=makerprogram@sina.cn
SMTP_PASS=your_password_or_auth_code
SMTP_FROM=小智助理 <makerprogram@sina.cn>

# 安全配置（文件读写权限）
ALLOWED_READ_DIRS=C:\Users\Administrator\.openclaw\workspace
ALLOWED_WRITE_DIRS=C:\Users\Administrator\.openclaw\workspace
```

### 3. 测试连接

```bash
# 测试 SMTP 发送
node scripts/smtp.js test

# 检查收件箱
node scripts/imap.js check --limit 5
```

---

## 📥 接收邮件（IMAP）

### 检查新邮件

```bash
# 检查最新 10 封邮件
node scripts/imap.js check

# 检查最新 5 封邮件
node scripts/imap.js check --limit 5

# 只检查未读邮件
node scripts/imap.js check --unseen

# 检查最近 2 小时的邮件
node scripts/imap.js check --recent 2h

# 检查指定邮箱
node scripts/imap.js check --mailbox INBOX
```

### 搜索邮件

```bash
# 搜索未读邮件
node scripts/imap.js search --unseen

# 按发件人搜索
node scripts/imap.js search --from "boss@example.com"

# 按主题搜索
node scripts/imap.js search --subject "报告"

# 搜索最近 7 天的邮件
node scripts/imap.js search --recent 7d

# 组合搜索
node scripts/imap.js search --unseen --from "boss@example.com" --limit 10
```

### 查看邮件详情

```bash
# 查看指定 UID 的邮件
node scripts/imap.js fetch <uid>
```

### 标记已读/未读

```bash
# 标记为已读
node scripts/imap.js mark-read <uid1> <uid2> ...

# 标记为未读
node scripts/imap.js mark-unread <uid1> <uid2> ...
```

### 下载附件

```bash
# 下载邮件的所有附件
node scripts/imap.js download <uid>

# 下载到指定目录
node scripts/imap.js download <uid> --dir ./attachments

# 下载指定附件
node scripts/imap.js download <uid> --file report.pdf
```

### 列出所有邮箱

```bash
node scripts/imap.js list-mailboxes
```

---

## 📤 发送邮件（SMTP）

### 发送纯文本邮件

```bash
node scripts/smtp.js send --to recipient@example.com --subject "你好" --body "这是一封测试邮件"
```

### 发送 HTML 邮件

```bash
node scripts/smtp.js send --to recipient@example.com --subject "HTML 邮件" --html --body "<h1>你好</h1><p>这是<strong>HTML</strong>格式的邮件</p>"
```

### 发送带附件的邮件

```bash
node scripts/smtp.js send --to recipient@example.com --subject "报告" --body "请查收附件" --attach ./report.pdf
```

### 发送给多人

```bash
# 多个收件人
node scripts/smtp.js send --to "a@example.com,b@example.com" --subject "通知" --body "大家好"

# 抄送
node scripts/smtp.js send --to recipient@example.com --cc "cc1@example.com,cc2@example.com" --subject "抄送" --body "你好"

# 密送
node scripts/smtp.js send --to recipient@example.com --bcc "bcc@example.com" --subject "密送" --body "你好"
```

### 从文件读取内容

```bash
# 从文件读取邮件正文
node scripts/smtp.js send --to recipient@example.com --subject "报告" --body-file ./message.txt

# 从文件读取 HTML 内容
node scripts/smtp.js send --to recipient@example.com --subject "新闻稿" --html --html-file ./newsletter.html

# 从文件读取主题
node scripts/smtp.js send --to recipient@example.com --subject-file ./subject.txt --body-file ./body.txt
```

---

## 📋 常用邮箱服务器配置

| 服务商 | IMAP 主机 | IMAP 端口 | SMTP 主机 | SMTP 端口 | 说明 |
|--------|-----------|-----------|-----------|-----------|------|
| **新浪邮箱** | imap.sina.cn | 993 | smtp.sina.cn | 465 | 使用授权码 |
| **QQ 邮箱** | imap.qq.com | 993 | smtp.qq.com | 587 | 使用授权码 |
| **163 邮箱** | imap.163.com | 993 | smtp.163.com | 465 | 使用授权码 |
| **126 邮箱** | imap.126.com | 993 | smtp.126.com | 465 | 使用授权码 |
| **Gmail** | imap.gmail.com | 993 | smtp.gmail.com | 587 | 使用应用专用密码 |
| **Outlook** | outlook.office365.com | 993 | smtp.office365.com | 587 | 使用应用密码 |

---

## ⚠️ 重要提示

### Gmail 用户
- Gmail **不接受**常规账户密码
- 必须生成 **应用专用密码**：https://myaccount.google.com/apppasswords
- 需要启用两步验证

### 163/QQ/新浪邮箱用户
- 使用 **授权码**，不是账户密码
- 需要在网页版邮箱设置中先启用 IMAP/SMTP 服务
- 授权码在邮箱设置 → 账户安全中获取

---

## 🔒 安全建议

1. **不要提交 `.env` 文件**到版本控制系统
2. 使用授权码/应用密码，而不是账户密码
3. 启用 SSL/TLS 加密连接
4. 定期更换密码
5. 限制 `ALLOWED_READ_DIRS` 和 `ALLOWED_WRITE_DIRS` 到必要的目录

---

## 🐛 常见问题

### 认证失败
- 检查用户名是否为完整邮箱地址
- 确认使用授权码/应用密码，而非账户密码
- 检查是否已启用 IMAP/SMTP 服务

### 连接超时
- 检查服务器地址和端口是否正确
- 确认网络连接正常
- 检查防火墙设置

### TLS/SSL 错误
- 确认 `IMAP_TLS` 和 `SMTP_SECURE` 设置正确
- 自签名证书可设置 `IMAP_REJECT_UNAUTHORIZED=false`

---

## 📝 命令速查

### IMAP 命令
```bash
node scripts/imap.js check [--limit N] [--unseen] [--recent 2h]
node scripts/imap.js search [--unseen] [--from xxx] [--subject xxx]
node scripts/imap.js fetch <uid>
node scripts/imap.js mark-read <uid> [uid2 ...]
node scripts/imap.js mark-unread <uid> [uid2 ...]
node scripts/imap.js download <uid> [--dir ./path]
node scripts/imap.js list-mailboxes
```

### SMTP 命令
```bash
node scripts/smtp.js send --to <email> --subject <text> --body <text>
node scripts/smtp.js send --to <email> --subject <text> --html --body "<html>..."
node scripts/smtp.js send --to <email> --subject <text> --attach <file>
node scripts/smtp.js test
```

---

## 📄 许可证

MIT License
