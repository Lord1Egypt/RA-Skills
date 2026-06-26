# wecom-deep-op - Enterprise WeChat All-in-One Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://openclaw.ai)
[![Enterprise WeChat](https://img.shields.io/badge/Enterprise-WeChat-07C160)](https://work.weixin.qq.com/)

> **One-stop Enterprise WeChat Automation Solution** - Built on the official WeChat plugin `@wecom/wecom-openclaw-plugin` v1.0.13+, this skill wraps all Enterprise WeChat (WeCom) MCP capabilities into a unified interface for seamless OpenClaw integration.

---

## 📖 Table of Contents

- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [📚 API Reference](#-api-reference)
- [🔐 Security & Privacy](#-security--privacy)
- [🔧 Configuration](#-configuration)
- [🐛 Troubleshooting](#-troubleshooting)
- [📄 License](#-license)
- [🙏 Acknowledgments](#-acknowledgments)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Unified Interface** | One skill for 5 services (Docs, Calendar, Meetings, Todos, Contacts) |
| **Complete Coverage** | Full MCP API coverage based on official WeChat plugin |
| **Production Ready** | Requires `@wecom/wecom-openclaw-plugin` **v1.0.13+** |
| **Secure by Design** | No token storage, user-controlled configuration |
| **TypeScript** | Complete type definitions for excellent DX |
| **MIT Licensed** | Free to use, modify, and distribute |

---

## 🚀 Quick Start

### Prerequisites

| Requirement | Description | Check Command |
|-------------|-------------|---------------|
| **OpenClaw** | v0.5.0 or higher | `openclaw --version` |
| **Node.js** | v18 or higher | `node --version` |
| **WeCom Bot** | Created with MCP permissions | Admin console |
| **Official Plugin** | `@wecom/wecom-openclaw-plugin` ≥ **v1.0.13** | `openclaw plugin list` |
| **Configuration** | Set `WECOM_*_BASE_URL` or `mcporter.json` | `echo $WECOM_DOC_BASE_URL` |

⚠️ **The official WeCom plugin is a hard dependency**. Without it or with version < v1.0.13, this skill will not start.

---

## 📚 API Reference

All functions are namespaced under `wecom_deep_op` and callable via:

```typescript
// OpenClaw MCP call
const result = await openclaw.mcp.call('wecom-deep-op', '<function>', params);
```

Or directly:

```typescript
import { WecomDeepOp } from 'wecom-deep-op';
const skill = new WecomDeepOp(config);
await skill.doc_get({ id: 'doc_123' });
```

---

### 📄 Document Management (`doc_*`)

| Function | Description | Parameters |
|----------|-------------|------------|
| `doc_get` | Export/retrieve document content (async polling supported) | `{ id: string }` |
| `doc_create` | Create a document or smart sheet | `{ title, ... }` |
| `doc_edit` | Edit/overwrite document content | `{ id, content, ... }` |

---

### 📅 Calendar Management (`schedule_*`)

| Function | Description | Key Parameters |
|----------|-------------|----------------|
| `schedule_create` | Create a schedule/event | `{ startTime, endTime, title, ... }` |
| `schedule_list` | List schedules with filters | `{ startTime?, endTime?, status? }` |
| `schedule_get` | Get schedule details | `{ id: string }` |
| `schedule_update` | Update a schedule | `{ id, ...updates }` |
| `schedule_cancel` | Cancel a schedule | `{ id: string }` |
| `schedule_add_attendee` | Add attendees to a schedule | `{ id, attendees: [] }` |
| `schedule_remove_attendee` | Remove attendees from a schedule | `{ id, attendees: [] }` |

---

### 📹 Meeting Management (`meeting_*`)

| Function | Description | Key Parameters |
|----------|-------------|----------------|
| `meeting_create` | Schedule a meeting | `{ startTime, endTime, title, ... }` |
| `meeting_list` | List meetings | `{ startTime?, endTime?, status? }` |
| `meeting_get` | Get meeting details | `{ meetingId: string }` |
| `meeting_cancel` | Cancel a meeting | `{ meetingId: string }` |
| `meeting_update_attendees` | Update meeting attendees | `{ meetingId, addAttendees?, removeAttendees? }` |

---

### ✅ Todo Management (`todo_*`)

| Function | Description | Key Parameters |
|----------|-------------|----------------|
| `todo_create` | Create a todo | `{ title, content?, ... }` |
| `todo_list` | List todos | `{ status?, ... }` |
| `todo_get` | Get todo details | `{ id: string }` |
| `todo_update_status` | Update todo status | `{ id, status }` |
| `todo_update` | Update todo content | `{ id, ...updates }` |
| `todo_delete` | Delete a todo | `{ id: string }` |
| `todo_accept` | Accept a todo | `{ id: string }` |
| `todo_refuse` | Refuse a todo | `{ id: string }` |

---

### 👥 Contact Management (`contact_*`)

| Function | Description | Parameters |
|----------|-------------|------------|
| `contact_get_userlist` | Get contact list (user's visible scope only) | `{}` |
| `contact_search` | Search contacts (local filter) | `{ name?: string,department?: number }` |

---

### 🔧 System Functions

| Function | Description | Returns |
|----------|-------------|---------|
| `ping` | Health check / readiness probe | `{ status: "ok" }` |
| `preflight_check` | Validate configuration completeness | `{ ok: boolean, errors: [] }` |

---

## 🔐 Security & Privacy

- 🔒 **No credential storage** - All tokens/keys come from environment or user config
- 📝 **Structured logging** - Debug, info, error levels
- 🌐 **Transparent data flow** - User controls endpoints and file inputs
- ⚠️ **Permission awareness** - Contacts limited to user's visible scope
- 🛡️ **Production hardened** - Retry logic, input validation, error handling

---

## 🔧 Configuration

This skill requires **5 base URLs** (one per service). Each must include the `uaKey` query parameter.

### Option 1: Environment Variables

```bash
export WECOM_DOC_BASE_URL="https://qyapi.weixin.qq.com/mcp/bot/doc?uaKey=YOUR_KEY"
export WECOM_SCHEDULE_BASE_URL="https://qyapi.weixin.qq.com/mcp/bot/schedule?uaKey=YOUR_KEY"
export WECOM_MEETING_BASE_URL="https://qyapi.weixin.qq.com/mcp/bot/meeting?uaKey=YOUR_KEY"
export WECOM_TODO_BASE_URL="https://qyapi.weixin.qq.com/mcp/bot/todo?uaKey=YOUR_KEY"
export WECOM_CONTACT_BASE_URL="https://qyapi.weixin.qq.com/mcp/bot/contact?uaKey=YOUR_KEY"
```

### Option 2: `mcporter.json` (recommended)

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

### Getting `uaKey`

1. Login to WeCom admin console
2. Navigate to **MCP Settings**
3. Create or find your bot's `uaKey`
4. Copy it to your config

---

## 🐛 Troubleshooting

| Issue | Likely Cause | Solution |
|-------|--------------|----------|
| `"plugin not found"` | `@wecom/wecom-openclaw-plugin` missing or wrong version | `openclaw plugin install @wecom/wecom-openclaw-plugin@latest` |
| `"BASE_URL required"` | Env var not set or `mcporter.json` missing | Set env vars or create config file |
| `"Network timeout"` | uaKey incorrect or URL malformed | Verify URL includes `?uaKey=...` |
| `"Permission denied"` | Bot lacks required MCP scopes | Grant all MCP permissions in admin console |
| `"Contact list empty"` | User's visible scope is limited | Normal behavior - only returns visible contacts |

Run diagnostics:

```bash
openclaw mcp call wecom-deep-op preflight_check
```

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built on **[Tencent WeChat Official OpenClaw Plugin](https://github.com/WecomTeam/wecom-openclaw-plugin)** (`@wecom/wecom-openclaw-plugin` v1.0.13)
- Thanks to WeChat team for excellent MCP APIs
- Community-maintained, not an official product

---

**Version**: 2.0.0  
**Last Updated**: 2026-03-22  
**Maintainer**: 老白 (Bai Xiaoyuan)
