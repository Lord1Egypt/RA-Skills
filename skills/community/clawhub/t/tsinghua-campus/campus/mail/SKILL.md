---
name: campus-mail
description: 清华校园邮件（收发）。配置在统一 campus/.env，支持多个邮箱账户。当用户需要"收邮件、看未读、发邮件"时使用。
metadata:
  openclaw:
    requires:
      os:
        - windows
        - macos
        - linux
---

# 邮件

收发邮件。配置从**统一配置 `campus/.env`** 读取（`MAIL_ACCOUNTS`，支持多账户），不硬编码凭据。

## 如果你是 AI，请阅读以下内容

### 铁律

- **铁律 1：AI 运行所有脚本**。禁止让用户敲命令。
- **铁律 2：脚本面向 AI**。stdout 输出 JSON，进度写 `runtime/logs/campus.log`，不写 stderr。
- **铁律 3：配置统一**。邮箱配置在 `campus/.env` 的 `MAIL_ACCOUNTS`（JSON 数组），与其他大配置（学号/姓名/CAS/API key）同一处。
- **铁律 4：发件需确认**。发送邮件是写操作，AI 必须先向用户展示收件人/主题/正文，用户确认后才执行。
- **铁律 5：隐私红线**。邮件含个人信息，面向用户输出时收件人/发件人保留，正文可展示。

### 使用

```
mail.py accounts                       # 列出配置的邮箱账户
mail.py list [--account X] [--days N]   # 收件列表（默认近1天，最多50封）
mail.py read --account X --uid <uid>    # 读单封邮件全文
mail.py send --from X --to Y --subject S --body B [--cc]  # 发邮件（需确认）
mail.py mark-read --account X [--uid U]  # 标已读（缺省全部未读）
```

输出 JSON：`accounts`（账户列表）、`list`（邮件 uid/发件人/主题/日期）、`read`（全文）、`send`（结果）、`mark_read`。

### 工作流

```
用户: 看邮件 / 有什么新邮件
AI:
  1. mail.py list --days 1 → 近1天邮件
  2. 汇报（发件人/主题），重要邮件读全文
  3. 用户确认后可标已读

用户: 给 X 发邮件
AI:
  1. mail.py send（不带执行）→ 展示收件人/主题/正文
  2. 用户确认 → 加 --confirm 执行（或直接执行前确认）
```

### 配置（统一 .env）

`skill/campus/.env`（复制 `.env.example`）：
```ini
STUDENT_ID=学号
STUDENT_NAME=姓名
CAS_USERNAME=学号
CAS_PASSWORD=统一认证密码
MAIL_ACCOUNTS=[{"name":"tsinghua","label":"清华邮箱","imap_host":"mails.tsinghua.edu.cn","imap_port":993,"smtp_host":"mails.tsinghua.edu.cn","smtp_port":465,"smtp_ssl":true,"user":"xxx@mails.tsinghua.edu.cn","password":"授权码","from_name":"姓名"}]
SCOPUS_API_KEY=
DEEPSEEK_API_KEY=
```

- 授权码获取：各邮箱设置→开启 IMAP/SMTP→生成授权码（不是登录密码）
- 清华：`mails.tsinghua.edu.cn`（IMAP 993 / SMTP 465 SSL）；QQ：`imap.qq.com`/`smtp.qq.com`（587 STARTTLS）
- 多账户：`MAIL_ACCOUNTS` 里加 JSON 对象即可

### 技术链路

- **收件**：`imaplib.IMAP4_SSL` 连接 IMAP → `SINCE` 搜索 → 解析 FROM/SUBJECT/DATE；`read` 用 `BODY.PEEK[]` 取全文
- **发件**：`smtplib` + `formataddr`（From 头）+ `Header`（中文主题）+ timeout
- **标已读**：`imap.store(ids, "+FLAGS", "\\Seen")`（用实际 uid 列表，勿硬编码序号）

### 边界

- 仅文本邮件；附件下载未实现。
- 发件前必须确认（写操作）。
- 默认账户：`list` 无 `--account` 时用第一个。

---

## 如果你是用户，请阅读以下内容

对 AI 说：
- **"看邮件"** / "有什么新邮件" — 收件列表
- **"读那封邮件"** — 读单封
- **"给 XX 发邮件"** — 发邮件（AI 会先给你确认）
