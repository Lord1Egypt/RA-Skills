---
name: tencent-exmail
description: 腾讯企业邮箱（exmail.qq.com）收发邮件技能。当用户想要发送邮件、查看收件箱、搜索邮件、下载附件、实时监听新邮件、或对腾讯企业邮箱进行任何邮件操作时触发。支持 IMAP/SMTP 协议，SSL 加密，附件上传/下载，邮件搜索，IMAP IDLE 实时推送通知。关键词：企业邮箱、exmail、腾讯邮件、发邮件、收邮件、查邮件、邮件搜索、邮件附件、实时通知、新邮件提醒。
user-invocable: true
metadata:
  {
    "openclaw": {
      "emoji": "📧",
      "skillKey": "tencent-exmail",
      "requires": {
        "bins": ["python3"],
        "pip": ["imapclient"],
        "env": ["EXMAIL_ADDRESS", "EXMAIL_PASSWORD"]
      }
    }
  }
---

# 腾讯企业邮箱 Skill

通过 IMAP/SMTP 协议操作腾讯企业邮箱（exmail.qq.com），支持收发邮件、搜索、附件等完整功能。

---

## 📋 配置说明

在 OpenClaw 配置中设置以下环境变量：

```json
{
  "skills": {
    "entries": {
      "tencent-exmail": {
        "enabled": true,
        "env": {
          "EXMAIL_ADDRESS": "your_name@your_company.com",
          "EXMAIL_PASSWORD": "your_password_or_auth_code"
        }
      }
    }
  }
}
```

> **注意**：如果账号已绑定微信，请使用邮箱控制台生成的「客户端专用密码」（授权码），而非登录密码。

---

## 🔧 服务器参数（已内置，无需手动配置）

| 协议 | 服务器 | 端口 | 加密 |
|------|--------|------|------|
| IMAP（收信） | `imap.exmail.qq.com` | `993` | SSL |
| SMTP（发信） | `smtp.exmail.qq.com` | `465` | SSL |
| POP3（收信）| `pop.exmail.qq.com` | `995` | SSL |

---

## 🚀 功能列表与使用方法

### 1. 发送邮件

**用户指令示例**：
- "发送邮件给 zhang@company.com，主题：项目进展，内容：……"
- "给客户发一封带附件的邮件"

**执行方式**：调用 `scripts/send_email.py`

```bash
python3 scripts/send_email.py \
  --to "recipient@example.com" \
  --subject "邮件主题" \
  --body "邮件正文内容" \
  [--cc "cc@example.com"] \
  [--attachment "/path/to/file.pdf"]
```

支持参数：
- `--to` 收件人（多个用逗号分隔）
- `--cc` 抄送（可选）
- `--bcc` 密送（可选）
- `--subject` 主题
- `--body` 正文（支持纯文本和 HTML）
- `--html` 发送 HTML 格式（flag）
- `--attachment` 附件路径（可多次使用添加多个附件）

---

### 2. 查看收件箱

**用户指令示例**：
- "查看我的收件箱"
- "显示最新 10 封邮件"
- "有什么未读邮件吗？"

**执行方式**：调用 `scripts/read_email.py`

```bash
python3 scripts/read_email.py \
  --action list \
  --folder INBOX \
  --limit 20 \
  [--unread-only]
```

---

### 3. 读取邮件详情

**用户指令示例**：
- "打开第 3 封邮件"
- "读取邮件 ID 为 XX 的内容"

```bash
python3 scripts/read_email.py \
  --action read \
  --uid <邮件UID>
```

---

### 4. 搜索邮件

**用户指令示例**：
- "搜索来自 boss@company.com 的邮件"
- "找主题包含「合同」的邮件"
- "搜索上周收到的邮件"

```bash
python3 scripts/read_email.py \
  --action search \
  --query "FROM boss@company.com" \
  [--folder INBOX] \
  [--limit 20]
```

搜索语法支持（IMAP 标准）：
- `FROM "sender@example.com"` — 按发件人
- `TO "me@company.com"` — 按收件人
- `SUBJECT "关键词"` — 按主题
- `BODY "关键词"` — 按正文
- `SINCE 01-Jan-2025` — 按日期
- `UNSEEN` — 未读邮件
- `SEEN` — 已读邮件
- 组合：`FROM "boss" SINCE 01-Mar-2025 UNSEEN`

---

### 5. 下载附件

**用户指令示例**：
- "下载邮件里的附件"
- "保存附件到桌面"

```bash
python3 scripts/read_email.py \
  --action download-attachment \
  --uid <邮件UID> \
  --save-dir "/path/to/save/dir"
```

---

### 6. 查看其他文件夹

```bash
python3 scripts/read_email.py \
  --action list-folders
```

常见文件夹名称：`INBOX`、`Sent Messages`、`Drafts`、`Deleted Messages`、`Junk`

---

### 7. 标记已读 / 移动邮件

```bash
# 标记已读
python3 scripts/read_email.py --action mark-read --uid <UID>

# 标记未读
python3 scripts/read_email.py --action mark-unread --uid <UID>

# 移动到文件夹
python3 scripts/read_email.py --action move --uid <UID> --target-folder "Archived"
```

---

### 8. 实时监听新邮件（IMAP IDLE）

**用户指令示例**：
- "实时监听我的邮箱"
- "有新邮件到了通知我"
- "后台监听邮件，保存到文件"

**首次使用需安装依赖**：
```bash
pip3 install imapclient
```

**执行方式**：调用 `scripts/watch_email.py`

```bash
# 监听收件箱，终端实时打印通知
python3 scripts/watch_email.py

# 监听并将新邮件信息写入 JSON 文件（供 OpenClaw 读取）
python3 scripts/watch_email.py \
  --hook-file ~/.openclaw/workspace/new_emails.json

# 后台运行（静默模式）
python3 scripts/watch_email.py \
  --hook-file ~/.openclaw/workspace/new_emails.json \
  --quiet &
```

**工作原理**：
- 使用 **IMAP IDLE** 协议——服务器主动推送，无轮询，响应延迟 < 1 秒
- 每 29 分钟自动重连（防止服务器 30 分钟超时断开）
- 断线自动重连，保持持续监听
- 新邮件信息写入 JSON 文件（最多保留最近 100 条）

**JSON 输出格式**（`--hook-file` 模式）：
```json
[
  {
    "timestamp": "2025-03-17T10:23:45",
    "folder": "INBOX",
    "uid": 1234,
    "subject": "项目进展汇报",
    "from": "张三 <zhang@company.com>",
    "date": "Mon, 17 Mar 2025 10:23:40 +0800",
    "size_kb": 12.5,
    "is_unread": true
  }
]
```

---

## 📎 附件处理规范

- 上传附件：用户提供本地文件路径，脚本自动 base64 编码
- 下载附件：自动解码保存到指定目录，默认 `~/Downloads/`
- 支持所有 MIME 类型（PDF、图片、Office 文档等）
- 单封邮件支持多个附件

---

## ⚠️ 错误处理

| 错误信息 | 可能原因 | 解决方案 |
|---------|---------|---------|
| `535 Authentication failed` | 密码错误或未使用授权码 | 检查密码，若绑定微信需使用客户端专用密码 |
| `Connection refused` | 网络问题或端口被封 | 检查网络，确认 465/993 端口开放 |
| `Mailbox not found` | 文件夹名称错误 | 先用 `list-folders` 查看正确名称 |
| `Message not found` | UID 失效 | 重新查询最新 UID |

---

## 🔒 安全说明

- 所有连接均使用 SSL/TLS 加密（IMAP:993, SMTP:465）
- 密码仅存储在本地 OpenClaw 配置中，不会上传
- 海外用户可改用 `hwimap.exmail.qq.com` / `hwsmtp.exmail.qq.com`

---

## 📚 参考文档

详细实现和故障排查请参阅：
- `references/server-config.md` — 服务器参数完整说明
- `references/troubleshooting.md` — 常见问题解答
