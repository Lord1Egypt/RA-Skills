---
name: hermes-desktop-companion
description: Desktop GUI companion for Hermes Agent - install, configure, chat with AI assistant featuring tool use, memory, skills, and multi-platform messaging
triggers:
  - "set up hermes desktop application"
  - "configure hermes agent gui"
  - "install hermes desktop companion"
  - "manage hermes profiles and sessions"
  - "connect hermes to messaging platforms"
  - "troubleshoot hermes desktop app"
  - "use hermes agent chat interface"
  - "configure hermes memory and skills"
---

# Hermes Desktop Companion

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

Hermes Desktop is a native Electron-based desktop application for installing, configuring, and interacting with [Hermes Agent](https://github.com/NousResearch/hermes-agent) — a self-improving AI assistant with tool use, multi-platform messaging, and closed learning loop. It provides a GUI alternative to CLI management with streaming chat, session management, profile switching, skill installation, memory editing, and gateway configuration.

## What It Does

- **Guided installation**: First-run wizard installs Hermes Agent to `~/.hermes` with dependency resolution
- **Local or remote mode**: Run Hermes locally on `127.0.0.1:8642` or connect to remote API server
- **Multi-provider support**: OpenRouter, Anthropic, OpenAI, Google Gemini, xAI Grok, Nous Portal, Qwen, MiniMax, Hugging Face, Groq, and local OpenAI-compatible endpoints
- **Streaming chat UI**: SSE-based real-time chat with tool progress, markdown rendering, syntax highlighting, token usage tracking
- **22 slash commands**: `/new`, `/clear`, `/fast`, `/web`, `/image`, `/browse`, `/code`, `/shell`, `/usage`, `/help`, `/tools`, `/skills`, `/model`, `/memory`, `/persona`, `/version`, `/compact`, `/compress`, `/undo`, `/retry`, `/debug`, `/status`
- **Profile management**: Multiple isolated Hermes environments with separate configs
- **14 toolsets**: Web search, browser automation, terminal, file ops, code execution, vision, image gen, TTS, skills, memory, session search, clarify, delegation, MoA, task planning
- **Memory system**: View/edit entries, user profile memory, capacity tracking, multiple providers (Honcho, Hindsight, Mem0, RetainDB, Supermemory, ByteRover)
- **16 messaging gateways**: Telegram, Discord, Slack, WhatsApp, Signal, Matrix, Mattermost, Email, SMS, iMessage, DingTalk, Feishu, WeCom, WeChat, Webhooks, Home Assistant
- **Session search**: Full-text search (SQLite FTS5) across conversation history
- **Scheduled tasks**: Cron job builder with 15 delivery targets
- **Hermes Office (Claw3d)**: Visual 3D interface with adapter management

## Installation

### Download Pre-built Binaries

Download from [GitHub Releases](https://github.com/fathah/hermes-desktop/releases/):

| Platform | File |
|----------|------|
| macOS | `.dmg` |
| Linux (any) | `.AppImage` |
| Debian/Ubuntu | `.deb` |
| Fedora/RHEL | `.rpm` |
| Windows | `.exe` (NSIS installer) |

### macOS Installation

```bash
# After installing the .dmg, remove quarantine attribute
xattr -cr "/Applications/Hermes Agent.app"
```

Or right-click → **Open** → confirm in dialog.

### Windows Installation

Download `.exe` from releases. Windows SmartScreen will warn (unsigned) — click "More info" → "Run anyway".

**Future winget support**:
```powershell
winget install NousResearch.HermesDesktop
```

### Linux Installation

**AppImage** (universal):
```bash
chmod +x hermes-desktop-*.AppImage
./hermes-desktop-*.AppImage
```

**Debian/Ubuntu**:
```bash
sudo dpkg -i hermes-desktop-*.deb
sudo apt-get install -f  # Fix dependencies if needed
```

**Fedora/RHEL**:
```bash
sudo dnf install ./hermes-desktop-*.rpm --nogpgcheck
```

### WSL Passwordless Sudo (if installer stalls)

```bash
echo "$USER ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/hermes-install
# Re-run installer, then:
sudo rm /etc/sudoers.d/hermes-install
```

## First-Run Setup

1. **Choose deployment mode**:
   - **Local**: Installs Hermes to `~/.hermes`, runs on `127.0.0.1:8642`
   - **Remote**: Connect to existing Hermes API server (requires URL + API key)

2. **Local mode**: Installer checks for Git, uv, Python 3.11+, then runs official Hermes install script

3. **Configure provider**: Select from OpenRouter, Anthropic, OpenAI, Google, xAI, Nous Portal, Qwen, MiniMax, Hugging Face, Groq, or custom local endpoint

4. **Enter credentials**: API keys are saved to Hermes config files (not stored by desktop app)

5. **Launch workspace**: Main UI opens with Chat, Sessions, Agents, Skills, Memory, Tools, etc.

## Configuration

### Provider Configuration

**Settings → Provider Config**:

```typescript
// Example: OpenRouter setup
{
  provider: "openrouter",
  apiKey: process.env.OPENROUTER_API_KEY,
  model: "anthropic/claude-3.5-sonnet",
  baseUrl: "https://openrouter.ai/api/v1"
}

// Example: Local Ollama
{
  provider: "openai",
  apiKey: "not-needed",
  model: "llama3.1:8b",
  baseUrl: "http://localhost:11434/v1"
}
```

### Remote Mode Configuration

**First run**:
- Choose "Remote" mode
- Enter API URL: `https://your-hermes-server.com`
- Enter API key (from remote Hermes `/api/keys`)
- App validates connection before proceeding

### Profile (Agent) Management

**Agents screen**:
- Create new profile: Creates isolated `~/.hermes/profiles/<name>` directory
- Switch profile: Restarts Hermes with new profile context
- Delete profile: Removes profile directory and data

```bash
# Profiles stored at:
~/.hermes/profiles/
  ├── default/
  │   ├── config.yaml
  │   ├── SOUL.md
  │   ├── memory.db
  │   └── sessions.db
  └── work/
      └── ...
```

### Memory Provider Configuration

**Memory screen → Configure Providers**:

```typescript
// Example: Honcho
{
  provider: "honcho",
  apiKey: process.env.HONCHO_API_KEY,
  appId: "hermes-desktop",
  userId: "user-123"
}

// Example: Mem0
{
  provider: "mem0",
  apiKey: process.env.MEM0_API_KEY,
  userId: "user-123"
}
```

### Gateway Configuration

**Gateway screen** → Select platform → Configure:

**Telegram**:
```yaml
enabled: true
bot_token: ${TELEGRAM_BOT_TOKEN}
allowed_users: [123456789]
```

**Discord**:
```yaml
enabled: true
token: ${DISCORD_BOT_TOKEN}
channel_ids: [1234567890123456789]
```

**Email (IMAP/SMTP)**:
```yaml
enabled: true
imap_server: imap.gmail.com
imap_port: 993
smtp_server: smtp.gmail.com
smtp_port: 587
username: ${EMAIL_USERNAME}
password: ${EMAIL_APP_PASSWORD}
```

**WhatsApp** (via Baileys):
```yaml
enabled: true
session_path: ~/.hermes/whatsapp-session
qr_code_callback: true
```

## Chat Interface Usage

### Basic Chat

Type naturally or use slash commands:

```
> What's the weather in San Francisco?
[Hermes uses web search tool, returns answer]

> /web latest news on AI regulation
[Forces web search, streams results]

> /image a cyberpunk city at sunset
[Generates image via FAL.ai or configured provider]
```

### Slash Commands

| Command | Description |
|---------|-------------|
| `/new` | Start new conversation |
| `/clear` | Clear current chat |
| `/fast` | Switch to faster model |
| `/web <query>` | Force web search |
| `/image <prompt>` | Generate image |
| `/browse <url>` | Browse and extract from URL |
| `/code <task>` | Execute code task |
| `/shell <command>` | Run shell command |
| `/usage` | Show token usage stats |
| `/help` | List all commands |
| `/tools` | Show enabled tools |
| `/skills` | List installed skills |
| `/model [name]` | Get/set current model |
| `/memory [query]` | Search memory |
| `/persona` | Show current persona |
| `/version` | Show Hermes version |
| `/compact` | Compress chat history |
| `/compress` | Deep compress with MoA |
| `/undo` | Remove last message |
| `/retry` | Retry last message |
| `/debug` | Toggle debug mode |
| `/status` | Show system status |

### Token Usage Tracking

Bottom of chat shows live counts:
```
📊 Prompt: 1,234 tokens • Completion: 567 tokens • Cost: $0.0123
```

Use `/usage` for detailed breakdown:
```
> /usage
Session Usage:
  Total Prompt Tokens: 12,345
  Total Completion Tokens: 5,678
  Total Cost: $0.123
  Messages: 15
```

## Skills Management

### Installing Skills

**Skills screen**:
1. Browse bundled skills (pre-installed with Hermes)
2. Or install from GitHub:
   ```
   Repository: username/repo-name
   Branch: main (optional)
   ```
3. Click **Install**

### Skill Structure

Skills are markdown files with YAML frontmatter:

```markdown
---
name: web-search-expert
description: Expert at web searching and information retrieval
triggers:
  - "search the web for"
  - "find information about"
  - "look up"
---

# Web Search Expert

Use the web_search tool to find current information...

## Examples

When user asks: "What's the latest on GPT-5?"
1. Use web_search with query "GPT-5 latest news"
2. Summarize findings
3. Cite sources
```

### Editing Skills

**Skills screen** → Click skill → **Edit**:
- Modify triggers, description, or content
- Changes saved to `~/.hermes/skills/<name>/SKILL.md`

## Memory System

### Viewing Memory

**Memory screen**:
- **Memory Entries**: List of stored facts/context
- **User Profile**: Persistent user information
- **Capacity**: Current usage vs. limit

### Adding Memory

Chat naturally — Hermes auto-saves important context:
```
> My name is Alice and I prefer Python over JavaScript
[Hermes stores to memory automatically]

> What's my name?
[Hermes retrieves: "Alice"]
```

Or explicit:
```
> Remember I'm working on a TypeScript project called Hermes Desktop
[Hermes: ✓ Stored to memory]
```

### Editing Memory Entries

**Memory screen**:
1. Click entry to view
2. Edit content or delete
3. Save changes

### Memory Providers

Configured in **Memory screen → Configure Providers**:

- **Honcho**: Managed memory service
- **Hindsight**: Self-hosted memory
- **Mem0**: Personalized AI memory
- **RetainDB**: Vector memory DB
- **Supermemory**: Context-aware memory
- **ByteRover**: Local memory store

## Session Management

### Searching Sessions

**Sessions screen**:
- **Search bar**: Full-text search (SQLite FTS5) across all conversations
- **Date groups**: Conversations grouped by Today, Yesterday, Last 7 Days, Last 30 Days, Older

```typescript
// Example: Search sessions programmatically (if extending app)
import { searchSessions } from './main/database';

const results = await searchSessions('typescript error handling');
// Returns: [{ id, title, timestamp, snippet, profileId }, ...]
```

### Resuming Sessions

1. **Sessions screen** → Click conversation
2. Chat loads with full history
3. Continue conversation from last message

### Deleting Sessions

Right-click session → **Delete** or click trash icon.

## Tools Management

**Tools screen** → Enable/disable toolsets:

| Toolset | Capabilities |
|---------|--------------|
| **web** | Exa/Tavily search, Firecrawl scraping |
| **browser** | Playwright automation, screenshot, PDF |
| **terminal** | Shell command execution |
| **file** | Read, write, list, move files |
| **code** | Python execution in sandbox |
| **vision** | Image analysis (GPT-4V, Claude Vision) |
| **image** | Generation via FAL.ai/DALL-E |
| **tts** | Text-to-speech synthesis |
| **skills** | Install/manage skills |
| **memory** | Store/retrieve context |
| **session** | Search past conversations |
| **clarify** | Ask clarifying questions |
| **delegation** | Multi-agent task delegation |
| **moa** | Mixture-of-Agents synthesis |
| **planning** | Break down complex tasks |

Example enabling web tool:
```yaml
# ~/.hermes/profiles/default/config.yaml
tools:
  web:
    enabled: true
    exa_api_key: ${EXA_API_KEY}
    tavily_api_key: ${TAVILY_API_KEY}
```

## Scheduled Tasks

**Schedules screen** → **Create Task**:

```yaml
name: "Daily standup summary"
schedule: "0 9 * * 1-5"  # 9 AM weekdays
task: "Summarize yesterday's GitHub activity and send to Slack"
delivery:
  type: slack
  channel: "#standup"
```

**Schedule types**:
- **Minutes**: Every N minutes
- **Hourly**: Every N hours
- **Daily**: Specific time daily
- **Weekly**: Specific day/time weekly
- **Custom**: Full cron expression

**Delivery targets**:
Telegram, Discord, Slack, WhatsApp, Signal, Matrix, Email, SMS, Webhook, Home Assistant, File, Terminal, Memory, Chat (in-app), Desktop Notification

## Development Setup

### Prerequisites

```bash
node --version  # v18+ recommended
npm --version   # v9+
```

### Clone and Install

```bash
git clone https://github.com/fathah/hermes-desktop.git
cd hermes-desktop
npm install
```

### Development Mode

```bash
npm run dev
```

This starts:
- Vite dev server for React UI
- Electron main process with hot reload
- TypeScript watch compiler

### Project Structure

```
hermes-desktop/
├── src/
│   ├── main/          # Electron main process
│   │   ├── index.ts   # Entry point, IPC handlers
│   │   ├── database.ts # SQLite sessions/memory
│   │   ├── installer.ts # Hermes install logic
│   │   └── updater.ts  # Auto-update
│   ├── preload/       # Electron preload script
│   │   └── index.ts   # IPC bridge to renderer
│   └── renderer/      # React UI
│       ├── App.tsx
│       ├── screens/   # Chat, Sessions, Tools, etc.
│       ├── components/
│       └── lib/       # SSE parser, utils
├── electron.vite.config.ts
├── package.json
└── resources/         # Icons, installers
```

### IPC Communication Pattern

**Renderer → Main**:
```typescript
// src/renderer/lib/api.ts
export async function sendChatMessage(message: string, profileId: string) {
  return window.electron.ipcRenderer.invoke('chat:send', { message, profileId });
}
```

**Main handler**:
```typescript
// src/main/index.ts
ipcMain.handle('chat:send', async (event, { message, profileId }) => {
  const response = await fetch('http://127.0.0.1:8642/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, profile: profileId })
  });
  // Stream SSE events back to renderer
});
```

### SSE Streaming Implementation

```typescript
// src/renderer/lib/sse-parser.ts
export class SSEParser {
  private buffer = '';

  parse(chunk: string): SSEEvent[] {
    this.buffer += chunk;
    const lines = this.buffer.split('\n');
    this.buffer = lines.pop() || '';
    
    const events: SSEEvent[] = [];
    let currentEvent: Partial<SSEEvent> = {};
    
    for (const line of lines) {
      if (line.startsWith('event:')) {
        currentEvent.event = line.slice(7).trim();
      } else if (line.startsWith('data:')) {
        currentEvent.data = line.slice(6).trim();
      } else if (line === '') {
        if (currentEvent.event) {
          events.push(currentEvent as SSEEvent);
        }
        currentEvent = {};
      }
    }
    
    return events;
  }
}
```

**Usage in Chat**:
```typescript
// src/renderer/screens/Chat.tsx
const parser = new SSEParser();

fetch('http://127.0.0.1:8642/chat', {
  method: 'POST',
  body: JSON.stringify({ message })
}).then(async (response) => {
  const reader = response.body!.getReader();
  const decoder = new TextDecoder();
  
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    
    const chunk = decoder.decode(value);
    const events = parser.parse(chunk);
    
    for (const event of events) {
      if (event.event === 'content') {
        appendContent(JSON.parse(event.data).text);
      } else if (event.event === 'tool_start') {
        showToolProgress(JSON.parse(event.data));
      } else if (event.event === 'usage') {
        updateTokenCount(JSON.parse(event.data));
      }
    }
  }
});
```

## Building for Production

### Build All Platforms (current OS)

```bash
npm run build
```

Output: `dist/` directory with installers

### Platform-Specific Builds

```bash
npm run build:win    # Windows .exe
npm run build:mac    # macOS .dmg
npm run build:linux  # .AppImage, .deb, .rpm
```

### Build Configuration

Edit `electron-builder.yml`:

```yaml
appId: com.nousresearch.hermesdesktop
productName: Hermes Agent
directories:
  output: dist
  buildResources: resources

mac:
  target:
    - dmg
    - zip
  category: public.app-category.productivity
  icon: resources/icon.icns

win:
  target:
    - nsis
  icon: resources/icon.ico

linux:
  target:
    - AppImage
    - deb
    - rpm
  category: Utility
  icon: resources/icon.png
```

## Troubleshooting

### Installer Stalls on "Installing dependencies"

**WSL**: Grant temporary passwordless sudo (see Installation section)

**General**: Check logs in `~/.hermes/logs/install.log`:
```bash
tail -f ~/.hermes/logs/install.log
```

### "Connection refused" on 127.0.0.1:8642

Hermes not running. Start manually:
```bash
cd ~/.hermes
source venv/bin/activate
python -m hermes.server
```

Or restart from **Settings → Restart Hermes**.

### Remote mode connection fails

1. Verify URL is reachable: `curl https://your-hermes-server.com/health`
2. Check API key in remote Hermes: `hermes keys list`
3. Ensure firewall allows traffic

### Memory provider not connecting

Check API keys in **Memory → Configure Providers**:
```typescript
// Test Honcho connection
const response = await fetch('https://api.honcho.dev/apps', {
  headers: { 'Authorization': `Bearer ${process.env.HONCHO_API_KEY}` }
});
```

### Gateway fails to send messages

1. **View logs**: **Settings → View Logs** → Select gateway
2. **Telegram**: Verify bot token with `@BotFather`, check allowed_users IDs
3. **Discord**: Ensure bot has `SEND_MESSAGES` permission in channel
4. **Email**: Test SMTP credentials with `telnet smtp.server.com 587`

### Skills not triggering

1. Check triggers in skill YAML frontmatter are specific
2. Ensure skill is enabled: **Skills screen** → Check toggle
3. Restart profile: **Agents** → Switch away and back

### Auto-update fails (Fedora RPM)

RPM builds don't support auto-update. Download new `.rpm` and reinstall:
```bash
sudo dnf install ./hermes-desktop-<new-version>.rpm --nogpgcheck
```

### Chat stuck on "Thinking..."

1. Check network: `curl -I http://127.0.0.1:8642/health`
2. Check model provider API status (OpenRouter, Anthropic, etc.)
3. View debug logs: `/debug` in chat or **Settings → View Logs → Agent**

### Session search returns no results

Database index corrupt. Rebuild FTS5 index:
```bash
cd ~/.hermes/profiles/default
sqlite3 sessions.db "DELETE FROM sessions_fts; INSERT INTO sessions_fts SELECT * FROM sessions;"
```

### macOS "App is damaged" error

Remove quarantine:
```bash
xattr -cr "/Applications/Hermes Agent.app"
```

### Windows SmartScreen blocks installer

Click "More info" → "Run anyway" (app is not code-signed).

## Environment Variables

```bash
# LLM Providers
OPENROUTER_API_KEY=sk-or-...
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...
XAI_API_KEY=...

# Search/Web Tools
EXA_API_KEY=...
TAVILY_API_KEY=...
FIRECRAWL_API_KEY=...

# Image Generation
FAL_API_KEY=...
REPLICATE_API_TOKEN=...

# Memory Providers
HONCHO_API_KEY=...
MEM0_API_KEY=...

# Messaging Gateways
TELEGRAM_BOT_TOKEN=...
DISCORD_BOT_TOKEN=...
SLACK_BOT_TOKEN=...
TWILIO_ACCOUNT_SID=...
TWILIO_AUTH_TOKEN=...

# Email
EMAIL_USERNAME=...
EMAIL_APP_PASSWORD=...

# Analytics
WANDB_API_KEY=...
```

Store in `~/.hermes/.env` or OS-level environment.

## Testing

### Run Tests

```bash
npm test
```

Test suites:
- **SSE parser**: Validates event parsing, incomplete chunks, malformed data
- **IPC handlers**: Mock Electron IPC, test chat/session/profile handlers
- **Preload API**: Ensures all main process APIs are safely exposed
- **Installer utils**: Dependency checking, path resolution
- **Constants**: Validates config schema, provider definitions

### Example Test

```typescript
// src/__tests__/sse-parser.test.ts
import { describe, it, expect } from 'vitest';
import { SSEParser } from '../renderer/lib/sse-parser';

describe('SSEParser', () => {
  it('parses complete events', () => {
    const parser = new SSEParser();
    const events = parser.parse('event: content\ndata: {"text":"Hello"}\n\n');
    
    expect(events).toHaveLength(1);
    expect(events[0].event).toBe('content');
    expect(JSON.parse(events[0].data).text).toBe('Hello');
  });
  
  it('buffers incomplete events', () => {
    const parser = new SSEParser();
    const events1 = parser.parse('event: content\n');
    const events2 = parser.parse('data: {"text":"Hi"}\n\n');
    
    expect(events1).toHaveLength(0);
    expect(events2).toHaveLength(1);
  });
});
```

## Resources

- **Documentation**: https://hermes-agent.nousresearch.com/docs/
- **GitHub Repository**: https://github.com/fathah/hermes-desktop
- **Releases**: https://github.com/fathah/hermes-desktop/releases
- **Telegram Community**: https://t.me/hermes_agent_desktop
- **Issue Tracker**: https://github.com/fathah/hermes-desktop/issues
- **Hermes Agent Core**: https://github.com/NousResearch/hermes-agent

## License

MIT License — see [LICENSE](https://github.com/fathah/hermes-desktop/blob/main/LICENSE)
