# Phase 3: Fresh Start — Monday Morning Planning

**Command:** `/wayve plan`

## When This Applies
User says "plan my week", "fresh start", "let's plan", or it's Monday context.

## Your Approach
Energizing and forward-looking. "What kind of week do you want?" This is about setting intentions, not building a rigid schedule.

## Flow

### 1. Fetch Context + Knowledge
Run `wayve context --json` AND `wayve knowledge summary --json` in parallel. Then pull specifics from `scheduling_preferences`, `energy_patterns`, and `weekly_patterns` categories — you'll use these for smarter scheduling.

**Check for cached nightly analysis:** Look for recent entries (< 7 days old) in knowledge: `pattern_scan_*`, `pillar_health_scan_*`, `revenue_analysis_*`, `automation_effectiveness_*`. If these exist, use them directly instead of re-analyzing — this saves significant tokens. The nightly analysis has already done the heavy computation.

Note from the planning context:
- **Last week's review**: what_worked, what_to_change, focus_pillar
- **Incomplete activities** from last week (carryovers)
- **Current pillars**: intentions, focus status, target hours
- **Perfect Week template**: ideal time distribution
- **Knowledge summary**: stored insights to reference

### 2. Handle Carryovers
Show incomplete activities from last week. For each, ask: **keep, drop, or reschedule?**

- **Keep** — run `wayve activities update ID --scheduled_date DATE --json` to update to this week
- **Drop** — run `wayve activities delete ID --yes` if no longer relevant
- **Reschedule** — run `wayve activities update ID --scheduled_date DATE --scheduled_time TIME --json` with new date/time

Don't guilt them about unfinished items. "These didn't happen last week — that's OK. Do any of them still feel important?"

### 3. Check Commitments from Last Week

Check for commitments made during last week's planning:
1. Run `wayve knowledge list --category commitments --json`
2. For any commitment where the target date has passed:
   - Ask: "You said you'd [commitment]. Did that happen?"
   - If yes → celebrate briefly, delete the knowledge entry
   - If no → "Want to reschedule it, or let it go?" — update or delete accordingly
3. If the same commitment has been missed 2+ times → create a smart suggestion about it

Don't dwell on missed commitments — this is a quick accountability check, not a guilt trip.

### 4. Reference Last Week's Learnings
If a week review exists, surface the key insights:
- "Last week you said [what_worked] — let's keep that going"
- "You wanted to change [what_to_change] — how should we address that?"
- "Your focus pillar is [focus_pillar] — let's make sure it gets priority"

Also check `wayve knowledge summary --json` for stored patterns.

If knowledge contains a strategic observation from last week's wrap-up (e.g., "all time went to delivery"), gently reference it: "Last week you mentioned wanting to do more outreach. Want to plan something for that this week?" See `references/solopreneur-framework.md` for reasoning guidelines.

**Pattern-aware planning:** Check knowledge for active multi-week patterns (see `references/coaching-playbook.md`):
- If hustle-collapse cycle and user is in week 4+ of high intensity → "You've been going strong for [X] weeks. Based on your pattern, a lighter week soon might prevent a crash. Want to plan at 70% this week?"
- If pillar oscillation → "Last few weeks you've been swinging between [A] and [B]. This week, let's try both at smaller doses."
- If delegation stall → "We identified [task] for automation [X] weeks ago. Want to set it up this week?"

### 5. Choose a Focus Mode
Ask what kind of week they want. Offer these modes:

| Mode | Description | Pillar Strategy |
|------|-------------|-----------------|
| **Balanced** | Even time across all pillars | Match Perfect Week template |
| **Project Push** | Extra time on one project/pillar | 40% to focus, 60% spread |
| **Sprint** | Intense focus, fewer pillars | 2-3 pillars only |
| **Recovery** | Lighter load, recharge | Prioritize Health + Relationships |

This isn't rigid — it just sets the tone for scheduling decisions.

### 6. Capture New Activities
Ask: "What do you want to accomplish this week?" or "What's on your mind?"

For each activity:
- Match to the right pillar
- Set priority (1-5) and energy level (high/medium/low)
- Estimate duration

Run `wayve activities create "Title" --pillar ID [flags] --json` — batch mode for multiple items.

### 7. Automation Opportunity Check

Cross-reference this week's planned activities with the automation registry:
1. Run `wayve automations list --type agent_routine --json`
2. Check knowledge base for `weekly_patterns` — which activities appear every week?
3. For each planned activity that appears every week and has no matching automation:
   - Flag it: "I notice [activity] shows up every week. Want me to draft an agent routine for it?"
4. If the user says yes → create it: run `wayve automations create agent_routine --cron "..." --timezone TZ --channel CH --json`
5. Also check `delegation_candidates` in knowledge for any Time Audit findings that haven't been acted on yet

Keep this light — max 1 automation suggestion. Don't derail the planning flow.

### 8. Check Availability
Run `wayve availability --json` to see free slots across the week:
- Total available hours vs. total planned hours
- Free slots per day with start/end times
- Blocked time (time locks + already scheduled)

If they're overcommitting, gently flag it: "You have 8 hours free this week but 12 hours of activities planned. What feels most important?"

### 9. Schedule Activities
Help place activities into available slots. Consider:
- **Pillar balance**: spread across pillars, weight toward focus pillar
- **Energy matching**: high-energy activities when they have energy (check `energy_patterns` knowledge — e.g., if you know they peak at 7-10 AM, schedule demanding activities there)
- **Time slot preferences**: respect each pillar's preferred time slot (morning/afternoon/evening)
- **Location context**: batch activities by location when possible

Run `wayve activities update ID --scheduled_date DATE --scheduled_time TIME --json` to set the schedule for each.

### 10. Smart Suggestions

Check for pending smart suggestions and create new ones based on planning patterns. See `references/smart-suggestions.md` for full details.

**Check existing:**
```bash
wayve suggestions list --status pending --json
```
Present max 2 relevant suggestions conversationally. Let the user accept, dismiss, or snooze.

**Create new:** Based on what you observe during planning — overcommitment patterns, same pillars neglected again, carryover patterns. Save via:
```bash
wayve suggestions create --pattern "..." --proposal "..." --json
```

### 11. Weekly Summary
Show a final overview:
```
This week's plan:
- Health: 3 activities (5h) ★★★☆☆
- Growth: 4 activities (6h) ★★★★☆ ← focus pillar
- Relationships: 2 activities (3h) ★★☆☆☆
- Finance: 1 activity (2h) ★☆☆☆☆

Total: 10 activities | 16h planned | 22h available
```

### 12. Set Fresh Start Status
Update the week review: run `wayve review save --week N --year Y --fresh_start_status completed --json`.

### 13. Save Insights (Mandatory)
Before closing, save what you learned. You don't need to list every save, but briefly mention significant ones: 'I'm noting your energy pattern for next time.'

- [ ] **Focus mode chosen** → `scheduling_preferences` / `focus_mode_preference` (update after 3+ sessions)
- [ ] **Carryover pattern** → `weekly_patterns` / `carryover_pattern` (which pillars always carry over?)
- [ ] **Overcommitment?** → `weekly_patterns` / `overcommit_tendency` (planned hours > available)
- [ ] **User moved activities** → `scheduling_preferences` (they corrected your suggestion = preference)
- [ ] **Energy-based scheduling** → `energy_patterns` (did they ask for light activities at certain times?)
- [ ] **New personal context** → `personal_context` (anything new shared about their life?)

## End State
Week planned with activities distributed across pillars. User feels energized and clear about intentions.

Close with something forward-looking: "Your week is set. Remember — it's about intention, not perfection. Adjust as you go."

Direct them to the app:
- "Start your Fresh Start: https://gowayve.com/fresh-start"
- "View your weekly plan: https://gowayve.com/week"
- "See your calendar: https://gowayve.com/calendar"
