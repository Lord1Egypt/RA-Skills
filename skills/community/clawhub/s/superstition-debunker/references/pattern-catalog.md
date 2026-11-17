# Folklore Fingerprint Catalog — Reference

## Why structural detection works

False viral claims and chain letters are optimized for *sharing*,
not for accuracy. That optimization leaves stable rhetorical
fingerprints: claims must evoke authority without citing it, create
urgency that preempts checking, survive being wrong
(unfalsifiability), and trigger emotion strong enough to forward.
Genuine information — even imperfect journalism — rarely stacks
these patterns, because it's optimized for defensibility instead.

The base rates matter: a message carrying "share with 10 people" +
"they don't want you to know" + an unnamed expert is overwhelmingly
more likely to be folklore than a scoop. Structure is a prior, not
a proof — but it's a strong prior.

## The catalog (families, weights, rationale)

### 1. Authority mimicry (w2 each)
| Pattern | Signature | Why it's a flag |
|---------|-----------|-----------------|
| named-expert vagueness | "doctors/professors confirmed" with no name | Real citations name people and journals |
| big-institution flex | "Harvard/NASA/FDA proved" | Institutions publish press releases with URLs; borrow-the-name is folklore's cheapest costume |
| military/secret research | "the army secretly studied" | Uncheckable by design; secrecy claims are evidence-shaped holes |

**Settling question:** "Which doctor/study?" — named institutions
publish named people.

### 2. Urgency & suppression (w3 each — the highest-weight family)
| Pattern | Signature |
|---------|-----------|
| they-don't-want-you-to-know | vague powerful "they" suppressing truth |
| censorship imminent | "before this is taken down" |
| share immediately | forwarding quotas (forward to 10...) |
| act-before-you-think | "before it's too late," "hurry" |

Highest weights because **deadlines disable verification — that is
their function**. A message that demands speed is a message that
fears checking. Suppression framing also pre-explains the absence of
sources ("of course there are no news reports — they're suppressing
it"), making it self-sealing.

### 3. Unfalsifiable structure (w1-3)
| Pattern | Signature |
|---------|-----------|
| no-testable-mechanism | energy/vibrations/quantum/toxins with no measurable claim |
| convenient immunity | "only works if you don't test it" |
| ancient-wisdom appeal | "used for thousands of years" |

Unfalsifiable claims arrange to survive being wrong. The immunity
pattern is worth w3 when explicit. Ancient-wisdom is only w1: many
old practices do work (willow bark → aspirin); age alone is weak
evidence either way.

### 4. Causal sleight of hand (w2 each)
| Pattern | Signature |
|---------|-----------|
| correlation-as-cause | "after X, they got sick" |
| single-case proof | "my friend's cousin swears" |
| post-hoc timing | "days later doctors found" |

Sequence ≠ causation; the vivid single case is an anecdote with a
face. The settling question for all three: "what did the comparison
group show?"

### 5. Numeric theater (w2 each)
| Pattern | Signature |
|---------|-----------|
| precise stat, no source | "90% of people" |
| suspicious round numbers | "9 out of 10 doctors" |
| micro-dose scare | "0.5g of X is poison" with no reference dose |

Numbers costume claims as science. Two questions disarm them:
denominator ("90% of whom?") and source ("measured by whom?"). The
micro-dose scare needs a reference dose — the phrase "the dose makes
the poison" (Paracelsus) is the antidote.

### 6. Emotional amplifiers (w2-3)
| Pattern | Signature |
|---------|-----------|
| children at risk (w3) | child-danger framing |
| gruesome detail | graphic imagery replacing data |
| fortune/curse chain | luck mechanics tied to forwarding |

Child-safety framing is the highest-sharing emotion — which is why
folklore wears it constantly. Luck chains are the direct descendants
of letter-writing-era chain letters; the engine is identical, only
the medium changed.

## Scoring model

- Sum weights of matched patterns.
- +2 bonus each time ≥2 patterns hit within one family (clustering
  signals deliberate structure, not sloppy writing).
- Verdicts: STRONG ≥10 or ≥4 families; MODERATE ≥6 or ≥3 families;
  WEAK ≥3; else NO signatures.

Calibration anchors (from the test corpus):
- Classic chain message (authority + quota + suppression + vibe
  mechanism): 10 → STRONG
- Dry scientific report (named cohort, denominators, adjustment
  factors): 0 → NO signatures

## What structural analysis can and cannot do

**Can:** triage, prioritize fact-check effort, generate settling
questions, teach pattern recognition, provide a calm non-confrontational
reply scaffold ("the *shape* of this is folklore" attacks the message,
not the sender).

**Cannot:** prove falsity. Some true stories are badly told
(MODERATE score), and sophisticated disinformation is deliberately
clean-shaped (score 0 — that's what state-adjacent ops spend money
on). Low score must never be quoted as "verified true."

## The settling-question technique

Every pattern carries one question whose answer either resolves the
claim or exposes its emptiness. In practice the questions collapse
to four master questions:

1. **Source:** who exactly says so, named, with a link?
2. **Denominator:** percentage/frequency of *whom*, measured how?
3. **Comparison:** what did the control/comparison group show?
4. **Mechanism:** one sentence, with quantities, how does it work?

A claim that survives all four is worth a real fact-check. A claim
that dodges all four is folklore regardless of its truth value.

## Family-chat diplomacy notes

- Attack the pattern, not the person: "this has the classic shape"
  not "you fell for fake news."
- Offer the questions, not the verdict: senders respond better to
  "which study?" than "false."
- Save your credibility for STRONG scores; let WEAK ones pass with
  a question mark.
- The `stats` mode doubles as a teaching tool: showing a parent
  "urgency & suppression dominates what you forward me" lands better
  than any lecture.
