# Skill Health Report — Template

```markdown
# 🩺 Skill Health Report

**Scanned:** <N> skills in <dir> · <date>

## 1. Trigger Overlaps

| Pair | Wake-both sentence | Verdict |
|---|---|---|
| A ↔ B | "…" (quoted, plausible user input) | 🔴 RED / 🟡 YELLOW / 🟢 GREEN |

(Only RED and YELLOW pairs listed; GREEN pairs omitted for signal-to-noise.)

## 2. Dead Zones — expansion space

| Frequent task | Covering skill | Idea |
|---|---|---|
| <task> | none | <one-line skill idea> |

## 3. Description Fitness

| Skill | Chars | Trigger phrase? | Verdict | Fix |
|---|---|---|---|---|
| <name> | <n> | ✓/✗ | 🔴/🟡/🟢 | <rewrite proposal> |

## 4. Duplicates

<pairs or "none">

## 5. Bloat

<skills with large references + no plausible triggers, or "none">

---

## Top 3 fixes by impact

1. <edit> — why it matters
2. <edit> — why it matters
3. <edit> — why it matters
```

Rules:
- One line per pair / per skill; no prose paragraphs
- Quote the wake-both sentence verbatim — never invent it
- Top-3 fixes must be concrete diffs ("change X's description sentence #2 to …")
