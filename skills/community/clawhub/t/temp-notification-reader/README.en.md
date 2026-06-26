# macOS Notification Reader

> Read macOS notifications and generate daily work summaries for OpenClaw

This is a skill for OpenClaw that reads macOS notification center content, helping the AI assistant understand your work dynamics.

---

## 🎯 What is this?

This tool exports your macOS notifications to OpenClaw's memory directory, allowing OpenClaw to:
- 📬 Know who's reaching out (Teams, Outlook, WeChat...)
- 📅 Understand your calendar reminders
- ✅ Extract action items (meetings, approvals, deadlines...)
- 🧠 Remember what you've been working on

---

## 📁 Output File Structure

```
memory/YYYY-MM-DD/
└── computer_io/
    └── notification/
        ├── YYYYMMDD-HHMMSS.md          # Raw notification export
        └── work-summary-YYYYMMDD-HHMMSS.md  # Work summary (recommended)
```

---

## 🚀 Installation

### Method 1: NPM Global Install (Recommended ✅)

```bash
# One-click install
npm install -g openclaw-macos-notification-reader

# First run for authorization
openclaw-notif

# Work summary mode
openclaw-work-summary
```

After installation, commands are globally available without manual copying.

---

### Method 2: Manual Install

```bash
# Clone the project
git clone https://github.com/gift-is-coding/macos-notification-reader.git

# Copy to OpenClaw skills directory
cp -r macos-notification-reader ~/.openclaw/workspace/skills/

# Make scripts executable
chmod +x ~/.openclaw/workspace/skills/macos-notification-reader/scripts/*.sh
```

### Step 2: First Run Authorization

```bash
~/.openclaw/workspace/skills/macos-notification-reader/scripts/export-notification.sh
```

On first run, macOS will prompt for notification access permission - click **Allow**.

---

## ⚙️ Configure Cron Job

### Method 1: Via OpenClaw Config (Recommended)

Edit `~/.openclaw/cron/jobs.json`, add:

```json
{
  "name": "Notification Reader",
  "schedule": "*/30 * * * *",
  "command": "~/.openclaw/workspace/skills/macos-notification-reader/scripts/export-notification.sh",
  "timezone": "Asia/Shanghai"
}
```

This will make OpenClaw automatically capture notifications **every 30 minutes**.

### Method 2: Manual Crontab

```bash
crontab -e
```

Add:

```cron
*/30 * * * * ~/.openclaw/workspace/skills/macos-notification-reader/scripts/export-notification.sh >> ~/.openclaw/logs/notification.log 2>&1
```

---

## 💼 Usage

### Export All Notifications

```bash
~/.openclaw/workspace/skills/macos-notification-reader/scripts/export-notification.sh
```

### Work Summary Mode (Recommended)

Only extract work-related notifications (Teams/Outlook/WeChat):

```bash
~/.openclaw/workspace/skills/macos-notification-reader/scripts/work-summary.sh
```

### Custom Time Range

```bash
# Only look at notifications from the last 1 hour
NOTIF_LOOKBACK_MINUTES=60 ~/.openclaw/workspace/skills/macos-notification-reader/scripts/export-notification.sh

# Work summary only from last 2 hours
WORK_LOOKBACK_MINUTES=120 ~/.openclaw/workspace/skills/macos-notification-reader/scripts/work-summary.sh
```

---

## 🔐 Privacy

- ✅ Data stored locally (OpenClaw memory directory), not uploaded to any server
- ✅ Only reads notification titles and content, not attachments
- ✅ One-click cleanup: `rm -rf ~/.openclaw/workspace/memory/*/computer_io/notification/`

---

## 🛠️ Troubleshooting

### Shows 0 Notifications?

1. Check if permission is granted:
   ```bash
   # Open System Settings
   open "x-apple.systempreferences:com.apple.preference.security?Privacy_Notifications"
   ```

2. Quick debug:
   ```bash
   python3 ~/.openclaw/workspace/skills/macos-notification-reader/scripts/read_notifications.py --minutes 5 --output /tmp/debug.txt
   cat /tmp/debug.txt
   ```

### Permission Denied?

```bash
chmod +x ~/.openclaw/workspace/skills/macos-notification-reader/scripts/*.sh
```

---

## 📞 Support

- Issues: https://github.com/gift-is-coding/macos-notification-reader/issues
- Learn more about OpenClaw: https://docs.openclaw.ai

---

**Made with ❤️ for OpenClaw**
