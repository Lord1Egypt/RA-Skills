# Skill Stocktake — AI-Powered Quality Audit

> Beyond structural hygiene: evaluate skill quality, actionability, and fitness using AI judgment.

## Problem

`heal.sh --strict` catches structural issues (missing frontmatter, unlinked refs, name mismatches). But it can't judge:
- Is this skill still actionable and current?
- Does it overlap with another skill?
- Should it be retired, merged, or improved?
- Is it used frequently enough to justify maintenance cost?

## Solution: Two-Pass Evaluation

### Pass 1: Inventory (Deterministic)
Run `heal.sh --strict` for structural checks (existing), then collect metadata:

```bash
# For each skill directory
for skill_dir in skills/*/; do
    skill_name=$(basename "$skill_dir")
    skill_md="${skill_dir}SKILL.md"

    # Extract frontmatter
    tier=$(grep 'tier:' "$skill_md" | head -1 | awk '{print $2}')
    line_count=$(wc -l < "$skill_md")
    ref_count=$(ls "${skill_dir}references/" 2>/dev/null | wc -l)
    last_modified=$(stat -f %Sm -t %Y-%m-%d "$skill_md" 2>/dev/null || stat -c %y "$skill_md" 2>/dev/null | cut -d' ' -f1)

    echo "${skill_name}|${tier}|${line_count}|${ref_count}|${last_modified}"
done
```

### Pass 2: AI Evaluation (Judgment)
Spawn a subagent with the inventory table + evaluation criteria. Process ~20 skills per agent to stay within context.

**Evaluation Criteria:**
- **Actionability:** Does the skill produce concrete artifacts when invoked?
- **Scope Fit:** Does it fit its declared tier? Is it doing too much or too little?
- **Uniqueness:** Does it overlap substantially with another skill?
- **Currency:** Are referenced tools, APIs, and patterns still current?
- **Trigger Clarity:** Could an LLM correctly decide when to invoke this skill?

### Verdict Categories

| Verdict | Meaning | Required Evidence |
|---------|---------|-------------------|
| **Keep** | Good as-is | Cite core value + evidence of use |
| **Improve** | Worth keeping, needs fixes | Cite specific section + action + target size |
| **Update** | Referenced tech is outdated | Cite what's outdated + what replaced it |
| **Retire** | Low quality, stale, or redundant | Cite (1) specific defect, (2) what covers same need |
| **Merge into [X]** | Substantial overlap with X | Cite overlap + line count + what content to integrate |

**Reason Quality Rules:**
- Never write "unchanged" alone — restate core evidence
- For Retire: must name what covers the same need
- For Merge: include line count and describe content to integrate
- For Improve: name section + action + target size

## Quick Scan Mode

For re-evaluation after changes (avoids re-scanning unchanged skills):

```bash
# 1. Check which skills changed since last evaluation
LAST_EVAL_DATE=$(jq -r '.evaluated_at' .agents/stocktake/results.json 2>/dev/null || echo "1970-01-01")
CHANGED_SKILLS=$(find skills/ -name "SKILL.md" -newer .agents/stocktake/results.json -exec dirname {} \; | xargs -I{} basename {})

# 2. If no changes, stop
if [ -z "$CHANGED_SKILLS" ]; then
    echo "No skills changed since last evaluation ($LAST_EVAL_DATE)"
    exit 0
fi

# 3. Re-evaluate only changed skills
echo "Quick scan: $CHANGED_SKILLS"
# Spawn agent with only changed skills
# Carry forward unchanged verdicts from results.json
```

## Results Schema

```json
{
  "evaluated_at": "2026-03-21T10:00:00Z",
  "mode": "full|quick",
  "batch_progress": {"total": 54, "evaluated": 54, "status": "completed"},
  "skills": {
    "vibe": {
      "verdict": "Keep",
      "reason": "Core judgment skill; produces council verdicts, complexity analysis, and actionable findings. 779 lines, 15 references — well-maintained.",
      "last_modified": "2026-03-21"
    },
    "converter": {
      "verdict": "Improve",
      "reason": "Cross-platform skill converter is useful but description frontmatter is thin (155 lines). Add concrete examples of Codex/Cursor output format. Target: 200+ lines.",
      "last_modified": "2026-02-15"
    }
  }
}
```

## Integration with heal-skill

Run stocktake as an optional mode of heal-skill:

```bash
# Structural checks (existing)
bash skills/heal-skill/scripts/heal.sh --strict

# Quality evaluation (new)
bash skills/heal-skill/scripts/heal.sh --stocktake         # full evaluation
bash skills/heal-skill/scripts/heal.sh --stocktake --quick  # quick scan
```

Results written to `.agents/stocktake/results.json`. Summary displayed to user.

## When to Run

- Before `/release` — ensures all skills are fit for distribution
- After adding/removing skills — detects overlap with existing skills
- Monthly maintenance — catches staleness and drift
- When skill count exceeds threshold (50+) — retirement pressure increases
