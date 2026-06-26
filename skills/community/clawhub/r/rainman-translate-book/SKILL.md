---
name: rainman-translate-book
description: "[DEPRECATED] This skill has been renamed to translate-book. Install the new version: clawhub install translate-book"
---

# rainman-translate-book (Deprecated)

This skill has been **renamed and moved** to `translate-book`.

All future development, bug fixes, and new features will be published under the new name. This package will not receive updates.

## Why the rename?

The skill name was simplified from `rainman-translate-book` to `translate-book` to match the SKILL.md `name` field and GitHub repository name, ensuring consistent behavior across Claude Code, Codex, and OpenClaw.

## How to migrate

Uninstall this deprecated version and install the new one:

```bash
clawhub uninstall rainman-translate-book
clawhub install translate-book
```

Or via npx:

```bash
npx skills add deusyu/translate-book -a claude-code -g
```

## New locations

- **ClawHub:** `translate-book`
- **GitHub:** https://github.com/deusyu/translate-book

## What is translate-book?

A Claude Code skill that translates entire books (PDF/DOCX/EPUB) into any language using parallel subagents. Pipeline: Calibre converts input to Markdown chunks, parallel subagents translate each chunk independently, manifest-based SHA-256 validation ensures integrity, then chunks are merged and built into HTML (with TOC), DOCX, EPUB, and PDF outputs.

Do not use this package for new installations. Use `translate-book` instead.
