# Diagnostic Rules — Full Reference

This document explains every rule-based check in `scripts/checkup.py`, why
the threshold was chosen, and how to tune it for your own portfolio.

## 1. Trust Check (`moderation`)

| Verdict | Severity | Meaning |
|---------|----------|---------|
| `clean` | — (no finding) | Healthy, no action needed |
| `pending` | `info` | Scan still running, recheck later |
| `suspicious` | `critical` | Flagged for review — surface immediately |
| `malware` | `critical` | Blocked — highest priority, fix and resubmit |

**Why critical**: a moderation issue affects discoverability and trust
immediately, regardless of how good the underlying metrics look. It always
outranks growth concerns.

## 2. Conversion Check (`conversion`)

```
ratio = installs_all_time / downloads
```

- Only evaluated when `downloads >= 20` (below that, the ratio is too noisy
  to mean anything — a single early adopter can swing it wildly).
- Default threshold: `ratio < 0.05` (i.e. fewer than 1 in 20 downloaders
  install) triggers a `warning`.

**Tuning**: if your skill is something people browse out of curiosity (e.g.
a reference/example skill) rather than something they install, this
threshold may be too aggressive — raise it or disable the check for that
slug.

**Why this matters**: downloads measure curiosity, installs measure
adoption. A large gap usually means the listing oversells or under-explains
— the description promises something the README/setup doesn't deliver
quickly enough.

## 3. Staleness Check (`staleness`)

Compares `version` field across runs. If unchanged for more than
`STALENESS_DAYS_WARN` (default: 90 days) while downloads are still growing,
flags a `warning`.

**Why this matters**: an actively-downloaded skill with no updates signals
either (a) it's genuinely finished and stable, which is fine, or (b) it's
stagnant and accumulating unaddressed issues. Skill Doctor can't tell these
apart automatically — it flags so a human can decide.

*Note: the current implementation tracks version changes via state
snapshots; a skill needs at least two check-up runs spanning the staleness
window before this rule can fire meaningfully.*

## 4. Momentum Check (`momentum`)

Pure delta reporting — compares current snapshot to the last stored one:

- Downloads increased → `info`, positive momentum noted
- Downloads flat → `info`, flagged as flat (not automatically bad, just
  worth noting if it persists across several runs)

This check never produces `warning` or `critical` on its own — momentum is
context, not a verdict.

## 5. Active-Install Drop Check (`risk`)

```
drop_pct = (previous_active - current_active) / previous_active
```

- Only evaluated when `previous_active >= 5` (avoids false alarms from
  tiny absolute numbers, e.g. 2 → 1 is a 50% drop but meaningless at that
  scale).
- Default threshold: `drop_pct >= 0.25` triggers `critical`.

**Why critical, not warning**: active installs dropping while total
installs stays flat means people are actively uninstalling — this is a
stronger and more urgent signal than a slow download trickle. It usually
means a recent version broke something.

## Adding a New Rule

1. Add the check inside `diagnose()` in `checkup.py`
2. Append a `findings.append({...})` entry with `category`, `severity`,
   `text`
3. If it should drive a prescription, add a matching branch in
   `prescribe()`
4. Document the new rule here with rationale and threshold

Keep the core engine generic — avoid hardcoding values specific to one
project's skills. Thresholds should be reasonable defaults that work across
different portfolios, not tuned to a single use case.
