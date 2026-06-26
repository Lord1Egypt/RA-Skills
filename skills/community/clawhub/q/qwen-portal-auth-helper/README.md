# Qwen Portal Auth Helper

> **Battle-tested solution for qwen-portal OAuth automation**  
> Solves the "interactive TTY required" problem, prevents cron task failures, and provides full monitoring.

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue.svg)](https://clawhub.com/skills/qwen-portal-auth-helper)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](./package.json)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Based on](https://img.shields.io/badge/based%20on-2026--03--09%20experience-orange.svg)](./SKILL.md)

## 🚨 The Problem

qwen-portal provides free models (2,000 requests/day) but **OAuth expires every 1-2 weeks**. When it expires:

1. Cron tasks fail with: `Qwen OAuth refresh token expired or invalid`
2. `openclaw models auth login --provider qwen-portal` fails: `requires an interactive TTY`
3. Manual intervention required, breaking automation
4. Tasks remain in error state even after authentication fix

## 💡 The Solution

This skill provides a complete solution:

- **Automated OAuth link extraction** using tmux (bypasses TTY requirement)
- **Health monitoring** for qwen-portal tasks
- **Self-healing scripts** to fix task states
- **Documented best practices** from real-world experience

## 🚀 Quick Start

### Installation
```bash
# Install from ClawHub
clawhub install qwen-portal-auth-helper

# Or clone manually
cd ~/.openclaw/skills/
git clone https://github.com/jazzqi/qwen-portal-auth-helper.git
```

### Get OAuth Link (when authentication expired)
```bash
cd ~/.openclaw/skills/qwen-portal-auth-helper
./scripts/get-qwen-oauth-link.sh
```
**Output**:
```
🔗 OAuth Link: https://chat.qwen.ai/authorize?user_code=M17WU0SC
📱 Device Code: M17WU0SC
```

### Check Authentication Health
```bash
./scripts/check-qwen-auth.sh
```

### Setup Weekly Monitoring
```bash
# Add to crontab (runs every Monday at 9 AM)
0 9 * * 1 ~/.openclaw/skills/qwen-portal-auth-helper/scripts/check-qwen-auth.sh
```

## 🔧 Features

### 1. OAuth Link Automation
```bash
# Traditional way (fails in automation):
openclaw models auth login --provider qwen-portal  # ❌ Error: requires interactive TTY

# Our solution:
./scripts/get-qwen-oauth-link.sh  # ✅ Works in cron, AI assistants, etc.
```

**How it works**: Uses tmux to create virtual terminal, captures output before command hangs.

### 2. Health Monitoring
- Scans all cron tasks using qwen-portal models
- Detects error states and consecutive failures
- Generates detailed reports with actionable advice
- Early warning before complete failure

### 3. Recovery Tools
- Resets task error states after authentication fix
- Provides step-by-step recovery checklist
- Validates fixes actually work

## 📋 Complete Workflow

### When tasks start failing:
```
1. Run: check-qwen-auth.sh
   → Identifies failing tasks, shows error details

2. Run: get-qwen-oauth-link.sh  
   → Provides OAuth link and device code

3. User: Click link, authenticate in browser
   → Authorization completes automatically

4. Test: openclaw cron run <task-id>
   → Verifies authentication works

5. Reset: Scripts help reset task state
   → Tasks return to normal operation
```

## 📊 Based on Real Experience

This skill was developed from solving actual production issues on **2026-03-09**:

- Two critical news collection tasks failing
- 9-10 consecutive errors before detection
- Multiple failed attempts before finding tmux solution
- Complete documentation in `.learnings/` system

## 🏗️ Project Structure

```
qwen-portal-auth-helper/
├── SKILL.md              # Complete documentation
├── README.md             # This file
├── package.json          # Package information
├── index.js             # Node.js API
├── _meta.json           # Skill metadata
├── .clawhub/config.json # ClawHub configuration
├── scripts/             # Core automation scripts
│   ├── get-qwen-oauth-link.sh
│   ├── check-qwen-auth.sh
│   └── reset-task-state.py
├── examples/            # Usage examples
│   └── quick-recovery.md
├── docs/                # Detailed documentation
└── PUBLISH_GUIDE.md     # Publishing instructions
```

## 🔗 Links

- **ClawHub**: https://clawhub.com/skills/qwen-portal-auth-helper
- **GitHub**: https://github.com/jazzqi/qwen-portal-auth-helper
- **Documentation**: [SKILL.md](./SKILL.md)
- **Quick Recovery**: [examples/quick-recovery.md](./examples/quick-recovery.md)

## 🤝 Contributing

Found a better way? Have another OAuth provider with similar issues?

1. Fork the repository
2. Add your improvements  
3. Submit pull request
4. Help others avoid the same pitfalls

## 📄 License

MIT License - see [LICENSE](./LICENSE) file for details.

## 🙏 Acknowledgments

- Based on real-world experience from 2026-03-09
- OpenClaw community for the platform
- All users who contributed feedback and testing

---

**Remember**: qwen-portal OAuth expires every 1-2 weeks.  
**Solution**: Weekly monitoring + this skill = no more surprises.

*Skill version: 1.0.0 | Based on 2026-03-09 battle-tested experience*