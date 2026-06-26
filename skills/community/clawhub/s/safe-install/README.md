# Safe Install

[English](./README.md) | [简体中文](./README.zh-CN.md) | [한국어](./README.ko-KR.md)

> A guarded installer for OpenClaw skills that scans content before activation and keeps rollback-ready snapshots.

| Item | Value |
| --- | --- |
| Package | `@mike007jd/openclaw-safe-install` |
| Runtime | Node.js 18+ |
| Interface | CLI + JavaScript module |
| Main commands | install, `history`, `rollback`, `policy validate` |

## Why this exists

Installing a skill is not just a file copy. It is a trust decision. Safe Install adds a review gate in front of that decision by validating policy, scanning the source with ClawShield, recording an installation fingerprint, and preserving a rollback target.

## What it does

- Resolves a local skill path or mapped registry entry from policy
- Validates installation policy before work begins
- Scans the candidate skill with ClawShield
- Blocks or allows installation based on policy and risk level
- Stores snapshots, active state, and history under `.openclaw-tools/safe-install`
- Rolls a skill back to the previous installed snapshot

## Primary workflow

1. Define a policy file for allowed sources and blocking rules.
2. Run Safe Install against a local path or named skill.
3. Review history and active state after installation.
4. Use rollback if a new version needs to be reverted.

## Quick start

Safe Install depends on ClawShield. In the private IndieSite workspace, that dependency is linked by npm workspaces already.

```bash
cd skills/openclaw/safe-install
node ./bin/safe-install.js ./fixtures/safe-skill --yes --format json
node ./bin/safe-install.js history --format table
```

## Commands

| Command | Purpose |
| --- | --- |
| `safe-install <skill[@version]|local-path>` | Scan and install a skill under the current policy |
| `safe-install history` | Show installation and block history |
| `safe-install rollback <skill>` | Restore the previous installed snapshot |
| `safe-install policy validate --file <path>` | Validate a policy JSON file |

## Policy model

Safe Install merges your config with these defaults:

```json
{
  "defaultAction": "prompt",
  "blockedPatterns": [],
  "allowedSources": [],
  "forceRequiredForAvoid": true
}
```

## What gets stored

- `snapshots/<skill>/<version>/<hash>` for rollback-ready copies
- `active/<skill>` for the current active version
- `history.json` for install and block records
- `state.json` for the current active map

## Project layout

```text
safe-install/
├── bin/
├── fixtures/
├── src/
├── test.js
└── SKILL.md
```

## Status

The current implementation focuses on local-path installs, policy validation, scan-driven decisions, history tracking, and rollback. It is designed as a safer control layer, not a full remote registry client.
