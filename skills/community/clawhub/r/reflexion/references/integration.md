# Integration Guide

Setup reflexion for different AI coding agents.

## Claude Code

### Project-level (recommended)

Add to `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "./.claude/skills/reflexion/scripts/capture.sh"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "./.claude/skills/reflexion/scripts/recall.sh"
          }
        ]
      }
    ]
  }
}
```

### Global (all projects)

Add to `~/.claude/settings.json` with absolute paths:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/skills/reflexion/scripts/capture.sh"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/skills/reflexion/scripts/recall.sh"
          }
        ]
      }
    ]
  }
}
```

## Codex CLI

Same hook format. Add to `.codex/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "./.codex/skills/reflexion/scripts/capture.sh"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "./.codex/skills/reflexion/scripts/recall.sh"
          }
        ]
      }
    ]
  }
}
```

## GitHub Copilot

Copilot doesn't support hooks. Add to `.github/copilot-instructions.md`:

```markdown
## Reflexion: Cross-Session Learning

This project uses reflexion for persistent learning across sessions.

Learning data is stored in `.reflexion/entries/` as JSON files.

Before starting tasks:
1. Check `.reflexion/entries/` for relevant past learnings
2. Search by keyword: `grep -l "keyword" .reflexion/entries/*.json`

After resolving non-obvious issues:
1. Create an entry in `.reflexion/entries/RFX-YYYYMMDD-XXX.json`
2. Run `./scripts/rebuild-index.sh` to update the keyword index

Entry format:
```json
{
  "id": "RFX-YYYYMMDD-XXX",
  "type": "error|correction|insight|pattern",
  "trigger": "what happened",
  "context": "what was attempted",
  "resolution": "what fixed it",
  "keywords": ["keyword1", "keyword2"],
  "occurrences": 1,
  "first_seen": "YYYY-MM-DD",
  "last_seen": "YYYY-MM-DD",
  "promoted": false
}
```
```

## OpenClaw

Copy to workspace:

```bash
cp -r reflexion ~/.openclaw/skills/reflexion
```

Promotion targets for OpenClaw:
- Behavioral patterns -> `SOUL.md`
- Tool gotchas -> `TOOLS.md`
- Workflow improvements -> `AGENTS.md`
- Project facts -> `CLAUDE.md`

## Verification

### Test capture hook

```bash
# Simulate a Bash tool error
echo '{"tool_name":"Bash","tool_input":{"command":"npm run build"},"tool_output":"npm ERR! Missing script: build"}' | bash scripts/capture.sh
```

Expected: creates a `.reflexion/entries/RFX-*.json` file and outputs `<reflexion-captured>`.

### Test recall hook

```bash
# Simulate a user prompt about npm/build
echo '{"prompt":"help me build this project with npm"}' | bash scripts/recall.sh
```

Expected: if matching entries exist, outputs `<reflexion-recall>` with past learnings. If none, outputs nothing.

### Test promotion

```bash
# Run promotion check
bash scripts/promote.sh
```

Expected: promotes entries with 3+ occurrences to CLAUDE.md.

### Status dashboard

```bash
bash scripts/status.sh
```

## Troubleshooting

### Scripts not executable

```bash
chmod +x scripts/*.sh
```

### No entries being captured

1. Check the hook is configured in settings.json
2. Verify the script path is correct (absolute or relative to project root)
3. Test manually with the verification commands above
4. Check if stdin is being passed (hooks need stdin JSON)

### Recall not finding matches

1. Run `bash scripts/rebuild-index.sh` to regenerate the keyword index
2. Check that entries have keywords: `cat .reflexion/entries/RFX-*.json | grep keywords`
3. Verify the index isn't empty: `cat .reflexion/index.txt`

### Promotion not working

1. Check entries have `occurrences >= 3` and a non-empty `resolution`
2. Ensure `python3` is available
3. Run `bash scripts/promote.sh` manually to see output
