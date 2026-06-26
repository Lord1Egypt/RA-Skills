---
name: skill-dreaming-extractor
version: 1.0.0
description: "Daily fact extraction from AI agent session history into a persistent learned.md memory file"
metadata:
  openclaw:
    requires: { bins: ["python3"] }
---

# Skill: Dreaming Extractor

Reads yesterday's real agent conversations, extracts structured facts using an LLM, and appends them to `memory/learned.md`. Designed to run daily via cron — builds a persistent, searchable knowledge base from your agent's actual interactions.

## What it does

- Scans yesterday's session JSONL files from `~/.openclaw/agents/`
- Filters out system noise (startup sequences, dreaming sessions, tool output)
- Extracts structured facts: decisions made, problems solved, config changes, corrections
- Appends extracted facts to `memory/learned.md` with confidence scores and source citations
- Enforces a daily token budget to cap cost

## Execution Steps

When triggered (by cron or manually), follow these steps:

### Step 1: Collect sessions

```bash
python3 skills/skill-dreaming-extractor/scripts/collect.py
```

Outputs a clean text file at `memory/.dreams/extraction-input/YYYY-MM-DD.txt` containing yesterday's real conversations. If output is "No real sessions found", stop here.

### Step 2: Check budget

```bash
python3 skills/skill-dreaming-extractor/scripts/budget.py --check
```

If output is "BUDGET EXCEEDED", stop. Do not proceed.

### Step 3: Extract facts

Read the collected input. For each meaningful exchange, extract structured facts:

```json
{
  "facts": [
    {
      "subject": "specific entity or concept (e.g., 'API endpoint', 'deployment target')",
      "predicate": "what happened or was decided (e.g., 'was deployed to', 'was updated to')",
      "object": "the outcome or target (e.g., 'production on 2026-04-14', 'v2 with retry logic')",
      "date": "YYYY-MM-DD",
      "confidence": 0.0-1.0,
      "source": "session-id:line-range"
    }
  ]
}
```

#### Extraction Rules

**INCLUDE:**
- Decisions made (architectural, business, operational)
- Problems solved and how
- Configuration changes with rationale
- New capabilities deployed or verified
- Corrections or feedback from the user
- External facts learned (API changes, service incidents, pricing)

**REJECT (scaffolding — never extract):**
- Session startup greetings / "back online" messages
- Tool call results (file contents, grep output, git status)
- Progress updates ("working on X", "let me check")
- Repetitions of the same fact across sessions
- Vague themes with no concrete data
- Meta-conversation about the conversation itself
- Token counts, cost reports, cache stats

**Quality gates:**
- Each fact MUST have at least 3 concrete tokens (subject + predicate + date minimum)
- Confidence 0.9+ = directly stated by user or confirmed by system output
- Confidence 0.7-0.89 = strongly implied, single source
- Confidence 0.5-0.69 = inferred, use sparingly
- Below 0.5 = do not extract

### Step 4: Write to learned.md

Append extracted facts to `memory/learned.md`:

```markdown
## Learned — YYYY-MM-DD

- **[subject]** [predicate] [object] | confidence: X.XX | source: [session-id:lines]
- ...
```

If the file doesn't exist, create it with a header first.

### Step 5: Log budget

```bash
python3 skills/skill-dreaming-extractor/scripts/budget.py --log --facts-count N
```

Where N = number of facts extracted.

### Step 6: Report

Output a summary:

```
Dreaming extraction complete for YYYY-MM-DD:
- Sessions processed: X
- Facts extracted: Y
- Confidence range: X.XX - X.XX
- Budget remaining: $X.XX / $2.00
```

## Manual Run

```bash
python3 skills/skill-dreaming-extractor/scripts/collect.py --date 2026-04-14
# Then follow steps 2-6
```

## Cost

- Estimated: ~$0.50–1.50/day (Sonnet, ~30–200K chars of session history)
- Hard cap: $2.00/day (configurable in budget.py)
- Monthly projection: ~$15–45

## Cron Setup

```bash
openclaw cron add "Dreaming Extractor" "3 3 * * *" "Run task spec: skills/skill-dreaming-extractor/SKILL.md"
```

Fires daily at 03:03 UTC (after sessions have closed for the day).

## Success Metrics

| Metric | Target |
|---|---|
| Facts per cycle with 3+ concrete tokens | ≥ 3 |
| Confidence variance (std dev) | ≥ 0.15 |
| Scaffolding ratio | < 10% |
| Citations per week (facts actually recalled) | ≥ 1 |

If citation count stays at 0 for 30 days, the system isn't adding value — retire it.
