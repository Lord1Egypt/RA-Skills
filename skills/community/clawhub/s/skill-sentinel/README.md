# ClawShield

[English](./README.md) | [简体中文](./README.zh-CN.md) | [한국어](./README.ko-KR.md)

> A static security scanner for OpenClaw skills that flags risky shell patterns, suspicious callbacks, and social engineering content before install time.

| Item | Value |
| --- | --- |
| Package | `@mike007jd/openclaw-clawshield` |
| Runtime | Node.js 18+ |
| Interface | CLI + JavaScript module |
| Main command | `scan` |

## Why this exists

Skill marketplaces and internal repositories both create supply-chain risk. ClawShield is designed to make that risk visible early by scanning skill files without execution and returning a risk level that can be enforced in CI or install workflows.

## What it scans for

- Download-and-execute chains such as `curl | sh`
- Obfuscated or dynamic execution patterns like `eval()` and base64 decode flows
- Suspicious outbound callbacks to unknown or disposable endpoints
- Social-engineering instructions that ask users to bypass safety
- Shell wrappers that hide remote execution

## Primary workflow

1. Point ClawShield at a skill directory.
2. Review the risk level and findings.
3. Export JSON or SARIF for automation if needed.
4. Use `--fail-on caution|avoid` to block unsafe changes in CI.

## Quick start

```bash
git clone https://github.com/mike007jd/openclaw-skills.git
cd openclaw-skills/clawshield
npm install
node ./bin/clawshield.js scan ./fixtures/malicious-skill --format table --fail-on caution
```

## Command

| Command | Purpose |
| --- | --- |
| `clawshield scan <skill-path> --format <table|json|sarif> --fail-on <caution|avoid> [--suppressions <path>]` | Scan a skill and optionally fail the run on a chosen risk level |

## Risk model

| Risk level | Meaning |
| --- | --- |
| `Safe` | No flagged findings after suppressions |
| `Caution` | Medium-severity findings need human review |
| `Avoid` | High-severity findings indicate material risk |

## Suppressions

ClawShield supports a `.clawshield-suppressions.json` file with rule IDs, file paths, line numbers, and justification text. Suppressions without justification are ignored.

## Project layout

```text
clawshield/
├── bin/
├── fixtures/
├── src/
├── test.js
└── SKILL.md
```

## Status

The current rule set is intentionally narrow and practical. It focuses on common high-signal patterns that are useful in local review, CI gates, and tools such as Safe Install.
