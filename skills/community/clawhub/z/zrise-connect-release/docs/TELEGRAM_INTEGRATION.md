# Zrise Connect - Telegram Integration Guide

## 📱 Overview

Integrate Zrise Connect with Telegram for:
- ✅ Task notifications
- ✅ Approval requests
- ✅ Status updates
- ✅ Employee interactions

---

## 🏗️ Architecture

```
Zrise Task
    ↓
poll_employee_work.py (detect new task)
    ↓
format_work_item_notification.py (format message)
    ↓
send_telegram_message.py (send to Telegram)
    ↓
Employee receives notification on Telegram
    ↓
Employee replies with command
    ↓
telegram_command_parser.py (parse command)
    ↓
Execute workflow
    ↓
Post result to Zrise
```

---

## ⚙️ Setup

### 1. Create Telegram Bot

```bash
# 1. Open Telegram, search @BotFather
# 2. Send /newbot
# 3. Follow instructions
# 4. Get bot token: 1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

### 2. Get Chat ID

```bash
# Method 1: Use @userinfobot
# Method 2: Use API
curl https://api.telegram.org/bot<TOKEN>/getUpdates

# For groups/channels:
# - Add bot to group
# - Send message
# - Check getUpdates for chat_id (negative number)
```

### 3. Configure OpenClaw

```json
// ~/.openclaw/openclaw.json
{
  "messaging": {
    "telegram": {
      "bot_token": "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz",
      "default_chat_id": "-1001234567890"
    }
  }
}
```

### 4. Configure Zrise Employee Mapping

```json
// config/zrise/telegram-mapping.json
{
  "employees": {
    "10": {
      "name": "Bùi Đăng Khoa",
      "telegram_chat_id": "123456789",
      "telegram_username": "khoa_username"
    },
    "11": {
      "name": "Employee 2",
      "telegram_chat_id": "987654321",
      "telegram_username": "emp2_username"
    }
  },
  "groups": {
    "my-workplace": "-1001234567890",
    "tasks": "-1001234567891"
  }
}
```

---

## 💬 Message Formats

### Task Notification

```
📋 Task Mới: [DEMO] BA Task

Project: Website bán hàng
Stage: Clarification
Priority: P1
Deadline: 19/03/2026

Link: https://zrise.app/web#id=42174

👉 Reply với:
  done - Hoàn thành
  clarify - Cần làm rõ
  help - Cần hỗ trợ
```

### Approval Request

```
🔔 APPROVAL REQUIRED

Task: 42174 - Viết email bảo trì
Workflow: email-draft

Preview:
[Kết quả AI...]

👉 Reply với:
  approve - Approve
  reject [lý do] - Reject
```

### Status Update

```
✅ Task Completed

Task: 42174
Workflow: email-draft
Duration: 4.2s
Message ID: 984619

View: https://zrise.app/web#id=42174
```

---

## 🤖 Bot Commands

### Employee Commands

| Command | Description |
|---------|-------------|
| `/start` | Register với bot |
| `/tasks` | List pending tasks |
| `/task <id>` | Xem chi tiết task |
| `/done <id>` | Mark task done |
| `/clarify <id> <message>` | Request clarification |
| `/help` | Show help |

### Admin Commands

| Command | Description |
|---------|-------------|
| `/poll` | Manual poll tasks |
| `/status` | System status |
| `/workflow <name>` | Run workflow |
| `/approve <id>` | Approve pending task |

---

## 🔧 Implementation

### Send Notification

```python
# send_telegram_notification.py
import requests

def send_task_notification(employee_id, task):
    # Get employee telegram chat_id
    chat_id = get_telegram_chat_id(employee_id)
    
    message = f"""📋 Task Mới: {task['name']}

Project: {task['project']}
Stage: {task['stage']}
Priority: {task['priority']}

👉 Reply: done / clarify / help"""
    
    send_telegram_message(chat_id, message)

def send_telegram_message(chat_id, text):
    bot_token = get_bot_token()
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    
    requests.post(url, json=data)
```

### Handle Reply

```python
# telegram_webhook_handler.py
def handle_message(update):
    chat_id = update['message']['chat']['id']
    text = update['message']['text']
    
    # Parse command
    if text.startswith('approve'):
        task_id = extract_task_id(text)
        approve_task(task_id)
        send_message(chat_id, "✅ Task approved!")
    
    elif text.startswith('reject'):
        task_id, reason = parse_reject(text)
        reject_task(task_id, reason)
        send_message(chat_id, f"❌ Task rejected: {reason}")
```

---

## 🔐 Security

### 1. Verify User Identity

```python
def verify_employee(telegram_user_id):
    # Check if telegram_user_id matches employee in mapping
    mapping = load_telegram_mapping()
    
    for emp_id, emp_data in mapping['employees'].items():
        if emp_data.get('telegram_user_id') == telegram_user_id:
            return emp_id
    
    return None  # Unauthorized
```

### 2. Rate Limiting

```python
# Max 10 commands per minute per user
rate_limiter = {}

def check_rate_limit(user_id):
    if user_id not in rate_limiter:
        rate_limiter[user_id] = []
    
    # Remove old timestamps
    rate_limiter[user_id] = [t for t in rate_limiter[user_id] 
                              if time.time() - t < 60]
    
    if len(rate_limiter[user_id]) >= 10:
        return False  # Rate limited
    
    rate_limiter[user_id].append(time.time())
    return True
```

### 3. Sensitive Data

```python
# Don't send sensitive data via Telegram
SENSITIVE_FIELDS = ['api_key', 'password', 'token', 'secret']

def sanitize_task_for_telegram(task):
    sanitized = task.copy()
    for field in SENSITIVE_FIELDS:
        if field in sanitized:
            sanitized[field] = '***'
    return sanitized
```

---

## 📊 Monitoring

### Track Metrics

```python
metrics = {
    'messages_sent': 0,
    'commands_received': 0,
    'approvals_via_telegram': 0,
    'errors': 0
}

def track_metric(name, value=1):
    metrics[name] += value
    save_metrics(metrics)
```

### Health Check

```python
def telegram_health_check():
    try:
        bot_token = get_bot_token()
        url = f"https://api.telegram.org/bot{bot_token}/getMe"
        response = requests.get(url, timeout=5)
        
        return {
            'status': 'ok' if response.status_code == 200 else 'error',
            'bot_info': response.json() if response.status_code == 200 else None
        }
    except Exception as e:
        return {'status': 'error', 'error': str(e)}
```

---

## 🚀 Deployment

### 1. Webhook (Recommended)

```python
# Set webhook
bot_token = "YOUR_BOT_TOKEN"
webhook_url = "https://your-domain.com/telegram/webhook"

requests.get(f"https://api.telegram.org/bot{bot_token}/setWebhook?url={webhook_url}")
```

### 2. Polling (Development)

```python
import time

def poll_updates():
    offset = 0
    while True:
        updates = get_updates(offset)
        for update in updates:
            handle_message(update)
            offset = update['update_id'] + 1
        time.sleep(1)
```

---

## 📝 Testing

### Test Bot

```bash
# Send test message
python3 send_telegram_message.py --chat-id 123456789 --message "Test message"

# Test webhook
curl -X POST https://your-domain.com/telegram/webhook \
  -H "Content-Type: application/json" \
  -d '{"message":{"chat":{"id":123},"text":"test"}}'
```

---

## 🎯 Best Practices

1. **Keep messages short** — Max 4096 chars
2. **Use formatting** — HTML/Markdown
3. **Add context** — Include task link
4. **Clear CTAs** — Tell user what to do
5. **Handle errors gracefully** — User-friendly messages
6. **Log everything** — For debugging
7. **Test thoroughly** — Before production

---

## 🔧 Troubleshooting

### Bot not responding?
```bash
# Check webhook status
curl https://api.telegram.org/bot<TOKEN>/getWebhookInfo

# Delete webhook (for polling)
curl https://api.telegram.org/bot<TOKEN>/deleteWebhook
```

### Messages not delivered?
- Check bot is admin in group
- Verify chat_id is correct
- Check bot token is valid

### User not authorized?
- Check telegram_user_id in mapping
- Verify employee exists in Zrise

---

**Telegram integration guide complete!** 📱
