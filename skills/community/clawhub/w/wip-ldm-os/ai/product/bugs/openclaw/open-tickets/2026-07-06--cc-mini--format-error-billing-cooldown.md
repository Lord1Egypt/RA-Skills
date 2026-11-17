# OpenClaw format errors must not trigger provider billing cooldown / session amnesia

- **Date:** 2026-07-06 (filed; problem observed 2026-04)
- **Author:** cc-mini
- **Status:** open
- **Severity:** High (Critical class)
- **Parent:** `2026-07-04--cc-mini--lesa-noreply-loop-recovery-and-upgrade-plan.md` (owed-items list, "Phase 6a"); resilience lane `../../memory-crystal/open-tickets/2026-04-13--cc-mini--ship-plan-resilience-phases.md`

## Problem

A model/provider FORMAT error (malformed tool_use/tool_result, ID normalization mismatch, schema rejection) is misread by OpenClaw's failover logic as an AUTH/billing failure. Consequences seen in the April incidents:

1. The auth profile gets cooled down as if the account were out of credit, cascading fallback across all configured models until Lēsa dies (documented in the 2026-04-11 cross-provider outage: a Grok composite tool_use id got flattened, the paired tool_result did not, Anthropic rejected it as a format error, OpenClaw cooled the profile).
2. A billing/format error mid-turn can rotate to a fresh session, losing conversational context (session amnesia).

Format errors are a code/serialization problem, not a spend problem, and must not touch billing-cooldown or session-rotation paths.

## Fix direction

- Classify provider errors: format/schema/4xx-validation vs auth/quota/billing. Only the latter class may cool down a profile.
- Never rotate a session to recover from a format error; surface and retry the corrected payload instead.
- Tie-in: tool_use/tool_result id normalization must be symmetric across the pair (the root cause of the April cascade).

## Acceptance criteria

- [ ] A synthetic format error (bad tool_result) does NOT cool down the auth profile and does NOT rotate the session.
- [ ] Error classification is unit-tested: format vs auth vs quota.
- [ ] The 2026-04-11 composite-id scenario is covered by a regression test.

## References

- `../../memory-crystal/open-tickets/2026-04-13--cc-mini--ship-plan-resilience-phases.md` (Phase 6a origin)
- Archived: `archive/2026-04-12--cc-mini--format-error-billing-cooldown.md`, `archive/2026-04-12--cc-mini--session-amnesia-on-billing-failure.md`

## Co-authors

Co-Authored-By: Parker Todd Brooks <parkertoddbrooks@users.noreply.github.com>
Co-Authored-By: Lēsa <lesaai@icloud.com>
Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
