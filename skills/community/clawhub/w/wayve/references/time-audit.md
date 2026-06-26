# Phase 5: Time Audit — Where Does Your Time Go?

**Command:** `/wayve time audit`

## When This Applies
User explicitly says "audit my time", "where does my time go", "time tracking", "track my time."

## Your Approach
Curious and analytical. Frame it as discovery, not judgment. Inspired by the "Buy Back Your Time" framework — the goal is to identify what to delegate, automate, or eliminate so you can spend time on what matters most. Keep all messages short and concise.

## Where Data is Stored

All data is persisted via CLI commands → Wayve API → Azure SQL Database. Nothing is saved unless you run the command.

| What | CLI command | Stored in |
|------|-----------|-----------|
| Audit config (name, dates, interval, active hours) | `wayve audit start ...` | `wayve.time_audits` |
| Log entries (activity, energy, skill, pillar) | `wayve audit log ...` | `wayve.time_audit_entries` |
| Report (pillar summary, patterns, delegation) | `wayve audit report ...` | Generated from entries |
| User preferences (timezone, active hours, config) | `wayve knowledge save ...` | Knowledge base |

**Available actions for `wayve audit`:**
- `start` — creates audit, returns `audit_id` (save this — you need it for every other call)
- `log` — logs one entry (requires `--audit ID`, `--what`, `--energy`)
- `report` — generates report from all entries (requires `--audit ID`)

**There is no `list` or `get` action.** You cannot retrieve existing audits without the `audit_id`. Always save the `audit_id` from the `start` response — both in the automation config and via knowledge base.

## Flow

### Phase A: Introduce the Time Audit

Before asking anything, explain what the user is signing up for. Keep it brief:

> **What is a Time Audit?**
> For 7 days, I'll send you a quick check-in every 30 minutes during your waking hours. You reply with what you did, which life pillar it belongs to, and your energy level (1-5). Takes about 30 seconds per check-in.
>
> At the end of the week, you'll get a report showing where your time actually goes — compared to where you *want* it to go. You'll see energy patterns, discover what drains you, and identify what you could delegate, automate, or eliminate.
>
> **What to expect:**
> - 7 days of short check-ins via notifications
> - A daily summary each evening
> - A full analysis report at the end
>
> Want to get started?

Wait for confirmation before proceeding. If the user wants a shorter audit, that's fine — but always default to 7 days.

### Phase B: Onboarding — Set Up the Audit

Walk through each setting one at a time. Ask permission for each before moving on. Be brief — one question per message.

**Step 1: Sleep schedule**
Ask: "What time do you usually go to sleep and wake up? I'll make sure not to send check-ins during those hours."

Save sleep hours via `wayve settings update --sleep-hours N --json` and use the times for `--active-start` / `--active-end`.

**Step 2: Check-in interval**
Ask: "Every 30 minutes works best for most people. Want to go with 30 min, or would you prefer every 15 or 60 minutes?"

Default: 30 minutes. Only change if the user explicitly asks.

**Step 3: Timezone**
Ask: "What's your timezone? (e.g., Europe/Amsterdam)"

Save via `wayve knowledge save --category "personal_context" --key "timezone" --value "USER_TIMEZONE" --json`.

**Step 4: Delivery channel**
Ask: "Where should I send the check-in notifications — Telegram, Slack, Discord, or somewhere else?"

**Step 5: Start date**
Ask: "Want to start today or tomorrow morning?"

Suggest starting tomorrow if it's already afternoon.

### Phase C: Execute — Create the Audit & Automations NOW

**CRITICAL: This is an execution phase, not a planning phase.** The user has confirmed all settings. You must now run the commands below in order. Do not summarize what you "will" do — do it. Each step = one command + one confirmation to the user.

**Step 1: Create the audit in Wayve**

Run NOW — this creates the audit record in the database (`wayve.time_audits`):
```bash
wayve audit start --name "7-Day Time Audit — Month Year" --start YYYY-MM-DD --end YYYY-MM-DD --interval 30 --active-start "HH:MM" --active-end "HH:MM" --json
```
The response contains an `id` field — this is the `audit_id`. **You need this ID for every subsequent call.** Confirm: "Audit created"

**Step 2: Save settings to knowledge base**

Run these immediately to persist user preferences (no need to ask permission — the user already provided the info):
```bash
wayve knowledge save --category "personal_context" --key "timezone" --value "USER_TIMEZONE" --json
wayve knowledge save --category "personal_context" --key "active_hours" --value "Mon-Thu HH:MM-HH:MM, Fri-Sun HH:MM-HH:MM" --json
wayve knowledge save --category "preferences" --key "time_audit_config" --value "audit_id: AUDIT_ID, interval: 30min, channel: telegram, duration: 7 days, start: YYYY-MM-DD, end: YYYY-MM-DD" --json
```
**Important:** Include the `audit_id` in the config so future sessions can find it. Confirm: "Settings saved"

**Step 3: Create automations via server-side scheduling**

Present each automation clearly before creating:
'I'll set up 2 notifications:
1. Check-in every [interval] during [active hours] via [channel]
2. Daily summary every evening at [time] via [channel]
Create both?'

After the user says yes, create each one immediately using `wayve automations create`. These run server-side — they work on every platform.

**3a. Check-in automation** (recurring, during active hours):
```bash
wayve automations create time_audit_checkin \
  --cron "*/30 8-21 * * *" \
  --timezone "USER_TIMEZONE" \
  --channel "USER_CHANNEL" \
  --config '{"audit_id": "AUDIT_ID"}' \
  --json
```
Build the cron from the user's active hours:
- Active 8:00-22:00, interval 30min → `*/30 8-21 * * *`
- Active 7:00-20:00, interval 60min → `0 7-19 * * *`
- Active 9:00-18:00, interval 30min → `*/30 9-17 * * *`
The hour range in cron is inclusive — use end_hour minus 1.

Confirm: "Check-in automation created — every 30 min during active hours"

**3b. Evening wind-down as daily summary** (recurring, every evening):
```bash
wayve automations create evening_winddown \
  --cron "30 21 * * *" \
  --timezone "USER_TIMEZONE" \
  --channel "USER_CHANNEL" \
  --json
```
Confirm: "Daily summary automation created — every evening at 21:30"

**Step 4: Verify everything is set up**

After creating all automations, verify and present a summary to the user:

1. Run `wayve audit report --audit AUDIT_ID --json` to confirm the audit exists
2. Run `wayve automations list --json` to confirm automations are active
3. Present a complete summary:

> **All set! Here's what's live:**
>
> | What | Status | Schedule |
> |------|--------|----------|
> | Time audit | Active | [start] → [end] |
> | Check-in notifications | Active | Every 30 min, [active hours] |
> | Daily summary | Active | Every day at 21:30 |
>
> **Your first check-in arrives [start date] at [active_hours_start].** Just reply with what you're doing and your energy level — e.g., "deep work, 4" or "gym, 5".

After the audit end date, suggest disabling the check-in: 'Your Time Audit is complete! Want me to turn off the check-in notifications?'
If the user agrees:
```bash
wayve automations update CHECKIN_ID --enabled false --json
```

If any step failed, tell the user which one and retry it. Do not move on until everything is confirmed working.

### Phase D: During the Audit — Log Entries

When the user responds to a check-in, keep it fast — 30 seconds per entry max. **Every response MUST be logged to the database via a CLI command.**

1. **Parse** what they said — e.g., "gym, 4" → what_did_you_do: "gym", energy_level: 4
2. **YOU determine the pillar** — match the activity to the right pillar based on the user's pillar setup (from planning context). "Gym" → Health, "Client call" → Mission, "Date night" → Relationships. Don't ask the user which pillar — you already know their pillars. Only ask if genuinely ambiguous (e.g., "reading" could be Growth or Experiences).
3. **Handle value level** — If the user provides value, use it. If not:
   - Personal activities (gym, cooking, socializing, sleep) → auto-assign value 1-2
   - Work activities without stated value → ask briefly: "Value? (1-5, business value)"
   - If the user seems annoyed by the value question, stop asking and auto-assign based on context
4. **Log immediately** via CLI command:
   ```bash
   wayve audit log --audit "AUDIT_ID" --what "gym" --energy 4 --pillar "matched-pillar-uuid" --value 1 --note "optional note" --json
   ```
5. **Confirm briefly**: "Logged: Gym → Health, energy 4/5, value 1/5 ✓"

**Parsing rules:**
- `"gym, 4"` → gym, energy 4, pillar: Health (auto), value: 1 (personal activity, auto)
- `"client call, 3, 4"` → client call, energy 3, value 4, pillar: Mission (auto)
- `"emails, 2"` → emails, energy 2, pillar: Mission (auto), ask for value
- `"reading, 5"` → reading, energy 5, pillar: ambiguous → ask: "Was that for work or personal growth?"
- `"nothing, just scrolling"` → scrolling, energy 3, pillar: none/Experiences, value: 1 (auto)

**Key rules:**
- Always ask for energy level — it's essential for the analysis
- Value level is important but don't let it slow down logging. Auto-assign for obvious cases.
- Never ask for the pillar unless truly ambiguous. You know the user's pillars.
- Keep confirmations to ONE line. No commentary, no advice during the audit.
- If the CLI command fails, tell the user and retry. Do not silently skip logging.

### Phase E: Analyze Results

After the audit period ends (or when the user says "show me results"):

**Step 1: Gather all data**

Run the following CLI commands in parallel:
```bash
wayve audit report --audit AUDIT_ID --json
wayve automations list --type agent_routine --json
wayve knowledge summary --json
wayve context --json
```
If you don't have the audit_id, retrieve it from knowledge: look for `preferences` / `time_audit_config`.

The report returns:
- `total_entries` — how many check-ins were logged
- `bucket_summary` — per pillar: entry_count, avg_energy, avg_value
- `time_patterns` — per time of day: entry_count, avg_energy
- `activity_matrix` — all entries with energy + value data (unfiltered, for your analysis)

**Step 2: Semantic Clustering**

Group the `activity_matrix` entries by similarity. This is your most important analysis step.

How to cluster:
- Read all `what_did_you_do` entries from the activity_matrix
- Group entries that describe the same type of work (e.g., "answered emails" + "responding to client messages" + "inbox cleanup" = **"Email & Client Communication"**)
- For each cluster, calculate:
  - `total_entries` — how many times this activity appeared
  - `total_hours` — entries × audit interval (e.g., 17 entries × 30min = 8.5 hours)
  - `avg_energy` — average energy level across entries (1-5)
  - `avg_value` — average value level across entries (1-5)
  - `repetitive` — true if 5+ entries (appears almost daily)

Present clusters sorted by total_hours descending. This shows the user where their time actually goes.

**Step 3: Automation Potential Scoring**

For each cluster, calculate an automation potential score:

```
automation_potential = repetitive ? "HIGH" : total_entries >= 3 ? "MEDIUM" : "LOW"

Adjust based on:
- avg_energy ≤ 2 (draining) → increase one level
- avg_value ≤ 2 (low business value) → increase one level
- avg_energy ≥ 4 (energizing) AND avg_value ≥ 4 (high value) → set to LOW (keep doing this yourself)
```

The formula is a guide, not rigid math. Use your judgment based on the full context. Activities that are draining + repetitive + low-value are the highest automation candidates.

**Step 4: Cross-Reference with Automation Registry**

Compare each high/medium-potential cluster against the user's existing automations (from the `wayve automations list` response):
- For each cluster, check: is there an existing agent routine that covers this?
- Note the gap: "This takes 8.5 hours/week and your agent handles 0% of it"
- If an automation exists but the cluster still shows high time investment, the automation may not be working effectively

**Step 5: Cross-Reference with Business Context**

Pull business context from the knowledge base (`personal_context` category):
- What tools does the user use? → Suggest automations using those tools
- What's their business type? → Make suggestions industry-specific
- What pain points did they share during onboarding? → Connect audit findings to stated pain points

Example: If knowledge says "uses Slack for client communication" and the cluster "Client Communication" is 8.5 hours → "Your agent can auto-draft weekly client updates in Slack based on your project notes."

**Step 6: Discuss with the User**

Now present your analysis conversationally. Walk through:

1. **Pillar distribution** — Where is time going vs. where they want it? Compare against Perfect Week template if one exists. Which pillars are starved?

2. **Top 3 time sinks** — The biggest clusters by hours. "You spent [X] hours on [cluster]. That's [Y]% of your tracked time."

3. **Energy patterns** — When do they have the most/least energy? Which activities drain vs. energize?

4. **Energy × Value quadrants** — Plot clusters into 4 quadrants:
   - **Focus** (high energy, high value) — sweet spot, do more of this
   - **Optimize** (low energy, high value) — valuable but draining, streamline or hire
   - **Reconsider** (high energy, low value) — enjoyable but doesn't pay, hobby?
   - **Automate** (low energy, low value) — drains you and doesn't generate returns, automate or eliminate

5. **Automation opportunities** — Present the ranked list from Step 3. For each high-potential cluster, suggest a specific automation.

6. **Business function lens** — When presenting clusters, also note which business function each cluster serves (Create, Attract, Convert, Deliver, Operate). This helps the user see not just WHERE their time goes, but whether it's strategically balanced for THEIR situation. Reference `references/solopreneur-framework.md` for reasoning guidelines. Don't prescribe ratios — ask: "All your work time went to Deliver. Is that what you want, or are there other areas of your business that need attention?"

**Important:** The Time Audit uses an **Energy × Value** matrix (how draining × how valuable to your business). This is different from the Analytics `wayve energy-matrix --json` command, which uses **Energy × Skill** (how draining × how much skill required). Both are useful:
- **Energy × Value** (Time Audit) → What to automate or eliminate (low value + draining = automate)
- **Energy × Skill** (Analytics) → What to delegate to others (low skill + draining = delegate)

### Phase E.5: Automation Discovery Report

After discussing the findings, generate a structured report. Present it to the user AND save it to knowledge.

**Use this exact format:**

```markdown
## Automation Discovery Report — [Date]

### Your Time Map
Total hours tracked: [X]h | Entries logged: [Y] | Days: [Z]

### Top Automation Opportunities (Ranked by Time Savings)

#### #1: [Cluster Name] — [X hours/week]
- **What you're doing:** [description of activities in this cluster]
- **Automation potential:** HIGH
- **Currently automated:** No
- **Suggested automation:** [specific, actionable — e.g., "AI agent drafts weekly client
  updates every Friday at 4pm based on your project notes in Notion"]
- **How to set it up:** [step-by-step prompt/instructions the user can give their agent]
- **Estimated time saved:** [X hours/week]
- **Pillar impact:** Frees time for [underserved pillar]

#### #2: [Cluster Name] — [X hours/week]
[same structure]

#### #3: [Cluster Name] — [X hours/week]
[same structure]

### Energy Insights
- **Peak energy window:** [time] — schedule high-value creative work here
- **Energy drain window:** [time] — schedule routine/admin work here or protect as rest
- **Most energizing activities:** [list]
- **Most draining activities:** [list]

### Pillar Balance
| Pillar | Actual Hours | Target Hours | Status |
|--------|-------------|-------------|--------|
| [name] | [X]h | [Y]h | [Over/Under/On track] |

### Recommended Next Steps
1. [Most impactful automation — set up this week]
2. [Second automation — set up next week]
3. [Pillar rebalancing action — schedule specific activities]
```

**Save the report highlights to knowledge:**
```bash
wayve knowledge save --category "delegation_candidates" --key "automation_discovery_report" --value "[Top 3 opportunities with hours and suggestions]" --json
```

### Phase F: Action Plan — Make It Happen

Don't just analyze — help the user take action NOW.

1. **Pick the #1 automation** from the Discovery Report. Ask: "Want to set this up right now?"
   - If yes → create an agent routine via `wayve automations create agent_routine --cron "EXPR" --timezone TZ --channel CH --config '{"agent_instructions": "..."}' --json`
   - Include the suggested prompt/instructions in the `config.agent_instructions` field
   - Set an appropriate schedule via `--cron`

2. **For the Focus quadrant activities** — help the user do more of these:
   - Use `wayve activities create "Title" --pillar ID --json` to schedule high-value activities for next week
   - Consider setting up recurrence with `wayve recurrence set --activity ID --frequency FREQ --json`

3. **For activities to eliminate** — help the user commit:
   - "You spent [X] hours on [activity] this week. Does it actually need to happen?"
   - If they agree to eliminate, save as knowledge: `wayve knowledge save --category "delegation_candidates" --key "eliminated_[activity]" --value "..." --json`

4. **Fill the gaps** — Reclaimed hours go to underserved pillars:
   - Check which pillars are below their Perfect Week targets
   - Suggest specific activities for those pillars
   - Schedule them using `wayve activities create "Title" --pillar ID --json`

5. **Set a review cadence** — "Want me to check in next month to see if these automations are working? I can set up a monthly audit reminder."
   - If yes → `wayve automations create monthly_audit --cron "EXPR" --timezone TZ --channel CH --json`

### Save Findings
Save key insights via `wayve knowledge save --json`:
- Category: `energy_patterns` — peak/low energy windows, energizing/draining activities
- Category: `pillar_balance` — actual vs. desired time per pillar, biggest gaps
- Category: `delegation_candidates` — top automation opportunities with specifics
- Category: `coaching_themes` — key insights about what generates value vs. what doesn't
- Category: `personal_context` — any new business context learned during the review

## End State
User has a clear Automation Discovery Report, has set up at least one new automation, and has concrete next steps for the others. The report is saved to knowledge for reference in future Fresh Start and Wrap Up sessions.

"Now you know exactly where your time goes — and more importantly, what your agent should take over next. During your next Fresh Start, we'll reference this report to keep the momentum going."

Direct them to the app:
- "View your time audit: https://gowayve.com/time-audit"
- "See your analytics: https://gowayve.com/analytics"
- "Plan your week with these insights: https://gowayve.com/week"
