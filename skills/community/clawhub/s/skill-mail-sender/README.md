---
name: mail-sender
description: 邮件发送工具，支持 HTML 和 Markdown 格式。当用户需要发送邮件、通知、报告、提醒或任何邮件相关任务时使用此技能。触发场景包括：(1) 发送 HTML 格式邮件，(2) 发送 Markdown 格式邮件（自动转换为 HTML），(3) 批量发送邮件给多个收件人，(4) 发送系统通知或报告，(5) 发送带格式的内容（表格、代码等）。
---

# Mail Sender

## 概述

邮件发送工具，提供安全、易用的邮件发送功能。支持 HTML 和 Markdown 格式，支持多收件人，配置灵活。

## 快速开始

### 1. 配置邮箱（首次使用）

#### 方式一：配置文件（推荐）

**推荐位置**：`~/.openclaw/skills/mail-sender/config.json`

```bash
# Linux/macOS
mkdir -p ~/.openclaw/skills/mail-sender
nano ~/.openclaw/skills/mail-sender/config.json

# Windows (PowerShell)
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.openclaw\skills\mail-sender"
notepad "$env:USERPROFILE\.openclaw\skills\mail-sender\config.json"
```

**配置文件内容**：
```json
{
  "sender_email": "your_email@163.com",
  "sender_password": "your_auth_code",
  "smtp_server": "smtp.163.com",
  "smtp_port": 465,
  "default_receivers": ["user@example.com"],
  "sender_name": "Wezin"
}
```

#### 方式二：环境变量

```bash
# Linux/macOS
export MAIL_SENDER_EMAIL="your_email@163.com"
export MAIL_SENDER_PASSWORD="your_auth_code"
export MAIL_DEFAULT_RECEIVERS="default@example.com"

# Windows (PowerShell)
$env:MAIL_SENDER_EMAIL="your_email@163.com"
$env:MAIL_SENDER_PASSWORD="your_auth_code"
$env:MAIL_DEFAULT_RECEIVERS="default@example.com"
```

#### 配置优先级

1. **构造函数参数**（最高优先级）
2. **环境变量**
3. **配置文件**
4. **默认值**

#### 配置文件查找顺序

1. `MAIL_CONFIG_PATH` 环境变量指定的路径
2. `~/.openclaw/skills/mail-sender/config.json`（优先）
3. `~/.openclaw/skills/config/mail-sender/config.json`（备选，卸载技能不影响配置）
4. `{skill_dir}/config.json`
5. `./.mail-sender-config.json`

> **注意**：推荐将配置文件放在 `~/.openclaw/skills/config/` 目录下，独立于技能安装目录，卸载重装技能不会丢失配置。

### 2. 发送邮件

**发送 HTML 邮件**：
```python
from mail_sender import send_mail

result = send_mail(
    subject='测试邮件',
    content='<h1>标题</h1><p>内容</p>',
    receivers='user@example.com'
)
print(result)  # {'success': True, 'message': '邮件发送成功！', 'failed_receivers': []}
```

**发送 Markdown 邮件**：
```python
from mail_sender import send_markdown

result = send_markdown(
    subject='报告',
    content='# 标题\n\n## 章节\n\n内容...',
    receivers='user@example.com'
)
```

## 核心功能

### 1. 发送 HTML 邮件

```python
# 单个收件人
send_mail(
    subject='会议通知',
    content='<h1>会议提醒</h1><p>时间：明天 10:00</p>',
    receivers='user@example.com'
)

# 多个收件人（字符串）
send_mail(
    subject='团队通知',
    content='<p>内容</p>',
    receivers='user1@example.com,user2@example.com'
)

# 多个收件人（列表）
send_mail(
    subject='项目更新',
    content='<p>更新内容</p>',
    receivers=['user1@example.com', 'user2@example.com']
)

# 使用默认收件人
send_mail(
    subject='系统通知',
    content='<p>内容</p>'
)
```

### 2. 发送 Markdown 邮件

```python
from mail_sender import send_markdown

# 简单 Markdown
send_markdown(
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

# 带表格的 Markdown
send_markdown(
    subject='数据分析报告',
    content='''
# 数据分析

| 指标 | 本周 | 上周 | 变化 |
|------|------|------|------|
| 用户数 | 1000 | 800 | +25% |
| 访问量 | 5000 | 4000 | +25% |
''',
    receivers='manager@example.com'
)
```

### 3. 自定义配置

```python
from mail_sender import MailConfig, MailSender

# 创建自定义配置
config = MailConfig(
    sender_email="your_email@163.com",
    sender_password="your_auth_code",
    sender_name="Wezin",
    default_receivers=["default@example.com"]
)

# 使用自定义配置
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

### 1. 发送报告
```python
send_markdown(
    subject='每日数据报告',
    content='''
# 数据概览

| 指标 | 数值 |
|------|------|
| 访问量 | 10,000 |
| 转化率 | 5% |
''',
    receivers='manager@example.com'
)
```

### 2. 系统通知
```python
send_mail(
    subject='系统维护通知',
    content='''
<h1>系统维护</h1>
<p>时间：今晚 22:00-23:00</p>
<p>影响：服务暂停 1 小时</p>
''',
    receivers='team@example.com,admin@example.com'
)
```

### 3. 定时任务
```python
from apscheduler.schedulers.blocking import BlockingScheduler
from mail_sender import send_markdown

def send_daily_report():
    report = generate_report()
    send_markdown(
        subject='每日报告',
        content=report,
        receivers='manager@example.com'
    )

scheduler = BlockingScheduler()
scheduler.add_job(send_daily_report, 'cron', hour=18)
scheduler.start()
```

## 配置验证

配置会自动验证以下内容：
- ✅ 发件人邮箱格式
- ✅ SMTP 端口范围（1-65535）
- ✅ 必需配置是否存在
- ⚠️ 默认收件人邮箱格式（仅警告）

## 最佳实践

1. ✅ **使用配置文件**：推荐 `~/.openclaw/skills/mail-sender/config.json`
2. ✅ **使用授权码**：不要使用邮箱登录密码
3. ✅ **检查返回值**：检查 `success` 字段
4. ✅ **合理使用**：避免发送垃圾邮件
5. ❌ **不要硬编码**：避免在代码中直接写密码

## 故障排查

| 问题 | 解决方案 |
|------|---------|
| 登录失败 | 检查是否使用授权码（不是登录密码） |
| 连接超时 | 检查 SMTP 服务器和端口 |
| 邮件被拒 | 检查收件人地址格式 |
| Markdown 转换失败 | 安装 `markdown` 库：`pip install markdown` |

## 依赖

- Python 3.6+
- `markdown`（可选，用于 Markdown 转换）

```bash
pip install markdown
```
