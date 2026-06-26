---
name: mail-sender
description: 邮件发送工具，支持 HTML 和 Markdown 格式。当用户需要发送邮件、通知、报告、提醒或任何邮件相关任务时使用此技能。触发场景包括：(1) 发送 HTML 格式邮件，(2) 发送 Markdown 格式邮件（自动转换为 HTML），(3) 批量发送邮件给多个收件人，(4) 发送系统通知或报告，(5) 发送带格式的内容（表格、代码等）。
---

# Mail Sender - 邮件发送技能

邮件发送工具，提供安全、易用的邮件发送功能。支持 HTML 和 Markdown 格式，支持多收件人，配置灵活。

## 功能特点

- ✉️ **多种格式** - 支持 HTML 和 Markdown 格式
- 👥 **多收件人** - 支持批量发送邮件
- 🔒 **安全配置** - 支持配置文件和环境变量
- 📝 **自动转换** - Markdown 自动转换为 HTML
- ⚙️ **灵活配置** - 多种配置方式，优先级清晰

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置说明

### 配置文件位置（按优先级）

1. `MAIL_CONFIG_PATH` 环境变量指定的路径
2. `~/.openclaw/skills/mail-sender/config.json`（优先）
3. `~/.openclaw/skills/config/mail-sender/config.json`（备选，卸载技能不影响配置）
4. `{skill_dir}/config.json`
5. `./.mail-sender-config.json`

> **推荐**：使用 `~/.openclaw/skills/config/mail-sender/config.json`，独立于技能安装目录。

### 配置文件示例

```json
{
  "sender_email": "your_email@163.com",
  "sender_password": "your_auth_code",
  "smtp_server": "smtp.163.com",
  "smtp_port": 465,
  "default_receivers": ["user@example.com"],
  "sender_name": "Your Name"
}
```

### 环境变量配置

```bash
export MAIL_SENDER_EMAIL="your_email@163.com"
export MAIL_SENDER_PASSWORD="your_auth_code"
export MAIL_DEFAULT_RECEIVERS="default@example.com"
```

## 使用方法

### 1. 发送 HTML 邮件

```python
from mail_sender import send_mail

# 单个收件人
result = send_mail(
    subject='测试邮件',
    content='<h1>标题</h1><p>内容</p>',
    receivers='user@example.com'
)

# 多个收件人
result = send_mail(
    subject='团队通知',
    content='<p>内容</p>',
    receivers='user1@example.com,user2@example.com'
)

# 使用默认收件人
result = send_mail(
    subject='系统通知',
    content='<p>内容</p>'
)
```

### 2. 发送 Markdown 邮件

```python
from mail_sender import send_markdown

result = send_markdown(
    subject='周报',
    content='''
# 本周工作总结

## 完成事项
- 完成功能 A
- 修复 Bug B

## 下周计划
1. 开发功能 C
2. 代码审查
''',
    receivers='team@example.com'
)
```

### 3. 自定义配置

```python
from mail_sender import MailConfig, MailSender

config = MailConfig(
    sender_email="your_email@163.com",
    sender_password="your_auth_code",
    sender_name="Your Name",
    default_receivers=["default@example.com"]
)

sender = MailSender(config)
result = sender.send_mail(
    subject='测试',
    content='<p>内容</p>'
)
```

## 返回值

所有发送函数返回统一的字典格式：

```python
{
    'success': True/False,          # 是否成功
    'message': '邮件发送成功！',      # 结果消息
    'failed_receivers': []          # 失败的收件人列表
}
```

## 常见邮箱配置

### 163 邮箱
```json
{
  "smtp_server": "smtp.163.com",
  "smtp_port": 465
}
```

### QQ 邮箱
```json
{
  "smtp_server": "smtp.qq.com",
  "smtp_port": 465
}
```

### Gmail
```json
{
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587
}
```

## 使用场景

1. **发送报告** - 发送每日/每周数据报告
2. **系统通知** - 发送系统维护、更新通知
3. **定时任务** - 结合定时任务发送定期邮件
4. **批量通知** - 批量发送通知给多个收件人

## 故障排查

| 问题 | 解决方案 |
|------|---------|
| 登录失败 | 检查是否使用授权码（不是登录密码） |
| 连接超时 | 检查 SMTP 服务器和端口 |
| 邮件被拒 | 检查收件人地址格式 |
| Markdown 转换失败 | 安装 `markdown` 库：`pip install markdown` |

## 注意事项

1. ✅ **使用授权码**：不要使用邮箱登录密码
2. ✅ **检查返回值**：检查 `success` 字段
3. ✅ **合理使用**：避免发送垃圾邮件
4. ❌ **不要硬编码**：避免在代码中直接写密码

## 依赖

- Python 3.6+
- `markdown`（可选，用于 Markdown 转换）

```bash
pip install markdown
```
