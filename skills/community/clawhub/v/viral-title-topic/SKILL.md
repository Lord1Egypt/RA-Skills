---
name: "viral-title-topic"
description: "Turn a product, an account, or posts you paste into title options and a topic list grounded in what people are already publishing. This title and topic workflow reads public posts on Douyin, Xiaohongshu, TikTok, and X when you want a live read, then writes hooks and titles you can shoot today. Use it for trend titles, topic selection, and the next post on an existing account."
---

# Viral Titles and Topics

## What you get

- A topic list grouped into angles you can shoot today.
- Three titles and one spoken hook for the angle you pick. Each title quotes a line you actually used.
- One cover still that carries the chosen title and still reads at thumbnail size.
- One short hook clip: that cover, moving, with the hook spoken on it and the title as a subtitle.

## Ways to run it

- From what you paste. Titles and topics from posts, comments, or a hot list you already copied. No lookup.
- From a live read. One confirmed lookup on Douyin, Xiaohongshu, TikTok, or X, then the same title sheet. Comments are their own lookup when the titles should use words people wrote.
- Titles only. Strike the cover and the clip on the card.

Open this when someone needs today's title and a hook they can post, not a multi-shot script.

## Scope and adjacent routes

Use this route to decide the title and leave with the hook. A multi-shot script and a full clip belong on a script workflow. Rewriting one finished piece onto several platforms belongs on a rewrite workflow.

## Inputs and defaults

The hard input is the subject: a product, an account, or the posts you paste. Ask only for that. Default to five topics and three titles on the one angle you pick, a 3:4 cover when the destination is Xiaohongshu and 9:16 otherwise, and one hook clip from that cover. Do not run a lookup when the user already pasted the evidence.

## Golden path

1. If the evidence is pasted, write the topic list and titles. This writing is free.
2. If a live read is required, search with `beatra.social.tools.search`, read the operation with `beatra.social.tools.get`, copy the `schema_hash` it just returned, show a lookup card, and call `beatra.social.execute` once. Allowed keys are `social.douyin.hot_search.list`, `social.douyin.video.search`, `social.douyin.video.comments.list`, `social.xiaohongshu.note.search`, `social.xiaohongshu.note.comments.list`, `social.tiktok.hashtag.trends.list`, and `social.twitter.trends.list`.
3. Write the titles from the returned lines or the pasted lines. Quote the line you used. Do not invent counts.
4. Upload a photo with `beatra.assets.upload` when one is supplied. The cover is one `beatra.images.generate` after `{"capability": "text_to_image"}` when there is no photo, or one `beatra.images.transform` after `{"capability": "image_to_image"}` when there is. One `beatra.images.edit` after `{"capability": "image_edit"}` sets the exact title on a clear band.
5. Pick a ready voice with `beatra.voices.list` and submit one `beatra.speech.synthesize` after `{"capability": "text_to_speech"}` for the hook line. These slots sit on the materials card.
6. On the video card, one `beatra.videos.animate` after `{"capability": "image_to_video"}` from the cover, with the hook as `driving_audio` and a model that admits it. Then one `beatra.videos.compose` burns the title as a subtitle and keeps the hook's sound. Poll with `beatra.tasks.get`.

## Decisions that require confirmation

Planning and the written deliverable are free. They are not approval.

Before every paid call, show a current production card and wait:

1. Work — what will be made, in the user's words, and whether this call is a generate or a lookup.
2. Credits — the live price just read from the model card or from `beatra.social.tools.get`. Do not reuse a remembered number.
3. Count — one paid call per slot. The materials card may list the cover, the title repair, and the hook line; each slot has its own `client_request_id`. A later lookup page is another call. The clip waits for its own card.
4. Identity — one new opaque `client_request_id` per call. A changed prompt, file, model, or control mints a new ID.
5. If we stop here — the free writing remains usable.
6. If the balance is insufficient — relay the official message and its top-up URL. Do not retry until the user says they have topped up.

A lookup and a generate are two cards. Approved covers and lines do not authorize the clip. Invoke every remote Beatra tool only through the bundled `scripts/mcp_client.py`. The tool name is the command argument and the JSON arguments are the standard input. Do not configure, call, or use a host Beatra Connector. Do not use REST/OpenAPI as a fallback.

If a create response is lost, retry only the identical payload and the same `client_request_id`. If the task id is lost, call `beatra.tasks.list`, then `beatra.tasks.get`, and match the frozen request before any identical retry. Call `beatra.tasks.cancel` only when the user asks to cancel, then confirm that task with `beatra.tasks.get`.

When the user asks how many credits remain, call `beatra.wallet.get`. When they ask what was charged, call `beatra.wallet.ledger`.

## References by task

Read [the scenario workflow](references/workflow.md) for the lookup keys, the clip payload, and a worked title.
Read [answers when a run goes wrong](references/faq.md) when a task stalls, a response is lost, a price looks wrong, or the title on the cover came back wrong.
Read [installation and authentication](references/installation-and-auth.md) when the connection is not ready.
Read [installation registration](references/installation-registration.md) for first-use registration.
Read [Bundled MCP Client diagnostics](references/mcp-connection.md) when a call fails before a task exists.
Read [tasks and results](references/tasks-and-results.md) when a task is queued, running, or missing.
Read [billing, errors, and recovery](references/billing-errors-and-recovery.md) when a charge, a refund, or a lost response needs the shared rules.
Read [uninstall and disconnect](references/uninstall-and-disconnect.md) when the user wants to stop and remove the connection.

## Updates and security

This Skill runs only the files installed with it and leaves them unchanged while
it runs; it never downloads or executes other code. It talks to Beatra's official
services over HTTPS, and a file you choose to upload goes only to the one-time
upload address Beatra issues for it.

Once a day at most, the bundled client reads Beatra's public version list. When
the store or tool you installed from has a newer version, it prints one line with
the command that updates it there. Updating stays your choice, through that store
or tool. See [updates and security](references/updates-and-security.md).
