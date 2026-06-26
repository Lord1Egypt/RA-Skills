---
name: yang-openclaw-health
description: Quick health check for OpenClaw installations by Yang. Checks Node.js version, Gateway status, config files, port conflicts, and common problems. Use when troubleshooting OpenClaw installation or configuration issues.
---

# OpenClaw Health Check by Yang

Quick diagnostics for OpenClaw installation issues. Run this to check common problems.

## Installation

```bash
npx clawhub@latest install yang-openclaw-health
```

## What it checks

- ✅ Node.js version (requires 18+)
- ✅ Gateway status (running/stopped)
- ✅ Config file existence
- ✅ Port conflicts (default 3000)
- ✅ Environment variables
- ✅ Permission issues

## Usage

After installation, run:

```bash
node ~/.openclaw/skills/yang-openclaw-health/diagnose.js
```

## Need Help?

If diagnostics show issues you can't fix:
- 📧 **Installation Service**: ¥99-299
- 🔗 **Landing Page**: https://yang1002378395-cmyk.github.io/openclaw-install-service/

## License

MIT
