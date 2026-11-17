---
name: superstition-debunker
description: Use when a forwarded message, viral post, chain letter, or "they don't want you to know" claim needs a quick credibility read — detects the rhetorical fingerprints of folklore (vague authority, suppression urgency, forwarding quotas, unfalsizable mechanisms, single-case causation, unsourced percentages) across 6 pattern families, scores myth-signature strength, and generates the exact questions that would settle it. Structural triage, not fact lookup.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [misinformation, folklore, chain-letters, critical-thinking, fact-checking, media-literacy]
---

# Superstition Debunker — Folklore Fingerprinting

Myths don't carry a "false" label — but they do carry *structural*
fingerprints. "Harvard doctors confirmed," "share before this is
taken down," "my cousin's neighbor died after," "90% of people" —
these aren't evidence, they're costumes. Real information looks
structurally different: named sources, checkable mechanisms,
denominators, and no forwarding quota. This skill scores any claim
against a catalog of folklore patterns and hands you the exact
questions that would settle it.

## When to Use

- A family group chat just received "URGENT, forward to 10 people"
- Deciding whether a viral health/safety claim deserves a fact-check
  rabbit hole or a one-line reply
- Teaching kids/parents media literacy with concrete patterns instead
  of "don't believe everything online"
- Triaging your own feed before resharing
- Building a family "is this real?" routine that scales

Don't use for: actual fact-checking (go to primary sources /
fact-checkers for verdicts), hate/harassment content moderation
(different problem), or scoring satire (structure is deliberately
myth-shaped — that's the joke).

## The Six Pattern Families

1. **Authority mimicry** — borrows credibility instead of earning it:
   vague "doctors confirmed," big-institution flex ("NASA proves"),
   secret/classified research (uncheckable by design).
2. **Urgency & suppression** — rushes you past verification:
   "they don't want you to know," "about to be deleted," forwarding
   quotas, "act before it's too late."
3. **Unfalsifiable structure** — arranges to survive being wrong:
   energy/vibrations/toxins with no measurable mechanism, "only
   works if you don't test it," ancient-wisdom appeals.
4. **Causal sleight of hand** — dresses sequence as cause:
   correlation-as-cause, single vivid case ("my friend's cousin"),
   post-hoc timing ("days later doctors found").
5. **Numeric theater** — numbers as costumes: precise percentages
   with no denominator or source, "9 out of 10 experts," micro-dose
   scares with no reference dose.
6. **Emotional amplifiers** — hijack sharing instincts: children at
   risk, gruesome imagery, luck/curse chain mechanics.

## Workflow

1. Get the full text of the claim (screenshot transcript or paste).
2. Score it:
   ```bash
   python3 scripts/myth_analyzer.py analyze "URGENT: Harvard doctors
   confirmed 90% of people who... share with 10 friends before this
   is taken down" --log
   ```
3. Read the verdict: **STRONG** (score ≥10 or ≥4 families — treat as
   folklore until primary sources appear), **MODERATE** (≥6 or ≥3
   families — verify before sharing), **WEAK** (≥3 — sloppy writing
   or possibly real), **NO signatures** (structure can't judge it;
   fact-check normally).
4. Use the per-pattern "ask" lines as your reply script — each is
   the question that would settle the claim ("Which study? Named
   institutions publish named people.").
5. `--log` accumulates analyses; `stats` shows which families
   dominate your feed — a media-diet readout.

## Calibration Examples (from tests)

- Chain-message style claim (Harvard + share-to-10 + energy
  frequencies + cousin anecdote): score 10 → **STRONG**
- Boring real-science report ("2014 study of 40,000 nurses, 23%
  lower mortality, adjusted for smoking"): score 0 → **NO
  signatures**
- The tool reads *rhetoric*, not truth: a badly-written true story
  can score MODERATE, and a carefully-worded lie can score 0.

## Common Pitfalls

1. **Treating the score as a truth verdict.** It's a rhetoric
   fingerprint. High score = folklore-shaped, low score = check
   facts the normal way. Say this explicitly when replying.
2. **Running it on satire.** The Onion is structurally mythic on
   purpose; the skill will happily flag it.
3. **Missing screenshots with little text.** The patterns live in
   words; a three-word claim has nothing to fingerprint — ask for
   the full forwarded text.
4. **Replying with the score alone.** The persuasion is in the
   *questions* ("which doctor? what study?") — lead with those, not
   with "my analyzer says 10."
5. **Forgetting survivorship in your own feed.** `stats` counts what
   you *analyze*, not what you *see*; it's a triage log, not an
   epidemiology of your inbox.

## Verification Checklist

- [ ] Full claim text captured (not a summary of it)
- [ ] Verdict reported as "myth signatures," never "false"
- [ ] At least one settling question included in any reply
- [ ] If STRONG + health/medical: point to a primary source or
      professional, not just the score
- [ ] Log reviewed occasionally (`stats`) for family patterns

## One-Shot Recipe: the family-chat reply

```bash
python3 scripts/myth_analyzer.py analyze "<pasted message>" --log
```
Reply template: "This has the classic chain-message shape — unnamed
'Harvard doctors,' a forwarding quota, and a scary stat with no
source. [The matched patterns.] The questions that would settle it:
which study? what's the denominator? Real warnings cite checkable
sources and never ask you to forward. Happy to dig if you find where
it came from."
