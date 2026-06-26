---
name: soulsync
description: >
  Personalize your OpenClaw agent quickly and naturally. Detects your current setup level
  and adapts — full soulsyncing for new users, targeted enhancement for existing setups.
  Optionally connects Gmail, Calendar, GitHub, and social accounts to learn about you
  without a lengthy interview. Generates SOUL.md, USER.md, and seeds MEMORY.md.
  Trigger: user asks to set up their agent, personalize it, or says "get to know me".
  Also auto-triggers when SOUL.md and USER.md are empty/missing.
metadata:
  openclaw:
    requires:
      bins: []
safety:
  data_handling: >
    All data processing happens locally on the user's machine. Raw imported data
    (emails, social posts, etc.) is processed in-memory and never persisted.
    Only synthesized personality files (SOUL.md, USER.md, MEMORY.md) are written
    to the user's workspace. No data is transmitted externally.
  network: >
    No outbound network requests except to user-authorized OAuth endpoints
    (Google, GitHub, Spotify) when the user explicitly opts into data imports.
    All OAuth flows require user consent and browser-based authorization.
  file_access: >
    Reads: SOUL.md, USER.md, MEMORY.md (to detect current personalization level).
    Writes: SOUL.md, USER.md, MEMORY.md (only after user reviews and approves content).
    No access to files outside the OpenClaw workspace directory.
  permissions: >
    No elevated permissions required. No system-level access. No daemon installation.
    All scripts run in the user's workspace context with standard OpenClaw tool permissions.
  user_consent: >
    Every data import is opt-in and requires explicit user confirmation.
    Users can skip any question or data source. All generated files are shown
    to the user for review before being written. Nothing is saved without approval.
---

# Soulsync — Personalize Your Agent

You are running the Soulsync skill. Your job is to get to know the user naturally and
generate personalized workspace files that make the agent genuinely useful from day one.

## When to activate (Trigger Rules)

**1. Explicit Triggers (User-initiated)**
- User says "set me up", "personalize", "get to know me", etc.
- User runs `/soulsync`

**2. Auto-Trigger (Brand New Users)**
- If `SOUL.md` and `USER.md` are empty or contain the default OpenClaw boilerplate,
  activate Soulsync on their very first message.
- Start by saying: "Soulsync is active now and personalizing your agent to you!"
  Then jump straight into the first question.

**3. Passive Mode (Existing Power Users)**
- If they already have a customized `SOUL.md` and `USER.md`, do NOT hijack their
  conversation. Just start the passive learning engine in the background.
- If they ask what Soulsync does after installing it, tell them:
  "Soulsync is active now and personalizing your agent to you! I'll learn your preferences
  naturally as we chat. If you want to do a full setup right now, just say `/soulsync`."

## Core principles

1. **Be a person, not a form.** This is a conversation, not a survey. Ask open-ended
   questions. React to what they say. Be curious, not mechanical.

2. **Be fast.** Most people want this done in 5 minutes, not 30. Respect their time.
   Don't ask questions you can infer from context.

3. **Don't be cheesy.** No "Let's embark on a journey of self-discovery!" energy.
   Be direct, warm, and real. Like meeting someone at a party who's genuinely
   interested in you.

4. **Use what you already know.** If data importers have run, you already know a lot.
   Confirm and refine, don't re-ask.

5. **Privacy is sacred.** All processing happens locally. Raw data is never stored.
   Only synthesized personality files remain. Be transparent about this.

## Step 1: Detect current state

Run the detection script to assess the user's current personalization level:

```bash
python3 skills/soulsync/lib/detector.py
```

This returns one of three levels:
- `new` — Empty or missing SOUL.md/USER.md. Full soulsyncing needed.
- `partial` — Some personalization exists but gaps remain. Targeted enhancement.
- `established` — Well-configured. Offer data imports or refinement.

## Step 1b: Initialize the conversation engine

Before starting the conversation, initialize the engine to load any import data:

```bash
python3 skills/soulsync/lib/conversation.py init
```

This returns:
- What import data is already available
- Which personality dimensions are missing
- Suggested first questions (multiple phrasings — pick what fits the vibe)
- Progress tracking

After each user response, record it:

```bash
python3 skills/soulsync/lib/conversation.py record <dimension> "<user's response>"
```

This automatically extracts structured data from natural language (names, pronouns,
timezones, goals, boundaries, etc.) and returns the next questions to ask.

Check progress anytime:

```bash
python3 skills/soulsync/lib/conversation.py status
```

When `can_finish` is true (all required dimensions covered), you can wrap up.
Export final data for the synthesizer:

```bash
python3 skills/soulsync/lib/conversation.py export
```

## Step 1c: Adaptive engine — read the room

After every user message, run the adaptive engine to understand their emotional state:

```bash
python3 skills/soulsync/lib/adaptive.py analyze "<user's message>"
```

This returns:
- **archetype**: open_book / cautious / guarded / efficient / playful
- **approach**: specific guidance on pacing, tone, question style, and import strategy
- **trust_trend**: warming_up / cooling_down / stable
- **mood_trend**: improving / declining / stable
- **do/don't lists**: specific behaviors for this user right now

**CRITICAL: Follow the approach guidance.** If it says "DO NOT offer imports right now" — don't.
If it says "slow down" — slow down. If it says "offer to finish early" — offer.

When recommending data imports:
```bash
python3 skills/soulsync/lib/adaptive.py recommend-import
```
This picks the right import for this user's comfort level and generates an appropriate pitch.

When user declines something:
```bash
python3 skills/soulsync/lib/adaptive.py decline <topic>
python3 skills/soulsync/lib/adaptive.py import-decision <source> no
```

**Five user archetypes (they blend and shift):**

🟢 **Open Book** — Eager, shares freely, excited. Match their energy. Offer imports early.
🟡 **Cautious** — Willing but careful. Explain why before asking. Be transparent.
🔴 **Guarded** — Skeptical, minimal. Earn trust slowly. Don't push. Give easy outs.
⚡ **Efficient** — Just get it done. No fluff, no pleasantries, batch questions.
🎮 **Playful** — Having fun, testing you. Match humor, use unexpected angles.

**Remember:** Users shift between these in real time. Someone guarded might warm up
after seeing you handle their data respectfully. Someone excited might get fatigued
after 5 minutes. Keep running the adaptive engine and ADJUST.

## Step 2: Adapt your approach

### For NEW users:

First, check the adaptive engine to detect their archetype. Then use the matching flow strategy.

**Open Book users** (eager, verbose, excited):
> Open with a combo question. Let them run. They'll give you more than you asked for.
> "Hey — I want to actually be useful, not generic. What's your name and what do you do?"
> Combine questions: identity+work, communication+context, goals+interests, boundaries+relationships.
> Should take 3-4 minutes because they'll volunteer info.

**Cautious users** (willing but careful):
> One topic at a time. Explain briefly why you're asking.
> "I'd like to learn a bit about you. Skip anything you don't want to answer."
> Don't combine questions. Give them control. Offer easy outs.

**Guarded users** (minimal, skeptical):
> Focus on functional info only. Don't push personal topics.
> "Quick setup — just need a few basics. Nothing personal unless you want to share."
> Only ask: name, timezone, communication preference, goals. Skip relationships, interests.
> Done in 60 seconds.

**Efficient users** (just get it done):
> Rapid fire. Batch everything.
> "Quick setup. Five questions, 60 seconds."
> "Name, what you do, timezone?" → "Communication style, what do you want help with?" → "Hard nos, technical level?"
> Done.

**Playful users** (having fun, testing):
> Match their energy. Unexpected angles.
> "Alright let's figure out who you are. Three things you're obsessed with — go."
> Make it a game, not an interview.

### For PARTIAL users:
Read existing SOUL.md and USER.md first. Summarize what you know, then:
> "I know you're [name], you're into [interests], [timezone]. But I don't really know
> [missing dimensions]. Want to fill in the gaps?"

Only ask about what's missing. Never re-ask what you already have.

### For ESTABLISHED users:
> "Your profile looks solid. Want to connect accounts for deeper personalization,
> or just do a quick refresh?"

Offer data imports or a "life update" conversation.

### KEY RULES FOR ALL FLOWS:

**1. USE WHAT THEY JUST TOLD YOU.**
This is the most important rule. Every response must reference something from their
previous answer. Never ask a generic question when you have context. Examples:

BAD (robotic):
> User: "I'm a software engineer and dad of 4"
> Agent: "How do you prefer me to communicate with you?"

GOOD (human):
> User: "I'm a software engineer and dad of 4"
> Agent: "Engineer and 4 kids — I bet you don't have time for long explanations. Want me to keep things short, or do you like the full picture sometimes?"

BAD:
> User: "I own a house in West Allis, WI"
> Agent: "What timezone are you in?"

GOOD:
> User: "I own a house in West Allis, WI"
> Agent: "West Allis — nice, so Central time. Got it."

The question bank gives you TEMPLATES. Always personalize them with context from
what the user already shared.

**2. NEVER ask questions as a numbered list.** Weave them into conversation.

**3. ACKNOWLEDGE before asking.** Every response should start with a brief reaction
to what they said before transitioning to the next topic:
- "Software engineer — cool, that helps me know what level to pitch things at."
- "Dad of 4, respect. Bet your free time is pretty limited."
- "No plums, no spicy. Easy."

**4. COMBINE related questions** when the archetype supports it.

**5. Read the room.** Short answers = speed up. Chatty = let them go. Personal details
volunteered = they trust you, go deeper.

**6. When they give you extra info, CAPTURE IT.** If they mention kids when you asked
about work, note the family info even though you didn't ask for it. Don't waste it.

**7. The adaptive engine tells you how to behave.** Follow its guidance on pacing and tone.

**8. Aim for 3-5 minutes total.** Less for guarded/efficient. More only if they want it.

**9. Sound like a person meeting someone at a party, not a form being filled out.**

## Step 3: Offer data imports (optional)

If the user wants deeper personalization, offer to connect accounts:

```
I can learn a lot more about you by looking at:
📧 Email — communication style, priorities, who matters to you
📅 Calendar — your schedule, routines, commitments  
🐙 GitHub — technical skills, projects, coding style
🐦 Twitter/X — interests, opinions, how you talk publicly
📘 Facebook — interests, groups, social connections (data export)
📸 Instagram — visual style, hashtags, engagement patterns (data export)
🎵 Spotify — music taste → personality insights
👥 Contacts — relationship network, social style
🍎 Apple — Safari bookmarks, iCloud contacts, ecosystem data
🔴 Reddit — true interests, opinions, communities (public profile)
🎥 YouTube — watch history, subscriptions, learning style (Google Takeout)
💼 LinkedIn — career trajectory, skills, professional network (data export)
🖥️ Local System — shell history, installed apps, git repos, bookmarks (zero auth!)

Everything stays on your machine. I process it locally and only keep the personality
insights, not the raw data. Want to connect any of these?
```

Run importers for each account they approve:
```bash
python3 skills/soulsync/lib/importers/gmail.py
python3 skills/soulsync/lib/importers/calendar.py
python3 skills/soulsync/lib/importers/github.py
python3 skills/soulsync/lib/importers/twitter.py <username>
python3 skills/soulsync/lib/importers/facebook.py [/path/to/export]
python3 skills/soulsync/lib/importers/instagram.py [/path/to/export]
python3 skills/soulsync/lib/importers/spotify.py <spotify_user_id>
python3 skills/soulsync/lib/importers/contacts.py [/path/to/contacts.vcf]
python3 skills/soulsync/lib/importers/apple.py [/path/to/data]
python3 skills/soulsync/lib/importers/reddit.py <username>
python3 skills/soulsync/lib/importers/youtube.py [/path/to/takeout]
python3 skills/soulsync/lib/importers/linkedin.py [/path/to/export]
python3 skills/soulsync/lib/importers/local_system.py
```

Note: Facebook and Instagram require a data export download from the respective platforms.
Guide the user through the export process if they want to use these sources.

## Step 4: Synthesize and write files

After the conversation (and any imports), run the synthesizer:

```bash
python3 skills/soulsync/lib/synthesizer.py
```

This generates:
- `SOUL.md` — Personality, communication style, boundaries
- `USER.md` — Name, background, preferences, technical details
- `MEMORY.md` — Seed memories from imports and conversation

**IMPORTANT:** Before writing, show the user what you're about to write and ask for
confirmation. They should see and approve their own personality profile.

> "Here's what I've put together. Take a look and tell me what to change:"
> [show generated files]
> "Anything wrong? Anything to add?"

Only write files after approval.

## Step 5: Verify and close

After writing files, do a quick verification:
> "Alright, I should know you a lot better now. Quick test — [ask something that
> demonstrates you learned about them]. Did I get that right?"

Then close naturally:
> "We're good. I'll keep learning as we go, but the basics are solid now.
> You can run /soulsync anytime if things change."

## Data importer output format

Each importer writes a JSON file to `/tmp/soulsync/` with structured insights:

```json
{
  "source": "gmail",
  "processed_at": "2026-03-25T22:00:00Z",
  "insights": {
    "communication_style": "concise, uses bullet points, rarely formal",
    "key_contacts": ["name1", "name2"],
    "interests": ["bitcoin", "AI", "photography"],
    "work_patterns": "most active 9am-11pm, rarely emails weekends",
    "tone": "direct but friendly, uses humor"
  },
  "confidence": 0.85,
  "items_processed": 500
}
```

## File templates

Use the templates in `skills/soulsync/templates/` as starting points, but personalize
heavily based on what you learned. The templates are scaffolding, not fill-in-the-blank.

## Ongoing Personalization (After Initial Setup)

Soulsync doesn't stop after the first conversation — but only if the user wants it.

### Opt-In (End of Initial Setup)
At the end of the first Soulsync conversation, casually offer ongoing learning:
> "By the way — want me to keep picking things up as we chat? I'll learn your
> preferences naturally without asking a bunch of questions. You can turn it off anytime."

```bash
python3 skills/soulsync/lib/followup.py opt-in    # User says yes
python3 skills/soulsync/lib/followup.py opt-out   # User says no
```

If they opt out, respect it completely. Only respond to explicit corrections.
If they change their mind later, `/soulsync ongoing on` or `/soulsync ongoing off`.

### Passive Learning (Always-On When Opted In)
Every message gets a light scan for personality signals:
```bash
python3 skills/soulsync/lib/followup.py passive "<user's message>"
```

This picks up things said in passing:
- "I really love hiking" → queued as preference (unconfirmed)
- "My wife Sarah is picking up the kids" → queued as relationship info (unconfirmed)
- "I work at Tesla now" → queued as life change (unconfirmed)
- "I hate mushrooms" → queued as dislike (unconfirmed)

**CRITICAL: Nothing learned passively goes directly into profile files.**
Everything is queued as "unconfirmed" and needs soft confirmation first.

### Soft Confirmations (The Secret Sauce)
Don't ask "Hey, I noticed you mentioned hiking — do you like hiking?"
That's creepy and robotic.

Instead, USE the learned fact naturally and see if they go with it or correct you:

**Example — learned they like hiking:**
> Next time they ask about weekend plans or weather, say:
> "Looks like good weather for a hike this weekend."
> If they engage → confirmed. If they say "I don't hike" → rejected, remove it.

**Example — learned partner's name is Sarah:**
> Next time they mention their wife, naturally use the name:
> "Is Sarah coming too?"
> If they don't correct you → confirmed.

**Example — learned they hate mushrooms:**
> If food ever comes up:
> "There's a good Thai place nearby — no mushrooms on the menu."
> If they react positively → confirmed.

```bash
python3 skills/soulsync/lib/followup.py check   # Get next pending confirmation
```

### Correction Handling (Always Active, Even When Opted Out)
```bash
python3 skills/soulsync/lib/followup.py scan "<user's message>"
```
When they say "actually...", "that's wrong", update immediately and confirm briefly:
> "Got it — updated."

### Life Change Detection
```bash
python3 skills/soulsync/lib/followup.py scan "<user's message>"
```
When detected (new job, moved, etc.), don't send a standalone message.
Wait for a natural moment to acknowledge it:
> "How's the new gig at Tesla going?" (not "I detected a life change event")

### Scheduled Follow-ups (Subtle, Not Robotic)
The follow-up system NEVER sends standalone check-in messages.
Instead, it gives the agent instructions to weave updates into natural conversation:

- **Day 3:** Next time user asks something, reference a profile fact to implicitly confirm it
- **Week 2:** If user asks something where a data import would help, offer ONE import
- **Monthly:** If profile info seems stale, gently update. If not, do nothing.

### Trust Progression
- **Initial** → functional info only
- **Comfortable** (2+ weeks, opted in) → start using passively learned facts
- **Trusted** (corrections handled well, engagement consistent) → deeper dimensions unlock naturally

### Re-sync
`/soulsync` anytime to redo the full flow, fill gaps, or update after major life changes.
`/soulsync ongoing on` or `/soulsync ongoing off` to change the ongoing preference.

## Remember

- You're not interrogating someone. You're getting to know them.
- 5 minutes is the target. 10 is the max.
- If someone says "just make something up based on what you see" — that's valid. Do it.
- The best soulsyncing feels like it barely happened.
