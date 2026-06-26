---
name: qq-email-watcher
description: 监控 QQ 邮箱白名单联系人的新邮件，通过 QQ 消息主动推送通知。支持 AI 智能摘要、验证码/关键信息高亮、简洁预览。当用户需要设置邮件提醒、管理 QQ 邮箱白名单、自动化邮件监控通知时使用。
---

# QQ 邮箱监控通知

## 功能特性

- 🔍 **IMAP 轮询** — 每 30 秒检查 QQ 邮箱，支持白名单过滤
- 🤖 **AI 智能摘要** — 调用 OpenClaw AI 提炼邮件关键信息（验证码、金额、链接等）
- ✂️ **智能预览** — 短邮件展示全文，长邮件 AI 总结
- 🔕 **去重机制** — 首次运行自动初始化已处理记录，重启不重复通知
- 🔒 **白名单管理** — 仅监控指定联系人的邮件

## 首次配置

### 1. 编辑脚本配置

在 `scripts/email_watcher.py` 顶部修改配置区：

```python
EMAIL = "你的QQ邮箱@qq.com"
AUTH_CODE = "你的IMAP授权码"
WHITELIST_FILE = "白名单文件路径"
QQ_TARGET = "你的QQ OpenID"
```

### 2. 创建白名单文件

```json
["734743044@qq.com", "3678898561@qq.com"]
```

### 3. 启动监听

```bash
python3 ~/.openclaw/workspace/skills/qq-email-watcher/scripts/email_watcher.py &
```

## 日常操作

**查看状态：**
```bash
ps aux | grep email_watcher
```

**添加白名单：** 编辑 `whitelist.json`，脚本下次轮询自动加载

**停止服务：**
```bash
pkill -f email_watcher.py
```

**查看日志：**
```bash
tail -f ~/.openclaw/workspace/email_watcher.log
```

## 消息格式

收到邮件时，QQ 收到类似：

```
📧 [邮件主题]
👤 发件人名称 <发件人@邮箱.com>
📝 【AI摘要】验证码邮件，验证码 **123456**，有效期 30 分钟。
```

## 文件结构

```
qq-email-watcher/
├── SKILL.md
├── scripts/
│   └── email_watcher.py    # 主监听脚本（含 AI 摘要）
└── references/
    └── configure.md        # 详细配置指南
```
