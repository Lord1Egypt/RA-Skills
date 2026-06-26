---
name: upkuajing-sms-tool
description: Official skill for upkuajing (跨境魔方). SMS tool API for sending SMS and tracking SMS task status. Includes SMS sending, task list, and task record list APIs.
metadata: {"version":"1.0.0","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"📱","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# UpKuaJing SMS Tool

Send SMS and track SMS task status using the UpKuaJing Open Platform API.

## Overview

This skill provides access to UpKuaJing's SMS service through:
- **SMS Send** (`sms_send.py`): Send SMS to phone numbers
- **SMS Task List** (`sms_task_list.py`): View SMS task list with time range filter
- **SMS Task Record List** (`sms_task_record_list.py`): View detailed records for a specific task

## Running Scripts

### Environment Setup

1. **Check Python**: `python --version`
2. **Install dependencies**: `pip install -r requirements.txt`

Script directory: `scripts/*.py`
Run example: `python scripts/*.py`

**Important**: Always use direct script invocation like `python scripts/sms_send.py`. **Do NOT use** shell compound commands like `cd scripts && python sms_send.py`.

## Three Main APIs

### SMS Send (`sms_send.py`)

Send SMS to phone numbers.

**Parameters**: See [SMS Send API](references/sms-send-api.md)

**Examples**:
```bash
# Send a simple SMS
python scripts/sms_send.py \
  --content "This is SMS content" \
  --phones '["13800138000"]'

# Send with two-way mode (supports receiving replies)
python scripts/sms_send.py \
  --content "This is SMS content" \
  --phones '["13800138000"]' \
  --channel_type 1

# Send to multiple phone numbers
python scripts/sms_send.py \
  --content "This is SMS content" \
  --phones '["13800138000","13800138001"]'
```

### SMS Task List (`sms_task_list.py`)

View SMS task list with optional time range filter.

**Parameters**: See [SMS Task List API](references/sms-task-list-api.md)

**Examples**:
```bash
# Get task list (first page, 10 items)
python scripts/sms_task_list.py --page_no 1 --page_size 10

# Filter by time range
python scripts/sms_task_list.py \
  --start_time 1775812273 \
  --end_time 1775900000 \
  --page_no 1 \
  --page_size 10

# Filter by status (0-待发送 1-发送中 2-发送完成)
python scripts/sms_task_list.py --status 2 --page_no 1 --page_size 10
```

### SMS Task Record List (`sms_task_record_list.py`)

View detailed records for a specific SMS task.

**Parameters**: See [SMS Task Record List API](references/sms-task-record-list-api.md)

**Examples**:
```bash
# Get records for task ID 1496
python scripts/sms_task_record_list.py --task_id 1496 --page_no 1 --page_size 10

# Filter by time range and status
python scripts/sms_task_record_list.py \
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
2. User doesn't have one: You can apply using the API (`auth.py --new_key`), the new key will be automatically saved to ~/.upkuajing/.env
Wait for user selection;

### **Account Top-up**
When API response indicates insufficient balance, explain and guide user to top up:
1. Create top-up order (`auth.py --new_rec_order`)
2. Based on order response, send payment page URL to user, guide user to open URL and pay, user confirms after successful payment;

### **Get Account Information**
Use this script to get account information for UPKUAJING_API_KEY: `auth.py --account_info`

## Fees

**SMS sending API calls incur fees**, different interfaces have different billing methods.
**Latest pricing**: Users can visit [Detailed Price Description](https://www.upkuajing.com/web/openapi/price.html)
Or use: `python scripts/auth.py --price_info` (returns complete pricing for all interfaces)

### SMS Send Billing Rules

**SMS sending is charged** — each send request incurs a fee based on the number of phone numbers.

### Task List & Record List Billing Rules

**Free of charge** — No fees for task list and task record list queries.

### Fee Confirmation Principle

**Any operation that incurs fees must first inform and wait for explicit user confirmation. Do not execute in the same message as the notification.**

## Workflow

### Decision Guide

| User Intent | Use API |
|-------------|---------|
| "Send an SMS" | SMS Send |
| "View my SMS tasks" | SMS Task List |
| "Check SMS delivery status" | SMS Task Record List |
| "Find tasks in a time range" | SMS Task List (with start_time/end_time) |

### SMS Send Flow

1. **Prepare SMS content**: content, phone number list
2. **Execute send**: Use sms_send.py with appropriate parameters
3. **Get response**: API returns task result synchronously

### Task Check Flow

1. **View task list**: Use sms_task_list.py with optional time filter
2. **Get task ID**: From the task list response
3. **View task records**: Use sms_task_record_list.py with task_id

## Error Handling

- **API key invalid/non-existent**: Check `UPKUAJING_API_KEY` in `~/.upkuajing/.env` file
- **Insufficient balance**: Guide user to top up
- **Invalid parameters**: **Must first check the corresponding API documentation in references/ directory**, get correct parameter names and formats from documentation, do not guess

### API Documentation Reference

- SMS Send: Check [references/sms-send-api.md](references/sms-send-api.md)
- SMS Task List: Check [references/sms-task-list-api.md](references/sms-task-list-api.md)
- SMS Task Record List: Check [references/sms-task-record-list-api.md](references/sms-task-record-list-api.md)

## Notes

- File paths use forward slashes on all platforms
- **Do not guess parameter names**, get accurate parameter names and formats from documentation
- **Prohibit outputting technical parameter format**: Do not display code-style parameters in responses, convert to natural language
- **Do not estimate or guess fees** — use `python scripts/auth.py --price_info` to get accurate pricing information
- **SMS sending is synchronous submission**: The API returns response immediately after submission, but the SMS server processes asynchronously; the `status` field in response indicates sending status (1-sending 2-completed 3-failed 4-partial success)

## Related Skills

Other UpKuaJing skills you might find useful:

- upkuajing-global-company-people-search — Global company and people search
- upkuajing-customs-trade-company-search — Search customs trade companies
- upkuajing-email-tool — Send emails and manage email tasks
- upkuajing-map-merchants-search — Map-based merchant search
- upkuajing-contact-info-validity-check — Check contact info validity