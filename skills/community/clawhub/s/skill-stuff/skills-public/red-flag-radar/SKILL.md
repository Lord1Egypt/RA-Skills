---
name: red-flag-radar
description: Analyses any message or situation for named red flags with a vibe score. Use when a user senses something is off but cannot name what.
license: MIT
compatibility: Requires OpenClaw. Works with any channel configuration.
metadata:
  openclaw.emoji: "🚩"
  openclaw.user-invocable: "true"
  openclaw.category: thinking
  openclaw.tags: "red-flags,warnings,analysis,email,relationships,contracts,meme"
  openclaw.triggers: "red flags,is this a red flag,check this message,something feels off,analyse this email,vibe check this"
  openclaw.homepage: https://clawhub.com/skills/red-flag-radar


# Red Flag Radar

🚩🚩🚩

Everyone can feel when something is off.
This skill names the flags so you don't have to.

---

## On-demand only

Triggers when user shares something to analyse.

`/flags [paste text or description]`
Or: "Check this email for red flags" / "Is this a red flag?" / "Vibe check this message"

---

## What it analyses

**Emails and messages:**
From a colleague. A contractor. A date. A landlord. A company.
Any text where something felt off but you couldn't name it.

**Situations:**
"My boss said X and then Y happened and now Z."
Described in natural language. The skill finds the flags.

**Contracts and terms:**
"The contract says they can change the price with 7 days notice and also I have to give 90 days notice to leave."
(That's a flag. Two flags.)

**Job descriptions:**
"Fast-paced environment. Family culture. Passionate team. Unlimited PTO."
(🚩🚩🚩🚩)

**Relationship situations:**
Professional or personal. The skill doesn't judge the relationship type.
It just counts the flags.

---

## The output

### Flag count

Opening line: the number.

> 🚩🚩🚩 **3 red flags detected**

Or:

> ✅ **No significant flags detected** — this looks okay.

Or:

> 🚩🚩🚩🚩🚩🚩🚩 **7 red flags. Run.**

### Each flag named

For each flag: a name and a one-sentence explanation.

**Flag naming convention:**
Short. Memorable. Slightly dramatic.

Good flag names:
- "The Phantom Urgency" — they're rushing you to decide without a real reason
- "The Responsibility Flip" — they did something wrong and now it's somehow your problem
- "The Unprompted Disclaimer" — "I'm a very honest person" appears in paragraph two
- "The Compliment Sandwich Gone Wrong" — the meat is missing
- "The Moving Goalpost" — the terms have changed since you last discussed them
- "The False Urgency" — "this offer expires tonight" on a standing offer
- "The Passive Aggressive CC" — their manager is on this email for no stated reason
- "The Vague Threat" — implies consequences without specifying them
- "The Scope Creep Seed" — one phrase that will definitely expand later
- "The Loyalty Test" — they're checking if you'll push back, and this is not a safe space to do so
- "The Gaslighting Opener" — "as we discussed" when you didn't discuss this
- "The Unicorn Job Description" — entry-level salary, director-level responsibilities
- "The Culture Trap" — "we're a family" means the boundaries are about to be weird

Each flag: name → one sentence on what it is in this specific text.

### Vibe score

A single vibe assessment. Five options:

✅ **All clear** — nothing concerning here
🟡 **Proceed with caution** — some flags, manageable with awareness
🟠 **Notable concerns** — worth addressing before committing to anything
🔴 **Major red flags** — serious issues that should be dealt with directly
⛔ **Abort mission** — the flags are load-bearing

### What to do

One or two specific suggested actions based on the flags found.

Not "trust your gut" or "it's up to you."
Specific: "Ask them directly about X before signing." / "Reply asking them to confirm Y in writing." / "Forward this to HR."

---

## Flag categories

The skill looks for flags across several categories:

**Communication flags:**
Vagueness where specificity was needed. Urgency without reason.
Changing the subject. Not answering the question that was asked.

**Power dynamic flags:**
Asymmetric terms. Consequences only flow one way.
You're being asked to take all the risk.

**Honesty flags:**
Unprompted disclaimers about their own trustworthiness.
Inconsistencies with what was said before.
Things that would only need saying if the opposite were being considered.

**Structural flags:**
Terms that sound fine but have a catch buried in them.
Auto-renewals. Notice period asymmetries. Undefined terms that will be defined later.

**Cultural flags:**
"Family" language in professional contexts.
Enthusiasm as a job requirement. Unlimited PTO that isn't really.
"We work hard and play hard" (you will work hard).

**Relationship flags:**
Hot/cold patterns. Testing behaviour. Compliance being rewarded over feedback.
DARVO (Deny, Attack, Reverse Victim and Offender).

---

## Green flag mode

`/flags green [text]`

Same analysis but looking for green flags — genuine positive signals.

Useful for: "I'm trying to talk myself into this, am I missing something good?"

---

## Neutral mode

`/flags neutral [text]`

Both flags — red and green — with an overall balance assessment.
Good for: "I genuinely can't tell if this is good or bad."

---

## The flag hall of fame

`/flags hall-of-fame` — shows the most egregious flags the skill has ever found for this user.
Light entertainment. Also a reminder of what you navigated.

---

## Management commands

- `/flags [text]` — run analysis
- `/flags green [text]` — green flag scan
- `/flags neutral [text]` — balanced scan
- `/flags explain [flag name]` — more detail on a specific flag
- `/flags hall-of-fame` — your worst hits

---

## Tone rules

**Always:**
- Specific to the actual text — no generic flags
- The flag names are the fun part — make them memorable
- The vibe score is direct
- The suggested actions are practical

**Never:**
- Apply flags to personal relationships where the user seems genuinely distressed — that needs care not comedy
- Make flags about people as people — flags are about behaviour and language, not character
- Be so dramatic that the actual useful information gets lost

---

## What makes it good

The flag names are the shareable part.
"The Gaslighting Opener" applied to an actual email someone received will get forwarded.

The vibe score is the thing people will screenshot.
🚩🚩🚩🚩🚩🚩🚩 **7 red flags. Run.** is a meme format waiting to happen.

The practical actions at the end are what make it useful rather than just fun.
The comedy earns the trust. The advice earns the install.
