# Telegram UI Integration

## /workplace Command — Hierarchical Navigation

### Top Level (no args or `/workplace`)

Show **parent workspaces and standalone workplaces** as the first level. Group by: top-level items (no parent) first.

Read `registry.json`, separate into:
- **Parents / standalone**: entries where `parent == null`
- **Children**: entries where `parent != null` (shown when user drills into a parent)

**Top-level message:**

```
📁 **Workplaces**
Current: **{current_name}** {current_path_short}
```

**Buttons:** One row per top-level workspace. Parent workplaces show children count.

```json
{
  "blocks": [{
    "type": "buttons",
    "buttons": [
      {"label": "📂 log-stream (2)", "style": "primary"},
      {"label": "🔧 multi-workplace ✓", "style": "secondary", "disabled": true}
    ]
  }]
}
```

- Current workspace (or its parent): `disabled: true`, `style: "secondary"`, append ` ✓`
- Parent workplaces: show `(N)` child count
- Standalone workplaces: no count

### Drill into Parent

When user clicks a parent workspace button (e.g. "📂 log-stream (2)"), show its children:

```
📂 **log-stream** — parent workspace
`/Users/.../opensource/log-stream`
```

**Buttons:** One per child + a "Use parent" option + back button.

```json
{
  "blocks": [{
    "type": "buttons",
    "buttons": [
      {"label": "⚙️ logstream", "style": "primary"},
      {"label": "🌐 logstream-dashboard ✓", "style": "secondary", "disabled": true},
      {"label": "📂 Use log-stream (parent)", "style": "secondary"},
      {"label": "← Back", "style": "secondary"}
    ]
  }]
}
```

- Current child: `disabled: true` with ` ✓`
- "Use parent" button: switches context to the parent workspace itself
- "← Back" button: returns to top-level list

### Colon Syntax — Direct Navigation

Support `parent:child` syntax for quick switching without menus:

```
/workplace log-stream:logstream          → switch to logstream under log-stream
/workplace log-stream:logstream-dashboard → switch to logstream-dashboard
/workplace log-stream                     → show log-stream's children (drill-in)
/workplace multi-workplace                → switch directly (standalone, no children)
```

**Resolution logic:**
1. If input contains `:`, split into `parent:child`
2. Find parent by name in registry (fuzzy match OK)
3. Find child by name where `child.parent == parent.uuid`
4. Switch to child

If no `:`, check if the name matches a parent with children → show drill-in view.
If it matches a standalone or child → switch directly.

### Switch Confirmation

After switching, send:

```
✅ Switched to **logstream**
📂 `/Users/.../log-stream/logstream`
📂 Parent: log-stream
🔗 Linked: logstream-dashboard

Agents: kernel, rust-dev, sdk-dev, reviewer, publisher
```

### Button Callback Routing

| Button text | Action |
|---|---|
| `📂 {parent} (N)` | Show parent's children (drill-in) |
| `⚙️/🌐/🔧 {name}` | Switch to that workspace |
| `📂 Use {name} (parent)` | Switch to parent workspace |
| `← Back` | Show top-level list |
| `📂 {name}` (loaded view) | Switch to loaded workplace |
| `➕ Load workplace` | Prompt for path/name |
| `➖ Unload workplace` | Show unload picker |
| `❌ {name}` | Unload that workplace |
| `▶️ Start {agent}` | `workplace agent start {agent}` |
| `⏹ Stop {agent}` | `workplace agent stop {agent}` |
| `▶️ Continue: {label}` | Set as active session, resume |
| `✨ New chat session` | Create new session, prompt for label |
| `🗑 Manage sessions` | Show session management view |

### Agent and Deploy Buttons

Same as before — shown after switching or via `/workplace agents` / `/workplace deploy`:

```json
{
  "blocks": [
    {"type": "text", "text": "**Agents for logstream:**"},
    {"type": "buttons", "buttons": [
      {"label": "▶️ Start rust-dev", "style": "success"},
      {"label": "▶️ Start reviewer", "style": "success"},
      {"label": "▶️ Start sdk-dev", "style": "success"},
      {"label": "🔄 Start kernel", "style": "primary"}
    ]}
  ]
}
```

### Loaded Workplaces

For `/workplace loaded`:

```
📂 **Loaded Workplaces** (2)
Active: **multi-workplace**
```

**Buttons:** One row per loaded workplace + management buttons.

```json
{
  "blocks": [
    {"type": "text", "text": "📂 **Loaded Workplaces** (2)\nActive: **multi-workplace**"},
    {"type": "buttons", "buttons": [
      {"label": "📂 log-stream", "style": "primary"},
      {"label": "🔧 multi-workplace ✓", "style": "secondary", "disabled": true}
    ]},
    {"type": "buttons", "buttons": [
      {"label": "➕ Load workplace", "style": "success"},
      {"label": "➖ Unload workplace", "style": "danger"}
    ]}
  ]
}
```

- Current workplace: `disabled: true` with ` ✓`
- Clicking a loaded workplace switches to it
- "➕ Load workplace" prompts for path/name/uuid
- "➖ Unload workplace" shows loaded list with unload buttons

### Load Confirmation

After loading a workplace:

```
✅ Loaded: **log-stream**
📂 `/Users/.../opensource/log-stream`
🔗 Also linked to current workplace

Loaded workplaces: 2
```

### Unload Flow

When user clicks "➖ Unload workplace", show loaded workplaces with unload buttons:

```json
{
  "blocks": [
    {"type": "text", "text": "Select workspace to unload:"},
    {"type": "buttons", "buttons": [
      {"label": "❌ log-stream", "style": "danger"},
      {"label": "← Back", "style": "secondary"}
    ]}
  ]
}
```

### Button Callback Routing (Loaded)

| Button text | Action |
|---|---|
| `📂 {name}` (in loaded view) | Switch to that loaded workplace |
| `➕ Load workplace` | Prompt for path/name |
| `➖ Unload workplace` | Show unload picker |
| `❌ {name}` | Unload that workplace |

### Status Card

For `/workplace status`:

```
📁 **logstream** (93cb20c8...)
📂 `/Users/.../log-stream/logstream`
🖥️ Host: dsgnmac2
📂 Parent: log-stream (74cdd6fd...)
🔗 Linked: logstream-dashboard

**Agents:**
🟢 kernel — persistent structure watcher
⚪ rust-dev — Rust systems developer
⚪ reviewer — code reviewer
⚪ publisher — release manager

**Loaded:** log-stream, multi-workplace
**Deploy:** dev | main | pre
```

## Session Management (Per-Workplace Chat Sessions)

Each workplace can have saved OpenClaw chat sessions. When switching workplaces, the user is offered to continue an existing session or start fresh.

### Session Storage

Sessions are tracked in `~/.openclaw/workspace/.workplaces/sessions.json`:

```json
{
  "<workplace-uuid>": {
    "sessions": [
      {
        "sessionId": "7cf414ae-01e9-4347-8211-2d948170b718",
        "label": "rust refactor",
        "created": "2026-02-17T18:00:00Z",
        "lastActive": "2026-02-17T22:30:00Z"
      }
    ],
    "activeSession": "7cf414ae-01e9-4347-8211-2d948170b718"
  }
}
```

Fields:
- `sessionId` — OpenClaw session ID (maps to a `.jsonl` transcript)
- `label` — user-given or auto-generated label describing the session
- `created` — ISO timestamp when session was created
- `lastActive` — ISO timestamp of last activity
- `activeSession` — the session to resume by default

### Switch Confirmation with Session Buttons

When switching to a workplace that has saved sessions, show session options **after** the switch confirmation:

```
✅ Switched to **logstream**
📂 `/Users/.../log-stream/logstream`
📂 Parent: log-stream

💬 **Chat Sessions:**
```

**Buttons:**

```json
{
  "blocks": [
    {"type": "text", "text": "💬 **Chat Sessions:**"},
    {"type": "buttons", "buttons": [
      {"label": "▶️ Continue: rust refactor", "style": "primary"},
      {"label": "▶️ Continue: bug fixes", "style": "secondary"}
    ]},
    {"type": "buttons", "buttons": [
      {"label": "✨ New chat session", "style": "success"},
      {"label": "🗑 Manage sessions", "style": "secondary"}
    ]}
  ]
}
```

- Most recent / active session: `style: "primary"`
- Other saved sessions: `style: "secondary"`
- "✨ New chat session": creates a new session, prompts for optional label
- "🗑 Manage sessions": shows delete/rename options

### Switch to Workplace with No Sessions

When switching to a workplace with no saved sessions, auto-create one:

```
✅ Switched to **multi-workplace**
📂 `/Users/.../workspace/multi-workplace`

💬 New chat session started.
```

A new session entry is created in `sessions.json` with an auto-label based on workplace name + date.

### New Chat Session Flow

When user clicks "✨ New chat session":

1. Create a new session entry in `sessions.json` with a generated sessionId (UUID)
2. Set it as `activeSession`
3. Confirm:

```
✨ **New chat session** for **logstream**
Session: `a1b2c3d4-...`

💡 Reply with a label (e.g. "api redesign") or I'll auto-name it.
```

### Continue Session Flow

When user clicks "▶️ Continue: {label}":

1. Set that session as `activeSession` in `sessions.json`
2. Update `lastActive`
3. Load recent context from the session transcript if available
4. Confirm:

```
▶️ Resuming **rust refactor** for **logstream**
Last active: 2h ago
```

### Manage Sessions

When user clicks "🗑 Manage sessions":

```
💬 **Sessions for logstream** (2)
```

**Buttons:**

```json
{
  "blocks": [
    {"type": "buttons", "buttons": [
      {"label": "✏️ rust refactor", "style": "secondary"},
      {"label": "✏️ bug fixes", "style": "secondary"}
    ]},
    {"type": "buttons", "buttons": [
      {"label": "🗑 Delete a session", "style": "danger"},
      {"label": "← Back", "style": "secondary"}
    ]}
  ]
}
```

- "✏️ {label}": rename that session (prompt for new label)
- "🗑 Delete a session": show sessions with delete buttons
- "← Back": return to session list

### Delete Session Flow

```json
{
  "blocks": [
    {"type": "text", "text": "Select session to delete:"},
    {"type": "buttons", "buttons": [
      {"label": "❌ rust refactor", "style": "danger"},
      {"label": "❌ bug fixes", "style": "danger"},
      {"label": "← Back", "style": "secondary"}
    ]}
  ]
}
```

After deletion, remove from `sessions.json`. If it was the `activeSession`, clear it.

### Button Callback Routing (Sessions)

| Button text | Action |
|---|---|
| `▶️ Continue: {label}` | Set as active session, resume |
| `✨ New chat session` | Create new session entry |
| `🗑 Manage sessions` | Show session management view |
| `✏️ {label}` | Prompt to rename session |
| `🗑 Delete a session` | Show delete picker |
| `❌ {label}` (in delete view) | Delete that session |
| `← Back` (in session views) | Return to session list |

### Session Context in Workplace Status

`/workplace status` includes active session info:

```
📁 **logstream** (93cb20c8...)
...
💬 Active session: rust refactor (2h ago)
📝 Total sessions: 3
```

## Platform Fallback

On platforms without inline buttons (WhatsApp, Signal), show hierarchical text:

```
📁 Workplaces (current: logstream)

1. 📂 log-stream (parent)
   1a. ⚙️ logstream ← current
   1b. 🌐 logstream-dashboard
2. 🔧 multi-workplace

Reply with number (e.g. "1b") or name (e.g. "log-stream:logstream-dashboard")
```

For `/workplace loaded` on platforms without buttons:

```
📂 Loaded Workplaces (2)
Active: multi-workplace

1. log-stream — /Users/.../opensource/log-stream
2. multi-workplace — /Users/.../workspace/multi-workplace ← current

Commands: "workplace load <path>" / "workplace unload <name>"
```
