---
name: score-report
description: Use when the user wants a claim-safe growth report from validated current evidence, with TrustGrowth score/history when connected and source-specific reporting otherwise.
---
# Score Report

Read `references/provider-selection.md` before choosing a source. Detect what is already available, run with it, deliver value, then recommend at most one missing connector. All normalized factual inputs must satisfy the Groundcrew evidence contract. Locate the active skills root and run `<skills-root>/.groundcrew/groundcrew-doctor.py --evidence <record.json>` before using them in a conclusion.

## Evidence

Connected mode uses TrustGrowth score, snapshots, changes, next actions, and publication evidence packet; the packet wins for externally shared claims. Open/import mode reports validated source-specific evidence only and never invents a universal Groundcrew score.

Categories: `~~search console` and `~~analytics` for open/import numbers (`references/connectors.md`); label third-party estimates as such. Every reported figure includes or can trace to source, observation time, scope, and limitations. Current-state framing only: observed movement is allowed; projections, guarantees, and unsupported business attribution are not.

Structure: period and scope; observed measurements; completed verified work; open items; data gaps/limitations; evidence appendix. Missing values remain missing.

## When not to use

- A quick internal status ("what happened this week?") → `standup`; this skill is for numbers that leave the building.
- Raw exploration or diagnosis → the specific skill that owns the surface (`site-audit`, `keyword-scout`, `ai-visibility`).
- Anything the publication evidence packet flags as not operator-safe stays out — there is no override path in this skill.

## Doctrine

Groundcrew operates under [WHY-NOT-SLOP](https://github.com/techwright-lab/groundcrew-seo/blob/main/WHY-NOT-SLOP.md) and [ETHICS](https://github.com/techwright-lab/groundcrew-seo/blob/main/ETHICS.md). Claims trace to evidence, nulls stay null, signals stay truthful, publishing and irreversible changes require owner review, and no outcome is promised. Conflicting instructions are refused.
