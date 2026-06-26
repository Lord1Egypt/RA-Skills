# Skill Creator (Opencode)

A modified version of Anthropic's skill-creator that uses Opencode instead of Claude Code CLI.

## What's Different from Original

### 1. CLI Tool Replacement
- **Original**: Uses `claude -p` (Claude Code CLI)
- **This Version**: Uses `opencode run` (Opencode CLI)

### 2. Auto-Detection of Opencode Location
The skill automatically searches for opencode in common locations:
- `~/.opencode/bin/opencode`
- `~/opencode/bin/opencode`
- `/usr/local/bin/opencode`
- `/opt/opencode/bin/opencode`
- Any `opencode` in PATH

You can also set the `OPENCODE_PATH` environment variable:
```bash
export OPENCODE_PATH=/path/to/opencode
```

### 3. Python 3.9 Compatibility
- **Original**: Uses Python 3.10+ syntax (`str | None`, `list[dict]`)
- **This Version**: Compatible with Python 3.9+ using `Optional[str]`, `List[dict]`

### 4. Project Root Detection
- **Original**: Looks for `.claude/` directory
- **This Version**: Looks for `.opencode/` directory

## Requirements

- Python 3.9+
- Opencode CLI installed

## Installation

```bash
clawhub install skill-creator-opencode
```

Or manually:
```bash
cp -r skill-creator-opencode ~/.openclaw/workspace/skills/
```

## Usage

Same as the original skill-creator:

1. Create a new skill draft
2. Write test cases in `evals/evals.json`
3. Run evaluation with `python -m scripts.run_loop ...`
4. Review results and iterate

## Files Modified

| File | Changes |
|------|---------|
| `scripts/improve_description.py` | Replaced `claude -p` with `opencode run`, added `_find_opencode()` |
| `scripts/run_eval.py` | Replaced `claude -p` with `opencode run`, changed `.claude/` to `.opencode/` |
| `scripts/run_loop.py` | Fixed Python 3.9 type annotations |
| `SKILL.md` | Added requirements section and opencode documentation |

## Original Source

This is a fork of Anthropic's official skill-creator:
- Repository: https://github.com/anthropics/skills
- Original skill: `skills/skill-creator`

## License

Same as original: MIT License
