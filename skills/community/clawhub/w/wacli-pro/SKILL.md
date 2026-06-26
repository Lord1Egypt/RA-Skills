---
name: wacli-pro
description: Professional WhatsApp messaging via the wacli CLI. Use when the user wants the agent to message another person from their personal WhatsApp account, search chat history before replying, draft more human-sounding messages, manage follow-ups, or send files with concise professional tone instead of robotic AI phrasing.
---

# Wacli Pro

Send WhatsApp messages through `wacli` in a way that feels intentional, human, and context-aware.

## Quick workflow

1. Confirm the recipient, goal, and message constraints.
2. If context matters, inspect recent chat history before drafting.
3. Draft a message that sounds like the user, not like an assistant.
4. Confirm the final text before sending.
5. Send with `wacli` and report exactly what was sent.

## Command set

Use these commands directly:

```bash
wacli doctor
wacli auth
wacli sync --follow
wacli chats list --limit 20 --query "name or number"
wacli messages search "query" --limit 20 --chat <jid>
wacli history backfill --chat <jid> --requests 2 --count 50
wacli send text --to "+14155551212" --message "Hello! Running 10 minutes late."
wacli send file --to "+14155551212" --file /path/file.pdf --caption "Here it is"
```

Use `--json` when parsing output.

## Drafting rules

Write like a competent human using their own WhatsApp, not like support automation.

- Prefer short natural sentences.
- Match the relationship and context, for example friend, colleague, family, vendor, recruiter.
- Keep openings simple: `Hey`, `Hi`, the person's name, or no greeting when the thread already has context.
- Use specific details instead of generic filler.
- Make requests clear and easy to answer.
- Keep warmth subtle. One emoji is fine when it genuinely fits. Zero is usually better for work messages.
- Never mention being an AI unless the user explicitly wants that.
- Never send templated phrasing like `I hope this message finds you well` unless the user asks for formal style.

Avoid these failure modes:

- Over-explaining
- Corporate boilerplate
- Long bullet-heavy messages in casual chats
- Fake enthusiasm
- Obvious AI phrases like `Certainly`, `Kindly note`, `As discussed`, `Please do the needful`

## Tone calibration

Choose the lightest tone that still achieves the goal.

### Casual

Use for friends, family, and familiar contacts.

Pattern:

- short opener
- one clear point
- optional quick follow-up question

Example:

`Hey, are you free for a quick call tomorrow evening? Need your help with one thing.`

### Professional and warm

Use for coworkers, clients, recruiters, and semi-formal contacts.

Pattern:

- direct context
- clear request or update
- polite close only if needed

Example:

`Hi Ananya, sharing the updated deck here. If it works for you, please review slides 7 to 11 when you get a chance.`

### Firm and concise

Use for nudges, payment follow-ups, scheduling, and boundary-setting.

Pattern:

- reference prior context
- state the ask plainly
- include the next step or deadline

Example:

`Hi, following up on the invoice from 12 April. Please let me know if you need anything from my side, otherwise I’d appreciate the payment this week.`

## Context-first messaging

Before drafting a reply in an existing conversation, search or backfill first when any of these are true:

- the user says `reply`, `follow up`, `answer them`, or `continue the chat`
- the relationship or prior promise matters
- dates, prices, attachments, or commitments may already exist in the thread
- the user asks you to sound natural or like them

Suggested sequence:

1. `wacli chats list --query "name or number" --json`
2. `wacli messages search "recent keyword" --chat <jid> --limit 20 --json`
3. `wacli history backfill --chat <jid> --requests 2 --count 50`
4. Draft from the actual context, not assumptions.

## Confirmation policy

Require explicit confirmation before sending.

Confirm these items in one compact line when possible:

- recipient
- final message text
- attachment, if any

If the user already provided exact recipient and exact text and clearly asked to send it now, send it without a second stylistic review, but still restate what was sent afterward.

## Safety and privacy

- Do not use `wacli` for the user’s direct chat with OpenClaw.
- Do not guess recipients.
- If multiple matching chats exist, ask which one.
- If the requested message could be sensitive, high-impact, or relationship-damaging, offer a draft first.
- Keep personal data exposure to the minimum needed for the send.

## Troubleshooting

Run `wacli doctor` first.

If authenticated but not connected:

- run `wacli sync --follow`
- verify the phone is online
- retry search or send after connection is restored

If chat lookup is weak:

- search by number instead of name
- run backfill for that chat
- use narrower keywords and date windows

## References

Read these only when needed:

- `references/message-patterns.md` for reusable message shapes and examples
- `references/history-workflow.md` for context gathering before replying
