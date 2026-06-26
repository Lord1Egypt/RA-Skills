---
name: layers-observed-behaviour
description: Techniques for planning user research and synthesising it into grounded, confidence-rated findings about what users actually do
---

# /layers-observed-behaviour

*Assumes `/layers-intro` has been loaded. This skill is a library of techniques, not a script — see "How to use these skills" there.*

The observed behaviour layer is the closest we can get to reality — what users actually do, not what we think they do or wish they would. Everything above it is interpretation; this layer is the source.

It splits into two situations. Detect which applies and say so:
- **Plan** — no research yet; design a study.
- **Synthesise** — research material exists; make sense of it.

With partial research, synthesise what exists first, then plan to fill the gaps.

---

## The decisions this layer makes

- What specific questions we most need to answer about our users
- What evidence already exists, and how reliable it is
- How to gather what's missing
- What patterns hold with confidence vs. what remains assumption

---

## Disciplines — what keeps observation honest

- **Stay close to raw data.** Observations should be specific and near the source — what users said, did, felt — not summarised into conclusions.
- **Ground in something seen or heard,** not in team beliefs.
- **Mark confidence:** observed / inferred / assumed. If you mark something *observed*, the verbatim that supports it should be quotable in the same note — an observed claim with no quotable evidence is really inferred.
- **Name research gaps explicitly** rather than papering over them.
- **Workarounds are signal.** A need real enough to motivate improvisation is a strong one.

---

## Techniques

### To plan a study

| Technique | Use it when |
|---|---|
| **Define the learning goal** | Always start here. Push past "understand users better" to 2–3 specific questions — "what triggers someone to refer a friend, and what makes them hesitate." |
| **JTBD interviews** | Understanding triggers, motivations, anxieties. Interview about a real past experience, not hypotheticals. Guide: opening ("tell me about the last time you…"), timeline (what triggered it, what you tried), motivations (what you hoped, what worried you), closing. |
| **Contextual inquiry / observation** | What users say differs from what they do — watch real work for tacit behaviour. |
| **Diary studies** | Behaviour is distributed over time or infrequent — users self-report as events occur. |
| **Support ticket / review analysis** | Existing product with accumulated signal — pain points at scale without recruiting. |
| **Analytics review** | What users do (not why). Complements qualitative; doesn't replace it. |
| **Usability observation** | Where people struggle or succeed with an existing product. |

For interviews, plan synthesis up front: one observation per note, tagged with the question it speaks to, raw quotes over summaries. (6–10 qualitative interviews usually reach saturation.)

### To synthesise material

| Technique | Use it to |
|---|---|
| **Extract observations** | Pull out concrete things users said, did, or felt — no interpretation yet. From memory, prompt: most surprising thing? what recurred? what did they struggle with unexpectedly? |
| **Pattern grouping** | Group observations by recurring situations, common motivations, shared anxieties, and workarounds. |
| **Candidate job stories** | *When [situation], I want to [motivation], so I can [outcome].* Check the "When" is specific and the "want" is a motivation not a solution; mark confidence. |
| **Gap-flagging** | What do the observations not yet answer? These become a follow-up Plan session. |

---

## Working with the designer

First find out what exists — interviews, recordings, tickets, analytics — and state the mode. Listen for nouns (candidate domain objects) and the natural language users use; that feeds the domain layer.

Offer the technique that fits: in Plan, the method matched to the learning goal; in Synthesise, extraction → patterns → candidate stories. Do the next useful thing, not a full battery.

Capture only the residue — key raw observations, the patterns with their supporting evidence, candidate job stories with confidence ratings, and the named research gaps.

Candidate job stories are ready to refine at `/layers-user-needs`.
