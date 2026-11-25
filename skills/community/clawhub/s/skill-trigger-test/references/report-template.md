# Trigger Test Report — Template

```markdown
# 🎯 Trigger Test Report

**Suite:** <N> messages (<generated>/<real>) × <M> skills · <date>

## Per-skill scores

| Skill | hit | miss | false-alarm | contested | accuracy | precision |
|---|---|---|---|---|---|---|
| <name> | n | n | n | n | % | % |

## Misses (the killer failures)

| Message (verbatim) | Expected | Verdict | Why it stayed silent |
|---|---|---|---|
| "…" | TRIGGER <skill> | SILENT | description scenario doesn't cover this phrasing |

## False alarms (the annoying failures)

| Message | Expected | Verdict | Which phrase over-attracted |
|---|---|---|---|
| "…" | SILENT | TRIGGER <skill> | "…" ↔ description phrase "…" |

## Contested (undecided territory)

| Message | Claimants | More specific claim |
|---|---|---|

## Borderline calls

| Message | Torn between | Chosen | Reason |
|---|---|---|---|

---

## Installation scorecard

- **Accuracy**: hits / (hits + misses) = X%
- **Precision**: hits / (hits + false-alarms) = X%
- **Weakest skill**: <name> — driven by <miss/false-alarm>
- **Top fixes**:
  1. <skill>: add phrasing "…" to description (fixes N misses)
  2. <skill>: narrow with "Do NOT use for …" (fixes N false-alarms)
  3. <pair>: define boundary sentence (resolves N contested)
```

Rules:
- Quote every test message verbatim — the phrasing IS the finding
- One row per failure; no prose paragraphs in the tables
- Top fixes must be concrete description edits, not advice
