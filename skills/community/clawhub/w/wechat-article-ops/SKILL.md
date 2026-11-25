---
name: "wechat-article-ops"
description: "Write a WeChat Official Account article with its cover, in-article pictures, and a short operating plan. This article workflow returns title options, the article, a lead cover, section pictures, and a two-week posting note. Use it when one topic should become a publishable article and a simple plan for what to post next."
---

# WeChat Article and Operating Plan

## What you get

- Three title options, one article, and a digest line.
- A share blurb of one or two sentences, and a two-week posting note: which days, which angle, and what the next piece reuses.
- One 2.35:1 lead cover, one picture per section you choose to illustrate, and one square picture for Moments.
- Optionally, one spoken opening of about thirty seconds, in a ready voice.

## Ways to run it

- Article and pictures. The default. The writing is free, then the cover, the section pictures, and the Moments picture.
- Article only. Strike the pictures on the materials card.
- With a spoken opening. Add one read of the opening on that same card when the user wants the article heard.

Open this when someone has a topic and a reader and wants a publishable Official Account piece, including what to forward and what to post next.

## Scope and adjacent routes

Use this route for one WeChat Official Account article plus a short plan for the next posts. A short-video script belongs on a script workflow. A Moments poster with no article belongs on a poster workflow. This route does not read Official Account analytics. The plan uses the columns and the pace you supply.

## Inputs and defaults

The hard inputs are the topic and who the article is for. Ask only for those. Default to a 2.35:1 cover, square section pictures, one 1:1 Moments picture, and a posting note of four slots over two weeks. Reuse a known brand color and the words that must appear. Put the title in the article. Burn it into the cover only when the user asks, and then with one edit onto a clear band.

## Golden path

1. Write the titles, the article, the digest, the share blurb, and the posting note. Show them. This writing is free.
2. Upload a brand or product image with `beatra.assets.upload` when one is supplied. The cover with no image is one `beatra.images.generate` after `beatra.models.list` with `{"capability": "text_to_image"}`. A cover that must keep that image, and every section or Moments picture after the cover exists, is one `beatra.images.transform` after `{"capability": "image_to_image"}`, using the cover or the uploaded image as the reference.
3. When the title must sit on the cover, one `beatra.images.edit` after `{"capability": "image_edit"}` sets those exact words on a clear band and leaves the picture alone.
4. When a spoken opening is on the card, pick a ready voice with `beatra.voices.list` and submit one `beatra.speech.synthesize` after `{"capability": "text_to_speech"}`.
5. Show the materials card and wait. Poll with `beatra.tasks.get` and deliver the article, the pictures, and `billing.net_charged_credits`. Keep the article usable if picture calls stop.

## Decisions that require confirmation

Planning and the written deliverable are free. They are not approval.

Before every paid call, show a current production card and wait:

1. Work — what will be made, in the user's words, and whether this call is a generate or a lookup.
2. Credits — the live price just read from the model card. Do not reuse a remembered number.
3. Count — one paid call per slot. The materials card may list the cover, the section pictures, the Moments picture, and the spoken opening; each slot has its own `client_request_id`.
4. Identity — one new opaque `client_request_id` per call. A changed prompt, file, model, or control mints a new ID.
5. If we stop here — the free writing remains usable.
6. If the balance is insufficient — relay the official message and its top-up URL. Do not retry until the user says they have topped up.

A lookup and a generate are two cards. Invoke every remote Beatra tool only through the bundled `scripts/mcp_client.py`. The tool name is the command argument and the JSON arguments are the standard input. Do not configure, call, or use a host Beatra Connector. Do not use REST/OpenAPI as a fallback.

If a create response is lost, retry only the identical payload and the same `client_request_id`. If the task id is lost, call `beatra.tasks.list`, then `beatra.tasks.get`, and match the frozen request before any identical retry. Call `beatra.tasks.cancel` only when the user asks to cancel, then confirm that task with `beatra.tasks.get`.

When the user asks how many credits remain, call `beatra.wallet.get`. When they ask what was charged, call `beatra.wallet.ledger`.

## References by task

Read [the scenario workflow](references/workflow.md) for the picture sizes and a worked article.
Read [answers when a run goes wrong](references/faq.md) when a task stalls, a response is lost, a price looks wrong, or a cover came back wrong.
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
