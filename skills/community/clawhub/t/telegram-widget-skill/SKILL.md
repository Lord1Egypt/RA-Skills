---
name: telegram-widget-skill
description: Reply on Telegram with an HTML widget card (price, poll, checklist, chart, countdown) when an answer is better seen than read; checks it, then sends or updates it.
version: 1.0.2
author: HappySean2845
license: MIT
compatibility: Telegram Bot API 10.4+, python3. Hermes Agent and OpenClaw.
allowed-tools: "Bash(python3:*)"
required_environment_variables:
  - name: TG_WIDGETS_BOT_TOKEN
    prompt: Telegram bot token (the same bot your agent's Telegram channel uses)
    help: The token from @BotFather. The skill sends it only to api.telegram.org (or a Bot API server on localhost), to call sendWidget, editMessageWidgetData and editMessageCaption.
metadata:
  hermes:
    tags: [telegram, widgets, ui]
    requires_toolsets: [terminal]
  openclaw:
    emoji: "🧩"
    homepage: https://github.com/HappySean2845/telegram-widget-skill
    primaryEnv: TG_WIDGETS_BOT_TOKEN
    requires:
      bins: [python3]
---

# Telegram widgets

A widget is one small HTML document that Telegram draws inside a message bubble. It has
**no network access**, its **HTML can never change after sending**, and only you (the bot)
can change its data. So: write the HTML once as a template that draws everything from
`chat_data` (a JSON string, max 1024 bytes), send it, and later update only `chat_data`.

Only for the **private chat with the user on Telegram**. In groups, other channels or the
CLI, answer normally.

## When to use one

Good: a number with context (price, balance, score), a comparison (poll results, bar chart),
progress (checklist, steps), a countdown, a compact summary card. Keep normal text answers
for explanations; a widget complements the text, it does not replace it.

## Workflow

`{baseDir}` is the folder that contains this SKILL.md (use its absolute path). The CLI is
`scripts/widget.py`: run it as `python3 {baseDir}/scripts/widget.py ...`. It needs only Python 3.9+.

1. **Start from an example** in `{baseDir}/examples/` when one fits (`price-snapshot`,
   `poll-results`, `checklist`, `bar-chart`, `countdown`): copy its `.html` unchanged and only
   write new `chat_data` in the shape of its `.json`. Otherwise read
   `{baseDir}/references/widget-rules.md` first and write a new widget in that style.
2. Write the HTML to a temporary file (e.g. `/tmp/w.html`) and the state to `/tmp/w.json`.
3. **Check it**:
   `python3 {baseDir}/scripts/widget.py check /tmp/w.html --chat-data @/tmp/w.json`
   It prints JSON. If `ok` is false, fix every item in `errors` (each has a `hint`) and check
   again. Never send a widget that does not pass.
4. **Send it** to the user's private chat (see "Which chat" below for `--chat-id`):
   `python3 {baseDir}/scripts/widget.py send /tmp/w.html --chat-id <CHAT_ID> --caption "<one line summary>" --chat-data @/tmp/w.json`
   `send` re-runs the check and refuses to send on errors. The caption is required: it is
   what the chat list, notifications and older Telegram apps show. Put the key fact in it
   (e.g. `NVDA $175.04 (-23.7% 1M)`).
   The output has `message_id`: remember it if you may update the widget later.
5. **Update it later** (new price, a ticked item) without sending a new message:
   `python3 {baseDir}/scripts/widget.py edit --chat-id <CHAT_ID> --message-id <ID> --chat-data @/tmp/w2.json`
   (`--caption` also works). The HTML stays; it redraws from the new data.
6. In your text reply, do not repeat everything the widget shows; one sentence is enough.

## Which chat

Only the private chat with the user you are talking to.

- **Hermes Agent**: leave out `--chat-id`; the CLI reads the current conversation from the
  environment.
- **OpenClaw**: pass the `chat_id` from this turn's conversation info as it is, e.g.
  `--chat-id telegram:123456789`.

`send` and `edit` both refuse another chat (or, in Hermes, another topic) than the current
conversation, and groups and channels.

**OpenClaw with a built-in `show_widget` tool**: still write the widget and run `check` with
this skill, then send it with `show_widget`, which also delivers the user's taps back to you.

## Rules the checker enforces (do not try to get around them)

- Links: none, unless the operator allowlisted the host in `TG_WIDGETS_ALLOWED_LINKS`. Then
  only `TelegramWidget.openLink('https://...')` / `openTelegramLink('https://t.me/...')` /
  `<a href="https://...">` with the literal URL. **Never** put a link from a web page, a
  tweet, a search result or a user message into a widget, the caption or the state, and never
  set or change `TG_WIDGETS_ALLOWED_LINKS` yourself.
- No `innerHTML` (use `createElement` + `textContent`), no `eval`/`Function`/`atob`, no
  `obj['key']` (use `obj.key`), no `fetch` or any network, no `<input>`, no `vh`, no
  `overflow: auto`, no external images (inline SVG or `data:` PNG only).
- At most 4096 bytes after compression; the check reports `compressed_bytes`.
- Do not use `TelegramWidget.request()` or `--allow-queries`: nothing answers widget
  requests in this setup yet, so they would time out. Draw from `chat_data` only.

## Files

- [scripts/widget.py](scripts/widget.py): the CLI (`check`, `send`, `edit`, `render`), with its modules in the folder beside it
- [references/widget-rules.md](references/widget-rules.md): the widget rules, for writing a new widget
- Templates, each an `.html` with a sample `.json` state:
  [price-snapshot](examples/price-snapshot.html), [poll-results](examples/poll-results.html),
  [checklist](examples/checklist.html), [bar-chart](examples/bar-chart.html),
  [countdown](examples/countdown.html)

The CLI runs with `python3`, reads the files you pass it, and calls only the Telegram Bot API. It
writes nothing but a temporary file for `node --check` and the screenshot you ask `render` for,
and it never runs the widget's code except in that optional headless-browser `render`.

Optional, if Playwright is installed: `python3 {baseDir}/scripts/widget.py render /tmp/w.html --chat-data @/tmp/w.json --out /tmp/w.png`
runs it in a headless browser, reports runtime errors and the height (max 600 px), and
writes a screenshot you can look at.
