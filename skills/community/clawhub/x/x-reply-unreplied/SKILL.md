---
name: x-reply-unreplied
description: Check X notifications, mentions, or reply threads and answer posts that still need a response from the user. Use when the user wants help replying to unreplied mentions or thread responses in a short, on-topic, first-person style.
---

# X Reply Unreplied

Use this skill for manual reply handling, not a scheduled inbox sweep.
It assumes browser access and works best when a `twitter-humanizer` skill is also available.

Do not use this skill to evade platform enforcement, simulate human behavior for detection avoidance, or mass-reply at scale.

If the user did not specify a scope, default to notifications and mentions that appear to expect a reply.
If the user did not specify a count limit, process up to 5 suitable reply opportunities in one run.

## Reply standard

- One thread at a time
- Reply only where the account has not already replied in the same thread
- Stay on the thread topic only
- Use first person
- CRITICAL NON-NEGOTIABLE: keep every reply to 1 or 2 short sentences.
- CRITICAL NON-NEGOTIABLE: never avoid, relax, or reinterpret this limit unless the user explicitly asks for longer replies.
- Sound like a real person in a real conversation — not a helpful assistant wrapping up the thread
- Real emotion is allowed: warmth, mild frustration, honest uncertainty, genuine agreement
- Saying "I don't know" or "I hadn't thought of that" is fine and human
- Do not start replies with: Absolutely, Certainly, Indeed, Honestly (as opener), Great point
- Do not force product mentions or links unless the user asked for them
- Read [references/human-voice.md](references/human-voice.md) before drafting any reply

## Workflow

1. Run `openclaw browser start` to open the openclaw managed browser. CRITICAL NON-NEGOTIABLE: always use this command. Never open a browser any other way. Then navigate to X and go to notifications or the requested inbox surface.
2. CRITICAL NON-NEGOTIABLE: once on the notifications surface, never refresh or reload the page for any reason for the entire run. Navigate between threads and back using clicks and the back button only.
3. Review candidates one by one.
   - Ignore obvious spam, rage bait, bot replies, or posts that do not need a response.
   - Open the thread and read enough context to understand what the person is reacting to.
   - Confirm the user account has not already replied in-thread.
   - Read [references/inbox-workflow.md](references/inbox-workflow.md).
4. Like the post before drafting or touching the reply box.
5. Draft the reply.
   - If the `twitter-humanizer` skill is available, use it to produce 2 short reply options and pick the better one.
   - Keep the reply friendly, direct, and thread-specific.
   - Read [references/reply-rules.md](references/reply-rules.md).
6. Post the reply.
7. Return to notifications using the back button and continue until the cap is reached or there are no more good candidates.
8. CRITICAL NON-NEGOTIABLE: close every `x.com` tab immediately after the run is complete. Do not leave any tab open.

CRITICAL NON-NEGOTIABLE: do not jump across multiple threads in parallel.
CRITICAL NON-NEGOTIABLE: finish one full thread cycle (open -> read -> decide -> draft -> post or skip -> return) before opening the next thread.

## Skip conditions

Do not reply when:

- The user already answered
- The message is abusive with no upside to engaging
- The post is pure spam or obvious automation
- The right answer would require facts you cannot verify quickly
- A reply would likely derail into support, legal, or security issues better handled elsewhere

## Completion report

At the end, report:

- How many threads were reviewed
- Which ones were replied to
- The final text used for each reply
- Which items were skipped and why
- Confirmation that all `x.com` tabs were closed
