# wecom-deep-op Quick Start (English)

Get up and running with Enterprise WeChat automation in 5 minutes.

---

## 📦 Installation

```bash
# From ClawHub
clawhub install wecom-deep-op

# Or clone GitHub repo
git clone https://github.com/Bingbox/wecom-deep-op.git
```

---

## ⚙️ Configuration

### Method 1: Environment Variables (Quick)

```bash
export WECOM_DOC_BASE_URL="https://qyapi.weixin.qq.com/mcp/bot/doc?uaKey=YOUR_KEY"
export WECOM_SCHEDULE_BASE_URL="https://qyapi.weixin.qq.com/mcp/bot/schedule?uaKey=YOUR_KEY"
export WECOM_MEETING_BASE_URL="https://qyapi.weixin.qq.com/mcp/bot/meeting?uaKey=YOUR_KEY"
export WECOM_TODO_BASE_URL="https://qyapi.weixin.qq.com/mcp/bot/todo?uaKey=YOUR_KEY"
export WECOM_CONTACT_BASE_URL="https://qyapi.weixin.qq.com/mcp/bot/contact?uaKey=YOUR_KEY"
```

Replace `YOUR_KEY` with your bot's `uaKey` from WeCom admin console.

---

### Method 2: mcporter.json (Recommended)

Create `~/.mcporter/mcporter.json`:

```json
{
  "providers": {
    "wecom": {
      "baseUrl": "https://qyapi.weixin.qq.com/mcp/bot",
      "uaKey": "YOUR_UA_KEY",
      "services": ["doc", "schedule", "meeting", "todo", "contact"]
    }
  }
}
```

This single config covers all 5 services automatically.

---

## 🔍 Verify Installation

Run a quick health check:

```bash
# MCP call
openclaw mcp call wecom-deep-op ping

# Or preflight check (validates config)
openclaw mcp call wecom-deep-op preflight_check
```

Expected output:

```json
{
  "status": "ok"
}
```

---

## 📚 Basic Usage Examples

### 📄 Create a Document

```typescript
const result = await openclaw.mcp.call('wecom-deep-op', 'doc_create', {
  title: 'Meeting Notes',
  content: '# Agenda\n1. Q1 Review\n2. Q2 Planning',
  type: 'doc'
});

console.log('Document created:', result.url);
```

---

### 📅 Schedule a Meeting

```typescript
const now = Math.floor(Date.now() / 1000);
const result = await openclaw.mcp.call('wecom-deep-op', 'meeting_create', {
  title: 'Weekly Sync',
  startTime: now + 3600, // 1 hour from now
  endTime: now + 7200,   // 2 hours from now
  type: 'online',
  agenda: 'Team standup, blockers, next steps'
});
```

---

### ✅ Create a Todo

```typescript
const result = await openclaw.mcp.call('wecom-deep-op', 'todo_create', {
  title: 'Review PR #123',
  content: 'Check the changes and leave comments',
  dueTime: Math.floor(Date.now() / 1000) + 86400 // Due tomorrow
});
```

---

### 👥 Search Contacts

```typescript
const users = await openclaw.mcp.call('wecom-deep-op', 'contact_get_userlist', {});
console.log('Contacts:', users.map(u => u.name));
```

---

## 🐛 Common Issues

| Problem | Cause | Fix |
|---------|-------|-----|
| `"plugin not found"` | Missing official plugin | `openclaw plugin install @wecom/wecom-openclaw-plugin@latest` |
| `"BASE_URL required"` | Missing env var | Set `WECOM_*_BASE_URL` or create `mcporter.json` |
| `"Invalid uaKey"` | Wrong key format | Ensure URL includes `?uaKey=xxx` exactly |
| Timeouts | Network/firewall | Check outbound connectivity to qyapi.weixin.qq.com |

Use `preflight_check` to diagnose configuration issues:

```bash
openclaw mcp call wecom-deep-op preflight_check
```

---

## 📖 Full Documentation

For complete API reference, see:
- **English**: [SKILL.en.md](./SKILL.en.md)
- **中文**: [SKILL.md](./SKILL.md)

Project overview:
- **English**: [README.en.md](./README.en.md)
- **中文**: [README.md](./README.md)

---

## 💡 Tips

1. **Always check `preflight_check` first** if something doesn't work
2. **Use `mcporter.json`** - it's cleaner than 5 separate env vars
3. **Test with `ping`** to ensure skill is loaded
4. **All timestamps are Unix seconds** (not milliseconds)
5. **Contact list is scoped** - bot only sees users it has permission to see

---

**Need help?** Open an issue: https://github.com/Bingbox/wecom-deep-op/issues
