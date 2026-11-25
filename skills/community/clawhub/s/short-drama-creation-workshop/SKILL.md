---
name: "short-drama-creation-workshop"
description: "Turn a short-drama idea into a workshop pack: a beat sheet, vertical storyboard stills, one spoken line per beat, and an original music bed. This short drama creation workshop writes the episode spine, generates stills, records dialogue, and creates a scene score you can review before a still is animated into a shot. Use it for romance, suspense, comedy, and tearjerker vertical dramas, with character, costume, and location held across the episode."
---

# Short Drama Creation Workshop

## What you get

- A production bible: who stays the same, which wardrobe and props are permanent, and which states belong to one beat only.
- One beat sheet. Each beat has one dramatic job, the visual anchors, the framing, the spoken line, and a duration.
- One vertical reference still for each principal character and recurring location, then one vertical still per beat you picture, held to those references.
- One spoken line per speaking beat, in that character's voice.
- One original instrumental bed.
- One vertical episode cut of the shots you accept for motion: the hook, the turn, and the landing, unless you name more. Each moving shot starts from its accepted still. The cut carries the lines, the bed, and subtitles.

## Ways to run it

- Workshop pack. The default. Bible and beat sheet first, then the stills, lines, and bed you confirm, then the cut.
- One animated shot. Only after a still from this run, or a still you supply, is the opening frame.
- A voice you supply. One clone, only when you hand over a clean single-speaker sample and confirm you have the rights to it. Otherwise each character uses a ready voice from the account.

Open this when someone brings a premise and wants one vertical episode they can watch, not a single cinematic shot and not a product ad.

## Scope and adjacent routes

Use this route for a vertical short drama told in beats: romance, suspense, comedy, or a tearjerker. A single cinematic shot with no episode spine belongs on a shot workflow. A comic panel belongs on a comic-drama workflow. A product ad with no dramatic beat belongs on a product-video workflow.

## Inputs and defaults

The hard input is the drama premise: who it is about, the conflict, and the ending feeling. Ask only for that when it is missing. Reuse a known cast, costume, and location.

Default to a vertical 9:16 frame, six to eight beats, one still per beat, one spoken line per speaking beat, and one instrumental bed. Picture every beat. Move the hook, the turn, and the landing, and leave the other beats as stills unless the user names them. Do not animate a shot until that still is accepted. Cap the moving shots at eight so they join into one cut.

## Golden path

1. Write the bible and the beat sheet and show them. Separate permanent identity from the state that belongs to one beat. This writing is free.
2. If the user supplies a face, a costume photo, or a location photo, upload it with `beatra.assets.upload` and keep that artifact as the reference. The first reference still with no photo is one `beatra.images.generate` after `beatra.models.list` with `{"capability": "text_to_image"}`. Every later still is one `beatra.images.transform` after `{"capability": "image_to_image"}`, using the accepted character and location artifacts, up to four.
3. Pick one ready voice per speaker with `beatra.voices.list` and reuse that voice id for every line of that speaker. A supplied sample is one `beatra.voices.clone` after `{"capability": "voice_clone"}`, and only after the user confirms the rights. Then one `beatra.speech.synthesize` per confirmed line after `{"capability": "text_to_speech"}`.
4. For the bed, call `beatra.models.list` with `{"capability": "text_to_music"}`, then one `beatra.music.generate` as an instrumental.
5. Show the materials card for the stills, lines, and bed, and wait. Then make only those slots.
6. For each shot accepted for motion, call `beatra.models.list` with `{"capability": "image_to_video"}` and submit one `beatra.videos.animate` from that still. Pass the spoken line as `driving_audio` when the beat has one, and choose a model that admits an image plus driving audio. When the user has also accepted an end frame, use `beatra.videos.interpolate` after `{"capability": "frames_to_video"}` instead. When they have character and location references but no single opening still, use `beatra.videos.generate_from_references` after `{"capability": "reference_to_video"}`.
7. The video card is separate. Approved stills, lines, and music do not authorize it.
8. When every moving shot has succeeded, join them once with `beatra.videos.compose`. The join costs nothing and needs no card of its own; it was named on the video card. Poll with `beatra.tasks.get` and deliver the cut, the parts, and `billing.net_charged_credits`.

A still that comes back with the wrong face, wardrobe, or prop is one `beatra.images.edit` after `{"capability": "image_edit"}`, on its own card, using that still as the base. One repair, then stop.

## Decisions that require confirmation

Planning and the written deliverable are free. They are not approval.

Before every paid call, show a current production card and wait:

1. Work — what will be made, in the user's words, and whether this call is a generate, a clone, or a lookup.
2. Credits — the live price just read from the model card. Do not reuse a remembered number.
3. Count — one paid call per slot. A materials card may list every still, line, and the bed; each slot has its own `client_request_id`. Video calls wait for their own card.
4. Identity — one new opaque `client_request_id` per call. A changed prompt, file, model, or control mints a new ID.
5. If we stop here — the free writing remains usable.
6. If the balance is insufficient — relay the official message and its top-up URL. Do not retry until the user says they have topped up.

A voice clone is its own card. Submit it only after the user confirms they have the rights to that sample, with `consent_attested` true. A lookup and a generate are two cards. Approved stills, lines, or music do not authorize a video. Invoke every remote Beatra tool only through the bundled `scripts/mcp_client.py`. The tool name is the command argument and the JSON arguments are the standard input. Do not configure, call, or use a host Beatra Connector. Do not use REST/OpenAPI as a fallback.

If a create response is lost, retry only the identical payload and the same `client_request_id`. If the task id is lost, call `beatra.tasks.list`, then `beatra.tasks.get`, and match the frozen request before any identical retry. Call `beatra.tasks.cancel` only when the user asks to cancel, then confirm that task with `beatra.tasks.get`.

When the user asks how many credits remain, call `beatra.wallet.get`. When they ask what was charged, call `beatra.wallet.ledger`.

## References by task

Read [the scenario workflow](references/workflow.md) for the shot table, the payloads, and a worked episode.
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
