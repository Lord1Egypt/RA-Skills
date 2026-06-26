# OpenClaw Session Compact Plugin 🔄

Intelligent session compression plugin for OpenClaw that automatically manages token consumption and supports **unlimited-length conversations**. By automatically compressing historical messages into structured summaries, it significantly reduces token usage (typically 85-95% savings).

## ✨ Key Features

- **Automatic Compression**: Triggers when session tokens approach threshold
- **Smart Summaries**: Preserves key information (timeline, todos, files)
- **Seamless Continuation**: Conversations continue without user intervention
- **Fallback Protection**: Code-based extraction when LLM unavailable
- **Recursive Compression**: Supports multiple compression cycles
- **CLI Commands**: `openclaw compact`, `openclaw compact-status`, `openclaw compact-config`, `openclaw sessions`, `openclaw session-info`

## 🚀 Quick Start

### 1. Installation

**From ClawHub** (recommended):

```bash
# Install the code plugin
clawhub install openclaw-session-compact
```

**Manual installation** (if ClawHub is not available):

> ⚠️ **Important**: This plugin requires compilation. Do not skip the build step!

```bash
# Step 1: Clone the plugin
git clone https://github.com/SDC-creator/openclaw-session-compact.git \
  ~/.openclaw/extensions/openclaw-session-compact

# Step 2: Install dependencies
cd ~/.openclaw/extensions/openclaw-session-compact
npm install --production

# Step 3: Build the plugin (TypeScript → JavaScript)
npm run build

# Step 4: Verify the build
ls dist/index.js  # Should exist
```

**Troubleshooting**:
- If you see `plugin not found` error, ensure `dist/` directory exists
- If build fails, check Node.js version (requires v18+ or v22+)

### 2. Plugin Configuration
After installation, configure the plugin in `~/.openclaw/openclaw.json`:

```json
{
  "plugins": {
    "allow": ["openclaw-session-compact"],
    "entries": {
      "openclaw-session-compact": {
        "enabled": true
      }
    }
  }
}
```

### 3. Restart Gateway
```bash
openclaw gateway restart
```

### 4. Verify Installation
```bash
openclaw status | grep session-compact
# Expected output: "openclaw-session-compact: loaded"
```

### 3. Compression Configuration (Optional)

Configure compression behavior in `~/.openclaw/openclaw.json`:

```json
{
  "plugins": {
    "entries": {
      "openclaw-session-compact": {
        "enabled": true,
        "config": {
          "max_tokens": 10000,
          "preserve_recent": 4,
          "auto_compact": true,
          "model": ""
        }
      }
    }
  }
}
```

**Using CLI to set configuration** (recommended):

```bash
# Set max_tokens threshold
openclaw config set plugins.entries.openclaw-session-compact.config.max_tokens 10000 --strict-json

# Set preserve_recent
openclaw config set plugins.entries.openclaw-session-compact.config.preserve_recent 4 --strict-json

# Set auto_compact
openclaw config set plugins.entries.openclaw-session-compact.config.auto_compact true --strict-json

# Restart gateway to apply changes
openclaw gateway restart
```

**View current configuration**:

```bash
openclaw config get plugins.entries.openclaw-session-compact.config
```

### 4. Usage

**CLI Commands**:

```bash
# Check current session status
openclaw compact-status

# Manually compress current session
openclaw compact

# Force compression (ignores threshold)
openclaw compact --force

# View configuration
openclaw compact-config

# View specific config value
openclaw compact-config max_tokens

# Set config value (not persisted)
openclaw compact-config max_tokens 5000

# List all saved sessions
openclaw sessions

# Show detailed session information
openclaw session-info --session-id my-session
```

**Automatic Mode** (Recommended):
```bash
# Start OpenClaw - compression works automatically
openclaw start
# Auto-compresses when conversation exceeds threshold
```

## 📊 How It Works

### Compression Flow

```
1. Monitor token usage
   ↓
2. Exceeds threshold (90%)?
   ├─ No → Continue conversation
   └─ Yes → Trigger compression
        ↓
3. Keep last N messages (default: 4)
   ↓
4. Compress old messages into structured summary
   ├─ Scope: Statistics
   ├─ Recent requests: Last 3 user requests
   ├─ Pending work: To-dos
   ├─ Key files: Important files
   ├─ Tools used: Tools mentioned
   └─ Key timeline: Conversation timeline
   ↓
5. Replace old messages with System summary
   ↓
6. Seamlessly continue conversation
```

### Compression Example

**Before**: 50 messages (1,250 tokens)
```
user: Message 1...
assistant: Message 2...
...
user: Message 49...
assistant: Message 50...
```

**After**: 5 messages (360 tokens) - **92% token savings**
```
system: Summary:
- Scope: 46 earlier messages compacted
- Recent requests:
  - Message 37: Discussing complex problem
  - Message 41: File operations
  - Message 45: Tool usage details
- Pending work: Continue debugging
- Key timeline:
  - user: Message 37...
  - assistant: Message 38...
  - user: Message 39...

user: Message 49...
assistant: Message 50...
```

## 🔧 Configuration Reference

| Parameter | Type | Default | Description | Recommended |
|-----------|------|---------|-------------|-------------|
| `max_tokens` | number | 10000 | Token threshold for compression | 5000-20000 |
| `preserve_recent` | number | 4 | Number of recent messages to keep | 4-6 |
| `auto_compact` | boolean | true | Enable automatic compression | true |
| `model` | string | '' | Model for summary generation | Global default |

### Configuration Examples

**Conservative Mode** (frequent compression, max token savings):
```json
{
  "max_tokens": 5000,
  "preserve_recent": 6
}
```

**Aggressive Mode** (fewer compressions, more context):
```json
{
  "max_tokens": 20000,
  "preserve_recent": 3
}
```

## 📚 API Documentation

### Core Functions

#### `compactSession(messages, config)`

Compresses a session and returns the result.

```typescript
async function compactSession(
  messages: Array<{ role: string; content?: string }>,
  config: CompactConfig
): Promise<CompactionResult>
```

**Parameters**:
- `messages`: Array of conversation messages
- `config`: Configuration object

**Returns**:
```typescript
interface CompactionResult {
  summary: string;           // Raw summary
  formattedSummary: string;  // Formatted summary
  removedCount: number;      // Messages removed
  savedTokens: number;       // Tokens saved
}
```

**Example**:
```typescript
const result = await compactSession(messages, {
  max_tokens: 10000,
  preserve_recent: 4
});

console.log(`Removed ${result.removedCount} messages, saved ${result.savedTokens} tokens`);
```

#### `shouldCompact(messages, config)`

Checks if compression is needed.

```typescript
function shouldCompact(
  messages: Array<{ content?: string }>,
  config: CompactConfig
): boolean
```

**Example**:
```typescript
if (shouldCompact(messages, config)) {
  console.log('Compression needed');
}
```

#### `estimateTokenCount(messages)`

Estimates token count for messages.

```typescript
function estimateTokenCount(
  messages: Array<{ content?: string }>
): number
```

**Note**: Uses simplified algorithm (4 chars ≈ 1 token).

## 🛠️ Development Guide

### Local Development

```bash
# Navigate to project
cd <project-root>

# Install dependencies
npm install

# Build
npm run build

# Development mode (watch for changes)
npm run dev

# Run tests
npm test

# Check coverage
npm run test:coverage
```

### Project Structure

```
openclaw-session-compact/
├── src/
│   ├── index.ts              # Plugin entry point (register function)
│   ├── compact/
│   │   ├── config.ts         # Configuration management
│   │   ├── engine.ts         # Core compression logic
│   │   └── __tests__/        # Unit tests (94 tests, 94.65% coverage)
│   │       ├── config.test.ts
│   │       ├── engine.test.ts
│   │       ├── engine-integration.test.ts
│   │       └── engine-mock.test.ts
│   └── cli/
│       └── register.ts       # CLI command registration (legacy)
├── bin/
│   └── openclaw-compact.js   # Standalone CLI entry point
├── package.json
├── openclaw.plugin.json      # OpenClaw plugin manifest
├── tsconfig.json
└── README.md
```

### Plugin Architecture

This project is an **OpenClaw plugin** (not just a workspace skill). Key differences:

| Aspect | Workspace Skill | Plugin |
|--------|----------------|--------|
| Location | `workspace/skills/` | `~/.openclaw/extensions/` |
| Purpose | Documentation for LLM | Executable code |
| Entry | `SKILL.md` with frontmatter | `dist/index.js` with `register()` |
| CLI | Not supported | Supported via `api.registerCli()` |

### Adding New Features

1. Add new function in `src/compact/engine.ts`
2. Add corresponding test in `src/compact/__tests__/` or `src/__tests__/`
3. Run `npm run test:coverage` to ensure coverage doesn't decrease
4. Update `README.md` documentation
5. Rebuild: `npm run build`
6. Sync to extensions: copy `dist/`, `package.json`, `openclaw.plugin.json` to `~/.openclaw/extensions/openclaw-session-compact/`

## 📦 Publishing to ClawHub

### Prerequisites

1. **Login to ClawHub**: `clawhub login` (GitHub OAuth)
2. **Verify identity**: `clawhub whoami`

### Publish as Code Plugin

```bash
# Build first
npm run build

# Publish to ClawHub
clawhub package publish . \
  --family code-plugin \
  --source-repo SDC-creator/openclaw-session-compact \
  --source-commit $(git rev-parse HEAD) \
  --version 1.0.0 \
  --changelog "Your changelog here" \
  --tags latest
```

### Required `package.json` Fields

```json
{
  "name": "openclaw-session-compact",
  "version": "1.0.0",
  "openclaw": {
    "extensions": ["./dist/index.js"],
    "compat": {
      "pluginApi": ">=2026.4.2"
    },
    "build": {
      "openclawVersion": "2026.4.5"
    }
  }
}
```

### Verify Publication

```bash
clawhub package inspect openclaw-session-compact
```

## 📈 Performance Metrics

- **Test Coverage**: 94.65% (94 tests passing)
- **Core Function Coverage**: 89.76%
- **Average Compression Time**: < 1 second (without LLM)
- **Token Savings**: Typically 85-95%
- **Memory Usage**: Low (no leaks)

## 🐛 Troubleshooting

### Issue: Plugin Not Recognized

**Cause**: Missing plugin configuration
**Solution**:
```bash
# Check plugin status
openclaw plugins list | grep compact

# Ensure plugin is in plugins.allow
# Add to openclaw.json:
# "plugins": { "allow": ["openclaw-session-compact"] }
```

### Issue: Compression Not Triggered

**Cause**: Token count below threshold
**Solution**:
```bash
# Check current token usage
openclaw compact-status

# Lower threshold for testing
openclaw compact-config max_tokens 1000
```

### Issue: Poor Summary Quality

**Cause**: LLM misconfigured or unavailable
**Solution**:
- Verify `model` configuration
- Ensure OpenClaw Gateway is running: `openclaw gateway start`
- System auto-falls back to code extraction

### Issue: Context Loss After Compression

**Cause**: `preserve_recent` set too low
**Solution**:
```json
{
  "preserve_recent": 6  // Increase to 6 or more
}
```

## 📝 Changelog

### v1.2.0 (2026-04-11)
- 🐛 **Fixed**: Configuration persistence — `loadFromOpenClawConfig()` correctly reads from `plugins.entries.<id>.config`
- ✨ **Added**: 16 comprehensive test cases for OpenClaw config loading (163 total tests)
- 📝 **Improved**: README with step-by-step installation guide and troubleshooting
- 🔧 **Updated**: Dependencies — `openclaw` → 2026.4.9, `basic-ftp` → 5.2.2
- 🔧 **Updated**: `openclaw.build.openclawVersion` → 2026.4.9

### v1.1.0 (2026-04-11)
- 🐛 **Fixed**: Configuration persistence issue - parameters now correctly persist to `openclaw.json`
- ✨ **Added**: `loadFromOpenClawConfig()` function for proper configuration handling
- ✨ **Added**: Debug logging for configuration troubleshooting
- 📝 **Updated**: README with correct configuration path (`plugins.entries.<id>.config`)
- 📝 **Updated**: Configuration examples using `openclaw config set` CLI commands
- 🔧 **Improved**: Default `max_tokens` increased from 5000 to 10000
- ✅ **Verified**: Configuration loading and persistence working correctly

### v1.0.0 (2026-04-06)
- ✨ Initial release
- ✅ 94 unit tests passing (94.65% coverage)
- ✅ CLI commands: `compact`, `compact-status`, `compact-config`
- ✅ Plugin architecture with `api.registerCli()`
- ✅ Published to ClawHub as code plugin
- ✅ Compression functionality verified
- ✅ Fallback mechanism validated
- 📚 Complete documentation

## 🤝 Contributing

Contributions are welcome! Please submit Issues and Pull Requests.

1. Fork the project
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

MIT License

---

**Project Status**: ✅ Stable Release
**Tests**: ✅ 94/94 Passing
**Coverage**: 📈 94.65%
**ClawHub**: ✅ Published (openclaw-session-compact@1.2.0)
**Maintainer**: SDC-creator

**Chinese Documentation**: [SKILL_CN.md](SKILL_CN.md)
