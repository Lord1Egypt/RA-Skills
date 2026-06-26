# Operational Hardening

These are generic lessons for making an X automation system more reliable in live mode.

## 1. Treat replies as higher-risk than normal posts
Even if normal posts work, replies may fail because of:
- reply restrictions on the target tweet
- account-level limitations
- endpoint-specific behavior differences

## 2. Validate reply targets before publishing
Before sending a reply, check whether the target tweet is reply-open if your tooling supports it.
If you cannot validate directly, prefer safer reply targets such as:
- mentions
- users already interacting with the account
- clearly open discussions

## 3. Never let one failed reply block the pipeline
If a reply slot fails permanently, mark it as skipped and continue to the next eligible slot.
Do not keep retrying the same blocked reply forever.

## 4. Store publish outcomes explicitly
For every publish attempt, record:
- slot kind
- text preview
- target/source URL if relevant
- success/failure
- tweet id if successful
- error reason if failed

## 5. Keep failure classes separate
Use different states for:
- posted
- skipped
- failed (temporary)
- failed (permanent)

This makes debugging and retry behavior much easier.

## 6. Prefer fallback behavior
If a reply cannot be posted, the system should be able to continue with:
- another reply candidate
- a normal post slot
- or a clean skip for that window

## 7. Build idempotent slot keys
Do not build publish de-duplication keys from mutable draft text.
Use stable fields such as:
- local date
- slot name
- kind/type
- source URL (if any)
- target time

This prevents tiny text rewrites from bypassing de-dup and causing same-source repost loops.

## 8. Add anti-repetition guardrails
Before final slot assignment, compare candidate drafts against recent posted previews (for example last 48h).
If similarity is high, defer that candidate and prefer a different source/angle.
Also limit over-concentration on the same top tag in the same day.

## 9. Make live mode observable
A live system should always be able to answer:
- what was supposed to post?
- what actually posted?
- what failed?
- what was skipped?
- why?
