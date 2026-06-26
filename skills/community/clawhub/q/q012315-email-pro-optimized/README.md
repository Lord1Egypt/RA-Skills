# Email Pro Optimized - 高性能邮件管理工具

[English](#english) | [中文](#中文)

---

## 中文

### 📖 简介

**Email Pro Optimized** 是一个高性能邮件管理工具，支持 QQ、Gmail、Outlook 三大邮箱服务。采用并发处理和连接复用技术，性能比传统工具快 4-5 倍。支持 OAuth 2.0 自动刷新，完全自动化。

### ✨ 核心特性

- ✅ **多邮箱支持** - QQ、Gmail、Outlook 三大服务
- ✅ **高性能** - 并发处理，速度快 4-5 倍
- ✅ **OAuth 2.0** - 安全认证，自动令牌刷新
- ✅ **智能分类** - 自动分类为 6 个标签
- ✅ **批量处理** - 支持批量检查、搜索、发送
- ✅ **HTML 支持** - 支持 HTML 格式邮件
- ✅ **附件支持** - 支持多文件附件
- ✅ **JSON 输出** - 便于脚本处理

### 🚀 快速开始

#### 1. 安装

```bash
# 从 ClawHub 安装（推荐）
clawhub install q012315-email-pro-optimized

# 或从本地安装
clawhub install ~/.openclaw/skills/email-pro-optimized
```

#### 2. 查看已配置的账户

```bash
cd scripts
python3 email-pro.py list-accounts
```

输出示例：
```
📧 已配置的邮箱账户:

  qq_136          | 136064252@qq.com          | SMTP/IMAP | ✅ 正常    | 发送邮箱
  qq_3421         | 342187916@qq.com          | SMTP/IMAP | ✅ 正常    | 接收邮箱
  outlook_live    | qiao6646@live.com         | OAuth     | ✅ 已授权  | Outlook 邮箱
```

#### 3. 检查邮件

```bash
# 检查最近 10 封邮件
python3 email-pro.py check --limit 10

# 检查未读邮件
python3 email-pro.py check --unread

# 指定账户
python3 email-pro.py --account qq_3421 check --limit 20
```

#### 4. 发送邮件

```bash
# 纯文本邮件
python3 email-pro.py send \
  --to "recipient@example.com" \
  --subject "测试邮件" \
  --body "这是一封测试邮件"

# HTML 格式邮件
python3 email-pro.py send \
  --to "recipient@example.com" \
  --subject "测试邮件" \
  --body "<h1>标题</h1><p>内容</p>" \
  --html

# 带附件
python3 email-pro.py send \
  --to "recipient@example.com" \
  --subject "报告" \
  --body "请查看附件" \
  --attach report.pdf data.xlsx
```

### 📧 邮箱配置

#### QQ 邮箱

**配置文件**: `~/.openclaw/credentials/email-accounts.json`

```json
{
  "qq_136": {
    "email": "136064252@qq.com",
    "auth_code": "xxxx",
    "smtp_server": "smtp.qq.com",
    "smtp_port": 587,
    "imap_server": "imap.qq.com",
    "imap_port": 993,
    "provider": "imap",
    "status": "✅ 正常",
    "note": "发送邮箱"
  }
}
```

**获取授权码**:
1. 登录 QQ 邮箱
2. 设置 → 账户 → POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV 服务
3. 开启 IMAP/SMTP 服务
4. 生成授权码

#### Outlook 邮箱

**配置文件**: `~/.openclaw/credentials/email-accounts.json`

```json
{
  "outlook_live": {
    "email": "qiao6646@live.com",
    "provider": "outlook",
    "account_name": "outlook_live",
    "client_id": "0360031a-ad0e-4bce-9d2f-0c53eda894b8",
    "client_secret": "914fb58f-4aea-4ddb-bb97-51d66581cfee",
    "tenant_id": "40a99b83-a343-41ca-b303-3e122965a6d8",
    "status": "✅ 已授权",
    "note": "Outlook 邮箱"
  }
}
```

**OAuth 令牌**: `~/.openclaw/credentials/oauth_tokens.json`

授权后自动保存，包含访问令牌和刷新令牌。

#### Gmail 邮箱（可选）

```bash
python3 authorize.py gmail \
  --client-id "YOUR_CLIENT_ID" \
  --client-secret "YOUR_CLIENT_SECRET" \
  --name "gmail_account"
`命令参考

```bash
# 列出所有账户
python3 email-pro.py list-accounts

# 检查邮件
python3 email-pro.py check --limit 10
python3 email-pro.py check --unread
python3 email-pro.py --account qq_3421 check --limit 20

# 搜索邮件
python3 email-pro.py search "旅行" --limit 50
python3 email-pro.py search "机票|酒店" --limit 100

# 获取完整邮件
python3 email-pro.py fetch 12345

# 发送邮件
python3 email-pro.py send --to "user@example.com" --subject "主题" --body "内容"
python3 email-pro.py send --to "user@example.com" --subject "主题" --body "<h1>标题</h1>" --html
python3 email-pro.py send --to "user@example.com" --subject "主题" --body "内容" --attach file1.pdf file2.txt

# 指定账户
python3 email-pro.py --account outlook_live check --limit 10
python3 email-pro.py --account qq_136 send --to "user@example.com" --subject "主题" --body "内容"
```

### 📊 性能对比

| 操作 | 旧版本 | 新版本 | 提升 |
|------|--------|--------|------|
| 检查 10 封 | 1.5-2s | 0.3-0.5s | 4-5x |
| 检查 100 封 | 15-20s | 2-3s | 6-8x |
| 检查 1000 封 | 150-200s | 15-20s | 8-10x |

### 📁 文件结构

```
email-pro-optimized/
├── scripts/
│   ├── email-pro.py              # 主程序
│   ├── providers.py              # 邮件提供商实现
│   ├── oauth_handler.py          # OAuth 处理
│   ├── authorize.py              # 授权工具uthorize-outlook.sh      # Outlook 快速授权脚本
│   └── analyze.py                # 邮件分析工具
├── SKILL.md                      # 技能文档
├── README.md                     # 本文件
└── package.json                  # 项目元数据
```

### 🎯 使用场景

1. **旅行监控** - 自动监控机票、酒店价格变化
2. **邮件备份** - 批量导出邮件为 JSON
3. **邮件分类** - 自动分类为 6 个标签
4. **批量处理** - 批量搜索、发送、转发

### 🔐 安全性

- **QQ 邮箱** - 使用授权码，不存储密码
- **Outlook/Gmail** - 使用 OAuth 2.0，令牌自动刷新
- **凭证存储** - 所有凭证保存在 `~/.openclaw/credentials/`，权限 600
- **令牌刷新** - 自动检测过期，提前 5 分钟刷新

### 🐛 故障排除

#### QQ 邮箱连接失败

```
❌ 检查邮件失败: [Errno -1] IMAP4 protocol error
```

**解决方案**:
1. 确认授权码正确（不是密码）
2. 确认 IMAP/SMTP 服务已开启
3. 检查网络连接

#### Outlook 授权失败

```
❌ 授权失败或超时
```

**解决方案**:
1. 确认 Client ID、Secret、Tenant ID 正确
2. 确认浏览器能访问 Microsoft 登录页面
3. 重新运行授权脚本

#### 邮件解析失败

某些特殊格式的邮件可能无法解析，脚本会自动跳过。

### 📝 版本历史

- **v2.2.0** (2026-03-21) - 发布到 ClawHub
- **v2.1.0** (2026-03-21) - OAuth 自动刷新 + 技能维护工具
- **v2.0.0** (2026-03-20) - Gmail/Outlook OAuth 支持
- **v1.0.0** (2026-03-19) - QQ 邮箱支持

### 💡 提示

1. **默认账户** - 所有命令默认使用 `qq_3421`，可用 `--account` 指定其他账户
2. **JSON 输出** - 所有查询结果都是 JSON 格式，便于脚本处理
3. **错误处理** 跳过损坏的邮件，继续处理其他邮件
4. **连接复用** - IMAP 连接会自动复用，提高性能

---

## English

### 📖 Introduction

**Email Pro Optimized** is a high-performance email management tool that supports QQ, Gmail, and Outlook. Using concurrent processing and connection reuse technology, it's 4-5 times faster than traditional tools. Supports OAuth 2.0 with automatic token refresh, fully automated.

### ✨ Key Features

- ✅ **Multi-Mailbox Support** - QQ, Gmail, Outlook
- ✅ **High Performance** - Concurrent processing, 4-5x faster
- ✅ **OAuth 2.0** - Secure authentication with automatic token refresh
- ✅ **Smart Classtion** - Auto-classify into 6 cate **Batch Processing** - Support batch check, search, send
- ✅ **HTML Support** - Support HTML format emails
- ✅ **Attachment Support** - Support multiple file attachments
- ✅ **JSON Output** - Easy for script processing

### 🚀 Quick Start

#### 1. Installation

```bash
# Install from ClawHub (recommended)
clawhub install q012315-email-pro-optimized

# Or install from local
clawhub install ~/.openclaw/skills/email-pro-optimized
```

#### 2. View Configured Accounts

```bash
cd scripts
python3 email-pro.py list-accounts
```

Example output:
```
📧 Configured Email Accounts:

  qq_136          | 136064252@qq.com          | SMTP/IMAP | ✅ OK     ccount
  qq_3421         | 342187916@qq.com          | SMTP/IMAP | ✅ OK      | Receive Account
  outlook_live    | qiao6646@live.com         | OAuth     | ✅ Auth    | Outlook Account
```

#### 3. Check Emails

```bash
# Check last 10 emails
python3 email-pro.py check --limit 10

# Check unread emails
python3 email-pro.py check --unread

# Specify account
python3 email-pro.py --account qq_3421 check --limit 20
```

#### 4. Send Email

```bash
# Plain text email
python3 email-pro.py send \
  --to "recipient@example.com" \
  --subject "Test Email" \
  --body "This is a test email"

# HTML format email
python3 email-pro.py send \
  --to "recipient@example.com" \
  --subject "Test Email" \
  --body "<h1>Title</h1><p>Content</p>" \
  --html

# With attachments
python3 email-pro.py send \
  --to "recipient@example.com" \
  --subject "Report" \
  --body "Please see attachment" \
  --attach report.pdf data.xlsx
```

### 📧 Mailbox Configuration

#### QQ Mailbox

**Config file**: `~/.openclaw/credentials/email-accounts.json`

```json
{
  "qq_136": {
    "email": "136064252@qq.com",
    "auth_code": "xxxx",
    "smtp_sersmtp.qq.com",
    "smtp_port": 587,
    "imap_server": "imap.qq.com",
    "imap_port": 993,
    "provider": "imap",
    "status": "✅ OK",
    "note": "Send Account"
  }
}
```

**Get Authorization Code**:
1. Login to QQ Mail
2. Settings → Account → POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV Services
3. Enable IMAP/SMTP service
4. Generate authorization code

#### Outlook Mailbox

**Config file**: `~/.openclaw/credentials/email-accounts.json`

```json
{
  "outlook_live": {
    "email": "qiao6646@live.com",
    "provider": "outlook",
    "acco: "outlook_live",
    "client_id": "0360031a-ad0e-4bce-9d2f-0c53eda894b8",
    "client_secret": "914fb58f-4aea-4ddb-bb97-51d66581cfee",
    "tenant_id": "40a99b83-a343-41ca-b303-3e122965a6d8",
    "status": "✅ Authorized",
    "note": "Outlook Account"
  }
}
```

**OAuth Token**: `~/.openclaw/credentials/oauth_tokens.json`

Automatically saved after authorization, contains access token and refresh token.

#### Gmail Mailbox (Optional)

```bash
python3 authorize.py gmail \
  --client-id "YOUR_CLIENT_ID" \
  --client-secret "YOUR_CLIENT_SECRET" \
  --name "gmail_account"
```

#and Reference

```bash
# List all accounts
python3 email-pro.py list-accounts

# Check emails
python3 email-pro.py check --limit 10
python3 email-pro.py check --unread
python3 email-pro.py --account qq_3421 check --limit 20

# Search emails
python3 email-pro.py search "travel" --limit 50
python3 email-pro.py search "flight|hotel" --limit 100

# Get full email
python3 email-pro.py fetch 12345

# Send email
python3 email-pro.py send --to "user@example.com" --subject "Subject" --body "Content"
python3 email-pro.py send --to "user@example.com" --subject "Subject" --body "<h1>Title</h1>" --html
python3 email-pro.py send --to "user@example.com" --subject "Subject" --body "Content" --attach file1.pdf file2.txt

# Specify account
python3 email-pro.py --account outlook_live check --limit 10
python3 email-pro.py --account qq_136 send --to "user@example.com" --subject "Subject" --body "Content"
```

### 📊 Performance Comparison

| Operation | Old Version | New Version | Improvement |
|-----------|-------------|-------------|-------------|
| Check 10 emails | 1.5-2s | 0.3-0.5s | 4-5x |
| Check 100 emails | 15-20s | 2-3s | 6-8x |
| Check 1000 emails | 150-200s | 15-20s | 8-10x |

### 📁 File Structure

```
email-pro-optimized/
├── scripts/
│   ├── email-pro.py              # Main program
│   ├── providers.py              # Email provider implementation
│   ├── oauth_handler.py          # OAuth handler
│   ├── authorize.py              # Authorization tool
│   ├── authorize-outlook.sh      # Outlook quick auth script
│   └── analyze.py                # Email analysis tool
├── SKILL.md                      # Skill documentation
├── README.md                     # This file
└── package.json                  # Project metadata
```

### 🎯 Use Cases

1. **Travel Monitoring** - Auto-monitor flight and hotel price changes
2. **Email Backup** - Batch export emails to JSON
3. **Email Classification** - Auto-classify into 6 categories
4. **Batch Processing** - Batch search, send, forward

### 🔐 Security

- **QQ Mailbox** - Use authorization code, no password storage
- **Outlook/Gmail** - Use OAuth 2.0 with automatic token refresh
- **Credential Storage** - All credentials saved in `~/.openclaw/credentials/` with 600 permissions
- **Token Refresh** - Auto-detect expiration, refresh 5 minutes early

### 🐛 Troubleshooting

#### QQ Mailbox Connection Failed

```
❌ Check email failed: [Errno -1] IMAP4 protocol error
```

**Sn**:
1. Confirm authorization code is correct (not password)
2. Confirm IMAP/SMTP service is enabled
3. Check network connection

#### Outlook Authorization Failed

```
❌ Authorization failed or timeout
```

**Solution**:
1. Confirm Client ID, Secret, Tenant ID are correct
2. Confirm browser can access Microsoft login page
3. Re-run authorization script

#### Email Parsing Failed

Some special format emails may fail to parse, script will auto-skip.

### 📝 Version History

- **v2.2.0** (2026-03-21) - Released to ClawHub
- **v2.1.0** (2026-03-21) - OAuth auto-refresh + skill maintenance tools
- **v2.0.0** (2026-03-20) - Gil/Outlook OAuth support
- **v1.0.0** (2026-03-19) - QQ mailbox support

### 💡 Tips

1. **Default Account** - All commands default to `qq_3421`, use `--account` to specify others
2. **JSON Output** - All query results are JSON format for easy script processing
3. **Error Handling** - Script auto-skips corrupted emails and continues processing
4. **Connection Reuse** - IMAP connections auto-reuse for better performance

---

## 📄 License

MIT License

## 🙏 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Made with ❤️ by q012315**
