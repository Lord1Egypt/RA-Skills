# platforms-first: Ask what each platform accepts, never recall it

## Priority: CRITICAL

## What goes wrong

A post is composed against remembered limits — a caption length, a media count,
"Instagram takes video" — and the server refuses it. The refusal arrives after
the work is done, and the guess at why is usually wrong.

Worse, a limit written into this file is true until the day it is not. Platforms
change what they accept, and a new platform can be added without this file
changing. Anything stated here is a claim with an expiry date.

## What to do instead

Call `platforms_list` **first**, naming the platforms you intend to post to.

With no arguments it returns every platform that can publish, with its accepted
media kinds, counts and caption limit. Naming platforms adds recommended sizes
and durations, the per-platform options, and the quirks that change how a post
is treated.

This is cheaper than composing a post, having it refused, and guessing.

## A capability exists, but one connection rejects it

The live capability response and a client's loaded tool schema can be different
versions. Compare the exact option and enum in `platforms_list` with the current
tool declaration. Distinguish stale displayed help from an actual runtime error.

- Scope an error to the connection that returned it. One connector rejecting an
  option does not establish a ViewPrinter or social-platform outage.
- After a connection refresh, rediscover the available tools. An updated,
  authenticated MCP connection may expose an option an older connector lacks.
  Confirm its declaration and access to the intended account before using it.
- Check structured errors and `isError` before reading a success payload. An
  `additionalProperties` validation failure is not a saved or queued post.
- A workspace permission restriction is not a stale-schema workaround: ask for
  an authorized refresh or correction rather than bypassing that restriction.
- Retry the same approved intent with the same idempotency key, checking for an
  existing post first if the prior result was ambiguous. Never drop the rejected
  option if doing so changes who sees the content or how it is published.

For a newly exposed publishing option, validate an authorized request as a held
`draft: true` post first. Preserve the exact request and accepted response, then
release that same draft only when publication is already approved. A held draft
does not prove the downstream platform will accept delivery; verify it separately.
If no authorized connection supports the option, report the specific blocker
with both schema versions rather than substituting a different post type.

## Three shapes that eliminate whole plans

Check these against `platforms_list` rather than trusting the summary here, but
know they exist, because each rules out an approach before you start:

- **A post is either a video or a set of images, never both.** There is no
  arrangement of `media_ids` that mixes them.
- **At least one platform cannot post images at all** and needs a video.
- **At least one platform accepts a caption with no media**, and the others
  refuse a text-only post.

`platforms_list` says which is which. Do not name them from memory.

## Context

- Applies before every compose, not once per conversation.
- `platform_options` keys are per platform and an unknown key is refused rather
  than ignored — `platforms_list` is where you learn what is valid.
