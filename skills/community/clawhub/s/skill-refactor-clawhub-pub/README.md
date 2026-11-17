# skill-md-optimizer

Refactor or audit any `SKILL.md` for **progressive disclosure** — a lean trigger
frontmatter, a layered body (hard constraints vs single-run flow), a converged
≤5-step loop, permission/context declarations, and a token budget that survives
context compaction. Ships a **deterministic, offline linter** (`scripts/check_skillmd.py`)
for the mechanical checks and a methodology for the judgment layer. Three modes:
`refactor` (default), `audit` (read-only), `readme` (polish the companion README).

> Cross-agent: the published package is host-neutral (ClawHub-native
> `metadata.openclaw`). One SKILL.md is the Agent-Skills open standard and reads
> on 20+ hosts — see `references/platform-frontmatter.md` for the 14-platform
> field matrix.

## Install

Clone and add the directory to your skill root (each host has its own folder):

```bash
git clone https://github.com/Elisabeth15501/skill-refactor
# WorkBuddy / Claude:  ~/.workbuddy/skills/skill-md-optimizer
# OpenClaw:            ~/.openclaw/skills/skill-md-optimizer
# or copy just the 11-file package (SKILL.md + references/ + scripts/ + assets/)
```

Requires Python 3 (stdlib only) and PyYAML (auto-installed if missing; offline
fallback marks the run `BLOCKED`, never passes silently).

## Usage

```bash
# mechanical screen (offline, deterministic)
python scripts/check_skillmd.py path/to/SKILL.md --platform clawhub --token-budget 3500

# JSON (CI / pre-publish hook), schema_version 1.0
python scripts/check_skillmd.py path/to/SKILL.md --json
```

Exit-code contract (same shape as `skill-publish-gate`):

| code | verdict | meaning |
|---|---|---|
| 0 | PASS | no blockers (advisory medium/low may remain) |
| 2 | NEEDS_FIX | only advisory items |
| 1 | BLOCKED | a blocker hit (syntax / missing name / over hard cap) |

Run it through the agent for the judgment layer: "optimize / refactor / slim down
this SKILL.md" triggers the five-step flow (resolve → lint → plan → emit → close
with a `BLOCKER=0 AND MEDIUM=0` acceptance gate).

## Platform copies

The published package keeps only the neutral core. Host-specific fields are
per-copy, not merged into one schema:

- **ClawHub / OpenClaw (primary):** `metadata.openclaw.requires` + `license: MIT-0`.
- **Claude / WorkBuddy host copy:** add `allowed-tools`, `context: fork`,
  `disable-model-invocation`, `user-invocable` (see `references/platform-frontmatter.md`).
- **SkillHub (CN):** keep `license` + CN content red lines.

## Lint rules

| family | IDs | what it checks |
|---|---|---|
| frontmatter | FM-001…FM-105 | YAML syntax, name/slug slug rule, description present + ≤1024 chars |
| platform | PL-CL-1/2, PL-SH-1 | ClawHub `license: MIT-0`; `requires` declaration (top-level **or** `metadata.openclaw.requires`) |
| body | BD-001…BD-004 | lines <500 hard / >200 soft; est token vs budget |
| trigger | TR-001 | frontmatter has a NOT-for boundary |
| structure | ST-001 | explicit "hard-constraint / every turn" layer present |
| references | RF-001 | body prose references to `references|assets|scripts` exist (code-fence examples exempt) |
| NL-Policy | NL-001/002 | `language:` justification; body three-state language picker |

Every finding carries a `hint` (diagnosis + suggested fix) for **human fallback**
when the agent cannot auto-fix.

## Layout

```
SKILL.md                  # the skill (refactor / audit / readme)
references/               # L3 on-demand detail
  platform-frontmatter.md # 14-agent field matrix + verified format split
  token_budget.md         # official budget anchors + estimation
  i18n_policy.md          # NL-Policy two shapes + three-state picker
  readme_quality.md       # README five questions + fixed order
  trigger_boundary_changelog.md
  skillmd_audit_sample.md # audit-mode output contract
scripts/check_skillmd.py  # deterministic offline linter
assets/checklist.html     # 33-item checkable audit list
assets/readme_template.md # readme skeleton
```

## License

MIT-0 (no proprietary content). See `LICENSE`.
