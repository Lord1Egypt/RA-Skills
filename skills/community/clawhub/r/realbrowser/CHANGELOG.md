# Changelog

All notable changes to RealBrowser by Ceki will be documented here.

## v0.1.1 — 2026-06-20

Compliance + documentation overhaul. **Recommended over v0.1.0.**

### Changed

- Repositioned skill as **real Chrome sessions for AI agents on sites you have authorization to operate on** (your own QA / monitoring / support / accessibility audits, public data within site Terms of Service)
- Removed pre-warm-for-captcha and CAPTCHA-escalation sections from SKILL.md
- Removed automatic bearer-token validation from `install.sh` — token verification is now a manual, opt-in step the user runs when ready
- Reduced `manifest.json` permissions to the minimum justified surface and added explicit `permissions_justification`
- Added prominent **privacy / consent / use-responsibly** section to SKILL.md and README.md
- Added explicit list of inappropriate use cases (third-party account creation, circumventing access controls, sites whose Terms of Service prohibit automation, anything you wouldn't be allowed to do manually)
- Reduced GitHub topics from anti-bot-leaning to use-case-leaning

### Unchanged

- All CLI command behavior
- Three modes (Self, Marketplace, Earn)
- API endpoints and SDK
- Repository structure

## v0.1.0 — 2026-06-20

Initial public release.

### Features

- Three modes: Self (own Chrome), Marketplace ($0.01/min in USDC), Earn (opt-in, 90% revenue share)
- CLI subcommands: rent, search, snapshot, navigate, click, type, scroll, switch-tab, configure, cdp, wait, chat, profile, upload, request-captcha, sessions, stop
- Python + Node.js SDKs (cli is primary, SDK for callbacks / advanced)
- MCP integration examples for Claude Desktop, Cursor, Cline
- Profile export/import (cookies + storage)
- Chat with the host (for OTP, confirms, support)

### Notes

- Ceki Chrome extension (for Self mode setup): https://browser.ceki.me/install
- Listing on ClawHub: https://clawhub.ai/skills/realbrowser
- Source: https://github.com/Ceki-me/realbrowser-skill
- Mirror: https://codeberg.org/cekibrowser/realbrowser-skill
