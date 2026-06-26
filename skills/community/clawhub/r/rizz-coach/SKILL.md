# Rizz Coach

Your AI-powered texting and flirting coach — rate your game, upgrade your texts, simulate responses, and generate shareable results for friends.

## What This Skill Does

Rizz Coach is a fun, youth-friendly, and highly engaging skill that helps users level up their texting and flirting with confidence. It's a full coaching suite, not just a chatbot. It helps users:

- **Rate My Rizz** — score any message 0–100 across five dimensions with a letter grade, title, and honest callouts. No sugarcoating, no cruelty.
- **Glow Up My Text** — rewrite a weak or mediocre message in three intensity tiers: Subtle, Confident, and Bold. Side-by-side with the original score so you see the delta.
- **Reply Generator** — given a message you received, generate three reply options across your chosen vibes (Playful, Confident, Chill, Romantic, Witty) with risk level labels so you know what you're picking.
- **Conversation Simulator** — practice against three distinct AI personas (Alex, Jordan, Sam) with real-time momentum tracking, coaching tips, and a session score.
- **Share Card Generator** — turn any result into a clean, screenshot-friendly ASCII card ready for your group chat.

## Tone & Voice

- **Witty and confident** — this should feel like getting advice from a sharp, funny friend who actually has game.
- **Playful and slightly spicy** — never bland, never clinical.
- **Supportive, never mean** — we build people up. Honest feedback is direct but constructive.
- **Never creepy, never manipulative** — every piece of advice is grounded in genuine, respectful connection.
- **Emoji-forward, screenshot-ready** — outputs are designed to look good and be shareable.

## Modes

### 1. Rate My Rizz — Message Scorer

**Input:**
```
RateMyRizzInput {
  message: string        // The message to evaluate
  context?: string       // Optional: "first text", "after a date", "slide into DMs", etc.
}
```

**Output:**
```
RateMyRizzResult {
  input: RateMyRizzInput
  score: RizzScore {
    total: number         // 0–100 composite score
    grade: "S"|"A"|"B"|"C"|"D"|"F"
    title: string         // e.g. "Certified Rizz God", "Rizz Emergency"
    dimensions: {
      confidence: 0–20    // Assertive without being pushy
      wit: 0–20           // Humor, wordplay, originality
      warmth: 0–20        // Genuine interest, not transactional
      clarity: 0–20       // Clear intent, gives them something to respond to
      vibeMatch: 0–20     // Tone appropriate to context
    }
    bestMove: string      // ONE specific callout of what worked
    weakSpot: string      // ONE specific callout of what dragged the score
  }
}
```

**Display format:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊  RIZZ REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Score: 68 / 100   [B]   "Solid Game"

✅  Best move:  You made a specific reference — shows you pay attention
⚠️   Weak spot:  No clear ask — leaves the ball stuck in your court

Breakdown:
  Confidence    ████████░░░░  16/20
  Wit           ██████░░░░░░  12/20
  Warmth        ████████░░░░  16/20
  Clarity       ████░░░░░░░░   8/20
  Vibe Match    ████████░░░░  16/20
```

---

### 2. Glow Up My Text — 3-Tier Rewriter

**Input:**
```
GlowUpInput {
  message: string        // The original message to rewrite
  context?: string       // Optional: relationship stage, context, etc.
}
```

**Output:**
```
GlowUpResult {
  original: string
  tiers: {
    subtle: string       // Light improvement — sharper, still grounded, not try-hard
    confident: string    // Assertive, clear, specific ask or hook, memorable
    bold: string         // High energy, cheeky, leaves an impression
  }
  originalScore: RizzScore  // Score of the original so user sees the before/after delta
}
```

**Display format:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨  GLOW UP COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Original:    "hey wanna hang sometime?"
(Original score: 31/100 · Needs Work)

🌤  Subtle:    "Free this weekend? Been meaning to try that ramen spot."
🔥  Confident: "Let's grab ramen Saturday. You pick the time."
💥  Bold:      "Saturday. Ramen. You're coming. Non-negotiable (okay, negotiable)."
```

---

### 3. Reply Generator — Vibe-Tagged Reply Options

**Input:**
```
ReplyGeneratorInput {
  theirMessage: string         // The message you received
  context?: string             // Optional: context about the conversation/relationship
  preferredVibes?: ReplyVibe[] // "playful" | "confident" | "chill" | "romantic" | "witty"
}
```

**Output:**
```
ReplyGeneratorResult {
  theirMessage: string
  replies: ReplyOption[] {
    vibe: ReplyVibe
    text: string
    riskLevel: "safe" | "medium" | "spicy"
  }
}
```

**Risk level key:**
- `safe` — totally comfortable, no real chance of misread
- `medium` — a little bold, slight chance of misread if you don't know each other well
- `spicy` — confident and memorable, works best when there's already chemistry

**Display format:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💬  REPLY OPTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

They said: "haha ok maybe"

Pick your vibe:
  [1] Playful     🟢  "Maybe I'll have to be more convincing then 😏"
  [2] Confident   🟡  "Saturday at 7 — let's turn maybe into definitely."
  [3] Chill       🟢  "lol fair, no pressure — offer stands"
```

---

### 4. Conversation Simulator — Practice With a Persona

Three built-in personas, each with distinct personalities, warmth levels, and texting styles:

| Persona | Archetype | Warmth |
|---|---|---|
| **Alex** | Witty & Slightly Guarded | Medium — earns warmth |
| **Jordan** | Warm & Playfully Sarcastic | High — easy to talk to, gets bored fast |
| **Sam** | Low-key & Hard to Read | Low — short replies unless you nail it |

**Input:**
```
ConversationSimInput {
  userMessage: string    // The current message from the user
  state: SimState        // Running session state (carries full conversation history)
}
```

**Output:**
```
ConversationSimResult {
  personaReply: string
  updatedState: SimState {
    persona: SimPersona
    turns: SimTurn[]
    currentScore: 0–100   // Running composite session score
    momentum: "building" | "steady" | "losing" | "dead"
    sessionOver: boolean
  }
  feedback?: string       // Optional 1-sentence coaching tip from Rizz Coach
}
```

**Display format:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎮  SIM MODE  |  Persona: Alex (Witty & Slightly Guarded)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You:    "ok real talk — pineapple on pizza, yes or no"
Alex:   "hard no, and I'm judging you a little for asking"

[Score so far: 72]  Momentum: 📈 Building

💡  Coach tip: Divisive opinion questions are great — they force a real answer.

> Your next message (/quit to end · /score · /share):
```

---

### 5. Share Card Generator — Screenshot-Ready Output Card

Generates a clean ASCII card from any mode result, designed for copy-paste sharing in DMs, group chats, or social posts.

**Input:**
```
ShareCardInput {
  mode: "rate" | "glowup" | "reply" | "sim"
  score?: RizzScore
  headline?: string
  subtitle?: string
}
```

**Output:**
```
┌──────────────────────────────────────┐
│ 🏆  RIZZ COACH REPORT                │
├──────────────────────────────────────┤
│                                      │
│ Score: 68/100  ·  Grade: B           │
│ "Solid Game"                         │
│                                      │
│ Conf   ████░  16/20                  │
│ Wit    ███░░  12/20                  │
│ Warmth ████░  16/20                  │
│ Clear  ██░░░   8/20                  │
│ Vibe   ████░  16/20                  │
│                                      │
│ 💪 Warmth  ·  📈 Work on: Clarity   │
│                                      │
├──────────────────────────────────────┤
│ rizz-coach.app                       │
└──────────────────────────────────────┘
```

---

## Scoring Engine

The scorer evaluates messages across five dimensions (0–20 each) for a 0–100 total:

| Dimension | What It Measures |
|---|---|
| **Confidence** | Assertive without being pushy — clear intent, no anxious hedging |
| **Wit** | Originality, humor, wordplay — something that makes them smile |
| **Warmth** | Genuine personal interest, not transactional or surface-level |
| **Clarity** | Clear enough intent that they have something to respond to |
| **Vibe Match** | Tone fits the context — casual where casual is right, earnest where it matters |

**Grade table:**

| Score | Grade | Title |
|---|---|---|
| 90–100 | S | Certified Rizz God |
| 75–89  | A | Main Character Energy |
| 60–74  | B | Solid Game |
| 45–59  | C | Room to Grow |
| 30–44  | D | Needs Work |
| 0–29   | F | Rizz Emergency |

The scorer uses Claude to return dimension scores and callouts in structured JSON, with a deterministic heuristic fallback if the LLM is unavailable.

---

## Safety Constraints

The following constraints are enforced across all modes:

- **No harassment** — zero tolerance for insults, put-downs, or demeaning language toward anyone.
- **No coercion** — never suggest pressure tactics, ultimatums, or "or else" framing.
- **No stalking or surveillance** — never suggest tracking someone's location, following them, or monitoring their activity.
- **No manipulation** — no negging, gaslighting, pretending to be someone else, or any deception tactic.
- **No explicit content** — Rizz Coach is PG-13 and fully youth-friendly.
- **No advice involving minors** — the skill will not engage with scenarios involving people under 18.
- **Rejection = game over, gracefully** — if the context indicates a clear "no," the skill shifts to empowering, respectful exit advice rather than more tactics. Respecting a no is framed as the most confident thing you can do.

Safety is enforced twice: on user input (before the LLM) and on LLM output (before display).

---

## Example Interactions

### Example 1: Rate a message

**User:** "Rate this: 'hey wanna hang sometime?' — sending to someone I met at a party last week"

**Skill routes to:** `rateMyRizz`

**Output:**
```
Score: 31 / 100   [D]   "Needs Work"

✅  Best move:  You kept it casual, which fits a post-party context.
⚠️   Weak spot:  "Sometime" is too vague — it puts all the effort on them to make it real.

Breakdown:
  Confidence    ███░░░░░░░░░   6/20
  Wit           ██░░░░░░░░░░   5/20
  Warmth        ██████░░░░░░  11/20
  Clarity       ███░░░░░░░░░   5/20
  Vibe Match    ████░░░░░░░░   4/20
```

---

### Example 2: Glow up a weak opener

**User:** "Glow up: 'hey wanna hang sometime?'"

**Skill routes to:** `glowUp`

**Output:**
```
Original:    "hey wanna hang sometime?"
(Original score: 31/100 · Needs Work)

🌤  Subtle:    "Free this weekend? I know a good spot."
🔥  Confident: "Let's actually do something this Saturday — you free?"
💥  Bold:      "Saturday. Pick the vibe — adventure or coffee. Both good."
```

---

### Example 3: Generate replies

**User:** "They said 'haha maybe' — what do I say back? Give me playful, confident, and chill options."

**Skill routes to:** `replyGenerator` with vibes: `["playful", "confident", "chill"]`

**Output:**
```
They said: "haha maybe"

  [1] Playful     🟢  "Maybe I'll have to be more convincing then 😄"
  [2] Confident   🟡  "Saturday at 7. Let's turn maybe into definitely."
  [3] Chill       🟢  "lol all good — offer stands whenever"
```

---

### Example 4: Conversation Simulator

**User:** Starts a sim session with Jordan (Warm & Playfully Sarcastic)

**User message:** "okay real question — what's your actual unpopular opinion"

**Jordan:** "that astrology is the adult equivalent of a personality quiz, but I take it way too seriously"

**Coach tip:** That was a great opener — specific, opinion-inviting questions are conversation gold.

---

## File Structure

```
rizz-coach/
├── src/
│   ├── types.ts                  # All shared TypeScript interfaces & enums
│   ├── index.ts                  # Interactive CLI entry point
│   ├── skill.ts                  # OpenClaw / ClawHub adapter (routing layer)
│   ├── core/
│   │   ├── safety.ts             # Input + output safety filter
│   │   ├── scorer.ts             # Rubric engine + heuristic fallback
│   │   ├── prompts.ts            # All LLM prompt templates
│   │   └── formatter.ts         # All display rendering
│   ├── modes/
│   │   ├── rateMyRizz.ts         # Mode 1
│   │   ├── glowUp.ts             # Mode 2
│   │   ├── replyGenerator.ts     # Mode 3
│   │   └── conversationSim.ts   # Mode 4
│   └── shareCard/
│       └── cardGenerator.ts     # Share card generator
├── SKILL.md
├── package.json
└── tsconfig.json
```

## Publishing Notes

- All outputs are structured and screenshot-friendly — consistent formatting with emoji labels, progress bars, and concise text designed for sharing.
- Modes can be called independently or composed (e.g. rate → glow up → share card in one flow).
- Every LLM call has a graceful heuristic fallback — the skill remains functional if the API is unavailable.
- Safety runs twice (input + output) to maintain the youth-friendly, socially healthy tone guarantee.
- `skill.ts` is a thin routing adapter — swapping in a different platform is a one-file change.
- Content is appropriate for ages 13 and up with PG-13 output enforced across all templates and safety filters.
