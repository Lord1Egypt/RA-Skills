# Session Note — Skill Release Lifecycle Draft (2026-05-24)

## Context

The user redirected the original `agent-skill-publishing-kit` draft into a broader class-level lifecycle skill named `skill-release-lifecycle`.

## Durable Lessons

1. **Name matters for routing and expectation-setting.**
   - `agent-skill-publishing-kit` sounded like a publishing tutorial.
   - `skill-release-gate` over-emphasized pre-release checks.
   - `skill-release-lifecycle` correctly communicates the full loop: pre-release gate, release verification, feedback classification, version-bump decision, re-release, changelog, and iteration.

2. **This class is a quality lifecycle, not a command tutorial.**
   - Do not merge `clawhub-auto-publish` command details into this skill.
   - Use `clawhub-auto-publish` only as the detailed execution manual for actual publish mechanics.

3. **Pre-release quality gates must not use distribution metrics.**
   - Downloads, stars, homepage placement, and search ranking are post-release signals only.
   - They should not decide whether a skill deserves publication.

4. **Public skills need stricter proof than local skills.**
   - Keep the threshold at at least 3 non-trivial real or dogfood runs.
   - Require at least 2 distinct input scenarios.
   - Require at least 1 output that was actually used, copied, published, or turned into action.
   - Require at least 1 observed issue, edge case, failure, unclear boundary, or UX observation; if none appeared, say so explicitly.

5. **Anti-scope is mandatory for public release.**
   - A narrow-feeling scope is not enough.
   - Public skills must include an explicit `What This Will Not Do` or equivalent anti-scope section.
   - Missing anti-scope is an Identity HARD Fail.

6. **Do not return an empty response after tool calls.**
   - In this session, the assistant twice executed tool calls and then returned an empty final response.
   - For skill/library maintenance tasks, tool results must be processed into a concise status report before ending the turn.

## Files Created in the Draft

- `SKILL.md`
- `references/publish-gate-example.md`
- `references/iteration-loop-example.md`
- `references/buffett-do-mini-example.md`

## Preferred Future Shape

Keep this as a class-level umbrella skill with rich `SKILL.md` and concise references. Do not split into narrow one-session skills.
