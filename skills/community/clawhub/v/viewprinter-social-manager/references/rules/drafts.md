# drafts: The word means two unrelated things

## Priority: HIGH

## What goes wrong

The user says "save it as a draft" and gets the opposite of what they meant —
either content sitting on a public platform when they expected it held back, or
nothing anywhere when they expected it staged on the platform.

## The two meanings

- **`draft: true` on the post holds it in ViewPrinter.** Nothing is queued and
  nothing reaches any platform. `posts_save` with its `post_id` and
  `draft: false` sends it.
- **The per-platform `draft` option inside `platform_options` uploads to the
  platform** for a creator to finish there.

These are unrelated. The first sends nothing anywhere; the second puts content
on the platform.

## What to do

Confirm which the user means before choosing. If the request is ambiguous —
and "save it as a draft" always is — ask, naming both outcomes in plain words
rather than in tool arguments.

## Context

- A held draft still needs approval when it is released. See `scheduling`.
