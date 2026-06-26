---
name: skill-auto-publish
description: Safely publish an already-reviewed skill to ClawHub, verify the live registry state, and return a clear release report.
category: workflow-kits
version: 2.4.0
created: 2026-05-21
owner: choosenobody
status: active
tags: [clawhub, publish, openclaw, skill, automation]
---

# ClawHub Auto Publish

Safely publish an already-reviewed skill to ClawHub, verify the live registry state, and return a clear release report.

## Features

- 🚀 **Safe Publish Flow** — publish only after basic inputs are checked.
- 🔍 **Input Check** — confirm slug, source path, version, changelog, and secrets.
- 🧾 **Registry Verification** — verify the live ClawHub state with `clawhub inspect`.
- 🌐 **Public Page Check** — check the public page when accessible.
- 🛑 **Honest Failure Handling** — report blocked or mismatched verification instead of pretending success.
- 📦 **Release Report** — return version, URL, install command, verification status, issues, and next action.

## When to Use

Use this skill when you want your agent to:

- publish a skill to ClawHub
- update an existing ClawHub skill
- republish after edits
- verify whether a published skill is live and correct

Use this skill to avoid:
- reporting success before checking the live registry
- relying on browser snapshot alone
- accidentally running management commands during a publish task

**Do NOT use this to decide whether a skill deserves release.** Use a release gate or lifecycle review first.

## How It Works

1. Read the user's publish request.
2. Check required inputs: skill slug, source path, target version, changelog, expected content.
3. Confirm the source path contains SKILL.md.
4. Check for secrets or private credentials before publishing.
5. If updating an existing skill, check the current live version first.
6. Publish with the local ClawHub CLI.
7. Verify the live registry state with `clawhub inspect <slug>`.
8. Check the public page text if accessible.
9. Return a release report with verification status, issues, and next action.

Common commands:

```bash
clawhub publish <path> --version <semver> --changelog "<note>"
clawhub inspect <slug>
```

**Note:** Slugs starting with `clawhub-` are protected by ClawHub. Choose a different slug if yours is blocked.
If local CLI syntax differs, inspect local CLI help first.

**Important:**
- Local file edits alone do not mean the skill was published.
- Publish command output alone does not mean the release was verified.
- Browser snapshot alone is not enough for public page verification.
- If the public page is blocked, stale, or mismatched, report that honestly instead of claiming success.

## Copy-Paste Prompt for Your Agent

```
Publish this ClawHub skill safely.

Skill slug:
[slug]

Source path:
[absolute path]

Target version:
[x.y.z]

Changelog:
[one specific release note]

Expected live content:
- [what should appear, change, or be removed on the live page]

Rules:
- Check that the source path contains SKILL.md.
- Check for secrets or private credentials before publishing.
- If updating an existing skill, check current live version first via clawhub inspect <slug>.
- If this is a first publish, confirm no live version exists for this slug.
- Do not publish if slug, source path, version, or changelog is missing.
- If your environment has a known canonical source path for this skill, use that path.
- If release review is required, confirm it is completed before publishing. If not completed, return NEEDS_INFO.
- Publish with the local ClawHub CLI.
- Verify with clawhub inspect <slug> after publishing.
- Check the public page if accessible.
- Do not report PASS from browser snapshot alone.
- If the public page is blocked, stale, or mismatched, report that honestly.
- Do not run rename, merge, delete, hide, or undelete.
```

## Output Format

```
Publish Status: PUBLISHED | FAILED | BLOCKED | NEEDS_INFO
Registry Verification: PASS | FAILED | MISMATCH | NOT_RUN
Public Page Verification: PASS | BLOCKED | MISMATCH | NOT_RUN

Skill:
Source Path:
Previous Version:
Target Version:
URL:
Install Command:
Command Used:
Verified By:
Issues:
Next Action:
```

## What This Will Not Do

It will not:

- decide whether a skill deserves release
- replace release review
- redesign the skill
- publish when required inputs are missing
- claim public verification from browser snapshot alone
- run rename, merge, delete, hide, or undelete
- touch unrelated OpenClaw or Hermes configuration