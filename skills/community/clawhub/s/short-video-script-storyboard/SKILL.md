---
name: "short-video-script-storyboard"
description: "Turn a topic, product, or audience note into a shootable short-video script and storyboard frames. This short video script and storyboard workflow confirms who it is for and the selling point, writes the hook, spoken lines, and shot list, then renders one still per shot. Use it for product clips, creator series, and shop videos when you need the script and the frames before anyone films or animates."
---

# Short Video Script and Storyboard

## What you get

- A one-page brief: audience, selling point, and the promise of the clip.
- A script with three hook options, spoken lines, on-screen text, and a shot list. The first shot is the hook, and it has to read with the sound off.
- One vertical still per shot. A product photo, when you supply one, is the product in every still.
- One spoken read of the chosen script, one instrumental bed, and one vertical clip joined from those shots, with the read, the bed, and subtitles already in it.
- The script and the stills on their own, if you stop before the clip.

## Ways to run it

- Script and clip. The default. The brief and the script are free, then the stills, the read, the bed, and the clip.
- Script only. Strike the stills and the clip on the materials card.
- With a live topic read. A separate lookup, before the script is frozen, on Douyin, Xiaohongshu, TikTok, or X. Comments are a separate lookup when the hook should use words people already wrote.

Open this when someone has a subject and an audience and wants a short video they can post, script and picture together.

## Scope and adjacent routes

Use this route when the piece is one short video: a product, a creator series, or a shop. A finished episode with a cast and a score belongs on a short-drama workshop. A WeChat article belongs on an article workflow.

## Inputs and defaults

The hard inputs are the subject and who it is for. Ask only for those. Default to a vertical 9:16 still, a script the length of a 30 to 45 second spoken clip, and four to six shots. Keep critical type and the product inside the center of the frame, clear of the lower caption band. Do not look up public posts unless the user asks for a live read or pastes nothing and still wants topics from the network.

## Golden path

1. Write the brief and the script. Show the three hooks and the shot list. This writing is free.
2. If a live read is in scope, search with `beatra.social.tools.search`, read the operation with `beatra.social.tools.get`, copy the `schema_hash` it just returned, show a lookup card, and call `beatra.social.execute` once. Allowed keys are `social.douyin.hot_search.list`, `social.douyin.video.search`, `social.douyin.video.comments.list`, `social.xiaohongshu.note.search`, `social.xiaohongshu.note.comments.list`, `social.tiktok.video.search`, and `social.twitter.tweet.search.recent`. Quote the line you used. Do not invent counts.
3. Upload a product photo with `beatra.assets.upload` when one is supplied. The first still with no photo is one `beatra.images.generate` after `{"capability": "text_to_image"}`. Every later still, and every still that must show that photo, is one `beatra.images.transform` after `{"capability": "image_to_image"}`.
4. Pick one ready voice with `beatra.voices.list`. One `beatra.speech.synthesize` after `{"capability": "text_to_speech"}` reads the chosen script. One `beatra.music.generate` after `{"capability": "text_to_music"}` writes an instrumental bed.
5. Show the materials card for the stills, the read, and the bed, and wait.
6. On the video card, one `beatra.videos.animate` after `{"capability": "image_to_video"}` per shot, from that shot's still. The read stays a separate file and is laid into the cut. An accepted end frame uses `beatra.videos.interpolate` after `{"capability": "frames_to_video"}`.
7. Join the shots with `beatra.videos.compose` once they have succeeded. Poll with `beatra.tasks.get` and deliver the clip, the script, the stills, and `billing.net_charged_credits`.

## Decisions that require confirmation

Planning and the written deliverable are free. They are not approval.

Before every paid call, show a current production card and wait:

1. Work — what will be made, in the user's words, and whether this call is a generate or a lookup.
2. Credits — the live price just read from the model card or from `beatra.social.tools.get`. Do not reuse a remembered number.
3. Count — one paid call per slot. A materials card may list every still, the read, and the bed; each slot has its own `client_request_id`. A later lookup page is another call. Video calls wait for their own card.
4. Identity — one new opaque `client_request_id` per call. A changed prompt, file, model, or control mints a new ID.
5. If we stop here — the free writing remains usable.
6. If the balance is insufficient — relay the official message and its top-up URL. Do not retry until the user says they have topped up.

A lookup and a generate are two cards. Approved stills, the read, or the bed do not authorize a video. Invoke every remote Beatra tool only through the bundled `scripts/mcp_client.py`. The tool name is the command argument and the JSON arguments are the standard input. Do not configure, call, or use a host Beatra Connector. Do not use REST/OpenAPI as a fallback.

If a create response is lost, retry only the identical payload and the same `client_request_id`. If the task id is lost, call `beatra.tasks.list`, then `beatra.tasks.get`, and match the frozen request before any identical retry. Call `beatra.tasks.cancel` only when the user asks to cancel, then confirm that task with `beatra.tasks.get`.

When the user asks how many credits remain, call `beatra.wallet.get`. When they ask what was charged, call `beatra.wallet.ledger`.

## References by task

Read [the scenario workflow](references/workflow.md) for the shot list, the payloads, and a worked clip.
Read [answers when a run goes wrong](references/faq.md) when a task stalls, a response is lost, a price looks wrong, or a still came back wrong.
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
