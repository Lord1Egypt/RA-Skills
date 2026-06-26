---
name: skill-dep-fixer
description: Generate a Node.js CLI tool that scans OpenClaw skill SKILL.md files and auto-fixes missing dependencies (npm, pip, brew, system binaries). Trigger phrases: "fix skill dependencies", "skill-dep-fixer", "check skill dependencies", "skills are broken", "openclaw doctor".
homepage: https://github.com/christianteohx/skill-dep-fixer
user-invocable: true
metadata:
  {
    "openclaw":
      {
        "emoji": "🔧",
        "requires": { "bins": ["node"] }
      }
  }
---

# skill-dep-fixer Skill

Generate a Node.js CLI tool that scans installed OpenClaw skills, detects missing dependencies, and optionally auto-fixes them.

## When to invoke

Trigger when the user says or asks for:
- "fix skill dependencies"
- "skill-dep-fixer"
- "check skill dependencies"
- "skills are broken"
- "openclaw doctor"
- "skill has missing deps"

## Instructions

When triggered, generate a complete Node.js CLI project that:

### Core requirements
- Node.js 18+
- No external runtime dependencies where possible
- One-file entry point with optional src/ submodules
- CLI argument parsing (manual or minimist-light)
- Colored terminal output with ANSI codes or chalk

### Commands to implement

```
skill-dep-fixer --dry-run     scan and report (no changes)
skill-dep-fixer --fix        install missing dependencies
skill-dep-fixer --skill name check a specific skill
skill-dep-fixer --json       JSON output
skill-dep-fixer --report     Discord-formatted compact report
skill-dep-fixer --help       show usage
```

### What to scan

Parse SKILL.md frontmatter from skills in:
- ~/.openclaw/skills/*/SKILL.md
- ~/.openclaw/workspace/skills/*/SKILL.md

Look for the metadata.openclaw.install array.

Example frontmatter:

```
metadata:
  openclaw:
    install:
      - id: gh
        kind: brew
        formula: gh
        bins: [gh]
        label: "Install GitHub CLI"
```

### Detection and fix logic

brew   : detect with brew list, fix with brew install
npm    : detect with npm list -g, fix with npm install -g
pip    : detect with pip show, fix with pip install
bins   : detect with which, not auto-fixable (report only)

### Output format

Text report (default):
- Header: "Skill Dependency Report"
- One line per skill: [icon] [name] [status] missing: [list]
- Status icons: ok, fixed, failed, mismatch
- Summary line at bottom

Discord report (--report): compact single-line per skill in a code block.

Exit codes: 0 = all fixed/satisfied, 1 = some failed.

## Keeping packages updated

When using any skill that wraps a Homebrew/package tool:

1. **Check if the skill has a newer version**: run `clawhub inspect <skill-name>` and compare version
2. **If ClawHub skill is newer**: run `clawhub update <skill-name>` to pull new SKILL.md
3. **If the underlying package has a newer version**: update it too:
   - Homebrew: `brew upgrade <tap>/<package>` (e.g., `brew upgrade christianteohx/tap/calctl`)
   - npm: `npm update -g <package>`
   - pip: `pip install --upgrade <package>`
4. **When publishing a skill update**: update both SKILL.md AND the underlying package in the right order:
   - First: update GitHub repo and create new release
   - Second: update Homebrew formula / package registry
   - Third: publish updated SKILL.md to ClawHub

This ensures agents using the skill always get the latest tool with matching documentation.

## Output

After generating, tell the user:

Homebrew (recommended):
```
brew install christianteohx/tap/skill-dep-fixer
```

Direct binary:
```
curl -fsSL https://github.com/christianteohx/skill-dep-fixer/releases/latest/download/skill-dep-fixer -o ~/bin/skill-dep-fixer
chmod +x ~/bin/skill-dep-fixer
```

npm:
```
npm install -g skill-dep-fixer
```

Build from source:
```
git clone https://github.com/christianteohx/skill-dep-fixer
cd skill-dep-fixer
npm install
node skill-dep-fixer.js --help
```
