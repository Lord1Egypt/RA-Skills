# Comparison Output Template

Structure for the document produced by `ux-compare`. Write to `docs/ux-comparisons/<topic>-YYYY-MM-DD.md`.

Topic slug matches the scope: `empty-states`, `onboarding`, `keyboard`, `destructive-actions`, `modals`, `whole-app`, etc.

```markdown
# UX Comparison: [Topic]

**Date**: YYYY-MM-DD
**Scope**: [What this comparison covers — specific feature, category, or whole-library]
**Compared**:
- [app-1]  (extracted YYYY-MM-DD)
- [app-2]  (extracted YYYY-MM-DD)
- [app-3]  (extracted YYYY-MM-DD — ⚠ stale, re-extract recommended)
**Source libraries**: `docs/ux-extracts/[app-1]/`, `docs/ux-extracts/[app-2]/`, etc.

## At a glance

[2–3 sentences: the headline findings. What converges? What diverges? What's surprisingly absent?]

## Convergence (strong signal)

Where most or all of the compared apps agree. These are defensible defaults — following them means users won't feel lost.

- **[Pattern]**: [how it's handled across the set, one sentence]
- **[Pattern]**: [...]

## Divergence (design decisions)

Where apps genuinely differ. Each divergence is a tradeoff — pick based on your context.

### [Pattern with divergence]

- **[App A]**: [what they do]
- **[App B]**: [what they do]
- **[App C]**: [what they do]

**Tradeoff**: [one sentence explaining when you'd pick each approach]

### [Another pattern]
[...]

## Unique approaches

Patterns only one app in the set uses. Call them out — either innovation worth borrowing, or weirdness worth avoiding.

- **[App]** — [pattern]. [Why they probably do it; whether it's borrowable]

## Absent across the set

What none or few of these apps do. Notable because it surfaces design *decisions by omission*.

- **[Absence]**: [X of N apps skip this]. [Interpretation — deliberate, convention, or overlooked?]

## Pattern-by-pattern detail

For each pattern category in scope, one section. Use this structure:

### [Pattern category, e.g. Empty list state]

**What each app does:**

- **[app-1]**: [concrete description — verbatim copy, layout, CTA behaviour]
  - *Source*: [path or anchor to the library entry, e.g. `ux-extracts/claude-ai/pattern-library.md#empty-states`]
- **[app-2]**: [...]
- **[app-3]**: [not covered in the extract — coverage gap]

**Convergent**: [what's shared across the set]

**Divergent**: [where the apps split]

**Unique**: [if any]

**Missing**: [if any app's library doesn't cover this]

### [Next pattern]
[...]

## Recommendations

This is the reason to have run the comparison. State positions. If you hedge here, the document is just a pile of bullets.

### For a new build in this space

1. **Safe default**: [the convergent choice — use this unless you have reason not to]
2. **Consider**: [divergent option A] — trades [benefit] for [cost]
3. **Consider**: [divergent option B] — trades [benefit] for [cost]
4. **Skip**: [unique approaches you'd avoid, with the reason]
5. **Fill a gap**: [absences worth addressing because your users would benefit]

### For an existing build in this space

- **Convergence you're missing**: [patterns common across references but not in your app]
- **Divergence worth reviewing**: [places your app does something unusual — is the reason still valid?]
- **Unique strengths**: [if your app already does something no reference does well, note it]

## Source library health

| Library | Extracted | Coverage for this comparison | Staleness risk |
|---------|-----------|----------------------------|----------------|
| [app-1] | YYYY-MM-DD | Full / Partial / Missing | Fresh |
| [app-2] | YYYY-MM-DD | Full | ⚠ 4 months — re-extract |

## What this comparison doesn't tell you

Be explicit about the limits:

- [e.g. "Performance was not captured in any extract — if speed is a key criterion, test directly."]
- [e.g. "Mobile patterns less thoroughly extracted for [app-3] — findings there may be partial."]
- [e.g. "All extracts used paid-tier accounts; free-tier UX may differ."]
```

## Guidelines for writing the comparison

- **Synthesise, don't list.** If you're just copying bullets from 5 libraries, you're not comparing — you're collating. The value is the *convergent / divergent / unique / absent* framing.
- **Be opinionated in recommendations.** *"It depends"* is the weakest possible output. State a position.
- **Cite sources.** Link to the specific section of the pattern library file. `ux-extracts/claude-ai/pattern-library.md#empty-states` is enough. Don't re-embed screenshots — the extract is the single source of truth.
- **Flag coverage gaps honestly.** "Not covered in app-3's extract" is not the same as "app-3 doesn't do this". One is a library gap, one is an app decision.
- **Date everything.** Both the comparison itself and each source library. Comparisons decay as fast as the libraries they're built on.
- **When app extracts are stale**, note it prominently — don't just mention it in the source table. Recommendations based on 6-month-old extracts should come with a qualifier.
- **Limit scope for sharpness.** A focused "empty states across 4 apps" is more useful than "whole-library comparison across 7 apps". Narrow wins.
