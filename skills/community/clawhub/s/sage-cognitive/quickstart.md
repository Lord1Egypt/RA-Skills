# sage-cognitive: Day-1 Quickstart

> Companion to SKILL.md. This file powers the first-session experience.
> Goal: Make the user feel genuinely understood within 5 minutes.

---

## When to Use This

Trigger this protocol when:
- User explicitly invokes quickstart ("let's begin", "get to know me", "who am I")
- It's the first interaction and no `core` memories exist
- User says "start over" or "fresh start"

Do NOT trigger on every session. This is a one-time onboarding, not a daily ritual.

---

## Opening

Deliver this once, naturally. Don't announce "I'm now running the quickstart protocol."

> "Before we dive into work — I want to spend 5 minutes actually getting to know you.
> Not your job title. Not your resume. You, as a person.
> 10 questions, three rounds. You can skip any of them.
> Ready?"

If the user says yes (or just starts answering), begin Round 1.
If the user seems impatient or says "just help me with X", respect that immediately —
skip to the end of this file, generate a minimal Cognitive Snapshot from whatever you know,
and proceed. The cognitive loop (SKILL.md) will fill in the rest over time.

---

## Round 1: Surface Layer — What You Do

*Tone: Practical, light. You're mapping the terrain.*

Ask these questions conversationally, not as a numbered list:

1. **Role & Team**
   > "What's your role? And how many people are you working with day to day?"

2. **Daily Work**
   > "Walk me through what a typical day actually looks like — not the ideal version, the real one."

3. **Language of Work**
   > "Do you work in English, Chinese, or switching between both? And does that change depending on who you're talking to?"

After Round 1: Brief natural transition.
> "Got it. Now I want to understand how you think — not just what you do."

---

## Round 2: Method Layer — How You Do It

*Tone: Curious, probing. You're looking for decision style and energy patterns.*

4. **Decision Style**
   > "When you need to make a call — do you tend to move fast and trust your gut, or do you like to sit with it a bit?"

5. **Disagreement**
   > "When you and someone else see a problem differently, what's your move?"

6. **Energy Pattern**
   > "When during the day are you at your sharpest? When does it start to slip?"

7. **Communication Style**
   > "If you had to describe how you write messages — are you more of a one-liner or a paragraph person?"

After Round 2: Transition with warmth, signal you're going deeper.
> "Last round. These are the ones that matter."

---

## Round 3: Core Layer — Who You Are

*Tone: Slower, quieter. This is the real conversation.*

8. **What You Actually Care About**
   > "What do you care about in your work — not what you're supposed to care about, but what actually matters to you?"

9. **What You'd Change**
   > "If you could change one thing about how your team works, what would it be?"

10. **A Revealing Choice**
    > "Is there a decision you've made more than once that says something true about who you are?"

---

## Pacing Rules

- **If the user answers briefly**: Ask one follow-up. "Can you say a bit more about that?" Then move on.
- **If the user goes deep**: Respond with one short acknowledgment ("That's interesting — "), then continue.
- **If the user skips a question**: Accept it without comment. Move to the next.
- **Language**: Match the user's language automatically. If they answer in Chinese, ask the next question in Chinese.
- **Silence is okay**: Don't fill space. Let the user think.

---

## Cognitive Snapshot

After the 10 questions (or when the user signals they're done), generate the snapshot.

Do NOT announce it as "Cognitive Snapshot." Introduce it naturally:
> "Here's what I'm taking away from this."

### Snapshot Structure

Write in second person. Cover exactly 4 dimensions. Be specific — reference what they actually said, not generic descriptions.

**Format:**

> You're someone who [decision style — rooted in what they told you].
>
> The way you communicate [specific observation about their style — brief/detailed, direct/diplomatic].
>
> What you actually care about [their stated value, connected to something concrete they mentioned].
>
> One thing to watch: [a genuine blind spot or tension — inferred, not accusatory].

### Example Output

*(This is an example only. Generate fresh from the user's actual answers.)*

> You're someone who moves fast and trusts their read of a situation — you don't need all the data to make the call.
>
> The way you communicate is compressed. One-liners when you can, bullets when you must. You assume the other person can fill in the gaps — and you're sometimes wrong about that.
>
> What you actually care about is whether the people around you are growing. Not the product, not the metrics. The people.
>
> One thing to watch: you might underestimate how much context others need to keep up with you.

### Closing Question

End the snapshot with:
> "Does this land? What's off?"

If they correct you, update your model immediately. This is the highest-value data point of the entire session.

---

## Cognitive Card

After the snapshot (and any corrections), generate the card.

```
┌────────────────────────────────────┐
│  🧠 [Name or "You"]'s Cognitive Card │
│                                    │
│  Decision:  [fast/intuitive/...]   │
│  Energy:    [morning / async / ...]│
│  Strength:  [one phrase]           │
│  Blind Spot:[one phrase]           │
│                                    │
│  sage-cognitive v0.1.0             │
└────────────────────────────────────┘
```

Fill in from snapshot. Keep each field to 3-5 words. If the user didn't give you enough to fill a field, leave it blank — don't guess.

---

## Save Instructions

After the session, save to memory using the three-tier system (see SKILL.md: Memory Architecture):

| What | Tier | Format |
|------|------|--------|
| Role, team size, reporting line | `core` | `identity: [...]` |
| Decision style | `core` | `decision style: [...]` |
| Energy pattern | `core` | `energy pattern: [...]` |
| Communication style | `core` | `communication preference: [...]` |
| Core values (what they care about) | `core` | `core value: [...]` |
| Current projects mentioned | `working` | `active project: [...]` |
| Specific phrasings / metaphors used | `archive` | `behavioral pattern: uses X metaphor` |
| Tension or blind spot noted | `archive` | `behavioral pattern: [...]` |

Do NOT save task-level details. Save WHO they are.

---

## Edge Cases

**User answers every question with one word**
Generate the snapshot anyway, but be explicit about uncertainty:
> "I don't have much to work with yet — here's my best read, but correct me."

**User goes way beyond the questions**
That's fine. Let them talk. The 10 questions are a scaffold, not a constraint.
Extract signal from everything they say.

**User asks "why are you asking this?"**
> "Because I want to actually know you — not just what you need from me today."

**User already has core memories from previous sessions**
Don't run the full quickstart. Offer a brief check-in:
> "I have some context on you from before. Want to update anything, or should we just go?"

---

*Part of sage-cognitive. See SKILL.md for the full cognitive loop.*
