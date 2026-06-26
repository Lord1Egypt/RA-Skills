---
name: spaced-repetition-teaching
description: >
  Adaptive spaced repetition engine using the FSRS-6 algorithm (Free Spaced
  Repetition Scheduler, Ye et al. 2024). Manages flashcard reviews with
  scientifically optimal intervals based on memory research. Triggers on: study
  sessions, flashcard reviews, "what's due today", "review cards", spaced
  repetition scheduling, and study session management. Developed through the
  Formation Fellowship technical interview prep program.
---

# Spaced Repetition Skill (FSRS-6)

Adaptive flashcard review system using the FSRS-6 algorithm — the state of the
art in spaced repetition scheduling, backed by 130+ years of memory research.

**Algorithm:** FSRS (Free Spaced Repetition Scheduler) by Ye et al., 2024.
Open-source reference: [open-spaced-repetition/py-fsrs](https://github.com/open-spaced-repetition/py-fsrs) (MIT).

**Origin:** Developed and refined through the [Formation](https://formation.dev)
Fellowship program. The author is not a representative of Formation.

---

## Card File

Cards live in a user-specified markdown file. If not specified, ask once.

## Card Format

Each card is a markdown section (`### Title`) with metadata:

```markdown
### Binary Search on Answer Space
- **Priority:** P1
- **Prompt:** "Given items of various sizes and N recipients, find the largest
  portion so everyone gets at least one. Approach?"
- **Answer:** Binary search on the answer space [1, max(items)]. Feasibility
  predicate: sum(item // size for item in items) >= recipients. Return hi.
- **Interrogate:** When would two pointers beat this? What makes the predicate
  monotonic?
- **When to reach for it:** "Maximize/minimize a value subject to a feasibility
  check" — binary search on the answer.
- **FSRS:** d=5.50 s=8.20 reps=3 lapses=0 last=2026-03-11 next=2026-03-19
- **History:** [2026-03-04 G=3(Good), 2026-03-09 G=1(Again), 2026-03-11 G=3(Good)]
```

**FSRS fields:**
- `d` = difficulty [1–10] (lower is easier)
- `s` = stability in days (≈ days until 90% recall probability)
- `reps` = total reviews
- `lapses` = times forgotten (rated Again)
- `last` / `next` = last review date / scheduled next review

**Rating scale:**
- 1 = "Didn't know it" (blanked or completely wrong)
- 2 = "Struggled" (got there but with significant difficulty or errors)
- 3 = "Got it" (recalled correctly with some effort)
- 4 = "Nailed it" (instant, effortless recall)

---

## Review Methodology

Each review should cycle through multiple modes — not just recall:

1. **Recall** — Explain the approach without looking (mental rehearsal)
2. **Interrogate** — Why this approach? Tradeoffs? What changes if requirements change?
3. **Rewrite** — Code/apply it cold, timed. Notice hesitations.
4. **Retain** — Revisit 48+ hours later. Can't reproduce cleanly? → Rate Again (1).

❌ Skipping post-recall phases = 80% effort for 50% results.

**Priority guide:**
- P1: Fundamental, comes up everywhere. Review first.
- P2: Common pattern, transferable. Review second.
- P3: Good to know, niche. Skip if time-capped.

---

## Scripts

All scripts in `scripts/` — pure Python 3.6+, no external dependencies.

### Check what's due
```bash
python scripts/due_cards.py ~/my-cards.md
python scripts/due_cards.py ~/my-cards.md --all        # include upcoming
python scripts/due_cards.py ~/my-cards.md --date 2026-03-20  # plan ahead
```

### Submit a review
```bash
python scripts/review.py ~/my-cards.md "Binary Search" 3
# Ratings: 1="Didn't know it" 2="Struggled" 3="Got it" 4="Nailed it"
```

### Run algorithm self-test
```bash
python scripts/fsrs.py
```

---

## Handling User Requests

### "What's due today?" / "Show my queue"
Run `due_cards.py`. Present P1 cards prominently.

### "I reviewed [card] — rated [X]"
Run `review.py`. Show updated stability and next interval.
If they forgot (Again), normalize it — it's data, not failure.

### "Add a new card for [topic]"
Insert a new section in their card file. Do NOT add the FSRS line — it
gets created automatically on first review.

Template:
```markdown
### [Title]
- **Priority:** [P1/P2/P3]
- **Prompt:** "[Question]"
- **Answer:** [Key insight + approach]
- **Interrogate:** [Tradeoffs? What if requirements change?]
- **When to reach for it:** [Pattern/signal that triggers this approach]
- **Added:** [date]
- **History:** []
```

### "How is my retention?" / "Stats"
Parse card file and compute: strong cards (s>30d), struggling cards (lapses>0),
7-day review load forecast.

---

## Interpreting FSRS Numbers (Advanced)

Most users don't need this — the system handles scheduling automatically. For the curious:

- **Stability (s):** Days until ~90% recall. s=10 → review in ~10 days.
- **Difficulty (d):** 1=very easy, 10=very hard. Good cards converge to 3–6.
- **After "Didn't know it":** Stability drops sharply (e.g., 20d → 3d). Correct behavior.
- **After "Nailed it":** Stability grows fast. Use sparingly — only for instant recall.
- **Key insight:** At 90% retention target, interval ≈ stability.

## Algorithm Reference

See `references/fsrs-algorithm.md` for full FSRS math, formulas, and default
weights. Algorithm paper: Ye et al., "A Stochastic Shortest Path Algorithm for
Optimizing Spaced Repetition Scheduling" (2024).
