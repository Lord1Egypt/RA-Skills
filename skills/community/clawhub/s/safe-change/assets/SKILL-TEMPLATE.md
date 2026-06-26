# Skill Template — safe-change Style

Template for creating impact-analysis companion skills in the safe-change style.
Copy and customize for new stack support (Python, Go, etc.) or new analysis dimensions.

---

## SKILL.md Template

```markdown
---
name: safe-change-<stack>
description: "Map blast radius before shipping on <stack> — run when editing a shared module, route handler, or config-dependent file."
---

# Safe Change — <Stack>

[One sentence: what problem this solves and for which stack]

## Quick Reference

| Situation | Action |
|-----------|--------|
| Editing a shared module | → Run `scan-impact.mjs` first |
| Risk score is High | → Stop, read report, get go/no-go |
| Test gap detected | → Write tests before changing |
| All checks pass | → Run verify gate |

## When to Use

[2-3 bullets: specific trigger conditions for this stack]

## How It Works — 6 Phases

### Phase 1 — Detect Stack
[Stack detection logic]

### Phase 2 — Build Impact Map
[What dimensions are collected and how]

### Phase 3 — Risk Score
[Heuristic table: Low / Medium / High conditions]

### Phase 4 — Render Report
[Output format description]

### Phase 5 — Checkpoint (mandatory)
[Pause instruction — this is the core gate]

### Phase 6 — Verify Gate
[What commands run in which order]

## Output Format

[Markdown report template with placeholders]

## Limitations

See `references/limitations.md`.

## Companion Skills

- safe-change (TypeScript/NestJS/Next.js) — the original
- deep-debugging — use after a bug ships
```

---

## scan-impact.mjs Extension Pattern

To add a new analysis dimension to `scan-impact.mjs`:

```javascript
// 1. Add a new async scanner function (max 40 lines)
async function scanNewDimension(root, targetRel) {
  // Read files, apply regex, return structured data
  return { count: 0, items: [] };
}

// 2. Call it in main()
const newDimension = await scanNewDimension(projectRoot, targetRelative);

// 3. Add to output object
const output = {
  // ... existing fields
  new_dimension: newDimension,
};

// 4. Include in risk score if relevant
// Update calculateRiskScore() to use the new data
```

Rules for new scanner functions:
- No external dependencies (Node stdlib only)
- Read-only (never write files)
- Must handle missing directories gracefully (try/catch or existsSync)
- Max 40 lines per function
- Return structured data (not raw strings)

---

## Risk Score Extension Pattern

Current thresholds in `calculateRiskScore()`:

```javascript
// High
importerCount >= 8 || endpointCount >= 3 || (testGap && envVarCount > 0 && recentMigrationCount > 0)

// Low
importerCount <= 2 && endpointCount === 0 && !testGap && envVarCount === 0 && recentMigrationCount === 0

// Medium: everything else
```

To add a new signal:

```javascript
// Add to the High condition
|| newDimension.criticalCount > 0

// Add to the Low condition
&& newDimension.count === 0

// Add to factors array
if (newDimension.count > 0) factors.push(`${newDimension.count} <label>`);
```

---

## verify-gate.sh Extension Pattern

To add a new check to the verify gate:

```bash
# After the existing checks, before print_success

# ---- Check N: Custom Check --------------------------------------------
if has_npm_script "custom-check"; then
  run_check "Custom Check (npm run custom-check)" "npm run custom-check"
else
  skip_check "Custom Check" "no 'custom-check' script in package.json"
fi
```

The `run_check` function handles:
- Printing the label and command
- Running in the project root
- Colored pass/fail output
- Stopping on failure (via `exit 1`)

---

## File Naming Conventions

```
safe-change-<stack>/
├── SKILL.md
├── README.md
├── package.json              # "name": "safe-change-<stack>"
├── scripts/
│   ├── scan-impact.mjs       # Main analyzer
│   └── verify-gate.sh        # Verify gate
├── references/
│   ├── example-impact-report.md
│   ├── usage.md
│   └── limitations.md
└── assets/
    └── SKILL-TEMPLATE.md     # This file
```

---

## Checklist Before Publishing

- [ ] `scan-impact.mjs --help` runs without error
- [ ] `verify-gate.sh --help` runs without error
- [ ] At least one realistic example in `references/example-impact-report.md`
- [ ] `references/limitations.md` is honest about what is not detected
- [ ] `package.json` has correct `openclaw.skill` and `version`
- [ ] Scripts are read-only (no file writes to source directories)
- [ ] Scripts handle missing directories gracefully
- [ ] Risk score thresholds are documented in SKILL.md
