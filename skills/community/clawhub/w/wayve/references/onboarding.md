# Phase 1: Onboarding — First-Time Setup

**Command:** `/wayve setup`

## When This Applies
No pillars found in `wayve context --json`, or user says "set up", "I'm new to Wayve", "getting started."

## Your Approach
Exploratory and pressure-free. "We can always adjust later." Don't overwhelm — if the user seems done, let them stop and come back later. This is about intention, not perfection.

## Setup Flow

### Step 1: Life Pillars
Help the user create 4-6 life pillars — areas of life that matter to them.

**Suggested defaults:**
| Pillar | Color | Example Intention |
|--------|-------|-------------------|
| Health | #10B981 (green) | "Move my body and fuel it well" |
| Relationships | #EC4899 (magenta) | "Nurture the people who matter" |
| Growth | #8B5CF6 (purple) | "Keep learning and evolving" |
| Finance | #F59E0B (gold) | "Build security and abundance" |
| Adventure | #06B6D4 (cyan) | "Experience new things and have fun" |

Ask what resonates — let them rename, add, or remove. For each pillar:
1. **Name** and **color** (hex)
2. **Intention** — one sentence about why this area matters
3. **Target hours per week** — how much time they'd ideally spend (e.g., Health: 5h)
4. **Preferred time slot** — morning, afternoon, evening, or flexible

Run `wayve pillars create "Name" --color "#HEX" --json` for each.

### Step 2: Understand Your Business

Before setting targets, understand the user's world. This context is critical for relevant automation suggestions later.

Ask these questions naturally (not as a checklist — weave into conversation):

1. **"What do you do?"** — Business type, role, niche (e.g., "I run a design agency")
2. **"Who do you serve?"** — Clients, audience, customers (e.g., "6 active clients, mostly SaaS startups")
3. **"What tools do you use daily?"** — Tech stack (e.g., "Figma, Slack, Notion, Gmail")
4. **"What takes the most time in your work?"** — Pain points (e.g., "Client communication eats half my day")
5. **"What's your goal for the next 3-6 months?"** — Business goals (e.g., "Get to 10 clients", "Launch my online course")
6. **"How many clients can you handle at once?"** — Capacity (e.g., "Max 6 before quality drops")
7. **"What's your rough monthly revenue right now?"** — Current revenue (optional, respect privacy. Only ask if the conversation feels right. If they don't want to share: "No problem — you can always share later if it becomes relevant.")
   If the user shares financial data, explain: 'This is stored securely in your Wayve account. You can view and delete it anytime at gowayve.com/knowledge-base.'

Save each answer to knowledge base immediately:
```bash
wayve knowledge save --category "personal_context" --key "business_type" --value "Design agency, solopreneur" --json
wayve knowledge save --category "personal_context" --key "business_clients" --value "6 active clients, mostly SaaS startups" --json
wayve knowledge save --category "personal_context" --key "business_tools" --value "Figma, Slack, Notion, Gmail" --json
wayve knowledge save --category "personal_context" --key "business_pain_points" --value "Client communication takes ~50% of work time" --json
wayve knowledge save --category "personal_context" --key "business_goals" --value "Get to 10 clients by June, launch online course" --json
wayve knowledge save --category "personal_context" --key "business_capacity" --value "Can handle max 6 clients simultaneously" --json
wayve knowledge save --category "personal_context" --key "revenue_monthly" --value "~€5000/month" --json  // only if shared
```

This information becomes essential during Time Audit analysis and automation suggestions. Without it, suggestions will be generic. With it, they become specific: "You use Slack for clients — your agent can auto-draft weekly updates."

If the user doesn't want to share business details, that's fine — move on. You'll learn more over time.

### Step 3: Frequency Targets
For each pillar, suggest a weekly frequency target beyond just hours — e.g.:
- Health: "Exercise 3x/week, cook at home 4x/week"
- Relationships: "Date night 1x/week, call a friend 2x/week"

Run `wayve frequencies create --pillar ID --type weekly --target N --json` for each target:
- `--pillar` — the pillar UUID
- `--type` — "weekly" (most common), "daily", or "monthly"
- `--target` — how many times per period (e.g., 3 for "3x/week")

These become trackable via `wayve frequencies progress --json`.

### Step 4: Time Locks
Ask about recurring commitments that block time every week:
- Work hours (e.g., Mon-Fri 9:00-17:00)
- Commute, gym class, school pickup, etc.

Run `wayve timelocks create "Name" --start-time HH:MM --end-time HH:MM [--days 1,2,3,4,5] [--pillar ID] --json` for each. Key parameters:
- `"Name"` — the time lock name
- `--start-time` (HH:MM), `--end-time` (HH:MM)
- `--days` — comma-separated ints, 0=Sunday through 6=Saturday
- `--pillar` — optional, link to a pillar if relevant (e.g., gym → Health)

### Step 5: First Activities
Help capture 3-5 activities for this week. Ask: "What are the most important things you want to do this week?"

For each activity, match to a pillar and suggest a time. Run `wayve activities create "Title" --pillar ID [flags] --json`:
- `"Title"`, `--pillar`, `--date` (YYYY-MM-DD), `--time` (HH:MM)
- `--duration`, `--priority` (1-5), `--energy` (high/medium/low)

Run `wayve availability --json` to find free slots before scheduling.

For multiple activities, use batch mode: pass an `activities` array (up to 100) instead of individual calls.

### Step 6: Perfect Week Design
Help design their ideal weekly time distribution across pillars. This is aspirational — the template they'll aim for each week.

Run `wayve templates create --name "My Balanced Week" --json`:
- `--name`: e.g., "My Balanced Week"
- `--perfect-week`: true
- `--distribution`: `{ "bucket-uuid": hours, ... }` — hours per pillar
- `--total-hours`: sum of all pillar hours

### Step 7: Calendar Preferences
Set their working hours via `wayve settings update --json`:
- `--calendar-start` (e.g., 7)
- `--calendar-end` (e.g., 22)
- `--max-hours` (e.g., 10)

### Step 8: Set Up Notifications & Weekly Rhythm

**How Wayve works:** At the start of each conversation, Wayve checks your pillar balance, patterns, and progress to give you personalized coaching. All your data is stored in your Wayve account and you can view or delete anything at gowayve.com/knowledge-base.

Wayve sends push notifications at key moments — reminders, check-ins, and briefs. These run automatically on Wayve's servers and get delivered to the chat where your agent lives, so you can reply directly.

**First: Set up the delivery channel**

Ask: "Where does your agent live — Telegram, Discord, or Slack? I'll send all notifications there so you can reply directly in the same chat."

**Ask explicit permission before collecting any credentials.** Explain what you need, why, and how it's stored. Never collect credentials without the user confirming.

Explain to the user: 'To send you notifications, I need your [channel] credentials. These are stored encrypted (AES-256-GCM) in your Wayve account and only used for delivering your notifications. You can revoke access anytime by deleting the automation. Is that OK?'

If the user agrees, set up credentials for the chosen channel:
- **Telegram:** bot_token + chat_id (explain how to get these via @BotFather and the getUpdates API)
- **Discord:** webhook_url (Server Settings > Integrations > Webhooks)
- **Slack:** webhook_url (api.slack.com/apps > Incoming Webhooks)

If the user declines sharing credentials, offer the `pull` channel instead — no credentials needed, notifications show up at session start.

No email — notifications must go to an interactive channel where the user can reply and the agent processes it.

Save the channel preference:
```bash
wayve knowledge save --category "preferences" --key "notification_channel" --value "telegram" --json
```

**Then: Set up notifications one by one**

Present these 3 as recommended, with flexible timing:

**1. Wrap Up Reminder** (weekly reflection)
Ask: "When do you want to do your weekly reflection? Most people do Sunday evening, but pick whatever works for you — Friday, Saturday, whatever fits."
- Default: Sunday 19:00
- Create: `wayve automations create wrap_up_reminder --cron "0 19 * * 0" --timezone USER_TZ --channel USER_CHANNEL --delivery-config 'USER_DELIVERY_CONFIG' --json`

**2. Fresh Start Reminder** (weekly planning)
Ask: "And when do you want to plan your week? The day after your reflection works well — but you choose."
- Default: Monday 8:30
- Create: `wayve automations create fresh_start_reminder --cron "30 8 * * 1" --timezone USER_TZ --channel USER_CHANNEL --delivery-config 'USER_DELIVERY_CONFIG' --json`

**3. Morning Brief** (daily overview)
Ask: "Want a quick daily overview of your schedule each morning? What time?"
- Default: 7:30 daily
- Create: `wayve automations create morning_brief --cron "30 7 * * *" --timezone USER_TZ --channel USER_CHANNEL --delivery-config 'USER_DELIVERY_CONFIG' --json`

**Optional (mention but don't push):**
"You can add more later — evening summaries, mid-week check-ins, frequency alerts. Just ask anytime."

Explain the weekly rhythm:
- **Wrap Up** (your chosen day): Reflect on the week, celebrate wins, choose focus for next week
- **Fresh Start** (your chosen day): Handle carryovers, capture new activities, plan the week
- **Daily Brief** (every morning): Quick overview of today's schedule and priorities

"You don't have to do these every week to get value from Wayve — but when you do, they make a real difference."

## App Links
When guiding the user, include links to the relevant pages on `gowayve.com`:
- Pillars setup: https://gowayve.com/buckets
- Time locks: https://gowayve.com/time-locks
- Weekly planning: https://gowayve.com/week
- Calendar view: https://gowayve.com/calendar
- Perfect Week designer: https://gowayve.com/perfect-week
- Account settings: https://gowayve.com/account

### Step 9: Save Initial Knowledge (Mandatory)
During onboarding, save everything you learn about the user:

- [ ] Timezone → `personal_context` / `timezone`
- [ ] Preferred name → `personal_context` / `preferred_name`
- [ ] Work schedule → `personal_context` / `work_schedule`
- [ ] Family/life situation (if shared) → `personal_context` / `family_situation`
- [ ] Calendar preferences → `scheduling_preferences` / `morning_routine`, `evening_boundary`
- [ ] Communication style → `preferences` / `communication_style`
- [ ] Any stated scheduling preferences → `scheduling_preferences`
- [ ] Notification channel → `preferences` / `notification_channel`
- [ ] Wrap Up day/time → `scheduling_preferences` / `wrap_up_schedule`
- [ ] Fresh Start day/time → `scheduling_preferences` / `fresh_start_schedule`

This is the foundation for all future personalization. The more you capture now, the smarter every future session will be.

### Step 10: Recommend the Time Audit

End the onboarding by strongly recommending the Time Audit as the next step:

"You're set up! One more thing I'd really recommend: a **Time Audit**. For 7 days, I'll check in every 30 minutes to log what you're doing. At the end, you'll see exactly where your time goes — and I can show you what your agent could take over.

It's the single most valuable thing you can do right now. Want to set it up?"

If yes → transition directly to the Time Audit flow (read `references/time-audit.md`).
If no → "No problem. You can start one anytime with `/wayve time audit`. For now, enjoy your first week with Wayve!"

## End State
User has pillars with intentions, basic time locks, a few activities scheduled, notifications set up on their preferred schedule, and understands the weekly rhythm. Time Audit has been recommended (and ideally started).

Close by pointing them to their new dashboard: "You're all set! Check out your dashboard anytime at https://gowayve.com/dashboard"
