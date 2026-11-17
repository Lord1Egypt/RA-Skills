# Journal Format

The full format for a session journal entry (see `SKILL.md` Step 2). Seven required
sections, in order. None are optional — a journal missing one of these is an
incomplete close, not a shorter one.

## Summary
3–5 sentences of prose. What happened, what shipped, what was decided this session.

## Session Fingerprint
One sentence. A behavioral snapshot — tone, judgment, pushback, drift from the norm.

## One Thing I'd Do Differently
One specific, self-caught reasoning failure from this session. Never "none" — the
point of this field is surfacing something that would otherwise go unexamined. If
nothing comes to mind immediately, look harder before writing it off.

## Files Accessed
Every file touched this session — read, written, or both. No sampling; if it was
touched, it's listed.

## What Shipped
Everything that went live, was committed, or was sent externally this session.

## Decisions Made
Any decisions that are now locked in — a direction chosen, an approach ruled out, a
scope boundary set.

## Open Threads
Mandatory. Never blank. If there is genuinely nothing open, write "None" explicitly
rather than omitting the section.

---

## Example

```markdown
# Session Journal — 2026-01-14

## Summary
Reviewed and merged the onboarding flow PR. Fixed two edge cases found in manual
testing — empty-state rendering and a race condition on the submit button. Deferred
analytics instrumentation to next session per the user's request.

## Session Fingerprint
Direct and technical throughout; pushed back once on a proposed shortcut that would
have skipped error handling, and the user agreed to do it properly instead.

## One Thing I'd Do Differently
Assumed the test suite already covered the empty-state case without checking first —
it didn't, and the bug reached staging before being caught in manual review. Should
have grepped for existing test coverage before assuming it existed.

## Files Accessed
- src/onboarding/Flow.tsx (read, written)
- src/onboarding/Flow.test.tsx (written)
- src/api/submit.ts (read)
- CHANGELOG.md (written)

## What Shipped
- PR #142 merged to main
- CHANGELOG.md updated

## Decisions Made
- Analytics instrumentation deferred to next session, not this one

## Open Threads
- Analytics instrumentation still pending
- Race condition fix should be backported to the v1 branch — not yet scheduled
```
