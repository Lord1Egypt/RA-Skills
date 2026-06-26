# WeChat File Helper Automation Skill

Automate WeChat File Helper (`filehelper.weixin.qq.com`) to send text messages. Handles login QR code automatically.

**Key Features:**
- Pure browser automation (no API keys needed)
- Automatic QR code detection and delivery
- Support for multiple messaging channels
- Cron-ready monitoring scripts

## When to Use

✅ **USE this skill when:**
- Send text messages to WeChat File Helper
- Need automatic QR code handling when logged out
- Want to use existing WeChat account (not personal)
- Integrate with cron for periodic messages

❌ **DON'T use this skill when:**
- Sending to personal WeChat accounts (ToS violation)
- Need real-time messaging (use API directly)
- Uploading files (not supported)
- Need message history/read receipts

## Requirements

- Browser extension enabled (`openclaw browser status` shows `enabled: true`)
- WeChat File Helper account (not personal WeChat)
- At least one messaging channel configured (for QR delivery)

---

## Workflow Overview (5 Steps)

```
┌─────────────────────────────────────────────────────────────────┐
│  1. Open filehelper.weixin.qq.com or reuse existing tab         │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│  2. Check login status - QR code needed?                         │
│     - URL ends with `/_/` → Logged in                           │
│     - Base URL → QR code displayed (logged out)                  │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│  3a. If logged out: Capture QR and send to user                 │
│     - Screenshot QR code                                        │
│     - Send via available channel (WhatsApp/iMessage/Slack)      │
│     - Wait for user to scan                                     │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│  3b. If logged in: Type message in textarea                     │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│  4. Click send button or press Enter                             │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│  5. Confirm message sent (check for success indicator)           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Step 1: Open or Reuse Tab

```bash
# Check if tab already exists
browser action=tabs targetUrl="https://filehelper.weixin.qq.com/"

# Open new tab if needed
browser action=open targetUrl="https://filehelper.weixin.qq.com/"
targetId="<new-target-id>"
```

---

## Step 2: Check Login Status

```bash
# Check URL to determine state
browser action=evaluate fn="window.location.href" targetId="<targetId>"
```

### Login Status Indicators

| URL Pattern | Status | Action |
|-------------|--------|--------|
| `filehelper.weixin.qq.com/_/` | ✅ Logged In | Proceed to Step 3b |
| `filehelper.weixin.qq.com/` | ❌ Logged Out | Proceed to Step 3a |

---

## Step 3a: Capture and Send QR Code (When Logged Out)

```bash
# Capture QR code screenshot
browser action=screenshot path="/tmp/wechat-qr.png" targetId="<targetId>"

# Send via first available channel
message action=send to="<owner-phone>" media="/tmp/wechat-qr.png"

# Or specify channel explicitly
message action=send channel="whatsapp" to="+1234567890" media="/tmp/wechat-qr.png"
message action=send channel="telegram" to="@username" media="/tmp/wechat-qr.png"
message action=send channel="slack" to="#channel" media="/tmp/wechat-qr.png"

echo "📱 QR code sent. Waiting for scan..."

# Poll for login success (every 5 seconds, max 60 attempts)
attempts=0
while [ $attempts -lt 60 ]; do
  sleep 5
  url=$(browser action=evaluate fn="window.location.href" targetId="<targetId>")
  if echo "$url" | grep -q "_/"; then
    echo "✅ Login successful!"
    break
  fi
  attempts=$((attempts + 1))
done
```

---

## Step 3b: Type Message (When Logged In)

```bash
# Take snapshot to get refs
browser action=snapshot targetId="<targetId>"

# Type message
browser action=act kind="type" ref="input-area" text="Hello from OpenClaw! 🦞" targetId="<targetId>"
```

---

## Step 4: Send Message

```bash
# Option 1: Click send button
browser action=act kind="click" ref="send-btn" targetId="<targetId>"

# Option 2: Press Enter
browser action=act kind="press" key="Enter" targetId="<targetId>"
```

---

## Step 5: Confirm Success

```bash
# Check for success indicator
browser action=evaluate fn="{
  const sent = document.body.innerText.includes('已发送') || 
               document.body.innerText.includes('sent') ||
               document.querySelector('.success, [class*=\"success\"]');
  !!sent;
}" targetId="<targetId>"
```

---

## Complete Scripts

### Quick Send (Single Command)

```bash
# Send a message - handles login automatically
wechat "Hello from OpenClaw!"
```

### Full Workflow Script

```bash
#!/bin/bash
# wechat-send.sh - Complete WeChat File Helper automation

MESSAGE="$1"
QR_FILE="/tmp/wechat-qr.png"
WEBSITE="https://filehelper.weixin.qq.com/"
TARGET_ID=""

echo "🔍 Checking WeChat File Helper status..."

# Step 1: Open or get existing tab
tabs=$(browser action=tabs targetUrl="$WEBSITE")
if echo "$tabs" | grep -q "targetId"; then
  TARGET_ID=$(echo "$tabs" | grep -o 'targetId="[^"]*"' | head -1 | cut -d'"' -f2)
  echo "✅ Using existing tab: $TARGET_ID"
else
  result=$(browser action=open targetUrl="$WEBSITE")
  TARGET_ID=$(echo "$result" | grep -o 'targetId="[^"]*"' | cut -d'"' -f2)
  echo "✅ Opened new tab: $TARGET_ID"
  sleep 2
fi

# Step 2: Check login status
url=$(browser action=evaluate fn="window.location.href" targetId="$TARGET_ID")

if echo "$url" | grep -q "_/"; then
  echo "✅ Already logged in"
else
  echo "❌ Not logged in - capturing QR..."
  
  # Capture QR code
  browser action=screenshot path="$QR_FILE" targetId="$TARGET_ID"
  
  # Send QR via owner's channel (set OWNER_PHONE env var)
  OWNER_PHONE="${OWNER_PHONE:-+1234567890}"
  message action=send to="$OWNER_PHONE" media="$QR_FILE" \
    -m "WeChat File Helper login required. Please scan QR code."
  
  echo "📱 QR code sent to $OWNER_PHONE"
  echo "⏳ Waiting for scan... (run again after scanning)"
  exit 0
fi

# Step 3: Type message
browser action=snapshot targetId="$TARGET_ID"
browser action=act kind="type" ref="input-area" text="$MESSAGE" targetId="$TARGET_ID"
echo "✅ Message typed"

# Step 4: Send
browser action=act kind="click" ref="send-btn" targetId="$TARGET_ID"
echo "✅ Send button clicked"

# Step 5: Confirm
sleep 1
result=$(browser action=evaluate fn="{
  document.body.innerText.includes('sent') || 
  document.body.innerText.includes('已发送')
}" targetId="$TARGET_ID")

if [ "$result" = "true" ]; then
  echo "✅ Message sent successfully!"
else
  echo "⚠️ Message may not have sent - check manually"
fi
```

### Cron Monitoring Script

```bash
#!/bin/bash
# cron-wechat.sh - Run every minute via cron

# Set owner phone for QR delivery
OWNER_PHONE="${OWNER_PHONE:-+1234567890}"

# Source main script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/monitor.sh"

# Log
echo "$(date): WeChat File Helper check"
```

---

## Common Selectors

| Element | Selector | Ref |
|---------|----------|-----|
| Message input | `textarea` or `div[contenteditable]` | `input-area` |
| Send button | `button[type="button"]` or `.send-btn` | `send-btn` |
| QR code container | `.qr-container or [class*="qr"]` | `qr-code` |
| Success indicator | Text containing "已发送" or "sent" | - |
| User avatar | `[class*="avatar"]` or `[class*="user"]` | - |

---

## Page States

| State | URL | Description |
|-------|-----|-------------|
| **Logged Out** | `https://filehelper.weixin.qq.com/` | Shows QR code for WeChat scan |
| **Logged In** | `https://filehelper.weixin.qq.com/_/` | Chat interface ready |

---

## Auto QR Delivery via Channels

The skill detects configured channels and sends QR to the first available:

```bash
# Check configured channels
openclaw config channels

# Priority order: WhatsApp → Telegram → Slack → First available
message action=send to="+1234567890" media="/tmp/wechat-qr.png"
```

---

## Limitations

- **No File Uploads**: File button clicks may fail or trigger unwanted dialogs
- **No Message History**: Cannot read past messages
- **Session Expiry**: May need re-login after inactivity (~1-2 hours)
- **QR Expiry**: QR refreshes every ~2 minutes if not scanned
- **ToS Warning**: Using personal WeChat accounts violates WeChat ToS
- **No Group Support**: File Helper is 1-on-1 only
- **Rate Limiting**: May be throttled on rapid message sending

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Can't find input | Run `snapshot` to refresh refs |
| Send button not working | Try pressing Enter instead |
| Session expired | QR code shown, re-scan to login |
| Wrong refs after reload | Page reload resets refs |
| QR not sending | Check configured channels |
| Messages not arriving | Verify recipient is correct |
| Cron not working | Check `crontab -e` entry |
| Browser not starting | Run `openclaw browser status` |

---

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/monitor.sh` | Main monitoring script |
| `scripts/capture_qrcode.sh` | Capture QR code only |
| `scripts/cron-wechat.sh` | Cron wrapper for monitoring |

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OWNER_PHONE` | Phone for QR delivery | `+1234567890` |

---

## See Also

- `openclaw browser status` - Check browser extension
- `openclaw config channels` - List messaging channels
- `chat-deepseek` - Similar automation for DeepSeek
- `imsg` - Send results to iMessage
- `whatsapp-login` - WhatsApp QR login