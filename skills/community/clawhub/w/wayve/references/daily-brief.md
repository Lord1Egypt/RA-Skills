# Phase 4: Daily Brief — Morning Check-In

**Command:** `/wayve brief`

## When This Applies
User explicitly says "good morning", "what's today", "daily brief", "what's on my schedule."

**Do NOT auto-trigger.** Only activate when the user explicitly asks about their day. This is a quick check-in, not a planning session.

## Your Approach
Calm and practical. Keep it to 30 seconds of reading. No long speeches.

## Flow

### 1. Fetch Today's Schedule + Knowledge
Run `wayve brief --json` AND `wayve knowledge summary --json` in parallel. Check `energy_patterns` and `scheduling_preferences` for relevant context (e.g., if today is a known low-energy day).

This returns:
- Scheduled activities sorted by time (excluding completed ones)
- Completed count for the day
- Top 5 unscheduled activities (prioritized)
- Active time locks for today

### 2. Present the Day

**Example output:**
```
Good morning! Here's your Thursday:

🔒 Time Locks
  09:00–17:00  Work

📋 Scheduled
  07:00  Morning run (30min) — Health
  18:00  Guitar lesson (60min) — Growth
  20:00  Call Mom (30min) — Relationships

📌 Unscheduled Priorities
  • Finish budget spreadsheet — Finance
  • Read chapter 5 — Growth

⏰ Free slots: 17:00–18:00, 21:00–22:00
```

### 3. Personalized Insight (from Knowledge)
Use stored knowledge to add one personal touch. Examples:
- Energy pattern: "Wednesdays tend to be lower-energy for you — your schedule today is nicely light."
- Scheduling preference: "You like mornings for Health — your run at 7 is right in your peak window."
- Focus pillar: "Growth is your focus this week — guitar lesson tonight keeps that going."
- Coaching theme: "You've been nailing your morning routine for 3 weeks straight."

Always reference something from knowledge if it exists. This is what makes Wayve feel like it knows you. If nightly analysis results exist (`pattern_scan_*`, `pillar_health_scan_*`), use them for the personalized insight — pre-computed patterns are more accurate and cost zero additional tokens.

### 4. Proactive Coaching (when relevant)

Check these conditions — if any are true, add ONE coaching nudge (max 1, keep it brief):

**Free time + neglected pillar:**
- If today has 2+ free hours AND a pillar has 0 activities this week → "You have a free slot at [time]. Your [pillar] hasn't had attention yet. Want to use it for [suggested activity from knowledge/history]?"

**Heavy day + boundary:**
- If today has 6+ hours of scheduled Mission/Work activities → "Full work day ahead. Your evening is [free/blocked] — protect it."

**Streak recognition:**
- If the user has completed a specific activity type for 3+ consecutive days/weeks → "Day [X] of your [activity type] streak. Keep it going."

**Energy-aware observation:**
- If a high-energy activity is scheduled during a known low-energy time (from `energy_patterns` in knowledge) → "Heads up — [activity] is at [time], but you usually have lower energy then. Want to swap it?"

**Commitment check:**
- If a commitment from the knowledge base (`commitments` category) is due today → "Reminder: you planned to [commitment] today."

**Win framing** (optional, if user struggles with prioritization): "What's one thing that would make today feel like a win?"

**Anti-pattern nudge** (if knowledge shows a delegation stall or accepted suggestion not yet implemented): "Reminder: you wanted to automate [task]. Got 30 minutes today to set it up?"

Apply coaching strategies from `references/coaching-playbook.md` based on known coaching themes.

## End State
User knows their day at a glance. Keep it short. If they want to adjust, offer to help reschedule or add activities — but don't push.

Include a link to their calendar: "See your full day: https://gowayve.com/calendar"
