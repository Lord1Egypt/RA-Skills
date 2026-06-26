# 🔒 secucheck

**Comprehensive security audit skill for OpenClaw**

Analyzes configuration, permissions, exposure risks, and runtime environment with context-aware recommendations.

## Installation

```bash
clawhub install secucheck
```

## Usage

Ask your OpenClaw agent:

```
security audit
```

Or:
- `secucheck`
- `run security check`
- `audit my setup`

## Expertise Levels

On first run, you'll be asked to choose a level:

| Level | Description |
|-------|-------------|
| 🌱 Beginner | Simple analogies, no jargon |
| 💻 Intermediate | Technical details, config examples |
| 🔐 Expert | Attack vectors + edge cases |

All levels run identical checks—only explanation depth varies.

## What It Checks

- ⚡ **Runtime**: Network exposure, VPN, containers, privileges
- 📢 **Channels**: DM policies, group policies, mention settings
- 🤖 **Agents**: Tool permissions, workspace isolation
- ⏰ **Cron Jobs**: Automated tasks, external data dependencies
- 🧩 **Skills**: Installed skill security scan
- 🔐 **Sessions**: Session isolation, memory settings
- 🌐 **Network**: Gateway binding, authentication

## Dashboard

Visual HTML report:

```
show dashboard
```

Displays:
- Overall security score
- Runtime environment status
- Findings by severity with collapsible details

## Auto-Review

This skill runs automatically when:
- Installing new skills
- Creating/modifying agents
- Creating/modifying cron jobs

## Risk Levels

| Icon | Severity | Meaning |
|------|----------|---------|
| 🔴 | Critical | Immediate action required |
| 🟠 | High | Significant risk, fix soon |
| 🟡 | Medium | Notable concern |
| 🟢 | Low | Minor issue or best practice |
| ⚪ | Info | Not a risk, but notable |

## Context-Aware

secucheck considers your environment:
- VPN/Tailscale? Network findings less critical
- Single user? Session isolation less important
- Containerized? Privilege escalation less severe

## Example Output

```
🔒 Security Audit Results

🟢 Good

| Severity | Count |
|----------|-------|
| 🔴 Critical | 0 |
| 🟠 High | 0 |
| 🟡 Medium | 1 |
| 🟢 Low | 2 |

Runtime: VPN active ✅ | No container | sudo available
```

## Safe by Design

- **Read-only**: Never modifies configuration automatically
- **Explicit consent**: All fixes require user confirmation
- **Impact warnings**: Explains what might break before applying

## License

MIT

## Author

[joon](https://github.com/joon) & OpenClaw Agent
