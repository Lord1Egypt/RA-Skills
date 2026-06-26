---
name: wechat-summary
description: Summarize WeChat conversations, triage unread messages, identify which items need a reply, and draft concise response suggestions while preserving privacy boundaries. Use when asked to digest a long chat, produce a catch-up summary, extract action items, decide whether to reply, or draft responses for WeChat messages or group threads.
---

# WeChat Summary

Focus on signal over volume. Summarize conversations in a way that helps the user decide what matters and what needs action.

## Workflow

1. Identify the scope:
   - one message
   - recent unread messages
   - a full conversation window
   - a noisy group thread
2. Separate content into:
   - actionable items
   - information only
   - social chatter
   - messages that may need a reply
3. For reply suggestions, match tone to the relationship and context.
4. In groups, avoid over-sharing private context from other chats or memory.
5. If confidence is low because message coverage is partial, say so.

## Summary modes

### Catch-up summary
Use for "what happened while I was away?"
- 3-7 bullets
- who said what
- any decision, request, or deadline

### Action-item summary
Use when the user mainly wants tasks.
- owner
- action
- due time if any
- missing information

### Reply triage
Use when the user asks what deserves a response.
Label items as:
- reply now
- can wait
- no reply needed

### Draft reply
Keep drafts short and sendable.
Offer one default draft; provide alternatives only if tone is uncertain.

## Group-chat policy

Be selective. In lively groups, do not manufacture a reply just because a message exists. If nothing meaningful should be said, say that no reply is needed.

## Output pattern

Use one of these structures depending on the task:

### Summary
- **What happened**
- **What matters**
- **What may need a reply**

### Triage
- **Reply now**
- **Can wait**
- **No reply needed**

### Draft
- **Suggested reply**
- **Why this works**

Keep the result compact and human.
