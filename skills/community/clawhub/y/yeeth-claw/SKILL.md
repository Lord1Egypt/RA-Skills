---
name: yeeth-claw
version: 1.0.0
description: |
  Supply chain security hooks for Claude Code. Intercepts npm, pip, yarn,
  pnpm, and cargo install commands before execution and checks each package
  for supply chain risk signals: package age (new packages flagged/blocked),
  typosquat detection via Levenshtein distance against ~100 high-value targets
  per ecosystem, and install script presence. Optionally submits blocked
  packages to the Argus API for full static analysis.
hooks:
  - type: PreToolUse
    matcher: Bash
    command: "python3 ~/.claude/hooks/openclaw/hook.py"
---

# yeeth-claw

Claude Code hooks for supply chain security. Intercepts package installation
commands and flags suspicious packages before Claude executes them.

## Hooks

### OpenClaw

PreToolUse hook that watches `npm install`, `pip install`, `yarn add`,
`pnpm add`, and `cargo add` commands. For each package it checks:

1. **Package age** — packages published < 30 days ago are flagged; < 7 days triggers a block
2. **Typosquat detection** — Levenshtein distance against ~100 high-value targets per ecosystem (npm, PyPI, crates.io)
3. **Install scripts** — postinstall hooks on flagged packages are noted as an additional risk signal

**Risk tiers:**

| Tier | Condition | Exit code |
|---|---|---|
| WARN | Age < 30d or typosquat score ≥ 0.65 | 1 (non-blocking) |
| BLOCK | Age < 7d and typosquat hit, or score ≥ 0.85 | 2 (blocks install) |
| ARGUS | Any BLOCK + Argus API configured | 2 + submits for full analysis |

## Installation

```bash
git clone https://github.com/yeeth-security/yeeth-claw.git
cd yeeth-claw/hooks/openclaw
bash install.sh
```

The install script copies the hook to `~/.claude/hooks/openclaw/` and merges
the Claude Code settings if `jq` is available.

**Restart Claude Code after installation** for the hook to take effect.

## Argus Integration

To enable full package analysis via the Argus API:

```bash
export OPENCLAW_ARGUS_URL=https://app.yeethsecurity.com
export OPENCLAW_ARGUS_KEY=<your-api-key>
```

When both are set, any BLOCK-tier package is submitted to Argus for full
static analysis and the job URL is included in the block message.

## Requirements

- Python 3.8+
- No third-party dependencies (stdlib only)

## Claude Code settings snippet

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/openclaw/hook.py"
          }
        ]
      }
    ]
  }
}
```
