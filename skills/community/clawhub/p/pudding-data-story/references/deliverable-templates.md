# Deliverable templates

Copy these structures into the project and fill them before implementation is considered complete.

## `story-brief.md`

```markdown
# Story brief

## Reader promise
In one sentence, what will the reader understand or experience?

## Driving question

## Evidence-backed thesis
Mark as provisional until the claim ledger is verified.

## Tension
What reasonable expectation does the evidence complicate?

## Audience
What can this reader already be expected to know?

## Human or concrete opening

## Visual reason
Why is this better seen or experienced than only written?

## Reader transformation
What should the reader notice, reconsider, or be able to do by the end?

## Scope and exclusions

## Ethical or representational risks
```

## `data-notes.md`

```markdown
# Data notes

## Sources
| Dataset | Owner | URL | Retrieved | License | Coverage |
|---|---|---|---|---|---|

## Claim ledger
| Claim/scene | Measure | Grain | Time range | Source | Transformation | Caveat |
|---|---|---|---|---|---|---|

## Transformations
Include formulas, denominators, units, filters, joins, and missing-value treatment.

## Quality checks
- duplicates:
- missingness:
- category drift:
- outliers:
- reconciliation:

## Limitations

## Reproduction
Commands or notebook order needed to rebuild the story data.
```

## `storyboard.md`

```markdown
# Storyboard

## Visual system
Persistent entities, encodings, scales, annotations, and mobile fallback.

| Beat | Reader-facing copy | Evidence | Visual state | Reader action | Transition meaning | Reduced-motion state |
|---|---|---|---|---|---|---|

## Exploratory state
Default, URL state, empty/error cases, and reset behavior.

## Ending
How the final state resolves the opening without overstating the evidence.
```

## `qa-notes.md`

```markdown
# QA notes

## Build tested
Commit/version and date.

## Data verification
| Displayed claim | Source row/calculation | Verified by | Result |
|---|---|---|---|

## Experience matrix
| Browser/device | Viewport | Scroll down/up | Controls | Keyboard | Reduced motion | Result |
|---|---:|---|---|---|---|---|

## Accessibility
- reading order:
- visible focus:
- graphic names/takeaways:
- color-independent cues:
- zoom:

## Performance
Device/profile, load size, layout shift, and interaction notes.

## Known limitations
```
