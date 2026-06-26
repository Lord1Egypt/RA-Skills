# Self-Improving Agent

Continuous learning and improvement system for OpenClaw agents.

## Features

- 📝 **Error Logging**: Automatically capture command failures and exceptions
- 🎓 **Learning Capture**: Record corrections and discoveries
- 🔄 **Periodic Review**: Regular retrospectives to consolidate learnings
- 🧠 **Memory Integration**: Promote important patterns to long-term memory
- 🛡️ **Rule Formation**: Create hardened rules to prevent recurring mistakes

## How It Works

```
Error occurs → Log immediately → Periodic review → Integrate to memory → Form rules → Prevent recurrence
```

This isn't just an error log—it's a complete learning loop that makes your agent smarter over time.

## Prerequisites

- OpenClaw agent environment

## Installation

### Via ClawHub (Recommended)

```bash
clawhub install self-improving-agent
```

### Manual Installation

1. Clone to `~/.openclaw/skills/self-improving-agent`
2. Create learning directories:
   ```bash
   mkdir -p <WORKSPACE>/.learnings
   ```

## Usage

The skill activates automatically when:

1. A command or operation fails unexpectedly
2. You correct the agent ("No, that's wrong...", "Actually...")
3. You request a capability that doesn't exist
4. An external API or tool fails
5. The agent discovers a better approach

You can also manually trigger reviews:

```
Review recent learnings
整合最近的教训到长期记忆
```

## Files

- `.learnings/ERRORS.md`: Command failures and exceptions
- `.learnings/LEARNINGS.md`: Corrections and discoveries
- `.learnings/FEATURE_REQUESTS.md`: Requested missing capabilities

## Origin

Based on `self-improving-agent@1.0.11` from [ClawHub](https://clawhub.ai)
Original repository: https://github.com/pskoett/pskoett-ai-skills

## License

MIT License - see [LICENSE](LICENSE) file
