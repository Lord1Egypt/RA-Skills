---
name: post-debugger
description: Diagnoses why a post underperformed using named failure modes. Use when a user's content did not land and they want the actual reason not the algorithm.
license: MIT
compatibility: Requires OpenClaw. Works with any channel configuration.
metadata:
  openclaw.emoji: "🐛"
  openclaw.user-invocable: "true"
  openclaw.category: content
  openclaw.tags: "content,debugging,analytics,writing,social-media,performance"
  openclaw.triggers: "why didn't this post work,my post flopped,what's wrong with this,post debugger,content didn't perform"
  openclaw.homepage: https://clawhub.com/skills/post-debugger


# Post Debugger

"The algorithm didn't show it to anyone."
Maybe. Or maybe something else happened.

This skill reads the post and tells you what it actually communicated to someone seeing it for the first time.

---

## On-demand only

`/debug [paste the post]`
Or: "Why didn't this post work?" / "What's wrong with this?"
Optionally: include the actual engagement numbers if you have them.

---

## Common failure modes

Most posts that underperform fail for one of these reasons.
The skill identifies which one(s) apply.

**The buried lead:**
The interesting thing is in paragraph three.
The first two paragraphs are context that the reader hasn't opted into yet.

**The generic opener:**
Starts with something too broad to be interesting.
"Leadership is hard." "Building a company is a journey."
Nothing in the first sentence gives a reason to keep reading.

**The performed emotion:**
The language signals that emotion is being performed rather than felt.
"I'm humbled and grateful." "This hit differently."
The reader sees the performance and disengages.

**The lesson without the story:**
Starts with the conclusion. Doesn't earn it.
"Here's what I learned: [lesson]."
The lesson without the specific experience that produced it has no weight.

**The hedged opinion:**
Has something to say but softens it into nothing.
"There are many ways to think about this, but for me, I tend to feel like..."
vs. "This is wrong and here's why."

**The wrong audience assumption:**
Written for people who already agree, not people who might be convinced.
Preaching to the choir reads differently to someone who doesn't already believe it.

**The lack of specificity:**
Vague claims that could apply to anyone.
"In my experience, X is important."
vs. "When I was [specific situation], X changed the outcome because [specific reason]."

**The formatting over substance:**
The post is structured like content (headers, bullets, numbered lists) but the actual ideas
inside the structure are thin.
The formatting is doing work the content isn't.

**The non-ending:**
The post just stops rather than landing.
Or ends with a call to action that isn't earned.
"Follow for more" when the post didn't demonstrate why following is worthwhile.

**The topic mismatch:**
The post is about something the audience doesn't follow you for.
Occasionally fine. Frequently alienating.

---

## The output

**🐛 Post debug: [first 5 words of post]...**

**What it communicated:**
[What a first-time reader actually receives from this post — not what was intended]

**The gap:**
[The difference between what was intended and what was communicated, if there is one]

**Primary failure mode:**
[The main reason it underperformed — from the list above, or something else specific]

**Secondary issues (if any):**
[Other factors]

**What to do differently:**
[Specific changes — either rewrite notes or an approach for the next version]

---

## The rewrite option

After the debug, the user can ask for a rewrite:
`/debug rewrite`

The skill rewrites addressing the identified issues.
Returns the rewrite alongside a note on what changed and why.

---

## What this skill won't say

- "The algorithm just didn't pick it up." Maybe true, not useful.
- "It was a great post, timing was just off." Maybe true, not useful.
- "Your audience isn't ready for this content." Almost always not the real reason.

The skill gives a real answer or says "I can't identify a clear reason — the post looks solid."

---

## Management commands

- `/debug [post]` — debug a post
- `/debug rewrite` — rewrite based on the debug
- `/debug vs [post2]` — compare two posts — why did one work better?

---

## What makes it good

Reading the post as a first-time reader, not as the writer.
The writer knows what they meant. The reader only has the words.
The gap between those two things is where most posts fail.

The named failure modes make feedback actionable.
"The buried lead" is more useful than "it didn't hook the reader."
It tells you exactly where the problem is and what to fix.

The willingness to say "this looks solid" when it does.
Post debugger that always finds a problem isn't honest — it's just pessimism.
Sometimes the post was fine and the variables were external.
