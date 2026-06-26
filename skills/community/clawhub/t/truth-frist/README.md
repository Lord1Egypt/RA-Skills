# Truth-First

Evidence-first verification for status, config, file contents, actions, connectivity, mounts, and model selection.

## What It Does

**Truth-First** forces the AI to verify claims before answering. Instead of relying on memory or assumptions, it:

1. Lists all claims that need verification
2. Gathers evidence using tools (read, status, grep, logs)
3. Classifies each claim as `Verified`, `Inferred`, or `Unknown`
4. Provides next-step commands for any `Unknown`
5. Cites evidence with paths, line numbers, or command outputs

## Installation

### Option 1: Manual Install

```bash
cd ~/.openclaw/skills
git clone <repo-url> truth-first
```

### Option 2: Via OpenClaw CLI

```bash
openclaw skill install <repo-url>
```

## Usage

The skill is automatically triggered for verification tasks. No manual activation needed.

### Example Prompts

- "Check if the gateway is running properly"
- "Verify my config has the correct model settings"
- "Is the backup file intact?"
- "Can you confirm the service restarted?"

## Response Framework

When Truth-First is active, responses follow this structure:

```
## Claims to Verify
- [ ] Claim 1: ...
- [ ] Claim 2: ...

## Evidence
### Claim 1: Verified ✅
- Source: /path/to/file
- Line 42: `model: kimi-k2.5`

### Claim 2: Unknown ❓
- No direct evidence found
- Next step: `rg -n "setting" ~/.openclaw/openclaw.json`
```

## Files

- `SKILL.md` - Core skill definition
- `agents/openai.yaml` - Agent profile for OpenAI-compatible models
- `references/patterns.md` - Reusable templates and evidence commands

## Requirements

- OpenClaw 2026.2.22 or later
- `ripgrep` (rg) for fast searches
- Standard shell tools (ls, stat, cat)

## License

MIT