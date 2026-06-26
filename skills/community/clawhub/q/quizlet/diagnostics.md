# Retention Diagnostics for Quizlet

## Signals to Track

- Accuracy trend by set and by tag.
- Time-to-answer for hard cards.
- Repeat misses on the same prompt pattern.
- Score drop between practice mode and test mode.

## Failure Pattern Map

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| High flashcard accuracy, low test score | Recognition without recall | Increase Test sessions and rewrite prompts |
| Same cards missed every session | Ambiguous wording or overloaded cards | Split cards and add context cues |
| Fast answers, low retention next day | Shallow processing | Add spaced review checkpoints |
| Strong in one tag, weak in another | Uneven set composition | Rebalance card volume per topic |

## Weekly Review Protocol

1. Export or log the top 10 missed cards.
2. Classify each miss: ambiguity, overload, missing context, or memory gap.
3. Rewrite at least the top 3 recurring misses.
4. Run one short validation test on rewritten cards.
5. Record outcomes in `~/quizlet/weak-cards.md`.

## Rewrite Templates

- Ambiguous prompt -> add domain qualifier and expected format.
- Overloaded prompt -> split into two sequential cards.
- Missing context -> include scenario or source cue.
- Pure memorization failure -> add mnemonic or contrast card.

## Decision Thresholds

- Rewrite threshold: card missed 2+ times in one week.
- Archive threshold: card is trivial and always correct for 3 weeks.
- Escalate threshold: entire tag below 65 percent after rewrites.
