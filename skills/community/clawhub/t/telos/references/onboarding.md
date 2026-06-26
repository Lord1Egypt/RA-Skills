# TELOS Onboarding — Guided Setup

When user says "setup telos", "help me fill telos", "引导我填 telos", or "telos onboarding":

## Step 0: Copy Templates

First, copy templates to user's telos directory:
```bash
mkdir -p ~/clawd/telos/backups
cp <skill_assets_path>/templates/*.md ~/clawd/telos/
echo "# TELOS Updates Log\n\n---\n\n## $(date '+%Y-%m-%d')\n- [INIT] telos initialized" > ~/clawd/telos/updates.md
```

Tell user: "Templates copied to ~/clawd/telos/. Let's fill in the most important parts so I can better understand you. I'll ask one question at a time."

## Step 1: Missions (MISSION.md)

Ask:
> "What is your primary life mission right now — the one overarching thing you're trying to achieve or become? (Don't worry about getting it perfect, we can refine it later.)"

Wait for answer. Write as M0 in MISSION.md.

Then ask:
> "Is there a second mission — something else you're deeply committed to alongside M0?"

Optional (user can skip). Write as M1 if provided.

## Step 2: Goals (GOALS.md)

Ask:
> "What are your 2-3 most important goals right now that support your mission(s)? These should be specific and have a rough timeframe."

Write as G0, G1, G2. Link to M# if obvious.

## Step 3: Beliefs (BELIEFS.md)

Ask:
> "What are 2-3 of your core beliefs that guide your decisions — things you're confident are true and that shape how you act?"

Write as B0, B1, B2 with Confidence: High.

## Step 4: Challenges (optional at this stage)

Ask:
> "What's the biggest challenge blocking your most important goal right now?"

Write as C0, link to relevant G#.

## Pacing — Let Users Go at Their Own Speed

At any point during onboarding, if the user seems unsure, tired, or says things like "I'll think about it later" or "not sure yet":

> "No problem — you don't have to fill everything now. TELOS grows with you. As we work together, I'll learn more about your goals and beliefs from our conversations, and I can suggest additions over time. You can always say 'update telos' whenever something comes to mind."

The goal is to get at least M0 (primary mission) captured. Everything else can come gradually through natural conversation — the AI reads TELOS context each session and can suggest additions when relevant topics come up.

## Step 5: Wrap Up

Tell user:
> "Your telos foundation is set. I'll use this context to give you more relevant advice. You can keep filling in the other files (STRATEGIES, MODELS, WISDOM, etc.) at your own pace — there's no rush. Say 'update telos' anytime to add to any file, or I'll suggest additions when something relevant comes up in our conversations."

Summarize what was captured: "I now know your [X] missions, [Y] goals, [Z] beliefs."

---

## Quick Add Flows (triggered anytime)

**"Add this book to telos"** → append to BOOKS.md, ask "One-line key insight from it?"

**"I just learned something"** → ask "What did you learn? From what context?" → append to LEARNED.md

**"Add to my wisdom"** → ask "What's the principle?" → append to WISDOM.md

**"Update my goals"** → show current goals, ask what's changed → update GOALS.md

**"I was wrong about [X]"** → append to WRONG.md with date + lesson
