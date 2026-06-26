# Security Transparency — venice-ai skill

## Overview

This skill provides CLI access to the official **Venice AI API** (https://venice.ai). It contains no obfuscated code, no telemetry, and no external dependencies beyond Python's standard library.

---

## Network Access

| Endpoint | Purpose |
|----------|---------|
| `api.venice.ai` | Official Venice AI API — all inference requests |
| **User-supplied URLs** | Fetch images/videos/audio when user provides a URL argument |

### URL Fetching Behavior

Several commands accept URLs as input (e.g., `--url`, `--image`, `--video`). When a URL is provided:
- The script fetches the content from that URL
- The fetched content is then sent to Venice API for processing

**This means:**
- ✅ API requests only go to `api.venice.ai`
- ⚠️ **User-supplied URLs are fetched** — don't pass internal/sensitive URLs
- ⚠️ Avoid passing URLs to internal hosts (e.g., `169.254.x.x`, `localhost`, internal hostnames)
- ⚠️ The skill will attempt to fetch whatever URL you give it

**The skill does NOT:**
- Phone home to any server besides those listed above
- Send telemetry or analytics
- Fetch URLs on its own — only when explicitly provided by the user
- Connect to any service without user instruction

---

## File System Access

| Path | Access | Purpose |
|------|--------|---------|
| `~/.clawdbot/clawdbot.json` | Read-only | Retrieve `VENICE_API_KEY` if not in environment |
| User-specified input paths | Read-only | Load user-specified files for upload |
| User-specified output paths | Write | Save generated images/videos/audio |

**Scope:**
- Only reads files explicitly passed as arguments
- Only writes to paths explicitly specified with `--output`
- No automatic file discovery or scanning

---

## Code Safety

✅ **No dangerous patterns:**
- No `eval()` or `exec()`
- No `subprocess` or `os.system()`
- No dynamic code execution
- No shell command injection vectors

✅ **Standard library only:**
- `urllib.request` / `urllib.error` — HTTP requests
- `json` — API payloads
- `argparse` — CLI argument parsing
- `base64` — Image/audio encoding
- `pathlib` / `os` — File path handling

---

## API Key Handling

- API key read from `VENICE_API_KEY` environment variable (preferred)
- Fallback: read from `~/.clawdbot/clawdbot.json` config
- Key is sent only to `api.venice.ai` in the `Authorization` header
- Key is never logged, printed, or transmitted elsewhere

---

## What This Skill Does

| Script | Function |
|--------|----------|
| `venice.py` | Text generation, vision/image analysis, model listing, embeddings, TTS, transcription |
| `venice-image.py` | Image generation, background removal |
| `venice-video.py` | Video generation (WAN, Sora, Runway) |
| `venice-upscale.py` | Image upscaling |
| `venice-edit.py` | AI image editing, multi-edit |
| `venice-music.py` | Music/audio generation |

All scripts are thin wrappers around Venice's documented REST API.

---

## SSRF Considerations

Since the skill fetches user-supplied URLs, operators running this in a shared/multi-tenant environment should:
- Run in a sandboxed environment or container
- Use network policies to restrict outbound access if needed
- Educate users not to pass internal URLs

For single-user setups (like personal OpenClaw instances), this is typically not a concern since you control what URLs you pass.

---

## Source Verification

All code is open and readable:
- Review scripts in `./scripts/`
- Compare against Venice API docs: https://docs.venice.ai
- No minified, obfuscated, or compiled code

---

## Author

- **GitHub:** [@jonisjongithub](https://github.com/jonisjongithub)
- **Skill homepage:** https://clawhub.ai/jonisjongithub/venice-ai

---

## Reporting Issues

If you find a security issue with this skill:
1. Open an issue on the GitHub repo (if available)
2. Contact the author via ClawHub
3. Report via OpenClaw Discord

---

*Last updated: 2026-04-06*
