# Knowledge & Learning System — How Wayve Remembers

Wayve's knowledge base (`wayve knowledge` CLI commands) is the AI's persistent memory about the user. Wayve's knowledge base stores **life planning insights** — patterns, preferences, energy data, recurring themes, and coaching observations that make every conversation smarter than the last.

This is what turns Wayve from a tool into a partner.

## How It Works

```
User interacts → AI observes patterns → Saves to Wayve knowledge base → Next session retrieves → AI gives personalized advice
```

The knowledge base is stored server-side via the Wayve API, so it persists across devices, sessions, and even different AI clients. It travels with the user's Wayve account.

## Mandatory: Always Retrieve Before Advising

**At the start of EVERY planning interaction**, before giving any advice:

1. Run `wayve knowledge summary --json` to see what's stored
2. If relevant categories exist, run `wayve knowledge list --category relevant_category --json` to get specifics
3. Reference stored insights naturally in your conversation — don't list them mechanically

Example: If you know the user prefers morning workouts and has low energy on Wednesdays, don't just dump that info. Weave it in: "I know Wednesdays tend to be lower-energy for you — want to keep it light with a walk instead of the gym?"

## Knowledge Categories & What to Store

### `personal_context` — Who the user is
Save when the user shares personal information that affects planning.

| Key | Example Value | When to Save |
|-----|---------------|--------------|
| `timezone` | `Europe/Amsterdam` | During onboarding or when mentioned |
| `work_schedule` | `Mon-Fri 9-17, remote Wednesdays` | When discussed |
| `family_situation` | `Partner + 2 kids (ages 4, 7)` | When mentioned |
| `commute` | `30 min bike ride` | When setting up time locks |
| `health_conditions` | `Bad knees — no running, prefers swimming` | When mentioned |
| `preferred_name` | `Tom` | First interaction |
| `life_stage` | `Just changed jobs, adjusting to new routine` | When mentioned |
| `business_goals` | `Get to 10 clients by June, launch online course` | During onboarding or when discussed |
| `business_capacity` | `Can handle max 6 clients simultaneously` | During onboarding or when discussed |
| `revenue_monthly` | `~€5000/month, varies` | When user shares during monthly check-in |
| `revenue_monthly_2026_03` | `€4800` | Monthly snapshot during first Wrap Up of month |
| `revenue_target` | `€8000/month by December` | During onboarding or strategy conversation |
| `client_count_current` | `5 active clients` | When user shares |
| `pricing` | `€100/hour consulting, €2500/project design` | When user shares |
| `crisis_event_2026_03` | `Lost biggest client, stressed` | When crisis detected |

### `energy_patterns` — When they're at their best/worst
Save after observing patterns across multiple interactions or from time audit data.

| Key | Example Value | When to Save |
|-----|---------------|--------------|
| `peak_energy_time` | `7-10 AM — best for deep work and exercise` | After time audit or repeated observation |
| `low_energy_time` | `2-4 PM — post-lunch dip, avoid complex activities` | After time audit |
| `low_energy_days` | `Wednesdays tend to be draining (back-to-back meetings)` | After 2-3 weeks of pattern |
| `energizing_activities` | `Running, guitar practice, cooking` | From time audit energy_skill_matrix |
| `draining_activities` | `Admin emails, budget reviews, cleaning` | From time audit energy_skill_matrix |
| `weekend_energy` | `Higher energy Saturdays, rest-focused Sundays` | After observing |

### `scheduling_preferences` — How they like to plan
Save when the user corrects your scheduling suggestions or states preferences.

| Key | Example Value | When to Save |
|-----|---------------|--------------|
| `morning_routine` | `Likes to exercise before work, 6:30-7:30 AM` | When observed/stated |
| `evening_boundary` | `Nothing after 9 PM — wind-down time` | When stated |
| `batch_preference` | `Prefers grouping similar activities on same day` | When they reorganize |
| `scheduling_style` | `Likes flexible time blocks, not minute-by-minute` | When they push back on detailed scheduling |
| `weekend_planning` | `Keeps Sundays unscheduled for spontaneity` | When stated |
| `focus_mode_preference` | `Usually picks Balanced, occasionally Project Push` | After 3+ Fresh Starts |
| `reminder_preference` | `15 min before activities, no evening reminders` | During automation setup |

### `pillar_balance` — Life area patterns
**Note:** Category names like `pillar_balance` are technical keys — when talking to the user, say 'pillar balance' in conversation.

Save after Wrap Ups, Life Scans, or when patterns emerge over weeks.

| Key | Example Value | When to Save |
|-----|---------------|--------------|
| `consistently_neglected` | `Relationships pillar — usually 1/3 target. Work eats into evening time.` | After 3+ weeks of pattern |
| `strongest_pillar` | `Health — consistently hits 100% since January` | After noticing multi-week streak |
| `seasonal_pattern` | `Finance gets more attention end of quarter` | After observing over months |
| `pillar_satisfaction` | `Happiest when Adventure pillar gets at least 2h/week` | From happiness insights |
| `focus_pillar_history` | `Last 4 weeks: Growth, Health, Growth, Relationships` | After each Wrap Up |

### `weekly_patterns` — What happens week to week
Save after Wrap Ups by comparing with previous weeks.

| Key | Example Value | When to Save |
|-----|---------------|--------------|
| `overcommit_tendency` | `Plans 12h but only has 8h available — happens most weeks` | After 2-3 weeks of pattern |
| `completion_trend` | `Improving: 55% → 68% → 74% over last 3 weeks` | After each Wrap Up |
| `hustle_collapse_cycle` | `3-4 weeks high (85%+) then 2-3 weeks low (45%). Last crash: week 8` | After detecting repeating pattern |
| `pillar_oscillation` | `Health and Relationships oscillate every 2-3 weeks` | After detecting for 6+ weeks |
| `growth_plateau` | `Stable at 55-65% for 5 weeks, no improvement` | After 4+ weeks of flat score |
| `seasonal_pattern` | `Q4 always busy (Mission 80%+), January slower` | After 3+ months of data |
| `common_blockers` | `Work meetings running over, kid activities rescheduling` | After hearing same blocker 2+ times |
| `what_always_works` | `Morning Health activities always get done. Evening ones don't.` | After noticing pattern |
| `carryover_pattern` | `Finance activities carry over most — probably overestimating time` | After 3+ Fresh Starts |

### `delegation_candidates` — Things to offload
Save after Time Audits and Life Scans.

| Key | Example Value | When to Save |
|-----|---------------|--------------|
| `delegate_to_person` | `Grocery shopping — partner can take over Wednesdays` | After time audit discussion |
| `automate` | `Bill payments — set up autopay for utilities` | After identifying in audit |
| `eliminate` | `Weekly status report — nobody reads it, ask manager to cancel` | After discussion |
| `batch` | `Email — check 2x/day instead of continuously` | After energy pattern analysis |

### `commitments` — Specific promises the user makes
Save when the user makes a concrete commitment during planning or conversation.

| Key | Example Value | When to Save |
|-----|---------------|--------------|
| `commitment_2026-03-16_call_mom` | `Call mom on Sunday afternoon` | During Fresh Start or conversation |
| `commitment_2026-03-20_proposal` | `Finish client proposal by Thursday` | When user commits to a deadline |
| `commitment_2026-03-18_no_work_evening` | `No work after 8pm Monday-Wednesday` | When user sets a boundary |

**Rules:**
- Always include the target date in the key (format: `commitment_YYYY-MM-DD_short_desc`)
- At the start of each session, check if any commitment dates have passed
- During Wrap Up, review all commitments from the week: completed or not?
- After review: delete fulfilled commitments, carry over or delete unfulfilled ones
- If the same commitment is missed 2+ times → create a smart suggestion about the underlying pattern
- Don't create too many — max 3-5 active commitments at a time

### `smart_suggestions` — AI-observed patterns with proposals
Managed via `wayve suggestions` commands (not directly via knowledge base). Stores JSON values with pattern, proposal, status, source_data.

| Key | Example Value | When to Save |
|-----|---------------|--------------|
| _(auto-generated from pattern)_ | `{"pattern": "Health pillar at 0% for 3 weeks", "proposal": "Schedule a 15-min walk Mon/Wed/Fri", "status": "pending", "created_from": "wrap_up"}` | During wrap-up, fresh-start, life scan, or weekly scan |

See `references/smart-suggestions.md` for full details on when and how to create suggestions.

### `coaching_themes` — Recurring topics in conversations
Save when the same theme comes up across multiple sessions.

| Key | Example Value | When to Save |
|-----|---------------|--------------|
| `perfectionism` | `Tends to over-plan and feel bad about 80% completion. Remind: 80% is great.` | After noticing in 2+ Wrap Ups |
| `work_life_boundary` | `Struggles to stop working at 6 PM. Has acknowledged this 3 times.` | After recurring discussion |
| `social_anxiety` | `Avoids scheduling social activities but feels happier when they happen` | From happiness insights + observations |
| `motivation_style` | `Responds well to data (producer score). Doesn't like emotional nudges.` | After observing reactions |
| `growth_mindset` | `Loves learning new skills — gets excited about Growth pillar ideas` | After noticing pattern |

### `preferences` — How they interact with Wayve
Save when user expresses preferences about the tool/AI interaction.

| Key | Example Value | When to Save |
|-----|---------------|--------------|
| `communication_style` | `Prefers brief messages, no emojis` | When stated or observed |
| `planning_depth` | `Likes high-level weekly overview, not hourly scheduling` | When they push back |
| `reflection_depth` | `Enjoys deep Wrap Up conversations, takes 15+ minutes` | After observing |
| `default_reminder_minutes` | `15` | During automation setup |
| `notification_channel` | `telegram` | During automation setup |
| `active_automations` | `morning_brief, wrap_up_reminder, fresh_start` | After setting up crons |

---

## When to Save — Specific Triggers

Don't just "save when meaningful." Save at these **specific moments**:

### During Onboarding
- [ ] User's timezone → `personal_context`
- [ ] Work schedule → `personal_context`
- [ ] Family/life situation if shared → `personal_context`
- [ ] Preferred name → `personal_context`
- [ ] Scheduling preferences stated → `scheduling_preferences`
- [ ] Automation preferences → `preferences`

### After Every Wrap Up
- [ ] Focus pillar chosen → `pillar_balance` (update `focus_pillar_history`)
- [ ] What worked / what to change → `weekly_patterns` (look for recurring themes)
- [ ] Mood/energy/fulfillment ratings → `energy_patterns` (track trends)
- [ ] If a pillar was at 0% → `pillar_balance` (update `consistently_neglected` if 3+ weeks)
- [ ] If completion rate improved/declined → `weekly_patterns` (update `completion_trend`)
- [ ] Any recurring blocker mentioned → `weekly_patterns` (update `common_blockers`)
- [ ] Any coaching insight → `coaching_themes`

### After Every Fresh Start
- [ ] Focus mode chosen → `scheduling_preferences` (update `focus_mode_preference` after 3+)
- [ ] Carryover patterns → `weekly_patterns` (which pillars always carry over?)
- [ ] Overcommitment detected → `weekly_patterns` (update `overcommit_tendency`)
- [ ] Scheduling corrections → `scheduling_preferences` (user moved activities = preference)

### After Time Audit
- [ ] Peak/low energy times → `energy_patterns`
- [ ] Energizing vs. draining activities → `energy_patterns`
- [ ] Delegation candidates → `delegation_candidates`
- [ ] Time allocation vs. intention mismatch → `pillar_balance`

### After Life Scan
- [ ] Major patterns discovered → `coaching_themes`
- [ ] Happiness correlations → `pillar_balance` (what makes them happy)
- [ ] Long-term trends → `weekly_patterns`
- [ ] Action items decided → `delegation_candidates` or `coaching_themes`

### During Any Conversation
- [ ] User corrects your scheduling → `scheduling_preferences`
- [ ] User shares personal info → `personal_context`
- [ ] User expresses frustration about a pattern → `coaching_themes`
- [ ] User states a preference about Wayve/AI → `preferences`
- [ ] Same blocker mentioned 2nd+ time → `weekly_patterns` (upgrade to insight)

---

## How to Save — Practical Patterns

### Single insight
```bash
wayve knowledge save --category "energy_patterns" --key "peak_energy_time" --value "7-10 AM — best for deep work and exercise. Confirmed across 3 weeks of morning activity completions." --confidence 0.9 --json
```

### Updating an existing insight
First check if it exists, then update:
```bash
wayve knowledge list --category energy_patterns --json
# → find the entry with key "peak_energy_time"
# → if found: wayve knowledge update ID --value "..." --json
# → if not found: wayve knowledge save --category "energy_patterns" --key "peak_energy_time" --value "..." --json
```

### Confidence levels
- `0.5-0.6` — Observed once, might be coincidence
- `0.7-0.8` — Observed 2-3 times, likely a real pattern (default)
- `0.9-1.0` — Confirmed across many weeks or explicitly stated by user

### When to update vs. create new
- **Update** when new data refines an existing insight (e.g., adding a 4th week of data to a trend)
- **Create new** when it's a genuinely different insight in the same category
- **Delete** — When you believe an insight is outdated or wrong, ask the user: 'This insight seems outdated — want me to update or remove it?' Only delete without asking when the user explicitly requests it ('forget that', 'delete that').

---

## How to Use Stored Knowledge — Practical Examples

### Morning Brief
```
Knowledge: peak_energy_time = "7-10 AM", energizing_activities = "Running, guitar"
→ "Your morning run is at 7 — that's your peak energy time. Great scheduling."
```

### Fresh Start (scheduling)
```
Knowledge: low_energy_days = "Wednesdays", batch_preference = true
→ Schedule lighter activities on Wednesday
→ Group similar pillar activities on the same day
```

### Wrap Up (reflection)
```
Knowledge: consistently_neglected = "Relationships", what_always_works = "Morning Health"
→ "Your Health morning routine is rock solid — 4 weeks running. Relationships is still getting squeezed though. Want to make that your focus next week?"
```

### Activity creation
```
Knowledge: evening_boundary = "Nothing after 9 PM", commute = "30 min bike ride"
→ Don't suggest activities after 9 PM
→ Account for commute time in scheduling
```

### Coaching moments
```
Knowledge: perfectionism = "Feels bad about 80% completion"
→ When they complete 80%: "80% is a strong week. You showed up for what matters."
→ Don't say: "You missed 20% of your activities."
```

### Recurring theme detection
```
If user mentions work-life boundary for the 3rd time:
→ Save/update coaching_themes with increased confidence
→ Next session: "I've noticed work boundaries keep coming up. Want to set a hard time lock at 6 PM? Sometimes structure helps more than willpower."
```

---

## Knowledge Hygiene

### Review periodically
During Life Scans or monthly check-ins:
1. Run `wayve knowledge list --json` to see all entries
2. Check if any insights are outdated (user changed jobs, moved, etc.)
3. Update or delete stale entries
4. Look for gaps — are there categories with no entries?

### Don't over-save
- Don't save every single observation — only patterns confirmed 2+ times
- Don't save session-specific details ("today they were tired") — save patterns ("tends to have low energy on Wednesdays")
- Don't duplicate what's already in the week review data — knowledge is for cross-week patterns

### Privacy & transparency
- If the user asks "what do you know about me?" → run `wayve knowledge summary --json` and share openly
- If the user says "forget that" or "don't track that" → delete the relevant entries immediately
- Never save sensitive medical, financial, or relationship details beyond what's needed for planning
- Frame it as: "I save planning patterns to give you better advice over time. You can see and delete anything anytime at https://gowayve.com/knowledge-base"

---

## Making It Automatic — The Learning Loop

The key to making this feel natural (not forced) is embedding knowledge saves into the existing conversation flow. Save insights at natural points in the conversation. For significant data (personal info, financial data, coaching observations), briefly mention it. For routine pattern saves, a simple note is fine.

### End-of-conversation checklist
Before ending any meaningful planning session, run through:

1. **Did I learn something new about the user?** → Save to `personal_context`
2. **Did I notice a pattern across weeks?** → Save to appropriate category
3. **Did the user correct my assumptions?** → Update existing insight or save new preference
4. **Did the user express a recurring frustration?** → Save to `coaching_themes`
5. **Did the user explicitly ask me to remember something?** → Save immediately with high confidence

### Retrieval checklist
At the start of any planning session:

1. **Always** run `wayve knowledge summary --json` — takes 1 second, gives you the full picture
2. **If relevant categories exist**, pull specific entries for the current phase
3. **Reference at least 1 stored insight** in your first substantive response — this shows the user you remember them
4. **If no knowledge exists yet**, that's fine — you're building it. Note what you learn during this session.

This creates a virtuous cycle: the more the user interacts, the smarter the advice gets, which makes them interact more.
