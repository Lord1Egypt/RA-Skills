# Telegram Footer Patch

![Footer Preview](./assets/footer-preview.jpg)

Patch OpenClaw's Telegram reply pipeline to append a one-line footer in private chats (`🧠 Model + 💭 Think + 📊 Context`).

## What it does
- Adds a one-line footer for Telegram private-chat replies
- Shows model, think level, and context usage in one line
- Supports dry-run preview
- Creates a backup before any file change
- Supports rollback and verification after restart
- Targets current OpenClaw runner bundles and, when needed, the real Telegram delivery path conservatively
- Final success must be confirmed by a real Telegram private-chat reply

## Recommended flow
1. Dry-run
2. Apply
3. Restart the gateway / service with a **true process restart** (**required** to take effect). Do not rely only on hot refresh / SIGUSR1; confirm a new PID if you can.
4. Send a real Telegram private-chat test message and verify the footer in the actual delivered reply

> Smoke test / marker verification only proves the patch hit candidate bundle files. If the real Telegram reply still has no footer, treat it as not fixed yet.

## Validated version boundary
- **Live-validated:** OpenClaw **2026.3.22**
- **Live-validated bundle path (2026.3.22):** `/usr/lib/node_modules/openclaw/dist/agent-runner.runtime-BWpOtdxK.js`
- **Live-validated:** OpenClaw **2026.4.5**
- **Live-validated bundle path (2026.4.5):** `/usr/lib/node_modules/openclaw/dist/agent-runner.runtime-UIIO4kss.js`
- **Live-validated:** OpenClaw **2026.4.12**
- **Live-validated bundle paths (2026.4.12):** `/usr/lib/node_modules/openclaw/dist/agent-runner.runtime-D6-wGQkR.js` and `/usr/lib/node_modules/openclaw/dist/delivery-iF4EZ9PY.js`
- **2026.4.12 lesson:** runner-only patching was not enough; the real Telegram delivery/send path also needed patching before a true restart + real-chat acceptance succeeded
- **Not live-validated:** other OpenClaw versions/builds
- **Claim boundary:** for untested versions, say “may be compatible” / “compatibility logic added”, not “supported”

## Before you run
- This updates OpenClaw frontend bundle files under `.../openclaw/dist/`.
- Run `python3 scripts/patch_reply_footer.py --dry-run` first.
- Confirm backups exist (`*.bak.telegram-footer.*`) and test rollback (`python3 scripts/revert_reply_footer.py --dry-run`).
- Use only on systems you control.

## Key files
- `SKILL.md` — usage guidance
- `scripts/patch_reply_footer.py` — patch script
- `scripts/revert_reply_footer.py` — rollback script
- `CHANGELOG.md` — release notes
- `LICENSE` — MIT license
