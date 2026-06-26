# Security Policy

## 🔒 Secure by Design

YumFu is designed with security as a priority. This document outlines our security practices and what you can expect.

---

## ✅ Safe Operations

### No Arbitrary Code Execution
- **No `eval()`** - Never used in any script
- **No `exec()` with user input** - Never used
- **No `os.system()`** - Never used  
- **No `subprocess.shell=True`** - Never used

All Python scripts use safe, parameterized APIs.

### Path Validation
- Save files are restricted to `~/clawd/memory/yumfu/saves/{universe}/`
- User IDs and universe names are validated and sanitized
- Path traversal attacks are prevented

### Input Sanitization
- All user inputs (user_id, universe, character names) are validated
- Only alphanumeric characters and safe separators (`-`, `_`) allowed
- No shell metacharacters accepted

### No Shell Injection
- All external commands use argument lists, not string concatenation
- Example: `["uv", "run", "script.py", "--user-id", user_id]` ✅
- NOT: `f"uv run script.py --user-id {user_id}"` ❌

---

## 🔐 Data Safety

### Local-Only Game Data
- **No external API calls** for save/load operations
- All game data stored locally on your machine
- No data sent to third parties

### User Isolation
- Each `user_id` has completely separate save files
- No cross-contamination between users
- Multi-user tested and verified safe

### Automatic Backups
- Old save files preserved in `~/clawd/memory/yumfu/backups/`
- Backups created before overwriting any save
- Recovery possible if something goes wrong

---

## 🔑 API Key Security

### GEMINI_API_KEY (Optional)
- **Read from environment variables only** - Never hardcoded
- **Never written to disk** by YumFu scripts
- **Optional** - Game works in text-only mode without it
- **Your key, your control** - We never see or store it

### Permissions Required
- **File system**: Read/write to `~/clawd/memory/yumfu/` only
- **Process execution**: Run Python scripts via `uv`
- **Optional**: Call Gemini API for image generation (if key provided)

---

## 🛡️ What We DON'T Do

- ❌ Access your network (except Gemini API when explicitly enabled)
- ❌ Read files outside the YumFu workspace
- ❌ Execute arbitrary code from user input
- ❌ Send your game data anywhere
- ❌ Modify system files
- ❌ Install additional software without permission

---

## 📝 Code Transparency

### Open Source
- **License**: GPLv3 - Full source code available
- **GitHub**: https://github.com/yumyumtum/yumfu
- **No obfuscation** - All code is human-readable

### Auditable
- All scripts are Python (easy to review)
- No compiled binaries
- No minified/packed code

---

## 🐛 Reporting Vulnerabilities

Found a security issue? We take security seriously.

**Please report to**:
- **GitHub Issues**: https://github.com/yumyumtum/yumfu/issues (for non-critical bugs)
- **Email**: thriller.yan@gmail.com (for critical vulnerabilities)

**What to include**:
1. Description of the vulnerability
2. Steps to reproduce
3. Potential impact
4. (Optional) Suggested fix

**Response time**: We aim to respond within 48 hours.

---

## 🔄 Security Updates

### Version Policy
- Security fixes are released immediately
- Backward compatibility maintained when possible
- ClawHub auto-update available (`clawhub update yumfu`)

### Changelog
All security-related changes are documented in:
- `CHANGELOG.md`
- GitHub release notes
- ClawHub version descriptions

---

## ✅ Best Practices for Users

### 1. Keep Updated
```bash
clawhub update yumfu
```

### 2. Review Permissions
Check what YumFu can access:
```bash
cat ~/clawd/skills/yumfu/SKILL.md | grep "requires"
```

### 3. Protect Your API Key
```bash
# Good: Environment variable
export GEMINI_API_KEY="your-key-here"

# Bad: Hardcoded in scripts (DON'T DO THIS)
```

### 4. Regular Backups
Your saves are automatically backed up, but you can also manually backup:
```bash
cp -r ~/clawd/memory/yumfu/saves ~/yumfu-backup-$(date +%Y%m%d)
```

---

## 📜 Compliance

### Data Privacy
- **GDPR**: No personal data collected or transmitted
- **Local-first**: All data stays on your machine
- **No telemetry**: No analytics or tracking

### Open Source License
- **GPLv3**: Source code must remain open
- **No proprietary forks**: Derivative works must also be GPLv3
- **Community auditable**: Anyone can review the code

---

## 🎯 Security Mindset

> "Security is not a feature, it's a foundation."

YumFu is built to be:
- **Safe by default** - No dangerous operations enabled
- **Transparent** - Open source, auditable
- **Isolated** - Your game data stays local
- **Minimal permissions** - Only what's needed

---

**Last Updated**: 2026-04-04  
**YumFu Version**: 1.0.0

For questions or concerns, please open a GitHub issue or contact the maintainer.
