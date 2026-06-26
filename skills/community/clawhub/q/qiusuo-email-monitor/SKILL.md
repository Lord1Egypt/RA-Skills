---
name: email-monitor
description: >
  Set up periodic email monitoring for any IMAP mailbox (Gmail, Outlook, QQ, etc.).
  Guides users through mailbox configuration, tests the connection, then creates a
  scheduled cron task to check for new emails at user-defined intervals and deliver
  summaries in a custom format. Use when a user wants to automatically monitor an
  inbox for new messages, set up periodic email fetching or summarization, or
  configure email alerts and digests on a schedule.
---

# Email Monitor Skill

This skill guides the user through a 6-step onboarding to set up automated email monitoring.

## Onboarding Flow

Work through these steps **in order**, one step per conversation turn. Do not skip ahead.

### Step 1 — Ask which mailbox to monitor

Ask the user:
> "请告诉我你想监控的邮箱地址是什么？（例如 yourname@gmail.com）"

### Step 2 — Provide provider-specific setup guidance

Based on the email domain, read `references/imap-setup.md` and show the user the relevant setup instructions:
- `@gmail.com` → Gmail IMAP + App Password guide
- `@outlook.com` / `@hotmail.com` → Outlook section
- `@qq.com` → QQ Mail section
- Others → Generic IMAP section

Ask the user to provide:
- Their **email address**
- Their **app password** (or account password for non-Gmail)

Store these in a local config file: `~/.openclaw/email-monitor/<sanitized-email>/config.json`

Config template:
```json
{
  "email": "<email>",
  "password": "<password>",
  "imap_host": "<host>",
  "imap_port": 993,
  "mailbox": "INBOX",
  "state_file": "~/.openclaw/email-monitor/<sanitized-email>/state.json",
  "max_emails": 20,
  "fetch_attachments": false,
  "attachment_dir": "~/Downloads/email-attachments"
}
```

### Step 3 — Test connection

Run the fetch script once to verify credentials and connectivity:

```bash
python3 <skill_dir>/scripts/fetch_emails.py --config ~/.openclaw/email-monitor/<sanitized-email>/config.json
```

- **Success**: Show the user a sample of fetched emails (first 3), confirm "连接成功！"
- **Failure**: Show the error message, help the user troubleshoot (wrong password, IMAP not enabled, etc.)

Only proceed to Step 4 after a successful test.

### Step 4 — Ask for polling interval

Ask:
> "连接成功！你希望每隔多久检查一次新邮件？（例如：每1小时、每2小时、每天早上8点）"

Parse the user's answer into a valid cron expression. Examples:
- "每小时" → `0 * * * *`
- "每2小时" → `0 */2 * * *`
- "每天早上8点" → `0 8 * * *`
- "每4小时" → `0 */4 * * *`

### Step 5 — Ask for notification format and attachment handling

Ask two questions in one message:

> **消息格式**：新邮件通知时，你希望看到哪些信息？
> - A) 简洁版：发件人 + 主题 + 日期
> - B) 标准版：发件人 + 主题 + 日期 + 摘要（前200字）
> - C) 自定义（请描述）
>
> **附件**：是否需要下载附件？如果需要，保存到哪个目录？

Update `config.json` with `fetch_attachments` and `attachment_dir` based on the response.

Store the notification format preference as `notify_format` in config.json:
- `"brief"` for A
- `"standard"` for B  
- `"<custom template string>"` for C

### Step 6 — Summarize and create cron job

Show a confirmation summary:
```
📧 邮件监控配置确认

邮箱：<email>
检查频率：每 X 小时（cron: <expr>）
通知格式：<format>
下载附件：<yes/no>（保存至：<dir>）

确认后将创建定时任务。确认吗？（是/否）
```

After user confirms, create the cron job using openclaw:

```bash
openclaw cron add "<cron-expr>" "检查邮件 <email>" --run "python3 <skill_dir>/scripts/fetch_emails.py --config ~/.openclaw/email-monitor/<email>/config.json"
```

Then confirm to the user that the cron task is active.

---

## Running Manually

At any time the user can say "现在检查一下邮件" or similar — run the fetch script and display results using the configured format.

## Format Templates

**brief**:
```
📩 [<date>] <from> — <subject>
```

**standard**:
```
📩 <subject>
👤 <from>
📅 <date>
---
<snippet>
```

## Config File Location

Always store per-account config at:
`~/.openclaw/email-monitor/<sanitized-email>/config.json`

Where `<sanitized-email>` = email address with `@` replaced by `_at_` and `.` replaced by `_`.
Example: `qiusuo9809_at_gmail_com`

## State File

The state file tracks the last fetched UID to avoid re-sending old emails.
It is auto-managed by `scripts/fetch_emails.py`.
If the user wants to re-fetch all emails, delete the state file.
