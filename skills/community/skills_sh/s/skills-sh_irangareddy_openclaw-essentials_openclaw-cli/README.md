# OpenClaw CLI Skill

Comprehensive reference for all openclaw CLI commands and workflows.

## Coverage

- **Setup & Onboarding** - Initial configuration and setup
- **Gateway Management** - Start, stop, configure gateway
- **Agent Management** - Multi-agent routing and identities
- **Skills & Hooks** - Automation and capabilities
- **Channels** - WhatsApp, Telegram, Discord, etc.
- **Models** - Authentication and configuration
- **Messaging** - Send messages, polls, reactions
- **Browser** - Headless browser control
- **Nodes** - iOS/Android node management
- **System** - Events, heartbeat, presence
- **Cron** - Scheduled jobs
- **Memory** - Vector search and indexing

## Quick Reference

### Most Used Commands

```bash
# Setup
openclaw onboard --install-daemon

# Gateway
openclaw gateway
openclaw gateway status

# Agents
openclaw agents list
openclaw agents add <name>

# Skills
openclaw skills list
openclaw skills info <name>

# Hooks
openclaw hooks enable session-memory
openclaw hooks list

# Channels
openclaw channels login
openclaw channels status

# Models
openclaw models status
openclaw models set <model-id>

# Health
openclaw doctor
openclaw status --deep
```

## See SKILL.md

Full documentation in `SKILL.md` with all commands, options, and workflows.
