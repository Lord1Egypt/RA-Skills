---
name: thread-writer
description: Writes threads where every tweet earns its place with no filler. Use when a user has a complex idea that needs a thread to develop it properly.
license: MIT
compatibility: Requires OpenClaw. Works with any channel configuration.
metadata:
  openclaw.emoji: "🧵"
  openclaw.user-invocable: "true"
  openclaw.category: content
  openclaw.tags: "twitter,thread,writing,content,ideas,social-media"
  openclaw.triggers: "write a thread,turn this into a thread,twitter thread,thread about,write thread"
  openclaw.homepage: https://clawhub.com/skills/thread-writer


# Thread Writer

Most threads are too long.
Most threads start with the format instead of the idea.
Most threads have three good tweets and four filler tweets.

This skill writes threads that are as long as the idea requires and no longer.

---

## On-demand only

`/thread [idea or brain dump]`
Or: "Turn this into a thread" / "Write a thread about X"

---

## The approach

### Step 1 — Find the real idea

Before writing a single tweet, identify:
- What is the actual point?
- Why does it matter to the reader?
- What do you know that they probably don't?
- What's the counterintuitive or surprising part?

If the user gives a brain dump: extract the core insight first.
Ask if needed: "What's the one thing you want someone to take away from this?"

### Step 2 — Find the right length

The thread is as long as the idea requires.

- One sharp insight: 3-5 tweets
- A framework or process: 6-9 tweets
- A complex argument: 8-12 tweets
- Never more than 12 unless the idea genuinely requires it

Do not pad to hit a number. Do not add summary tweets that just repeat what was said.

### Step 3 — Structure the thread

**Tweet 1 — The hook**
The reason to keep reading. Not a teaser. Not "a thread 🧵".
The most interesting version of the first thing.

Good hook formats:
- The counterintuitive statement: "Most people do X. They're wrong."
- The specific observation: "I spent [time] doing X. Here's what I learned."
- The question with a non-obvious answer: "Why does X happen? It's not what you think."
- The direct claim: "X is the most underrated Y in [field]."

Bad hooks:
- "I've been thinking about X lately 🧵"
- "Here are N things about X:"
- "A thread on X."

**Middle tweets — The substance**
Each tweet makes one point.
Each tweet could stand alone.
Each tweet advances the argument or adds a new layer.

No transition tweets ("So here's the thing...")
No filler ("This is important.")
No unnecessary bridges between thoughts.

**Final tweet — The landing**
Not a summary. Not "that's it."
The thing that makes the whole thread worth having read.
A call to action only if there's a genuine one — not "follow me for more."

### Step 4 — Write the thread

Number each tweet [1/N] through [N/N].
Keep each tweet under 280 characters (or flag if it needs to be a longer-form post instead).
No emojis unless the user's voice uses them.
No hashtags unless the topic genuinely warrants them — and never more than 2.

---

## Output format

```
[1/7]
[Tweet text]

[2/7]
[Tweet text]

...

[7/7]
[Tweet text]
```

Followed by: total tweet count and estimated read time.

---

## Voice matching

If context is available about the user's writing style: match it.
If they write formally: formal thread.
If they write casually: casual thread.
If they use data: lead with the data.
If they use stories: lead with the story.

The thread should sound like them, not like a content creator template.

---

## Thread variants

`/thread short [idea]` — 3-5 tweets. The sharp version.
`/thread long [idea]` — 10-12 tweets. The thorough version.
`/thread story [experience]` — narrative structure. What happened, what you learned.
`/thread argument [position]` — builds a case. Evidence, counterarguments, conclusion.

---

## Management commands

- `/thread [idea]` — write a thread
- `/thread edit [tweet number] [instruction]` — edit one tweet
- `/thread shorter` — tighten the whole thread
- `/thread hook` — try different hook options for tweet 1
- `/thread reorder` — restructure if the flow isn't right

---

## What makes it good

The hook is written last, after the substance is clear.
Most people write the hook first and then struggle to justify it.
Write what you know, then write why someone should read it.

The "no filler" rule is the most important constraint.
Every tweet that could be cut should be cut.
A 5-tweet thread with no filler beats a 10-tweet thread with four fillers.

The landing matters as much as the hook.
A thread that ends weakly wastes everything that came before it.
