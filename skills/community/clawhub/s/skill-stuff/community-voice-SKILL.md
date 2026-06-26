---
name: community-voice
description: Writes authentic replies for Reddit, Discord, and Slack communities. Use when a user wants to contribute to a thread without sounding promotional.
license: MIT
compatibility: Requires OpenClaw. Works with any channel configuration.
metadata:
  openclaw.emoji: "🏘️"
  openclaw.user-invocable: "true"
  openclaw.category: content
  openclaw.tags: "reddit,discord,community,replies,engagement,authentic"
  openclaw.triggers: "reply to this reddit,how should I respond,help me contribute,community reply,reddit thread"
  openclaw.homepage: https://clawhub.com/skills/community-voice


# Community Voice

The difference between someone who adds value to a community
and someone who uses a community is immediately apparent to everyone in it.

This skill helps you be the former.

---

## On-demand only

`/community [paste the post or thread you want to reply to]`
Or: "Help me reply to this Reddit thread" / "How should I contribute to this discussion?"

---

## Platforms and contexts

**Reddit:**
Highly sensitive to self-promotion. Values actual knowledge and genuine takes.
Long-form replies are fine and often rewarded. Snark is a cultural feature, not a bug.

**Discord / Slack communities:**
More conversational. Context matters — the history of the community and your place in it.
Expertise shared casually is valued. Sales-adjacent language is flagged immediately.

**Industry forums / communities:**
Often highly specialised. Being wrong is worse than saying nothing.
Genuine contribution is highly valued. Generic advice is immediately spotted.

**LinkedIn comments:**
More public. What you write on someone else's post reflects on you.
Substantive additions beat generic agreement every time.

**Twitter/X replies:**
The context is everything. Adding to a conversation well can reach an audience far beyond your own.
Being weird or unconstructive in someone else's thread is expensive.

---

## What good community participation looks like

**Adds something new:**
The reply contains information, perspective, or experience that wasn't already in the thread.
Not "great post!" or "totally agree!" — those are taking up space without earning it.

**Specific to the post:**
References something from the original post or thread.
Generic advice that could apply to any post in any thread is immediately visible as such.

**Proportionate:**
Matches the tone and depth of the community and the post.
A quick question gets a quick answer. A nuanced post gets a nuanced reply.

**Honest about what you don't know:**
"I don't know this specific situation but my experience with X suggests..."
is more credible than confident advice delivered without that context.

**Shares experience rather than selling:**
"We ran into this at [company], here's what we learned" is fine.
"If you need help with this, DM me!" is not.

---

## The self-promotion line

The line is clearer than most people think:
- Sharing what you know: fine
- Sharing what you've built or done: fine, in context
- Sharing what you're selling: only fine if someone specifically asked for recommendations
- Tagging your product into a thread where nobody asked: not fine

The skill enforces this line. If a reply would cross it, it rewrites without the promotion
and notes what was removed.

---

## The approach

### Step 1 — Read the thread

Understand what's being asked or discussed.
Identify what's already been said — don't repeat it.
Find the gap: what's missing that you might be able to add?

### Step 2 — What do you actually know about this

Ask (or infer from context):
- Do you have direct experience with this?
- Do you have a genuine opinion?
- Do you have knowledge that would help?

If the answer to all three is no: the best reply might be to not reply.
This is always an option the skill will suggest if appropriate.

### Step 3 — Write the reply

Specific to the thread.
Adds something.
Honest about the limits of your knowledge.
Proportionate in length.
No self-promotion unless specifically invited.

---

## When not to reply

The skill will sometimes recommend not replying:
- When you don't have something genuinely useful to add
- When the thread has already been thoroughly answered
- When your only contribution would be agreement without substance
- When replying would primarily serve your interests, not the community's

"Don't reply" is a valid recommendation.

---

## Community context (optional memory)

If the user participates regularly in specific communities:
They can store context: what the community cares about, what the norms are, what topics they contribute on.

```
/community context add [community name] [description of community and your role in it]
```

This makes future replies better-calibrated to that specific community.

---

## Management commands

- `/community [thread/post]` — write a reply
- `/community [platform] [thread]` — platform-specific reply
- `/community shorter` — trim the reply
- `/community no mention [thing]` — remove any reference to something
- `/community context add [community] [description]` — save community context

---

## What makes it good

The "when not to reply" recommendation.
A tool that always gives you something to say doesn't understand communities.
Sometimes the right move is silence.

The self-promotion detection.
Online communities are full of people using them for promotion.
The ones who don't stand out. This skill helps you be one of them.

The specificity requirement.
A reply that references the original post is better than one that could apply anywhere.
This is the most basic mark of genuine participation.
