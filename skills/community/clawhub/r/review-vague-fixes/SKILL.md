---
name: review-vague-fixes
description: Review comments are unactionable — "improve this", "handle errors", "refactor" without specifics or suggested alternatives.
emoji: 👀
metadata:
  clawdis:
    os: [macos, linux, windows]
---

# review-vague-fixes

A review that says "this needs work" without saying what work is a cost on the author, not a contribution. The author has to either guess what the reviewer meant or push back and ask — both eat time and erode trust.

## Symptoms

- Comments like "refactor this", "improve error handling", "make this cleaner" with no example.
- Blanket style gripes on a change that was explicitly about functionality.
- "I don't like this" with no reason and no alternative.
- Comments that could apply to any file in the codebase — no specificity to what's in front of the reviewer.

## What to do

- Every review comment should state *what* to change, *where*, and *why*. If you can't say why, you probably don't have a concrete objection.
- When you want a refactor, give an example: paste the shape you'd prefer, or point at a similar pattern elsewhere in the codebase.
- Distinguish blocking from nice-to-have. Mark must-fix clearly; leave nitpicks labeled as such.
- Reference the exact line, symbol, or behavior. "In `processOrder`, the retry loop won't back off" beats "improve this function".
- If you don't know the right fix, say so — "this concerns me because X; not sure what the right answer is" is honest and inviting, unlike a vague demand.
