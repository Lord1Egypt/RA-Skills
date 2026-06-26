---
name: upkuajing-email-tool
description: Official skill for upkuajing (跨境魔方). Email tool API for sending emails and tracking email task status. Includes email sending, task list, and task record list APIs.
metadata: {"version":"1.0.0","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"✉️","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# UpKuaJing Email Tool

Send emails and track email task status using the UpKuaJing Open Platform API.

## Overview

This skill provides access to UpKuaJing's email service through:
- **Email Send** (`mail_send.py`): Send emails to recipients
- **Email Task List** (`mail_task_list.py`): View email task list with time range filter
- **Email Task Record List** (`mail_task_record_list.py`): View detailed records for a specific task

## Running Scripts

### Environment Setup

1. **Check Python**: `python --version`
2. **Install dependencies**: `pip install -r requirements.txt`

Script directory: `scripts/*.py`
Run example: `python scripts/*.py`

**Important**: Always use direct script invocation like `python scripts/mail_task_list.py`. **Do NOT use** shell compound commands like `cd scripts && python mail_task_list.py`.

## Three Main APIs

### Email Send (`mail_send.py`)

Send emails to recipients.

**Parameters**: See [Email Send API](references/email-send-api.md)

**Examples**:
```bash
# Send a simple email
python scripts/mail_send.py \
  --subject "Test Email" \
  --content "This is the email content" \
  --emails '["recipient@example.com"]'

# Send email with reply address
python scripts/mail_send.py \
  --subject "Test Email" \
  --content "This is the email content" \
  --reply_email "support@example.com" \
  --emails '["recipient@example.com"]'

# Send to multiple recipients
python scripts/mail_send.py \
  --subject "Test Email" \
  --content "This is the email content" \
  --emails '["user1@example.com","user2@example.com"]'
```

### Email Task List (`mail_task_list.py`)

View email task list with optional time range filter.

**Parameters**: See [Email Task List API](references/email-task-list-api.md)

**Examples**:
```bash
# Get task list (first page, 10 items)
python scripts/mail_task_list.py --page_no 1 --page_size 10

# Filter by time range
python scripts/mail_task_list.py \
  --start_time 1775812273 \
  --end_time 1775900000 \
  --page_no 1 \
  --page_size 10

# Filter by status (0-待发送 1-发送中 2-发送完成)
python scripts/mail_task_list.py --status 2 --page_no 1 --page_size 10
```

### Email Task Record List (`mail_task_record_list.py`)

View detailed records for a specific email task.

**Parameters**: See [Email Task Record List API](references/email-task-record-list-api.md)

**Examples**:
```bash
# Get records for task ID 1496
python scripts/mail_task_record_list.py --task_id 1496 --page_no 1 --page_size 10

# Filter by time range and status
python scripts/mail_task_record_list.py \
  --task_id 1496 \
  --start_time 1775812273 \
  --end_time 1775900000 \
  --status 2 \
  --page_no 1 \
  --page_size 10
```

## API Key and UpKuaJing Account

- **API Key**: Stored in `~/.upkuajing/.env` file as `UPKUAJING_API_KEY`
- **First check**: If not set, prompt user to provide or apply at [UpKuaJing Open Platform](https://developer.upkuajing.com/)

### **API Key Not Set**
First check if the `~/.upkuajing/.env` file has UPKUAJING_API_KEY;
If UPKUAJING_API_KEY is not set, prompt the user to choose:
1. User has one: User provides it (manually add to ~/.upkuajing/.env file)
2. User doesn't have one: Guide user to apply at [UpKuaJing Open Platform](https://developer.upkuajing.com/)
Wait for user selection;

### **Account Top-up**
When API response indicates insufficient balance, explain and guide user to top up:
1. Create top-up order (`auth.py --new_rec_order`)
2. Based on order response, send payment page URL to user, guide user to open URL and pay, user confirms after successful payment;

### **Get Account Information**
Use this script to get account information for UPKUAJING_API_KEY: `auth.py --account_info`

## Fees

**Email sending API calls incur fees**, different interfaces have different billing methods.
**Latest pricing**: Users can visit [Detailed Price Description](https://www.upkuajing.com/web/openapi/price.html)
Or use: `python scripts/auth.py --price_info` (returns complete pricing for all interfaces)

### Email Send Billing Rules

**Email sending is charged** — each send request incurs a fee based on the number of recipients.

### Task List & Record List Billing Rules

**Free of charge** — No fees for task list and task record list queries.

### Fee Confirmation Principle

**Any operation that incurs fees must first inform and wait for explicit user confirmation. Do not execute in the same message as the notification.**

## Workflow

### Decision Guide

| User Intent | Use API |
|-------------|---------|
| "Send an email" | Email Send |
| "View my email tasks" | Email Task List |
| "Check email delivery status" | Email Task Record List |
| "Find tasks in a time range" | Email Task List (with start_time/end_time) |

### Email Send Flow

1. **Prepare email content**: Subject, content, recipients
2. **Execute send**: Use mail_send.py with appropriate parameters
3. **Get response**: API returns task result synchronously

### Task Check Flow

1. **View task list**: Use mail_task_list.py with optional time filter
2. **Get task ID**: From the task list response
3. **View task records**: Use mail_task_record_list.py with task_id

## Error Handling

- **API key invalid/non-existent**: Check `UPKUAJING_API_KEY` in `~/.upkuajing/.env` file
- **Insufficient balance**: Guide user to top up
- **Invalid parameters**: **Must first check the corresponding API documentation in references/ directory**, get correct parameter names and formats from documentation, do not guess

### API Documentation Reference

- Email Send: Check [references/email-send-api.md](references/email-send-api.md)
- Email Task List: Check [references/email-task-list-api.md](references/email-task-list-api.md)
- Email Task Record List: Check [references/email-task-record-list-api.md](references/email-task-record-list-api.md)

## Notes

- File paths use forward slashes on all platforms
- **Do not guess parameter names**, get accurate parameter names and formats from documentation
- **Prohibit outputting technical parameter format**: Do not display code-style parameters in responses, convert to natural language
- **Do not estimate or guess fees** — use `python scripts/auth.py --price_info` to get accurate pricing information
- **Email sending is synchronous submission**: The API returns response immediately after submission, but the email server processes asynchronously; the `status` field in response indicates sending status (0-pending 1-sending 2-completed)

## Related Skills

Other UpKuaJing skills you might find useful:

- upkuajing-global-company-people-search — Global company and people search
- upkuajing-customs-trade-company-search — Search customs trade companies
- upkuajing-map-merchants-search — Map-based merchant search
- upkuajing-contact-info-validity-check — Check contact info validity