# Wayve CLI Command Reference

Complete reference for all Wayve CLI commands. Consult this when you need exact flags, argument types, or subcommand options.

## Table of Contents
- [Authentication](#authentication)
- [Planning & Context](#planning--context)
- [Coaching Context](#coaching-context)
- [Activities](#activities)
- [Pillars](#pillars)
- [Projects](#projects)
- [Time Locks](#time-locks)
- [Week Reviews](#week-reviews)
- [Analytics](#analytics)
- [Knowledge Base](#knowledge-base)
- [Time Audits](#time-audits)
- [Checklist Items](#checklist-items)
- [Recurrence](#recurrence)
- [Focus Templates](#focus-templates)
- [User Settings](#user-settings)
- [Happiness Insights](#happiness-insights)
- [Pillar Frequencies](#pillar-frequencies)
- [Smart Suggestions](#smart-suggestions)
- [Automations](#automations)

---

## Authentication

### `wayve auth login`
Start a magic link login flow.

```bash
wayve auth login --email USER@EMAIL
```

### `wayve auth status`
Check current authentication status.

```bash
wayve auth status [--json]
```

### `wayve auth logout`
Log out of the current session.

```bash
wayve auth logout
```

---

## Planning & Context

### `wayve context`
Get everything needed to plan a user's week in one call. **Call this first** when helping plan.

```bash
wayve context [--week N] [--year Y] [--json]
```

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--week` | int 1-53 | No | Week number (default: current) |
| `--year` | int | No | Year (default: current) |
| `--json` | flag | No | Output as JSON instead of markdown |

Returns: pillars, activities (scheduled/unscheduled/incomplete), time_locks, user_preferences, last_week_review, frequency_progress, perfect_week template, knowledge_summary.

### `wayve availability`
Find free time slots for scheduling.

```bash
wayve availability [--week N] [--year Y] [--slot-min N] [--json]
```

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--week` | int 1-53 | No | Week number (default: current) |
| `--year` | int | No | Year (default: current) |
| `--slot-min` | int 15-240 | No | Minimum slot size in minutes (default: 30) |
| `--json` | flag | No | Output as JSON instead of markdown |

Returns: total_available_hours, total_scheduled_hours, by_day (with slots array showing start/end/duration).

**Energy hints:** If the user has stored energy patterns in their knowledge base (e.g., `energy_patterns` / `peak_energy_time: "7-10 AM"`), each slot includes an `energy_hint` field:
- `"peak"` — user's known high-energy window, ideal for demanding/creative work
- `"moderate"` — no specific pattern known for this time
- `"low"` — user's known low-energy window, ideal for routine/admin work
- `null` — no energy data stored yet

Use energy hints to schedule high-energy activities in peak slots and routine work in low-energy slots.

### `wayve brief`
Concise daily overview with today's schedule and priorities.

```bash
wayve brief [--date YYYY-MM-DD] [--json]
```

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--date` | YYYY-MM-DD | No | Date (default: today) |
| `--json` | flag | No | Output as JSON instead of markdown |

Returns: scheduled activities (sorted by time), completed_count, top 5 unscheduled, today's time_locks.

---

## Coaching Context

### `wayve coaching`

Get a unified coaching context for proactive, personalized guidance — all in one call.

**When to use:** At session start for proactive coaching, before any flow, or when you need a quick health check on the user's journey.
**When NOT to use:** For detailed week planning data → `wayve context`. For specific analytics (producer score, patterns) → `wayve score` / `wayve patterns`. For today's schedule → `wayve brief`.

```bash
wayve coaching [--week N] [--year Y] [--json]
```

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--week` | int 1-53 | No | Week number (default: current) |
| `--year` | int | No | Year (default: current) |
| `--json` | flag | No | Output as JSON instead of markdown |

**Returns:**
- `journey` — stage (new/onboarded/active_rituals/power_user), weeks active, last wrap-up/fresh-start dates, time audit status, ritual consistency
- `pillar_health` — per pillar: completed/total activities, completion %, frequency on track, target hours
- `red_flags` — auto-generated warnings (e.g., "Health has 0 activities this week", "Producer score declining", "No Wrap Up in 3 weeks")
- `producer_score` — current % and trend (up/stable/down/unknown)
- `automation_coverage` — agent routines count, push notifications count (total and enabled)
- `coaching_themes` — stored coaching observations from knowledge base
- `active_commitments` — current commitments from knowledge base
- `knowledge_highlights` — key insights from energy_patterns, delegation_candidates, pillar_balance, weekly_patterns
- `pending_suggestions_count` — number of pending smart suggestions

---

## Activities

### `wayve activities create`
Create a single activity.

**When NOT to use:** For recurring blocks → use `wayve timelocks create`. For updating existing → use `wayve activities update`.

**NOTE:** No batch mode in CLI. For multiple activities, run multiple `wayve activities create` commands.

```bash
wayve activities create "Title" --pillar ID \
  [--date YYYY-MM-DD] [--time HH:MM] [--duration N] \
  [--priority N] [--energy high|medium|low] \
  [--flexibility fixed|flexible] \
  [--location home|office|gym|outdoors|anywhere] \
  [--project ID] [--description "..."] [--json]
```

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| (positional) | string (max 500) | Yes | Activity title |
| `--pillar` | UUID | Yes | Pillar to assign to |
| `--description` | string (max 5000) | No | Details |
| `--date` | YYYY-MM-DD | No | When |
| `--time` | HH:MM | No | What time |
| `--duration` | int 1-480 | No | How long in minutes |
| `--project` | UUID | No | Link to project |
| `--priority` | int 1-5 | No | 1=lowest, 5=highest |
| `--energy` | high/medium/low | No | Energy cost |
| `--flexibility` | fixed/flexible | No | Can it move? |
| `--location` | home/office/gym/outdoors/anywhere | No | Where |
| `--json` | flag | No | Output as JSON |

### `wayve activities update`
Update an existing activity.

```bash
wayve activities update ID [--title "..."] [--completed true|false] \
  [--date YYYY-MM-DD] [--time HH:MM] [--pillar ID] \
  [--duration N] [--priority N] [--energy high|medium|low] \
  [--project ID] [--json]
```

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| (positional) | UUID | Yes | Activity ID |
| `--title` | string (max 500) | No | New title |
| `--completed` | true/false | No | Mark done |
| `--date` | YYYY-MM-DD | No | Reschedule or unschedule |
| `--time` | HH:MM | No | Change time |
| `--pillar` | UUID | No | Move to different pillar |
| `--duration` | int 1-480 | No | Change duration |
| `--priority` | int 1-5 | No | Change priority |
| `--energy` | high/medium/low | No | Change energy |
| `--project` | UUID | No | Link/unlink project |
| `--json` | flag | No | Output as JSON |

### `wayve activities delete`
Permanently delete an activity.

```bash
wayve activities delete ID --yes
```

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| (positional) | UUID | Yes | Activity ID |
| `--yes` | flag | Yes | Confirm deletion |

### `wayve activities search`
Search activities by text, pillar, date range, or completion status.

```bash
wayve activities search "query" [--pillar ID] \
  [--start-date YYYY-MM-DD] [--end-date YYYY-MM-DD] \
  [--completed] [--limit N] [--json]
```

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| (positional) | string (max 200) | No | Text search in titles |
| `--pillar` | UUID | No | Filter by pillar |
| `--start-date` | YYYY-MM-DD | No | Start of range |
| `--end-date` | YYYY-MM-DD | No | End of range |
| `--completed` | flag | No | Filter to completed only |
| `--limit` | int 1-100 | No | Results (default: 20) |
| `--json` | flag | No | Output as JSON |

### `wayve activities list`
List activities for a given week or with filters.

```bash
wayve activities list [--week N] [--pillar ID] [--completed] [--limit N] [--json]
```

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--week` | int 1-53 | No | Week number (default: current) |
| `--pillar` | UUID | No | Filter by pillar |
| `--completed` | flag | No | Filter to completed only |
| `--limit` | int 1-100 | No | Results (default: 20) |
| `--json` | flag | No | Output as JSON |

---

## Pillars

### `wayve pillars create`
Create a new life pillar.

```bash
wayve pillars create "Name" --color "#HEX" \
  [--intention "..."] [--target-hours N] \
  [--preferred-time morning|afternoon|evening|flexible] [--json]
```

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| (positional) | string (max 100) | Yes | Pillar name |
| `--color` | hex string | Yes | e.g., "#10B981" |
| `--intention` | string (max 500) | No | Why this area matters |
| `--target-hours` | number 0-168 | No | Weekly target |
| `--preferred-time` | morning/afternoon/evening/flexible | No | When |
| `--json` | flag | No | Output as JSON |

### `wayve pillars update`
Update an existing pillar.

```bash
wayve pillars update ID [--name "..."] [--color "#HEX"] \
  [--intention "..."] [--target-hours N] [--focus true|false] [--json]
```

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| (positional) | UUID | Yes | Pillar ID |
| `--name` | string (max 100) | No | New name |
| `--color` | hex string | No | New color |
| `--intention` | string (max 500) | No | New intention |
| `--target-hours` | number 0-168 | No | New weekly target |
| `--focus` | true/false | No | Set as focus pillar |
| `--json` | flag | No | Output as JSON |

### `wayve pillars reorder`
Set pillar display order.

```bash
wayve pillars reorder --ids "id1,id2,..." [--json]
```

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--ids` | comma-separated UUIDs | Yes | New order |
| `--json` | flag | No | Output as JSON |

### `wayve pillars archive` / `wayve pillars restore`
Archive or restore a pillar.

```bash
wayve pillars archive ID
wayve pillars restore ID
```

### `wayve pillars list`
List all pillars.

```bash
wayve pillars list [--json]
```

---

## Projects

### `wayve projects create`
Create a new project.

```bash
wayve projects create "Name" [--pillar ID] [--color "#HEX"] \
  [--description "..."] [--goal-type target|habit] \
  [--target-value N] [--target-unit "..."] [--json]
```

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| (positional) | string 1-200 | Yes | Project name |
| `--pillar` | UUID | No | Link to pillar |
| `--color` | hex string | No | Color |
| `--description` | string (max 1000) | No | Details |
| `--goal-type` | target/habit | No | Type (default: "target") |
| `--target-value` | positive number | No | e.g., 100 pages |
| `--target-unit` | string (max 50) | No | e.g., "hours", "pages" |
| `--json` | flag | No | Output as JSON |

### `wayve projects update`
Update an existing project.

```bash
wayve projects update ID [--name "..."] [--current-value N] \
  [--status active|completed|archived] [--json]
```

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| (positional) | UUID | Yes | Project ID |
| `--name` | string 1-200 | No | New name |
| `--current-value` | number >= 0 | No | Progress |
| `--status` | active/completed/archived | No | "archived" = soft delete |
| `--json` | flag | No | Output as JSON |

### `wayve projects delete`
Permanently delete a project.

```bash
wayve projects delete ID --yes
```

### `wayve projects list`
List projects by status.

```bash
wayve projects list [--status active|completed|archived] [--json]
```

---

## Time Locks

### `wayve timelocks create`
Create a recurring time block.

```bash
wayve timelocks create "Name" --start-time HH:MM --end-time HH:MM \
  [--days 1,2,3,4,5] [--pillar ID] [--color "#HEX"] \
  [--recurrence weekly|daily|biweekly|monthly] [--json]
```

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| (positional) | string 1-200 | Yes | Name |
| `--start-time` | HH:MM | Yes | Start |
| `--end-time` | HH:MM | Yes | End |
| `--days` | comma-separated ints (0-6) | No | 0=Sunday |
| `--pillar` | UUID | No | Link to pillar |
| `--color` | hex string | No | Color |
| `--recurrence` | daily/weekly/biweekly/monthly | No | Default: weekly |
| `--json` | flag | No | Output as JSON |

### `wayve timelocks update`
Update an existing time lock.

```bash
wayve timelocks update ID [--name "..."] [--start-time HH:MM] [--end-time HH:MM] \
  [--days 1,2,3,4,5] [--pillar ID] [--color "#HEX"] \
  [--recurrence weekly|daily|biweekly|monthly] [--json]
```

### `wayve timelocks delete`
Delete a time lock.

```bash
wayve timelocks delete ID --yes
```

### `wayve timelocks list`
List all time locks.

```bash
wayve timelocks list [--json]
```

---

## Week Reviews

### `wayve review save`
Save or update a week review.

```bash
wayve review save --week N --year Y \
  [--mood N] [--energy N] [--fulfillment N] \
  [--proud-of "..."] [--what-worked "..."] [--what-to-change "..."] \
  [--focus-pillar ID] [--wrap-up-status STATUS] [--fresh-start-status STATUS] \
  [--json]
```

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--week` | int 1-53 | Yes | Week |
| `--year` | int | Yes | Year |
| `--mood` | int 1-5 | No | Overall mood |
| `--energy` | int 1-5 | No | Energy |
| `--fulfillment` | int 1-5 | No | Fulfillment |
| `--proud-of` | string (max 1000) | No | Wins |
| `--what-worked` | string (max 1000) | No | Keep doing |
| `--what-to-change` | string (max 1000) | No | Adjust |
| `--focus-pillar` | UUID | No | Next week's focus pillar |
| `--wrap-up-status` | enum | No | Ritual status |
| `--fresh-start-status` | enum | No | Ritual status |
| `--json` | flag | No | Output as JSON |

### `wayve review save-pillars`
Save per-pillar review data.

```bash
wayve review save-pillars --data 'JSON' [--json]
```

The `--data` flag accepts a JSON object with `week_review_id` and `buckets` array (max 20). Each pillar entry: `{ bucket_id, score (1-5), satisfaction (1-5), note (max 1000), hours_planned, hours_actual, activities_planned, activities_completed }`.

### `wayve review get`
Get a specific week's review.

```bash
wayve review get --week N --year Y [--json]
```

### `wayve review list`
List all week reviews.

```bash
wayve review list [--json]
```

### `wayve review flow-status`
Get current ritual flow status.

```bash
wayve review flow-status [--json]
```

---

## Analytics

**When NOT to use:** For current week's pillar health → use `wayve coaching`. For time audit analysis → use `wayve audit report`.

### `wayve score`
Get producer score: completion rate (0-100), per-pillar breakdown, 12-week trend.

```bash
wayve score [--week N] [--year Y] [--json]
```

### `wayve patterns`
Get task patterns: frequently incomplete activities, energy patterns by time, pillar distribution (4 weeks).

```bash
wayve patterns [--json]
```

### `wayve energy-matrix`
Get energy/skill matrix: activities grouped by energy/value, delegation candidates (8 weeks).

```bash
wayve energy-matrix [--json]
```

---

## Knowledge Base

**When NOT to use:** For smart suggestions → use `wayve suggestions`. For planning context → use `wayve context`.

### `wayve knowledge summary`
Get a summary of all stored knowledge.

```bash
wayve knowledge summary [--json]
```

### `wayve knowledge list`
List knowledge entries, optionally filtered by category.

```bash
wayve knowledge list [--category CAT] [--json]
```

### `wayve knowledge get`
Get a specific knowledge entry.

```bash
wayve knowledge get ID [--json]
```

### `wayve knowledge save`
Create a new knowledge entry (or save an AI insight).

```bash
wayve knowledge save --category CAT --key "KEY" --value "VALUE" \
  [--confidence N] [--source "..."] [--json]
```

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--category` | string (max 100) | Yes | Category |
| `--key` | string (max 200) | Yes | Key name |
| `--value` | string (max 2000) | Yes | Content |
| `--confidence` | float 0-1 | No | Default: 0.8 |
| `--source` | string (max 200) | No | Source of insight |
| `--json` | flag | No | Output as JSON |

### `wayve knowledge update`
Update an existing knowledge entry.

```bash
wayve knowledge update ID [--value "..."] [--confidence N] [--json]
```

### `wayve knowledge delete`
Delete a knowledge entry.

```bash
wayve knowledge delete ID --yes
```

---

## Time Audits

**When NOT to use:** For ongoing time tracking (not an audit) → create regular activities instead.

### `wayve audit start`
Start a new time audit.

```bash
wayve audit start [--name "..."] --start YYYY-MM-DD --end YYYY-MM-DD \
  [--interval N] [--active-start HH:MM] [--active-end HH:MM] [--json]
```

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--name` | string (max 100) | No | Default: "Time Audit" |
| `--start` | YYYY-MM-DD | Yes | Start date |
| `--end` | YYYY-MM-DD | Yes | End date |
| `--interval` | int 15-120 | No | Interval in minutes (default: 30) |
| `--active-start` | HH:MM | No | Active hours start (default: 08:00) |
| `--active-end` | HH:MM | No | Active hours end (default: 20:00) |
| `--json` | flag | No | Output as JSON |

### `wayve audit log`
Log a time audit entry.

```bash
wayve audit log --audit ID --what "description" --energy N \
  [--value N] [--pillar ID] [--note "..."] [--json]
```

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--audit` | UUID | Yes | Audit ID |
| `--what` | string 1-500 | Yes | What you did |
| `--energy` | int 1-5 | Yes | 1=draining, 5=energizing |
| `--value` | int 1-5 | No | 1=very low value, 5=very high value |
| `--pillar` | UUID | No | Link to pillar |
| `--note` | string (max 500) | No | Additional note |
| `--json` | flag | No | Output as JSON |

### `wayve audit report`
Generate a time audit report.

```bash
wayve audit report --audit ID [--json]
```

Returns: pillar_summary (with avg_energy + avg_value) + activity_matrix (all entries with energy x value data, grouped into quadrants: Focus, Optimize, Reconsider, Automate).

### `wayve audit delete`
Permanently delete a time audit and all its entries.

```bash
wayve audit delete ID --yes
```

---

## Checklist Items

### `wayve checklist list`
List checklist items for an activity.

```bash
wayve checklist list --activity ID [--json]
```

### `wayve checklist create`
Add a checklist item to an activity.

```bash
wayve checklist create --activity ID --title "..." [--json]
```

### `wayve checklist update`
Update a checklist item.

```bash
wayve checklist update --activity ID --item ITEM_ID \
  [--completed true|false] [--title "..."] [--json]
```

### `wayve checklist delete`
Delete a checklist item.

```bash
wayve checklist delete --activity ID --item ITEM_ID --yes
```

---

## Recurrence

### `wayve recurrence get`
Get recurrence rule for an activity.

```bash
wayve recurrence get --activity ID [--json]
```

### `wayve recurrence set`
Set or update a recurrence rule on an activity.

```bash
wayve recurrence set --activity ID --frequency daily|weekly|biweekly|monthly \
  [--days 1,3,5] [--interval N] [--end-date YYYY-MM-DD] [--json]
```

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--activity` | UUID | Yes | Activity ID |
| `--frequency` | daily/weekly/biweekly/monthly | Yes | How often |
| `--days` | comma-separated ints (0-6) | No | For weekly/biweekly |
| `--interval` | int 1-12 | No | Default: 1 |
| `--end-date` | YYYY-MM-DD | No | When to stop |
| `--json` | flag | No | Output as JSON |

### `wayve recurrence delete`
Remove recurrence from an activity.

```bash
wayve recurrence delete --activity ID --yes
```

---

## Focus Templates

### `wayve templates list`
List all focus templates, or only the active one.

```bash
wayve templates list [--active] [--json]
```

### `wayve templates create`
Create a new focus template.

```bash
wayve templates create --name "..." \
  [--distribution 'JSON'] [--total-hours N] [--perfect-week] [--json]
```

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--name` | string (max 100) | Yes | Template name |
| `--distribution` | JSON string | No | `{ "bucket_id": hours }` per pillar |
| `--total-hours` | float 0-168 | No | Total weekly hours |
| `--perfect-week` | flag | No | Mark as Perfect Week template |
| `--json` | flag | No | Output as JSON |

### `wayve templates update`
Update a focus template.

```bash
wayve templates update ID [--name "..."] [--distribution 'JSON'] \
  [--total-hours N] [--json]
```

### `wayve templates activate`
Activate a focus template.

```bash
wayve templates activate ID [--json]
```

### `wayve templates delete`
Delete a focus template.

```bash
wayve templates delete ID --yes
```

---

## User Settings

### `wayve settings get`
Get user preferences.

```bash
wayve settings get [--json]
```

### `wayve settings update`
Update user preferences.

```bash
wayve settings update [--calendar-start N] [--calendar-end N] \
  [--max-hours N] [--sleep-hours N] [--json]
```

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--calendar-start` | int 0-23 | No | Day starts at |
| `--calendar-end` | int 1-24 | No | Day ends at |
| `--max-hours` | int 1-24 | No | Max schedulable hours per day |
| `--sleep-hours` | float 0-24 | No | Sleep hours per day |
| `--json` | flag | No | Output as JSON |

### `wayve profile get`
Get user profile. Alias: `wayve settings profile`.

```bash
wayve profile get [--json]
```

### `wayve profile update`
Update user profile.

```bash
wayve profile update --name "..." [--json]
```

---

## Happiness Insights

### `wayve happiness`

Analyze mood correlations: what activities, pillars, and patterns correlate with higher or lower mood ratings across weeks.

**When to use:** During Life Scans, or when the user wants to understand what makes them happiest.
**When NOT to use:** For current week mood → check last week's review via `wayve context`. For pillar health → use `wayve coaching`.

```bash
wayve happiness [--recalculate] [--json]
```

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--recalculate` | flag | No | Force fresh calculation. Default: uses cached correlations. |
| `--json` | flag | No | Output as JSON |

**Returns:** Array of correlations showing which activities/pillars/patterns correlate with higher or lower mood ratings. Use this to connect "you're happiest when you invest in Relationships" or "mood dips when Health is neglected."

---

## Pillar Frequencies

### `wayve frequencies list`
List all frequency targets.

```bash
wayve frequencies list [--json]
```

### `wayve frequencies create`
Create a frequency target for a pillar.

```bash
wayve frequencies create --pillar ID --type weekly|daily|monthly --target N [--json]
```

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--pillar` | UUID | Yes | Pillar to set target for |
| `--type` | weekly/daily/monthly | Yes | Tracking period |
| `--target` | int 1-100 | Yes | Activities per period |
| `--json` | flag | No | Output as JSON |

Examples: "exercise 3x/week" → `--pillar <Health ID> --type weekly --target 3`

### `wayve frequencies update`
Update a frequency target.

```bash
wayve frequencies update ID [--target N] [--json]
```

### `wayve frequencies delete`
Delete a frequency target.

```bash
wayve frequencies delete ID --yes
```

### `wayve frequencies progress`
Get per-pillar frequency targets vs. actual completion for the week.

```bash
wayve frequencies progress [--week N] [--year Y] [--json]
```

---

## Smart Suggestions

Track observational suggestions — patterns paired with proposals.

### `wayve suggestions list`
List suggestions, optionally filtered by status.

```bash
wayve suggestions list [--status pending|accepted|dismissed|snoozed] [--json]
```

### `wayve suggestions create`
Create a new suggestion.

```bash
wayve suggestions create --pattern "..." --proposal "..." [--source "..."] [--json]
```

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--pattern` | string (max 1000) | Yes | What was observed |
| `--proposal` | string (max 1000) | Yes | What is proposed |
| `--source` | string (max 100) | No | Context: "wrap_up", "fresh_start", "life_scan", "analytics" |
| `--json` | flag | No | Output as JSON |

**Status flow:** pending → accepted / dismissed / snoozed. After `accepted`, Wayve is done.

### `wayve suggestions accept`
Accept a suggestion.

```bash
wayve suggestions accept ID
```

### `wayve suggestions dismiss`
Dismiss a suggestion.

```bash
wayve suggestions dismiss ID
```

### `wayve suggestions snooze`
Snooze a suggestion until a given date.

```bash
wayve suggestions snooze ID --until YYYY-MM-DD
```

### `wayve suggestions delete`
Delete a suggestion.

```bash
wayve suggestions delete ID --yes
```

---

## Automations

Manage AI agent routines and server-side push notifications. Agent routines are playbooks stored in Wayve (not executed server-side). Push notifications are scheduled messages delivered via Telegram, Discord, Slack, email, or pull model.

**When to use:** Setting up morning briefs, wrap-up reminders, agent routines, or any scheduled automation.
**When NOT to use:** For one-off reminders → create an activity instead. For knowledge persistence → use `wayve knowledge save`.

### `wayve automations list`
List automations, optionally filtered by type.

```bash
wayve automations list [--type agent_routine|push] [--json]
```

### `wayve automations create`
Create a new automation.

```bash
wayve automations create TYPE --cron "EXPR" --timezone TZ --channel CH \
  [--name "..."] [--config 'JSON'] [--delivery-config 'JSON'] [--json]
```

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| (positional) | string | Yes | Automation type (see types below) |
| `--cron` | string | Yes | 5-field cron: `minute hour day month weekday` (e.g., `30 7 * * *` = 7:30 AM daily) |
| `--timezone` | string | Yes | IANA timezone (e.g., `Europe/Amsterdam`) |
| `--channel` | string | Yes | `telegram` / `discord` / `slack` / `email` / `pull`. Defaults to `pull` for agent routines. |
| `--name` | string | No | Display name |
| `--config` | JSON string | No | Type-specific config (see below) |
| `--delivery-config` | JSON string | No | Channel credentials (encrypted at rest). Telegram: `{"bot_token":"...","chat_id":"..."}`. Discord/Slack: `{"webhook_url":"..."}`. Email: `{"email":"..."}`. Not needed for `pull`. |
| `--json` | flag | No | Output as JSON |

**Automation Types:**

| Type | Category | Default Schedule | Description |
|------|----------|-----------------|-------------|
| `agent_routine` | Agent | None | AI playbook stored in Wayve. Not server-executed. |
| `morning_brief` | Push | 7:30 daily | Today's activity count and schedule overview |
| `evening_winddown` | Push | 21:00 daily | Day's completion summary |
| `wrap_up_reminder` | Push | Sunday 19:00 | Nudge to do the Wrap Up ritual |
| `fresh_start_reminder` | Push | Monday 8:30 | Nudge to plan the week |
| `mid_week_pulse` | Push | Wednesday 12:30 | Mid-week progress check |
| `friday_check` | Push | Friday 15:00 | Uncompleted activities reminder |
| `frequency_tracker` | Push | 20:00 daily | Off-track pillar frequency alerts |
| `monthly_audit` | Push | 1st of month 11:00 | Monthly review reminder |
| `time_audit_checkin` | Push | Per audit config | Time audit check-in prompt |

**Config structure per type:**
- `agent_routine`: `{ description, agent_instructions, skills: string[], pillar_id }`
- `time_audit_checkin`: `{ audit_id }`
- All others: no config needed (templates are built-in)

### `wayve automations update`
Update an existing automation.

```bash
wayve automations update ID [--enabled true|false] [--cron "EXPR"] [--name "..."] [--json]
```

### `wayve automations delete`
Delete an automation.

```bash
wayve automations delete ID --yes
```

### `wayve automations pending`
Get pending (unacknowledged) automation messages.

```bash
wayve automations pending [--json]
```

### `wayve automations ack`
Acknowledge a pending automation message.

```bash
wayve automations ack ID
```

### `wayve automations bundle`
Create a bundle of common automations.

```bash
wayve automations bundle starter|full --timezone TZ --channel CH [--delivery-config 'JSON'] [--json]
```

**Bundles:**
- `starter` (3 automations): morning_brief + wrap_up_reminder + fresh_start_reminder
- `full` (8 automations): starter + evening_winddown + mid_week_pulse + friday_check + frequency_tracker + monthly_audit
