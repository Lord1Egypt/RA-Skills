---
name: skill-chain
description: Supply chain intelligence for OpenClaw skills. Use when analyzing the local skill ecosystem, understanding tool and package dependencies, discovering skill categories, mapping relationships between skills, checking security posture, auditing skill health, detecting overlaps, or generating an ecosystem health report. Trigger on "analyze my skills", "skill supply chain", "what tools do my skills use", "skill dependencies", "skill inventory", "ecosystem report", "which skills use X package", "skill categories", "popular skills", "skill security", "skill health", "skill completeness", "overlapping skills".
---

# SkillChain

Supply chain intelligence and ecosystem analysis for OpenClaw skills. Operates offline-first against locally installed skills; optionally enriches with live clawhub metadata (stars, downloads, moderation verdicts) when network is available.

## When to Use

| Trigger | Action |
|---------|--------|
| "Analyze my skills" / "skill inventory" | `ingest analyze-all` (one-shot) |
| "What tools / packages do my skills use?" | `analyze packages` |
| "Show dependencies for skill X" | `analyze supply-chain --skill <slug>` |
| "Which skills share package X?" | `analyze find-users --package <name>` |
| "Skill categories / ecosystem breakdown" | `analyze categories` |
| "How complete / healthy are my skills?" | `analyze health` |
| "Do any skills overlap or duplicate?" | `analyze overlaps` |
| "Sync online popularity / security data" | `ingest enrich` |
| "Full ecosystem report with insights" | `analyze report` |
| "Rebuild graph from scratch" | `ingest reset && ingest scan` |

## Workflow

### One-shot (recommended)

```bash
# Reset, scan, health check, overlap analysis, full report — all in one command
python3 scripts/ingest.py analyze-all

# With custom directories
python3 scripts/ingest.py analyze-all --dirs ~/.cursor/skills-cursor ~/.openclaw/skills ~/Downloads/skills-main/skills
```

### Step 1 — Ingest (build the graph from local skills)

```bash
# Auto-discover skills under default paths
python3 scripts/ingest.py scan

# Specify directories explicitly
python3 scripts/ingest.py scan --dirs ~/Downloads/skills-main/skills ~/.codex/skills ~/Downloads/ontology

# Online enrichment: adds stars, downloads, moderation verdict from clawhub
# Skipped automatically if network is unavailable
python3 scripts/ingest.py enrich

# Check what's currently in the graph
python3 scripts/ingest.py status

# Reset and rebuild
python3 scripts/ingest.py reset
python3 scripts/ingest.py scan
```

### Step 2 — Analyze

```bash
# Ecosystem overview (counts, categories, top packages)
python3 scripts/analyze.py stats

# Category distribution
python3 scripts/analyze.py categories

# Skill completeness health scores (0-100 per skill, with specific issues)
python3 scripts/analyze.py health

# Detect overlapping or complementary skill pairs
python3 scripts/analyze.py overlaps

# Top N skills by a metric
python3 scripts/analyze.py top --by stars --limit 10
python3 scripts/analyze.py top --by downloads --limit 10

# Skill profile card (dependencies, tools, bins, invocation pattern, online metrics)
python3 scripts/analyze.py profile --skill ontology

# Full supply chain for a skill (invoked_via → requires_bin → tools → packages → skill deps)
python3 scripts/analyze.py supply-chain --skill agent-browser

# Find all skills that use a specific package
python3 scripts/analyze.py find-users --package playwright

# Most-used packages across all skills
python3 scripts/analyze.py packages --top 20

# Full markdown report with Key Insights section
python3 scripts/analyze.py report
```

## Data Sources

| Source | What it provides | Required? |
|--------|-----------------|-----------|
| `SKILL.md` frontmatter | name, description, license, `allowed-tools`, `metadata.requires.bins`, `read_when` | Yes |
| `requirements.txt` | Declared Python package deps (pypi) | When present |
| `pyproject.toml` | Python deps: PEP 621, Poetry, optional-deps | When present |
| `Pipfile` | Python deps (Pipfile format) | When present |
| `package.json` | npm deps: dependencies / devDeps / peerDeps | When present |
| `scripts/*.py` AST scan | Implicit Python imports (non-stdlib only) | When present |
| `_meta.json` / `.clawhub/origin.json` | slug, version, registry | When present |
| clawhub API (online) | stars, downloads, moderation verdict, owner | Optional |

## Graph Relations

| Relation | Meaning |
|----------|---------|
| `belongs_to_category` | skill belongs to a functional category |
| `requires_package` | skill depends on a pypi / npm package |
| `uses_tool` | skill uses a detected tool (heuristic) |
| `requires_tool` | skill requires a system binary (`metadata.requires.bins`) |
| `invoked_via` | skill is called through a tool channel (`allowed-tools`) |
| `depends_on_skill` | skill references another skill in its description |

## Default Scan Paths

The ingest script checks these locations by default:

- `~/.openclaw/skills`
- `~/.openclaw/extensions` (extensions exposing their own skills via `<plugin>/skills/*`)
- `/Applications/OpenClaw.app/Contents/Resources/skills` (macOS app bundle, when installed)

In addition, `ingest scan` augments the user-provided or default `--dirs`
arguments with:

- `<project_root>/skills` — project-local skills folder when this skill lives
  inside a repository
- `$(npm root -g)/openclaw/skills` — globally installed OpenClaw skills from
  a Node.js / npm environment

Any directory containing a `SKILL.md` file is treated as a skill.

## Ontology Contract

```yaml
ontology:
  reads: [Skill, SkillCategory, Tool, SoftwarePackage]
  writes: [Skill, SkillCategory, Tool, SoftwarePackage]
  storage: memory/skillchain/graph.jsonl
  schema: schema/skillchain.yaml
  preconditions:
    - "At least one local skill directory is accessible"
  postconditions:
    - "Every discovered skill has a Skill entity"
    - "Skills with requirements.txt have SoftwarePackage entities and requires_package relations"
```

## Storage

Graph data is written to `memory/skillchain/graph.jsonl` using the same append-only JSONL format as the `ontology` skill. Reuse `scripts/ontology.py` from the ontology skill for low-level graph operations.

## References

- `references/model.md` — Full ontology model (types, relations, constraints)
- `schema/skillchain.yaml` — Machine-readable schema for validation
