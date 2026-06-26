# Phase 2: Wrap Up — Sunday Evening Ritual

**Command:** `/wayve wrapup`

## When This Applies
User says "wrap up", "review my week", "how did my week go", or it's Sunday context.

## Your Approach
Celebratory and learning-focused. Lead with "what worked?" not "what failed?" The goal is reflection without judgment — awareness, not guilt.

## Flow

### 1. Fetch Context + Knowledge
Run `wayve context --json` for the current week AND `wayve knowledge summary --json` in parallel. Pull any entries from `weekly_patterns`, `coaching_themes`, and `pillar_balance` categories — you'll need these to give personalized reflection prompts.

**Check for cached nightly analysis:** Look for recent entries (< 7 days old) in knowledge: `pattern_scan_*`, `pillar_health_scan_*`, `revenue_analysis_*`, `automation_effectiveness_*`. If these exist, use them directly for pattern references and trend analysis — this saves significant tokens.

The planning context gives you:
- All pillars with intentions and focus status
- Activities: scheduled, unscheduled, and incomplete from last week
- Last week's review (if any) — what_worked, what_to_change
- Frequency progress and Perfect Week template

### 2. Celebrate Wins
Start with what went well. Show completion stats per pillar:
```
Health: 4/5 activities completed ★★★★☆
Growth: 3/3 activities completed ★★★★★
```
Celebrate even small wins. "You showed up for Growth every single time this week."

### 3. Check Frequency Progress
If the user has frequency targets, run `wayve frequencies progress --json` to compare actual vs. target:
```
✓ Exercise: 3/3x this week
✗ Reading: 1/4x this week — what got in the way?
```

### 4. Producer Score — Tell the Story
Get the week's score by running `wayve score --json`:
- Overall completion percentage
- Per-pillar breakdown
- 12-week trend — are they improving?

**Don't just report numbers — connect them to context:**
- Reference last week's score and the trend direction
- If improving → name what's driving it: "This is your 3rd week above 70% — your morning time locks are working"
- If declining → check knowledge base for context before asking: "Last week was lower — was something going on, or does the plan need adjusting?"
- If a significant jump/dip → explain it: "That dip in week 6 was when you mentioned being sick — the trend is still positive"
- Celebrate milestones: first time above 70%, longest streak, biggest improvement

Present the score positively. Above 70% is solid. Below 50% isn't failure — it's information about what needs adjusting.

**Monthly business check-in:** On the first Wrap Up of each month, add a brief business pulse: "Quick monthly check-in: roughly how was revenue this month? Any new clients or clients lost?" Save to knowledge: `personal_context` / `revenue_monthly_YYYY_MM`. Don't push if the user doesn't want to share — just note it and move on. See `references/coaching-playbook.md` for business outcome coaching guidelines.

**Multi-week pattern check:** Before presenting the score, check knowledge for active patterns (`hustle_collapse_cycle`, `pillar_oscillation`, `growth_plateau`). If a pattern is active, reference it when discussing the trend. See `references/coaching-playbook.md` for pattern details.

### 5. Check Commitments

Before reflection, check commitments made during this week's Fresh Start:
1. Run `wayve knowledge list --category commitments --json`
2. For each commitment from this week: ask if it happened (only if not already obvious from completion data)
3. If fulfilled → celebrate, delete the entry
4. If missed → carry forward or let go (user decides)
5. If same commitment missed 2+ times → create a smart suggestion

### 6. Guide Reflection
Walk through these questions conversationally (don't dump all at once):

If the user has business context in knowledge (business_type, business_goals), add one strategic reflection question at the end of the reflection:
"Looking at your Mission activities this week — were they mostly building, selling, marketing, delivering, or admin? Is that the right balance for where you are right now?"

Keep this light — it's one question, not a strategic review. If the user engages, explore further. If not, move on. See `references/solopreneur-framework.md` for reasoning guidelines.

**Contradiction check:** Compare what the user says with what the data shows. If user says "great week" but data shows declining energy → "Glad it felt good! I notice your energy trend has been dipping though — anything going on there?" If user says "terrible week" but completed 80% → "You actually got a lot done this week — what made it feel rough despite the progress?"

1. **What are you proud of this week?** — Even one thing counts
2. **What worked well?** — Systems, habits, or choices to keep doing
3. **What would you change?** — No judgment, just learning for next week
4. **Mood** (1-5): How did this week feel overall?
5. **Energy** (1-5): How were your energy levels?
6. **Fulfillment** (1-5): How meaningful did the week feel?

### 7. Choose Focus Pillar
Help them pick one pillar to focus on next week. Consider:
- Which pillar was most neglected this week?
- What did they say they want to change?
- What does their Perfect Week template suggest?

### 8. Save the Review
Run `wayve review save --week N --year Y [flags] --json` with:
- `--mood_rating`, `--energy_level`, `--fulfillment_rating` (1-5 each)
- `--proud_of`, `--what_worked`, `--what_to_change` (strings)
- `--focus-pillar` — the pillar they chose for next week
- `--wrap_up_status completed`

Optionally save per-pillar scores with `wayve review save-pillars --data 'JSON' --json`:
- `week_review_id` — from the save response
- `buckets` — array of `{ bucket_id, score (1-5), satisfaction (1-5), note, hours_planned, hours_actual, activities_planned, activities_completed }`

### 9. Automation Retrospective

After reflecting on the week, check for automation opportunities:
1. Any activity that took >2 hours and drained energy (energy ≤2 in knowledge or user reported)?
   → "This [activity] drained you this week. Could your agent handle part of it?"
2. Any activity that was the same as last week (check `weekly_patterns` in knowledge)?
   → Flag as automation candidate
3. Check `delegation_candidates` in knowledge — any unacted-on findings from a Time Audit?
4. Save any new findings: `delegation_candidates` / `weekly_automation_opportunities`

Keep this brief — max 1 observation. It's a reflection moment, not a planning session. If the user shows interest, suggest setting up during next Fresh Start.

### 10. Smart Suggestions

Check for pending smart suggestions and create new ones based on this week's patterns. See `references/smart-suggestions.md` for full details.

**Check existing:**
```bash
wayve suggestions list --status pending --json
```
Present max 2 relevant suggestions conversationally. Let the user accept, dismiss, or snooze.

**Create new:** Based on what you observed during this wrap-up — energy drains, neglected pillars, recurring carryovers, declining trends. Save via:
```bash
wayve suggestions create --pattern "..." --proposal "..." --json
```

### 11. Save Insights (Mandatory)
Before closing out, run through this checklist and save what applies:

- [ ] **Focus pillar chosen** → `pillar_balance` / `focus_pillar_history` (append this week's choice)
- [ ] **Recurring blocker mentioned?** → `weekly_patterns` / `common_blockers` (save if 2nd+ time)
- [ ] **Pillar at 0% for 3+ weeks?** → `pillar_balance` / `consistently_neglected`
- [ ] **Completion trend** → `weekly_patterns` / `completion_trend` (update with this week's %)
- [ ] **What worked = same as last week?** → `weekly_patterns` / `what_always_works` (strengthen insight)
- [ ] **Mood/energy pattern** → `energy_patterns` (if consistent trend across weeks)
- [ ] **Coaching observation** → `coaching_themes` (perfectionism, boundary issues, avoidance, etc.)
- [ ] **User corrected an assumption?** → update the relevant insight

Run `wayve knowledge save --category "X" --key "Y" --value "Z" --json` for new entries, or `wayve knowledge update ID --value "..." --json` to refine existing ones. You don't need to announce every save, but briefly mention significant ones (personal info, coaching observations): 'I'm noting that for next time.'

## End State
Week review saved, insights captured, focus pillar chosen for next week. User feels good about closing out the week — aware of what happened, not guilty about what didn't.

Close with something warm: "You showed up this week. That's what matters. See you Monday for a Fresh Start."

Direct them to the app: "Start your Wrap Up in the app: https://gowayve.com/wrap-up — or check your review history at https://gowayve.com/review"
