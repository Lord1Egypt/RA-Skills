# skill-subtraction

> The core of AI skill management is "lean and focused," not "more is better."

A systematic audit tool for installed AI skills, practicing the philosophy of **regular subtraction**. Scans all installed skills, evaluates their value by category, and generates structured keep / archive / uninstall recommendations to help users maintain a lean and efficient skill set.

Inspired by Swyx (Latent Space host / smol.ai founder) on AI skill management — most people habitually keep adding skills, installing every new one they see, ending up with dozens but rarely using most of them.

## Why Subtraction?

| Problem | Description |
|---------|-------------|
| **Cognitive overload** | More skills = higher selection cost, defeating the purpose of efficiency |
| **Judgment interference** | Outdated skills act as noise, clouding decisions when facing new problems |
| **High maintenance cost** | Skills need updates and debugging; too many means wasted effort |

## Features

- **Auto-scan**: One-click scan of all installed skills under the current Agent platform. The script auto-detects its host platform via its own path — placed under `~/.workbuddy/skills/` it scans WorkBuddy, under `~/.codex/skills/` it scans Codex, and so on; also scans the current workspace's `.workbuddy/skills/` for project-level skills
- **Bilingual output**: Supports both Chinese and English reports via `--lang zh` (default) or `--lang en` flag; stderr messages, issue descriptions, and audit report templates are fully localized
- **Multi-platform**: Not just WorkBuddy — compatible with Codex, Claude Code, Cursor, Cline, Continue, LobsterAI, and any AI assistant platform that follows the `~/.<agent>/skills/` directory convention; use `--all` to scan all installed platforms at once
- **Categorized evaluation**: Classifies skills into Tool / Business / News / Productivity types, scoring across 6 metrics (usage frequency, necessity, current relevance, enabled status, maintenance status, unique value)
- **Smart recommendations**: Auto-generates keep / archive / uninstall suggestions with special rules for deduplication, disabled-skill detection, and project-end detection
- **Safe cleanup**: Archive operations save skill configurations first; uninstall only executes after user confirmation — never deletes without consent

## Directory Structure

```
skill-subtraction/
├── SKILL.md                          # Main skill definition (workflow + trigger rules)
├── LICENSE                           # MIT License
├── README.md                         # Chinese README
├── README_en.md                      # English README (this file)
├── .gitignore
├── scripts/
│   └── audit_skills.py               # Skill scanning script, outputs structured JSON
└── references/
    └── evaluation_framework.md       # Full evaluation framework (categories, scoring matrix, dedup rules)
```

## Installation

### Option 1: Manual Install

```bash
# Clone the repository
git clone https://github.com/helloyxs/skill-subtraction.git

# Copy to your AI assistant platform's skills directory
# WorkBuddy
cp -r skill-subtraction ~/.workbuddy/skills/
# Codex
cp -r skill-subtraction ~/.codex/skills/
# Claude Code
cp -r skill-subtraction ~/.claude/skills/
# Cursor / Cline / Continue etc. — same pattern
```

### Option 2: Direct Download

Download the ZIP, extract it, and place the `skill-subtraction` folder under your platform's skills directory (e.g., `~/.workbuddy/skills/`, `~/.codex/skills/`, etc.).

## Usage

In your AI assistant platform's conversation, simply say:

- "Check what skills I have installed"
- "Do a skill subtraction"
- "Which skills should I delete"
- "Audit my skills"

The skill auto-triggers and executes a 5-step workflow:

1. **Scan** — Run `audit_skills.py` to collect metadata for all installed skills (includes batch install detection and source stats). Supports `--lang en` for English output.
2. **Classify** — Categorize into 6 functional domains (Dev & Engineering / Data & Connectors / Content & Media / Domain Business / Productivity & Workflow / Meta & Agent Control) plus subcategories; identify install source (user / platform / agent-created)
3. **Evaluate** — Score across 6 weighted metrics, composite score ranges 24-100
4. **Recommend** — Generate keep / archive / uninstall report (Chinese or English, based on `--lang` or user language)
5. **Cleanup** — Execute after user confirmation (archive saves config first)

### Run the Scan Script Directly

```bash
# Scan user-level skills (Chinese output, default)
python3 scripts/audit_skills.py

# English output
python3 scripts/audit_skills.py --lang en

# Specify a custom skills directory (e.g., Windows LobsterAI non-standard path)
python3 scripts/audit_skills.py --skills-dir "C:\Users\admin\AppData\Roaming\LobsterAI\SKILLs"

# Scan all installed agent platforms
python3 scripts/audit_skills.py --all

# Scan project-level skills with a specific workspace
python3 scripts/audit_skills.py --workspace /path/to/workspace
```

Example JSON output:

```json
{
  "audit_time": "2026-08-12 10:30:00",
  "total_skills": 7,
  "user_skills": 7,
  "project_skills": 0,
  "skills": [
    {
      "name": "skill-subtraction",
      "scope": "user",
      "path": "~/.workbuddy/skills/skill-subtraction",
      "description": "Skill subtraction — audit and cleanup of installed skills...",
      "agent_created": true,
      "file_count": 4,
      "dir_size_kb": 12.5,
      "last_modified": "2026-08-12 10:30:00"
    }
  ]
}
```

## Evaluation Framework

### Scoring Matrix

| Composite Score | Recommendation | Description |
|----------------|----------------|-------------|
| 80-100 | Keep | High-value skill, master it deeply |
| 50-79 | Archive | Uncertain value, save config then uninstall, re-activate when needed |
| 24-49 | Uninstall | Low value, clean up directly |

### Special Rules (Override Scoring)

1. **Zero usage + irrelevant → Uninstall directly**
2. **Complete overlap → Keep the best one** (deduplication)
3. **Disabled + never manually invoked → Uninstall**
4. **Project-level + project ended → Uninstall**
5. **Data source defunct → Uninstall**

See [`references/evaluation_framework.md`](references/evaluation_framework.md) for the full framework.

## Audit Cycle Recommendations

| Frequency | Scenario |
|-----------|----------|
| Quarterly | When skill count exceeds 10 |
| After each project ends | Clean up project-level skills |
| When business direction shifts | Re-evaluate business-type skills |
| When feeling "too many skills" | Anytime |

## Requirements

- Python 3.10+
- WorkBuddy, Codex, Claude Code, Cursor, Cline, Continue, LobsterAI, or any compatible AI assistant platform (anything following the `~/.<agent>/skills/` directory convention)

## License

[MIT](LICENSE)
