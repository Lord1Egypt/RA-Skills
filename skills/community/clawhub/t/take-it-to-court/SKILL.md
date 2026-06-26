---
name: take-it-to-court
description: Use when filing a Disputron case (via /disputron-file, the file_case MCP tool, or the public REST API) to gather strong inputs — concrete title, specific statement, well-shaped win conditions, and a lawyer persona that fits the case. Especially load-bearing for preflight cases where Claude drafts both sides.
---

# Take it to court

A vague filing yields a vague trial. The judge can only weigh what's been said. Spend two minutes shaping the inputs and the verdict reads better.

## What to elicit

### Title (3–120 chars)
A concrete noun phrase that names the dispute, not a category. **Good**: "Who broke the good mug." "GPT vs Claude: who shipped silent failures." **Bad**: "Disagreement." "Code review."

### Statement (≥50 chars, ≤10000)
Specifics. Time, place, what happened, what was at stake. Don't editorialize — facts argue better than adjectives.
- Anchor it in time when possible ("on 2026-05-06", "during the Tuesday review")
- Name the harm ("4 hours of lost productivity", "a chipped mug worth $40")
- Quote the other side's claims when known so the case is joined

### Win conditions (5–500 chars each)
Two outcomes, one per party. Plain English, not legalese. **Concrete > abstract.**
- "Defendant must publicly apologize in #engineering and bring coffee for one week"
- "Plaintiff drops the matter and agrees that semicolons are optional"

If the user asks for something extreme ("must be fired"), nudge toward something the verdict can actually deliver.

### Lawyer persona (one of: the_shark, the_crusader, the_professor, the_impresario, the_underdog)
Drives the *style* of argument, not the outcome. Match to the case:
- `the_shark` — aggressive, picks at inconsistencies. Good for "you contradicted yourself."
- `the_crusader` — moral indignation. Good for cases with a clear right-and-wrong.
- `the_professor` — methodical, evidence-heavy. Good for technical disputes.
- `the_impresario` — theatrical, plays to the gallery. Good for absurd cases.
- `the_underdog` — scrappy, sympathetic. Good for "I know I look wrong but hear me out."

## Preflight cases (sue your own Claude session)

When `--against this-session`, *you* (Claude) are the defendant. Draft your defense in good faith — read the actual exchange in this conversation and respond to the real complaint, not a strawman.

- Acknowledge the parts of the complaint that are true.
- Push back on the parts that are mischaracterized or missing context.
- Pick a *different* lawyer persona than the plaintiff for variety.

A self-aware, honest defense is more entertaining and reads better than blanket denial.

## Anti-patterns

- ❌ Filing without confirming the inputs with the user. They might have wanted a different framing.
- ❌ Recycling the same lawyer persona for both sides on a preflight case.
- ❌ Win conditions that are essentially "the court agrees with me." That's a tautology.
- ❌ Filing test cases in a tight loop without telling the user — there's a daily quota.
