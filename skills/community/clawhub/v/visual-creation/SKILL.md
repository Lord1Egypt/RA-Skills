---
name: "visual-creation"
description: "Turn one visual brief into a visual creation set: a poster and matching stills that keep the same subject, palette, and type. Visual creation lays out what each frame shows, then makes the poster and stills. Use it for a brand look, a poster series, and a set of pictures that have to belong together."
---

# Visual Creation

## What you get

- A frame plan: what the poster shows, and what each matching still shows.
- One poster.
- The stills you confirm, held to the same subject, palette, and type as the poster.
- One short motion cut of the poster, with an instrumental sting already in it.

## Ways to run it

- Poster, stills, and motion. The default.
- Plan only. Strike the frames on the card.
- Poster and stills. Strike the motion cut.

Open this when the job is a set of pictures that have to look like one family, and a short motion of the poster to post with them.

## Scope and adjacent routes

Use this route when the job is a set of pictures that have to look like one family. A product listing set with a clip belongs on a product-asset workflow. An event kit with a spoken read and a jingle belongs on an event-kit workflow.

## Inputs and defaults

The hard input is the visual brief: the subject and the feeling of the set. Ask only for that. Default to a vertical 3:4 poster, three square or 4:5 stills, a motion cut of about four seconds, and one instrumental sting. Keep type, palette, and subject consistent across the set. Do not invent a campaign, a store listing, or a review.

## Golden path

1. Write the frame plan and show it. This writing is free.
2. Upload a reference with `beatra.assets.upload` when one is supplied. The poster is one `beatra.images.generate` after `beatra.models.list` with `{"capability": "text_to_image"}` when there is no reference, or one `beatra.images.transform` after `{"capability": "image_to_image"}` when there is. Pass the artifact. Do not send a reference into `beatra.images.generate`.
3. Each confirmed still is one `beatra.images.transform` from the accepted poster. One `beatra.images.edit` after `{"capability": "image_edit"}` repairs a still that broke the palette or the subject.
4. One `beatra.music.generate` after `{"capability": "text_to_music"}` writes the sting. These slots are the materials card.
5. On the video card, one `beatra.videos.animate` after `{"capability": "image_to_video"}` from the poster. Then one `beatra.videos.compose` lays the sting under the motion. Poll with `beatra.tasks.get` and deliver the set plus `billing.net_charged_credits`.

## Decisions that require confirmation

Planning and the written deliverable are free. They are not approval.

Before every paid call, show a current production card and wait:

1. Work — what will be made, in the user's words, and whether this call is a generate or a lookup.
2. Credits — the live price just read from the model card. Do not reuse a remembered number.
3. Count — one paid call per slot. The materials card may list the poster, the stills, and the sting; each slot has its own `client_request_id`. The motion cut waits for its own card.
4. Identity — one new opaque `client_request_id` per call. A changed prompt, file, model, or control mints a new ID.
5. If we stop here — the free writing remains usable.
6. If the balance is insufficient — relay the official message and its top-up URL. Do not retry until the user says they have topped up.

A lookup and a generate are two cards. Approved pictures and music do not authorize the motion cut. Invoke every remote Beatra tool only through the bundled `scripts/mcp_client.py`. The tool name is the command argument and the JSON arguments are the standard input. Do not configure, call, or use a host Beatra Connector. Do not use REST/OpenAPI as a fallback.

If a create response is lost, retry only the identical payload and the same `client_request_id`. If the task id is lost, call `beatra.tasks.list`, then `beatra.tasks.get`, and match the frozen request before any identical retry. Call `beatra.tasks.cancel` only when the user asks to cancel, then confirm that task with `beatra.tasks.get`.

When the user asks how many credits remain, call `beatra.wallet.get`. When they ask what was charged, call `beatra.wallet.ledger`.

## References by task

Read [the scenario workflow](references/workflow.md) for the payloads and a worked set.
Read [answers when a run goes wrong](references/faq.md) when a task stalls, a response is lost, a price looks wrong, or a still left the family.
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
