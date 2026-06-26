# YumFu v1.0.2 - Privacy & Security Release 🔒

## 🎯 Overview

This release addresses ClawHub security scanner feedback and privacy concerns with comprehensive documentation and user controls.

## 🔒 Privacy Improvements

### New: PRIVACY.md
Complete privacy policy documenting:
- What data is stored (saves, logs, images)
- Where data is stored (exact file paths)
- Optional vs mandatory features
- External API calls (Gemini only)
- Privacy levels (max privacy / balanced / full)
- Data cleanup instructions
- Audit yourself checklist

### New: Session Logging Controls
- **Optional logging**: Set `YUMFU_NO_LOGGING=1` to disable
- Session logger respects privacy flag
- All log methods become no-ops when disabled
- No directories created if logging disabled
- Privacy notice in docstrings

### GEMINI_API_KEY Now Optional
- Removed from `requires.env` metadata
- Removed `primaryEnv` declaration
- Documented as optional in all files
- Text-only mode: `YUMFU_NO_IMAGES=1`
- Consistent messaging everywhere

## 🛡️ Security Improvements (v1.0.1)

### New: SECURITY.md
Comprehensive security policy:
- No eval/exec/os.system usage
- Path validation & sanitization
- Input validation
- No shell injection
- API key security
- Vulnerability reporting

### New: SECURITY_ANALYSIS.md
Technical security review:
- Identified concerns
- Recommended improvements
- Implementation checklist
- Risk assessment

### Updated: SKILL.md Code Examples
- Removed dangerous `exec("string")` patterns
- Safe `exec({command})` patterns
- Stdin-based JSON passing
- Security comments added

## 📦 Privacy Levels

Users can now choose their comfort level:

### 🔒 Maximum Privacy (No external calls)
```bash
export YUMFU_NO_IMAGES=1
export YUMFU_NO_LOGGING=1
unset GEMINI_API_KEY
```
- Text-only gameplay
- Local saves only
- No conversation logs
- Zero network calls

### 🎨 Balanced (Images, no logging)
```bash
export GEMINI_API_KEY="your-key"
export YUMFU_NO_LOGGING=1
```
- AI-generated images
- Local saves only
- No conversation logs
- Gemini API only

### 📚 Full Features (Images + storybooks)
```bash
export GEMINI_API_KEY="your-key"
# YUMFU_NO_LOGGING not set
```
- AI-generated images
- Storybook PDFs
- Full session logs
- Gemini API only

## 📊 Data Transparency

### What YumFu Stores
- **Game Saves** (ALWAYS): `~/clawd/memory/yumfu/saves/`
- **Backups** (ALWAYS): `~/clawd/memory/yumfu/backups/`
- **AI Images** (if GEMINI_API_KEY): `~/.openclaw/media/outbound/yumfu/`
- **Session Logs** (if not disabled): `~/clawd/memory/yumfu/sessions/`

### What YumFu Sends
- **Google Gemini API** (OPTIONAL): Scene descriptions only
- **Nothing else**: No telemetry, no tracking, no third parties

## 🔄 Migration Guide

### From v1.0.0 or v1.0.1
No breaking changes! Safe drop-in upgrade:

```bash
# Via ClawHub
clawhub update yumfu

# Via Git
cd ~/clawd/skills/yumfu
git pull origin main
```

### Enable Max Privacy
```bash
export YUMFU_NO_LOGGING=1
export YUMFU_NO_IMAGES=1
```

### Review Your Data
```bash
# See what's stored
ls -lh ~/clawd/memory/yumfu/saves/
ls -lh ~/.openclaw/media/outbound/yumfu/

# Read privacy policy
cat ~/clawd/skills/yumfu/PRIVACY.md

# Read security policy
cat ~/clawd/skills/yumfu/SECURITY.md
```

## 📝 Files Changed

### Added
- `PRIVACY.md` - Privacy policy (5917 bytes)
- `SECURITY.md` - Security policy (4767 bytes)
- `SECURITY_ANALYSIS.md` - Technical review (5643 bytes)

### Modified
- `scripts/session_logger.py` - Privacy controls
- `SKILL.md` - Privacy section, safe code examples
- `README.md` - Privacy badge, quick summary

## ✅ Verified Safe

- ✅ No eval() usage
- ✅ No exec() with user input
- ✅ No os.system()
- ✅ No subprocess.shell=True
- ✅ Path validation everywhere
- ✅ Input sanitization
- ✅ Local-first architecture
- ✅ Open source (GPLv3)

## 🎉 Credits

Thank you to the ClawHub security scanner and reviewers for the detailed feedback!

## 📚 Resources

- **GitHub**: https://github.com/yumyumtum/yumfu
- **ClawHub**: https://clawhub.ai/skills/yumfu
- **Privacy Policy**: [PRIVACY.md](PRIVACY.md)
- **Security Policy**: [SECURITY.md](SECURITY.md)

---

**Questions?** Open a GitHub issue or contact thriller.yan@gmail.com
