---
name: telegram-web
description: Telegram Web platform skill for SurfAgent, covering chat state, composer flows, send verification, and when to use the Telegram Web adapter over raw browser control.
version: 1.0.0
metadata:
  openclaw:
    homepage: https://surfagent.app
    emoji: "✈️"
---

# Telegram Web

> Telegram Web operating skill. Use this with the core `browser-operations` skill.

This skill teaches agents how to work Telegram Web without treating a brittle chat UI like a generic web form.

## 1. Use this skill for

- chat and sidebar state checks
- visible message extraction
- composer state inspection
- draft filling
- proof-aware send flows
- deciding when to use the Telegram Web adapter instead of raw browser control

## 2. Tool preference

Use this order:
1. Telegram Web adapter state tools
2. Telegram Web adapter composer and send tools
3. targeted browser evaluation only when needed
4. raw generic browser actions as fallback

Prefer Telegram-native verbs over improvised DOM pokes.

## 3. Telegram Web truths that matter

Telegram Web is not a normal static page.

It has:
- dynamic sidebar and chat panes
- contenteditable composer behavior
- route changes inside the app shell
- send flows where clicking alone is weak proof

Important: a send attempt is not success unless the UI shows the message actually landed.

## 4. Core Telegram loop

Default loop:
1. confirm Telegram Web state
2. open or confirm the correct chat
3. inspect visible messages or composer state
4. fill the draft if needed
5. verify the intended text is present
6. send
7. verify the composer changed and the message appears

## 5. Proof rules

For Telegram Web, success requires:
1. correct chat is open
2. intended text is present before send
3. composer clears or materially changes after send
4. last visible message reflects the sent content, or stronger site-native confirmation exists

Do not claim success from only:
- clicking the send button
- a keypress firing
- draft text existing before send
- absence of an error

## 6. When to use the Telegram Web adapter

Prefer the Telegram Web adapter for:
- opening Telegram Web
- checking page and composer state
- extracting visible messages
- extracting visible chats
- opening a chat
- filling the current composer draft
- sending a message with immediate post-send checks

Current Telegram Web adapter verbs:
- `tgweb_health_check`
- `tgweb_open`
- `tgweb_get_state`
- `tgweb_open_chat`
- `tgweb_extract_visible_messages`
- `tgweb_extract_chats`
- `tgweb_get_composer_state`
- `tgweb_fill_composer_draft`
- `tgweb_send_message`

## 7. When raw browser control is acceptable

Use targeted browser control only when:
- you need a one-off UI probe not covered by the adapter
- you can verify the result immediately in the visible chat
- the action is narrow and low-risk

Even then:
- keep calls targeted
- avoid broad DOM scraping
- verify the post-send state, not just the action attempt

## 8. Common Telegram Web blockers

Watch for:
- wrong chat open
- composer not actually focused or writable
- stale sidebar or pane state
- account/login mismatch
- modal or onboarding overlays
- send control present but not truly actionable

When blocked:
- name the blocker plainly
- say whether it is retryable, adapter-fixable, or human-blocked
- do not quietly lower the proof bar

## 9. Token-efficiency rules for Telegram Web

Prefer:
- state checks over full-app reads
- visible message extraction over giant DOM dumps
- composer-state inspection over repeated page snapshots
- one send action followed by verification

Avoid:
- dumping the full app shell for a single chat task
- repeated blind retries on the composer
- claiming success before the message is visibly present

## 10. Minimal Telegram Web checklist

Before claiming a Telegram Web task done, confirm:
- correct account
- correct chat
- intended draft content visible before send
- send actually happened
- visible post-send result confirmed afterward

## 11. Relationship to other docs

Use alongside:
- `browser-operations` for universal browser rules
- the Telegram Web adapter repo for concrete MCP/tool surface
- runtime wrappers when working from Claude Code, Codex, Cursor, Hermes, and others
