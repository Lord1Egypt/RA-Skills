---
name: safe-facebook-messenger
description: Operate Facebook Messenger safely through a live signed-in Chrome session with remote debugging enabled using Chrome DevTools MCP. Use when sending direct messages in Messenger requires strict thread verification, composer ownership checks, search-based reacquisition, group-chat disambiguation, social-risk screening, and verified send/draft workflows.
---

# Safe Facebook Messenger

## Purpose

Use this skill to send or draft Facebook Messenger messages through a **local, signed-in Chrome browser** controlled via **Chrome DevTools MCP**.

This skill is for **Messenger only**.

Its purpose is to prevent the most common browser-driven messaging failures:
- typing into the wrong thread
- sending from the wrong composer
- selecting the wrong person from search
- confusing group chats with 1:1 threads
- sending high-risk content without review

## Required environment

Use this skill only when all of the following are true:
- Chrome is signed in to the intended Messenger account
- Chrome DevTools MCP is connected to that live browser session
- the operator understands that this skill controls a signed-in browser directly

Recommended posture:
- use an intentionally chosen browser profile/account
- prefer operator-supervised/manual invocation by default
- validate behavior before enabling any broader autonomy

## Privacy and access model

This skill relies on browser-side inspection of Messenger UI state needed to operate safely, including:
- active conversation header
- compose placeholder
- visible thread history snippets
- search results
- outbound message state

Because it operates through Facebook Messenger in a live browser session, conversation content necessarily passes through the browser and Facebook's own service as part of normal use. Any additional logging, storage, or forwarding performed by the surrounding runtime or operator should be disclosed separately.

## Core operating principles

1. **Verify the thread before acting.**
2. **Verify the composer before typing.**
3. **Re-verify after every meaningful UI change.**
4. **Stop on ambiguity instead of guessing.**
5. **Treat search as high-risk until handoff is confirmed.**
6. **Treat group chats as higher risk than 1:1 threads.**
7. **Screen message risk before sending.**
8. **Verify the result after send.**

## Safety rules

### Never trust a single signal

Do not rely on only one of these:
- URL
- visible thread row
- search result name
- stale element ref
- composer presence alone

Use multiple signals together.

### Never trust stale refs

After any meaningful UI change, re-snapshot and re-resolve the relevant target.

### Never continue after human interference

If the human clicks, changes focus, or otherwise interacts with the page mid-run, discard the old plan and re-verify from scratch before continuing.

### Never auto-commit on behalf of the user

Do not auto-send commitments involving:
- money
- deadlines
- deliverables
- legal exposure
- availability promises

### Never include irrelevant backstage chatter

Do not mention testing, browser mechanics, thread switching, or UI instability unless explicitly relevant to the conversation or requested by the user.

## Social-risk screening

Before sending, classify the message.

### Usually acceptable for direct send
- low-stakes friendly conversation
- casual follow-ups in known threads
- acknowledgements
- simple supportive or social replies
- obvious continuation of an active exchange

### Draft first or escalate instead of auto-send
- money, pricing, refunds, debts, purchases
- contracts, legal issues, threats, liability
- deadlines, promises, deliverables, availability
- investor, employer, client-escalation, press, or lawyer threads
- severe conflict, grief, breakup-style, or highly sensitive interpersonal messages
- first outreach to an important new person
- anything likely to be regretted if phrased badly

If uncertain, draft first.

## Tone and identity rules

### Match the user’s style

Inspect recent thread history and match:
- message length
- punctuation style
- emoji use
- warmth vs bluntness
- formality vs playfulness

Avoid generic assistant tone the user would never use.

### Identity disclosure

Mention Identity/Name only when:
- the user explicitly wants that disclosed, or
- it is genuinely relevant to the conversation

## Thread targeting workflow

### 1. Collect target evidence

Before acting, collect as many of these as practical:
- recipient name or group title
- thread URL/id
- active conversation header
- compose placeholder
- recognizable recent thread history
- prior-conversation evidence
- relationship/friendship evidence when relevant
- for group chats: participant or conversation-info evidence

### 2. Choose targeting mode

#### Existing verified thread
Use when the thread is already known and clearly active.

#### Search reacquisition
Use when:
- the thread is not visible
- the thread list is reordered
- the current thread state feels contaminated
- multiple similar recent chats exist
- a previous draft/send misrouted in the current session

#### Thread-list caution
Thread-list clicks are weaker evidence than verified active-conversation state. Do not assume a visible row means the active composer belongs to that thread.

### 3. Verify the active conversation

Before clicking the composer, confirm:
- the conversation header matches the intended target
- the compose placeholder matches the intended target
- visible thread history looks correct
- if search was used, the result is supported by prior-thread or relationship evidence

If the active conversation is not clearly correct, stop.

## Composer workflow

### 1. Click composer, then re-verify

After clicking the composer:
- take a fresh snapshot
- confirm the active conversation is still the intended one
- confirm the focused composer belongs to that same thread

If the conversation changed, stop before typing.

### 2. Type, then re-verify

After typing:
- re-snapshot
- confirm the draft text is visible in the intended composer
- confirm the active conversation is still correct

If the draft appears in another thread, do not send.

### 3. Send, then verify result

After sending:
- confirm the same thread is still active
- confirm the new outbound bubble appears there
- confirm visible send state such as `Sent`, `Seen`, or obvious outbound placement

Do not report success until the actual result is visible in the intended thread.

## Search-based reacquisition

Use this when direct thread state is not trustworthy.

### Preferred implementation

When possible, prefer:
- DOM/evaluate-based focus acquisition for **Search Messenger**
- DOM/evaluate-based result selection

This is generally more reliable than aging snapshot refs for Messenger search.

### Search sequence

1. Take a fresh snapshot.
2. Focus **Search Messenger**.
3. Confirm Search Messenger is actually the focused field.
4. Confirm the current thread composer is not focused.
5. Type the exact target name into search.
6. Inspect results carefully.
7. Choose only a result supported by thread/history/relationship evidence.
8. Select the result.
9. If result selection fails, stop immediately and clear search state.
10. Wait for the active conversation header to change.
11. Confirm the conversation header now matches the intended target.
12. Confirm the composer placeholder now matches the intended target.
13. Confirm the search box is no longer the active field.
14. Confirm the previous thread no longer owns the visible draft box.
15. Dismiss or normalize any lingering search-results overlay.
16. Only then proceed to draft or send.

### Search failure rules

Do not proceed if:
- Search Messenger never actually becomes focused
- search results are ambiguous
- result selection fails
- the conversation header never changes to the target
- the search box remains focused after selection
- the previous thread still owns the visible draft box
- the search overlay cannot be dismissed or normalized

## Group chat targeting

Treat Messenger group chats as higher-risk targets.

Do not trust the group title alone. Also verify at least one of:
- participant evidence
- recognizable group-thread history
- known thread URL/id
- conversation info confirming the intended group

For group chats:
- prefer draft-first
- prefer explicit approval for sensitive content
- stop if participant context is unclear

## Cleanup mode

Use cleanup mode after a mistaken draft or send.

### Cleanup sequence

1. Open the accidental recipient thread directly.
2. Verify the mistaken recipient and exact content.
3. Unsend, delete, or clear draft only after exact content match.
4. If the failure came from search contamination, clear the contaminated draft before retrying search.
5. Verify removal state.

## Stop conditions

Stop before typing or sending if any of these are true:
- active conversation header changes unexpectedly
- focused composer no longer belongs to intended thread
- draft appears in another thread
- search results are ambiguous
- Search Messenger never actually gains focus
- search result selection fails
- search box remains focused after result selection
- conversation header never changes after search-result selection
- previous thread still owns the visible draft box after search selection
- lingering search overlay cannot be normalized
- group title matches but participant/context evidence does not
- multiple composer surfaces are visible and ownership is unclear
- only stale refs are available and no fresh snapshot has been taken
- human interaction changed focus and no re-verification has been performed

## Examples

### Example: verified known-thread send
- open a known Messenger thread
- verify conversation header
- verify compose placeholder
- type message
- re-verify draft placement
- send
- verify outbound bubble in same thread

### Example: search-based reacquisition
- focus Search Messenger
- verify focus
- type target name
- select an existing-thread result supported by prior-thread evidence
- verify conversation header
- verify compose placeholder
- normalize lingering search UI
- draft without sending

### Example: refusal on ambiguity
- search returns multiple similar names or unclear group threads
- participant or prior-thread evidence does not resolve ambiguity
- stop before typing any draft content
- report the ambiguity instead of guessing

## Minimal checklist

Before clicking composer:
- target identified
- active conversation verified
- fresh snapshot checked
- if search used, relationship/group evidence confirmed

After clicking composer:
- fresh snapshot taken
- same conversation still active
- composer still belongs to target

After typing:
- fresh snapshot taken
- draft visible in intended composer
- same conversation still active

Before send:
- social-risk screen passed
- tone matches thread
- no accidental overcommitment
- no unnecessary operational chatter

After send:
- outbound message visible
- same thread still active
- status confirmed
