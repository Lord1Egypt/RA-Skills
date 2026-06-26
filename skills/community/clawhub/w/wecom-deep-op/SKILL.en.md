# wecom-deep-op Skill Specification

**English version of the skill definition for "wecom-deep-op"，The skill is One-stop Enterprise WeChat automation solution that unifies Document, Calendar, Meeting, Todo, and Contact operations through the official WeCom MCP APIs. **

---

## 📋 Basic Information

| Field | Value |
|-------|-------|
| **Name** | `wecom-deep-op` |
| **Version** | 2.0.0 |
| **Category** | productivity |
| **License** | MIT |
| **Min OpenClaw** | 0.5.0 |
| **Plugin** | `@wecom/wecom-openclaw-plugin` ≥ 1.0.13 |

---

## 📝 Description

One-stop Enterprise WeChat automation solution that based on the official WeCom plugin @wecom/wecom-openclaw-plugin v1.0.13 and above。You can conveniently operate all WeCom MCP capabilities including documents, calendar, meetings, to-dos, and contacts, fully leveraging the synergy between OpenClaw and WeCom.

---

## 🏷️ Tags

`wecom`, `enterprise-wechat`, `mcp`, `document`, `calendar`, `meeting`, `todo`, `contact`, `openclaw`

---

## 🔌 Exported Functions

All functions are available under the `wecom-deep-op` namespace and callable via OpenClaw MCP:

```typescript
await openclaw.mcp.call('wecom-deep-op', '<function_name>', params);
```

### 📄 Document Operations (`doc_*`)

#### `doc_get`

Export or retrieve document content. Supports async polling for large documents.

```typescript
interface Params {
  id: string; // Document ID
}
```

Returns:
```typescript
{
  id: string;
  title: string;
  content: string;
  createdAt: number;
  updatedAt: number;
}
```

---

#### `doc_create`

Create a new document or smart sheet.

```typescript
interface Params {
  title: string;
  content?: string;
  type?: "doc" | "sheet"; // Default: "doc"
  parentId?: string; // Optional parent folder ID
}
```

Returns:
```typescript
{
  id: string;
  title: string;
  url: string;
  createdAt: number;
}
```

---

#### `doc_edit`

Edit or overwrite document content.

```typescript
interface Params {
  id: string;
  content: string;
  format?: "markdown" | "html"; // Default: "markdown"
}
```

Returns:
```typescript
{
  id: string;
  updated: boolean;
  updatedAt: number;
}
```

---

### 📅 Calendar Operations (`schedule_*`)

#### `schedule_create`

Create a schedule/calendar event.

```typescript
interface Params {
  title: string;
  startTime: number; // Unix timestamp (seconds)
  endTime: number;
  location?: string;
  description?: string;
  attendees?: Array<{ userId: string; }>;
  reminders?: Array<{ type: "minute" | "hour" | "day"; offset: number }>;
}
```

Returns:
```typescript
{
  id: string;
  title: string;
  startTime: number;
  endTime: number;
}
```

---

#### `schedule_list`

List schedules with optional time filters.

```typescript
interface Params {
  startTime?: number; // Unix timestamp
  endTime?: number;
  status?: "confirmed" | "cancelled" | "tentative";
  limit?: number; // Default: 50, Max: 100
}
```

Returns:
```typescript
Array<{
  id: string;
  title: string;
  startTime: number;
  endTime: number;
  status: string;
}>
```

---

#### `schedule_get`

Get detailed schedule information.

```typescript
interface Params {
  id: string;
}
```

Returns full schedule object with attendees, reminders, etc.

---

#### `schedule_update`

Update an existing schedule.

```typescript
interface Params {
  id: string;
  updates: {
    title?: string;
    startTime?: number;
    endTime?: number;
    location?: string;
    description?: string;
  };
}
```

---

#### `schedule_cancel`

Cancel a schedule.

```typescript
interface Params {
  id: string;
}
```

---

#### `schedule_add_attendee`

Add attendees to a schedule.

```typescript
interface Params {
  id: string;
  attendees: Array<{ userId: string }>;
}
```

---

#### `schedule_remove_attendee`

Remove attendees from a schedule.

```typescript
interface Params {
  id: string;
  attendees: Array<{ userId: string }>;
}
```

---

### 📹 Meeting Operations (`meeting_*`)

#### `meeting_create`

Schedule a meeting (similar to `schedule_create` but for meetings).

```typescript
interface Params {
  title: string;
  startTime: number;
  endTime: number;
  type?: "online" | "offline";
  location?: string;
  agenda?: string;
  attendees?: Array<{ userId: string }>;
}
```

Returns:
```typescript
{
  meetingId: string;
  title: string;
  startTime: number;
  endTime: number;
  joinUrl?: string;
}
```

---

#### `meeting_list`, `meeting_get`, `meeting_cancel`

Similar patterns to schedule operations.

- `meeting_list`: List meetings with filters
- `meeting_get`: Get meeting details by `meetingId`
- `meeting_cancel`: Cancel a meeting

---

#### `meeting_update_attendees`

Update meeting attendee list.

```typescript
interface Params {
  meetingId: string;
  addAttendees?: Array<{ userId: string }>;
  removeAttendees?: Array<{ userId: string }>;
}
```

---

### ✅ Todo Operations (`todo_*`)

| Function | Description |
|----------|-------------|
| `todo_create` | Create a new todo item |
| `todo_list` | List todos (optionally filtered by status) |
| `todo_get` | Get todo details |
| `todo_update_status` | Update todo status (pending/completed) |
| `todo_update` | Update todo content/fields |
| `todo_delete` | Delete a todo |
| `todo_accept` | Accept a todo assignment |
| `todo_refuse` | Refuse a todo assignment |

---

### 👥 Contact Operations (`contact_*`)

#### `contact_get_userlist`

Get the contact list (only returns users visible to the current bot/user).

```typescript
interface Params {}
```

Returns:
```typescript
Array<{
  userId: string;
  name: string;
  department?: number;
  position?: string;
  mobile?: string;
  email?: string;
}>
```

---

#### `contact_search`

Search contacts with local name filtering.

```typescript
interface Params {
  name?: string; // Partial name match (case-insensitive)
  department?: number; // Department ID filter
}
```

Returns filtered user list.

---

### 🔧 System Functions

#### `ping`

Health check / readiness probe.

```typescript
interface Params {}
```

Returns:
```typescript
{ status: "ok" }
```

---

#### `preflight_check`

Validate configuration completeness.

```typescript
interface Params {}
```

Returns:
```typescript
{
  ok: boolean;
  errors: Array<{
    field: string;
    message: string;
  }>;
  config: {
    docBaseUrl?: string;
    scheduleBaseUrl?: string;
    meetingBaseUrl?: string;
    todoBaseUrl?: string;
    contactBaseUrl?: string;
  };
}
```

---

## ⚙️ Configuration

This skill requires **5 base URLs**, each with a `uaKey` query parameter.

### Environment Variables

```bash
WECOM_DOC_BASE_URL="https://qyapi.weixin.qq.com/mcp/bot/doc?uaKey=xxx"
WECOM_SCHEDULE_BASE_URL="https://.../schedule?uaKey=xxx"
WECOM_MEETING_BASE_URL="https://.../meeting?uaKey=xxx"
WECOM_TODO_BASE_URL="https://.../todo?uaKey=xxx"
WECOM_CONTACT_BASE_URL="https://.../contact?uaKey=xxx"
```

### mcporter.json (Recommended)

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

---

## 🔒 Security Considerations

- **No credential storage** - All sensitive data comes from environment or user config
- **Least privilege** - Only requests scopes explicitly granted to the bot
- **Input validation** - All parameters validated before API calls
- **Error sanitization** - No sensitive data leaked in error messages
- **Transparent flow** - Users control endpoints and data

---

## 🏗️ Architecture

```
User → OpenClaw MCP → wecom-deep-op → @wecom/wecom-openclaw-plugin → WeCom API
```

The skill acts as a **unified facade** over the official WeCom plugin, providing:
- Consistent parameter patterns
- Error normalization
- Retry logic for transient failures
- Async polling for long-running operations (e.g., doc export)

---

## 🧪 Testing

Unit tests available in `test/index.test.ts`. Run:

```bash
npm test
```

Mocked responses ensure reliability without real API calls.

---

## 📦 Distribution

- **ClawHub**: `clawhub install wecom-deep-op`
- **GitHub**: https://github.com/Bingbox/wecom-deep-op
- **NPM**: (Not published - this is an OpenClaw skill, not a library)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure `npm test` passes
5. Submit a pull request

---

## 📄 License

MIT - See [LICENSE](../LICENSE) file.

---

**Last Updated**: 2026-03-22  
**Maintainer**: 老白 (Bai Xiaoyuan) <bingbox0515@gmail.com>  
**Skill ID**: `wecom-deep-op`  
**Version**: 2.0.0
