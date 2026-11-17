---
name: "Changelog Writer"
description: "Turn a list of raw commit notes or release bullet points into a clean, user-facing changelog. Documentation-only skill with no executable code or network access."
version: "0.0.1"
---

# Changelog Writer

This skill rewrites rough engineering notes into a changelog that end users can actually read. It is documentation only: no scripts, no subprocesses, no network requests, no file-system operations beyond reading what the user pastes in.

## When to use it

Use it when:

- A release is about to ship and the commit log is a mix of `fix:`, `chore:`, and half-finished sentences.
- A support person needs a plain-language summary of what changed between two versions.
- A project manager needs a "what's new" block for a store listing or release page.

Do not use it for writing marketing copy, pricing pages, or legal text.

## How it works

1. Read the whole input first. Do not paraphrase line by line; group by user-visible effect.
2. Classify each item into one of five buckets: New, Improved, Fixed, Changed, Removed.
3. Drop anything that has no user-visible effect, such as internal refactors, test-only changes, or CI tweaks.
4. Rewrite each surviving item from the user's point of view. "Refactor auth module" becomes "Sign-in is faster and no longer drops the session on slow connections".
5. Keep the order stable: New, Improved, Fixed, Changed, Removed. Within a bucket, put the most impactful item first.

## Output format

Produce markdown with a single `##` heading per bucket, and one bullet per item:

```markdown
## New
- Dark mode is available from the settings panel.

## Improved
- Search returns results roughly twice as fast on large libraries.

## Fixed
- The window no longer resets its size after a restart.
```

## Style rules

- One sentence per bullet. If a bullet needs a second sentence, it is usually two changes and should be split.
- Lead with the verb or the noun the user cares about, not with "We".
- No version numbers inside bullets. The heading carries the version.
- No vague words such as "various", "several", "some improvements". Name the thing.
- If an item cannot be explained without internal jargon, rewrite it until it can, or drop it.

## Edge cases

- If the input is empty, say so plainly instead of inventing changes.
- If two bullets describe the same change, merge them and keep the clearer wording.
- If a change is user-visible but embarrassing, still list it under Fixed, described neutrally.
- If the user asks for a specific bucket that has no items, omit that bucket entirely.

## What this skill will not do

- It will not guess at changes that are not in the input.
- It will not add a "security" section unless the input explicitly mentions a security fix.
- It will not produce a changelog longer than the input justifies.
