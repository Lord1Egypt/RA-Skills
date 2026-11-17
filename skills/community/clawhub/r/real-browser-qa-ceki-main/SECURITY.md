# Security Policy

## Reporting a vulnerability

If you find a security issue in this skill (the SKILL.md instructions, the install.sh script, or the manifest) please report it privately.

**Do not open a public GitHub issue.**

Contact: open a private security advisory at [github.com/Ceki-me/real-browser-qa-ceki/security/advisories/new](https://github.com/Ceki-me/real-browser-qa-ceki/security/advisories/new) or email `security@ceki.me`.

Expected acknowledgment: within 3 business days.
Expected fix or status update: within 14 days for high-severity findings.

## Scope

This repository contains:

- The skill's `SKILL.md` instructions for AI agents
- The `install.sh` setup script
- The `manifest.json` ClawHub metadata
- Integration examples for popular MCP hosts

**Out of scope:**
- The `ceki-sdk` CLI / Python SDK ([separate repo](https://pypi.org/project/ceki-sdk/) — report there)
- The Ceki backend API (closed source, report to `security@ceki.me`)
- The Ceki Chrome extension ([separate distribution](https://browser.ceki.me/install) — report to `security@ceki.me`)
- The ClawHub registry itself (report to ClawHub security)

## What we consider a vulnerability here

- The install.sh transmits unexpected data, persists unexpected state, or escalates privileges beyond what's declared in `manifest.json`
- SKILL.md instructions lead an AI agent to violate user privacy or intended scope
- A malicious `manifest.json` entry or example config can leak the user's API key
- A supply-chain risk via the `ceki-sdk` dependency declaration

## What we don't consider in scope

- General critiques of marketplace mechanics, pricing, or licensing — open a discussion instead
- Anti-bot regressions on third-party sites — see SKILL.md "When NOT to use"
