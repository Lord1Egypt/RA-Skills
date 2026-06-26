---
name: gmail
description: Gmail platform skill for SurfAgent, covering mailbox checks, mailbox triage, latest-thread opening, compose and reply task runners, tab hygiene, sent-message verification, proof rules, and when to use the Gmail adapter over raw browser control.
version: 1.3.0
metadata:
  openclaw:
    homepage: https://surfagent.app
    emoji: "📧"
---

# Gmail

> Gmail-specific operating skill. Use this with the core `browser-operations` skill.

This skill teaches agents how to work Gmail without guessing at selectors, lying about send success, or burning tokens on giant browser reads.

## 1. Use this skill for

- inbox, spam, sent, drafts, and outbox-style mailbox checks
- deterministic latest-thread opening from a mailbox view
- mailbox triage with urgency and action-signal scoring
- compose flows
- reply flows inside opened threads
- draft filling
- send verification
- Sent Mail and in-thread reply verification
- Gmail-specific blockers and recoveries
- deciding when to use the Gmail adapter instead of raw browser control

## 2. Tool preference

Use this order:
1. Gmail deterministic task runners
2. Gmail adapter state tools
3. Gmail adapter compose/reply tools
4. targeted browser evaluation only when needed
5. raw generic browser actions as fallback

Prefer Gmail-native verbs over rediscovering Gmail from scratch every run.

## 3. Gmail truths that matter

Gmail is not a normal static form page.

It has:
- dynamic compose surfaces
- editor behavior that can reject naive HTML injection
- mailbox navigation state that can be misleading from generic perception alone
- send flows where a click is not proof

Important: Gmail enforces Trusted Types in places, so direct `innerHTML` approaches are unreliable for rich content workflows.

## 4. Core Gmail loop

Default loop:
1. confirm current Gmail state or mailbox
2. choose the narrowest deterministic Gmail task runner that fits
3. verify the target surface is real
4. fill or extract only what the task needs
5. verify draft, mailbox, or thread state
6. send only when requested
7. verify the visible result with mailbox/thread proof

## 5. Verified compose flow

Known-good pattern:
- confirm inbox or current mailbox state first
- open compose deliberately
- confirm dialog is actually open
- fill `to`, `subject`, and `body`
- inspect composer state after fill
- send using the real Gmail Send control
- confirm Gmail shows a send alert like `Message sent`
- open Sent Mail
- verify the sent message exists and the content renders as expected

## 6. Proof rules

For Gmail, success requires all three layers:

1. **compose proof**
   - compose dialog open
   - target fields present
   - intended values visible in fields

2. **send proof**
   - send control activated
   - Gmail alert or live region confirms `Message sent`
   - compose closes or transitions correctly

3. **render proof**
   - Sent Mail contains the message, or
   - opened sent thread visibly preserves the result

Do not claim success from only:
- clicking Send
- a selector existing
- lack of an error
- draft text being present before send

## 7. Rich formatting rule

If the task cares about formatting, proof must come from rendered output, not only compose state.

That means:
- verify after send in Sent Mail or opened sent thread
- use screenshot or render inspection when formatting matters
- do not assume editor formatting survived the send path

## 8. Gmail adapter, when to use it

Prefer the Gmail adapter for:
- opening Gmail
- mailbox state inspection
- compose open/state
- filling drafts
- sending drafts
- opening Sent Mail
- visible thread extraction

Current Gmail adapter verbs:
- `gmail_health_check`
- `gmail_open`
- `gmail_get_state`
- `gmail_open_label`
- `gmail_extract_visible_threads`
- `gmail_open_visible_thread_row`
- `gmail_get_open_message`
- `gmail_open_compose`
- `gmail_open_reply`
- `gmail_get_composer_state`
- `gmail_fill_compose_draft`
- `gmail_send_compose`
- `gmail_open_sent`

Deterministic Gmail task runners:
- `gmail_compose_and_send_task`
- `gmail_reply_and_send_task`
- `gmail_check_mailbox_task`
- `gmail_open_latest_thread_task`
- `gmail_triage_mailbox_task`

## 9. When raw browser control is still acceptable

Use targeted evaluate or browser control when:
- you need render-only verification not yet wrapped by the adapter
- you need a one-off Gmail UI probe
- the adapter is missing a narrow site action
- Gmail has drifted into an odd hydration state and you need a focused diagnosis before changing the adapter

Even then:
- keep calls targeted
- inspect only the relevant surface
- verify the visible result

## 10. Common Gmail blockers

Watch for:
- compose dialog not actually open
- inline reply surface behaving differently from full compose
- wrong mailbox or label state
- stale draft surface
- editor accepting text differently than expected
- send button present but not truly actionable
- rich formatting lost in final render
- account/login mismatch
- multiple Gmail tabs causing verification to read the wrong surface

Current adapter rule: Gmail task runners should enforce tab hygiene and collapse duplicate Gmail tabs down to one working tab when they take control of the surface.

Mailbox triage is heuristic and proof-oriented. It is for ranking visible threads and guiding the next action, not for pretending to be a full Gmail classification engine.

When blocked:
- restate the blocker plainly
- say whether it is adapter-fixable, retryable, or human-blocked
- do not quietly downgrade the proof standard

## 11. Token-efficiency rules for Gmail

Prefer:
- task runners over hand-built action chains
- state checks over full page reads
- compose-state inspection over broad DOM dumps
- visible thread extraction over giant inbox scraping
- small post-action verification steps over repeated full reads

Avoid:
- full-page HTML grabs for simple compose tasks
- repeated generic perception when Gmail-specific state tools exist
- large reads of the inbox when only one draft or sent result matters

## 12. Minimal Gmail checklist

Before claiming a Gmail task done, confirm:
- correct account
- correct mailbox or thread
- compose, reply, mailbox, opened-thread, or triage surface is real
- intended values, extracted rows, or triage ranking are present
- send or action actually happened
- resulting message or state is visible afterward
- duplicate Gmail tabs were not left behind by the workflow

## 13. Relationship to other docs

Use alongside:
- `browser-operations` for the universal browser rules
- Gmail adapter docs for the concrete MCP/tool surface
- runtime wrappers for Claude Code, Codex, Cursor, Hermes, and others
