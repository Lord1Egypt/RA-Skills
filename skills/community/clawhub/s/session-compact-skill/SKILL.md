---
name: openclaw-session-compact
description: |
  Intelligent session compression plugin for OpenClaw that automatically manages token consumption and supports unlimited-length conversations. Compresses historical messages into structured summaries to reduce token usage by 85-95%. Provides CLI commands: compact, compact-status, compact-config, sessions, session-info.
---

# OpenClaw Session Compact Plugin v1.2.1

Intelligent session compression plugin for OpenClaw that automatically manages token consumption and supports **unlimited-length conversations**. By automatically compressing historical messages into structured summaries, it significantly reduces token usage (typically 85-95% savings).

## ✨ New in v1.2.1

- 🐛 **Fixed**: Configuration persistence — `loadFromOpenClawConfig()` correctly reads from `plugins.entries.<id>.config`
- ✨ **Added**: 16 comprehensive test cases for OpenClaw config loading (163 total tests)
- 📝 **Improved**: README with step-by-step installation guide and troubleshooting
- 🔧 **Updated**: Dependencies — `openclaw` → 2026.4.9, `basic-ftp` → 5.2.2
- 🔧 **Updated**: `openclaw.build.openclawVersion` → 2026.4.9

### v1.1.0 Highlights

- **Session Persistence**: JSON file-based storage with version tracking
- **Token Usage Tracking**: Actual API usage + cache token metrics
- **Rich Message Structure**: ContentBlock types (text, tool_use, tool_result)
- **Session Lifecycle Manager**: Auto-compaction, state management, events
- **New CLI Commands**: `sessions`, `session-info`

## 🚀 Quick Start

### Installation

**From ClawHub** (recommended):

```bash
clawhub install openclaw-session-compact
```

**Manual installation**:

```bash
git clone https://github.com/SDC-creator/openclaw-session-compact.git \
  ~/.openclaw/extensions/openclaw-session-compact
cd ~/.openclaw/extensions/openclaw-session-compact
npm install --production
```

### Configuration

Add to `~/.openclaw/openclaw.json`:

```json
{
  "plugins": {
    "allow": ["openclaw-session-compact"],
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

**重要**：配置参数从 OpenClaw 配置系统读取。修改配置后需要重启 Gateway：

```bash
openclaw gateway restart
```


## 💡 Usage Scenarios

### Scenario 1: CLI Commands

```bash
# Check current session status
openclaw compact-status

# Manually trigger compression
openclaw compact

# Force compression (ignores threshold)
openclaw compact --force

# View configuration
openclaw compact-config
```

### Scenario 2: Automatic Compression

```bash
# Start OpenClaw - compression works automatically
openclaw start

# When conversation history exceeds the threshold, it auto-compresses
# and continues seamlessly without user intervention
```

### Scenario 3: Long Conversation Handling

**Problem**: Conversations exceeding 10,000 tokens cause:
- Rapid token consumption
- Slower response times
- Potential model limits exceeded

**Solution**: Session Compact automatically compresses history:

```
Before: 50 messages (1,250 tokens)
        ↓ [Auto-compress]
After:  5 messages (360 tokens) - 92% token savings
```

## 🔧 Configuration Options

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

**Aggressive Mode** (fewer compressions, more context retained):
```json
{
  "max_tokens": 20000,
  "preserve_recent": 3
}
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

### Fallback Mechanism

When LLM is unavailable, automatically falls back to **code extraction** mode:
- Extract timeline directly from message content
- Use preset templates for summary fields
- Ensures functionality without LLM dependency

## 🛠️ Troubleshooting

### Common Issues

#### 1. Compression Not Triggered

**Cause**: Token count below threshold
**Solution**:
```bash
# Check current token usage
openclaw compact-status

# Lower threshold for testing
openclaw compact --force
```

#### 2. Poor Summary Quality

**Cause**: LLM misconfigured or unavailable
**Solution**:
- Verify `model` configuration
- Ensure OpenClaw Gateway is running: `openclaw gateway start`
- System auto-falls back to code extraction

#### 3. Context Loss After Compression

**Cause**: `preserve_recent` set too low
**Solution**:
```json
{
  "preserve_recent": 6  // Increase to 6 or more
}
```

#### 4. Plugin Not Recognized

**Cause**: Missing plugin configuration
**Solution**:
```bash
# Check plugin status
openclaw plugins list | grep compact

# Ensure plugin is in plugins.allow in openclaw.json
```

## 📈 Performance Metrics

- **Test Coverage**: 82.78% (163 tests passing)
- **Core Function Coverage**: 89.76%
- **Average Compression Time**: < 1 second (without LLM)
- **Token Savings**: Typically 85-95%
- **Memory Usage**: Low (no leaks)

## 🧪 Testing

```bash
# Run tests
npm test

# Check coverage (163 tests, 82.78%)
npm run test:coverage
```

## 📚 Technical Documentation

For detailed API documentation and examples, see [README.md](README.md).

### Core API

```typescript
// Compress session
const result = await compactSession(messages, config);

// Check if compression is needed
const needsCompact = shouldCompact(messages, config);

// Estimate token count
const tokens = estimateTokenCount(messages);
```

## 🤝 Contributing

Contributions are welcome! Please submit Issues and Pull Requests.

1. Fork the project
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

MIT License

---

**Status**: ✅ Stable Release
**Tests**: ✅ 163/163 Passing
**Coverage**: 📈 82.78%
**ClawHub (Code Plugin)**: ✅ Published (openclaw-session-compact@1.2.1)
**ClawHub (Skill)**: ✅ Published (session-compact-skill@1.2.1)
**Version**: v1.2.1
**Maintainer**: SDC-creator
