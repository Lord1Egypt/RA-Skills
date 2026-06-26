# Worth It Auto-Logger

*Free companion skill for [Worth It — Agent Profitability Tracker](https://www.shopclawmart.com/listings/worth-it-agent-profitability-tracker-961a92fb) on ClawMart.*

## What This Does

Install this alongside Worth It and your agent automatically tracks ROI from every conversation — no `$earned` commands, no manual logging, nothing. It silently:

1. **Auto-detect which project is active** at session start
2. **Track session duration** and log time automatically
3. **Read conversations for value signals** and create entries
4. **Log costs** from tool use (API calls, image gen, etc.)
5. **Show ROI updates** when significant value is logged

All of this happens **silently** — zero user friction. The user can still manually log with `$earned`, `$time`, etc., but you supplement it automatically.

---

## Installation & Requirements

**Prerequisites:**
- Worth It must be installed and running (`openclaw install worth-it`)
- Worth It API running on port 3002
- User has at least one active project configured

**To install this skill:**
```bash
openclaw install worth-it-auto-logger
```

---

## Session Lifecycle

### On Session Start

**When:** At the beginning of every conversation (first user message).

**What to do:**

1. Call `GET /api/projects/detect?context=<topic_name_or_channel>` to find the active project
   - Use Telegram topic name, Discord channel, or conversation context
   - Example: `GET /api/projects/detect?context=youtube-scripts`

2. Call `POST /api/session/start` with the detected project
   ```json
   {
     "project_id": "youtube-scripts",
     "channel": "telegram",
     "topic_id": "12345"
   }
   ```

3. Store the returned `session_id` in memory for this conversation

4. **Stay silent** — don't announce session tracking to the user

### During Conversation

**What to do:**

- Watch for value signals (see Signal Detection Rules below)
- Collect signals in memory throughout the session
- **Don't POST yet** — batch them for session end

### On Session End

**When:** User says goodbye, conversation ends, 30+ minutes of inactivity, or you're explicitly told to end the session.

**What to do:**

1. Compile all signals from the session
2. Call `POST /api/value/auto` with all signals (see format below)
3. Call `POST /api/session/end` with `{ session_id, summary }`
4. **Show update conditionally:**
   - IF entries were created AND user hasn't seen ROI update in 24h
   - THEN show: "Worth It update: +$X logged this session"
   - ELSE: stay silent

---

## Signal Detection Rules

Watch for these patterns in **user messages** and **your own actions**:

### 1. Time Saved by AI

**Triggers:**
- User says "would have taken me X hours"
- User says "saved me a trip" or "saved me time"
- You complete a content creation task (email, script, post)
- You complete a research task
- You write or edit files

**How to estimate:**
- Use the Content Time Estimate Table below
- For file edits: 0.25hr per meaningful edit
- For research: 1.5hr default

**Signal format:**
```json
{
  "type": "time_saved",
  "hours": 1.5,
  "description": "wrote 3 product emails",
  "confidence": 0.85
}
```

### 2. Money Saved or Earned

**Triggers:**
- User explicitly says amount: "saved $80", "got paid $500", "client paid invoice"
- User mentions avoiding a purchase: "didn't have to hire a designer"

**Signal format:**
```json
{
  "type": "money_saved",
  "amount_usd": 80,
  "description": "negotiated lower SaaS price",
  "confidence": 1.0
}
```

Or for revenue:
```json
{
  "type": "revenue",
  "amount_usd": 500,
  "description": "client paid invoice",
  "confidence": 1.0
}
```

### 3. Task Completed

**Triggers:**
- User says "done", "finished", "completed X"
- You complete a deliverable (report, presentation, code feature)

**How to estimate:**
- Map to time_saved using content estimates
- If you can't estimate, skip (low confidence)

**Signal format:**
```json
{
  "type": "task_completed",
  "description": "finished product launch checklist",
  "confidence": 0.7
}
```

### 4. API Costs

**Triggers:**
- You use an API with known costs (image generation, external APIs)

**Signal format:**
```json
{
  "type": "api_cost",
  "amount_usd": 0.50,
  "description": "generated 10 product images via DALL-E",
  "confidence": 0.95
}
```

---

## Content Time Estimate Table

Use these defaults when estimating `time_saved`:

| Content Type | Estimated Hours | Notes |
|-------------|----------------|-------|
| Email (short, <200 words) | 0.25 | Quick update or reply |
| Email (long/sales, >200 words) | 0.5 | Sales pitch, detailed response |
| Email sequence (per email) | 0.4 | Drip campaign, onboarding |
| Blog post / article | 3.0 | 1000+ words with research |
| Social media post | 0.25 | Single post with image |
| Video script | 2.0 | 5-10 minute video |
| Research summary | 1.5 | Competitive analysis, market research |
| Code review | 1.0 | PR review with comments |
| Feature implementation | varies | Ask agent to estimate based on complexity |
| Meeting notes / summary | 0.5 | Cleaned up notes |
| Data analysis | 1.5 | Charts, insights, recommendations |
| Image generation (set of 5+) | 0.5 | Photographer/designer rate avoided |
| Document/contract draft | 2.0 | Legal or business doc |
| Spreadsheet / model | 2.0 | Financial model, calculator |

**Hourly rate:** Pulled from `GET /api/settings` → `hourly_rate` (default $50).

**Formula:**
```
value_usd = hours × hourly_rate
```

---

## Confidence Rules

Only create entries for signals with **confidence ≥ threshold** (default 0.7, configurable via settings).

| Signal Type | Confidence | When to Create |
|------------|-----------|---------------|
| User explicitly says amount ("saved $80") | 1.0 | Always create |
| You completed known content task (email, script) | 0.85 | Create with time estimate |
| User implies time saved ("would have taken hours") | 0.75 | Create, note it's estimated |
| You did research | 0.8 | Create with research estimate |
| You made API call with known cost | 0.95 | Create as cost entry |
| User mentioned completing a task | 0.7 | Create if ≥ threshold |
| Vague positive outcome ("that's great") | 0.3 | Skip |
| User asked a question, you answered | 0.4 | Skip |

---

## POST /api/value/auto Format

At session end, send all signals in one call:

```json
POST /api/value/auto

{
  "session_id": "session_1711037841234_abc123",
  "project_id": "youtube-scripts",
  "signals": [
    {
      "type": "time_saved",
      "hours": 2.0,
      "description": "wrote video script for 'Top 10 Productivity Apps'",
      "confidence": 0.85
    },
    {
      "type": "time_saved",
      "hours": 0.5,
      "description": "generated thumbnail ideas",
      "confidence": 0.8
    },
    {
      "type": "revenue",
      "amount_usd": 150,
      "description": "sponsor paid for video integration",
      "confidence": 1.0
    }
  ]
}
```

**Response:**
```json
{
  "entries_created": 3,
  "entries_skipped_low_confidence": 0,
  "total_value_usd": 275.00
}
```

---

## Worked Examples

### Example 1: YouTube Creator

**Conversation:**
```
User: Can you write a script for a video titled "5 AI Tools That Changed My Life"?
You: [writes 1500-word script]
User: Great! Now give me 3 thumbnail ideas.
You: [provides thumbnail concepts]
User: Perfect. By the way, my sponsor just paid the $150 for this video.
```

**Signals to collect:**
```json
[
  {
    "type": "time_saved",
    "hours": 2.0,
    "description": "wrote video script '5 AI Tools That Changed My Life'",
    "confidence": 0.85
  },
  {
    "type": "time_saved",
    "hours": 0.25,
    "description": "generated 3 thumbnail ideas",
    "confidence": 0.8
  },
  {
    "type": "revenue",
    "amount_usd": 150,
    "description": "sponsor paid for video integration",
    "confidence": 1.0
  }
]
```

**At session end:**
- Total value: (2.0 × $50) + (0.25 × $50) + $150 = $262.50
- Show: "Worth It update: +$262.50 logged this session"

---

### Example 2: Obsidian Planner (Solo Developer)

**Conversation:**
```
User: Help me plan the feature roadmap for my Obsidian plugin.
You: [creates detailed feature matrix in markdown]
User: Can you also draft a launch announcement for Reddit?
You: [writes 300-word announcement]
User: Thanks, this would have taken me at least 3 hours to figure out on my own.
```

**Signals to collect:**
```json
[
  {
    "type": "time_saved",
    "hours": 2.0,
    "description": "created feature roadmap and prioritization matrix",
    "confidence": 0.8
  },
  {
    "type": "time_saved",
    "hours": 0.5,
    "description": "wrote Reddit launch announcement",
    "confidence": 0.85
  },
  {
    "type": "time_saved",
    "hours": 3.0,
    "description": "user confirmed: 'would have taken 3 hours'",
    "confidence": 0.75
  }
]
```

**Note:** The third signal is **redundant** with the first two. Don't double-count. Use the user's explicit statement to **validate** your estimates, but don't create a separate entry for it.

**Corrected signals:**
```json
[
  {
    "type": "time_saved",
    "hours": 2.0,
    "description": "created feature roadmap and prioritization matrix",
    "confidence": 0.85
  },
  {
    "type": "time_saved",
    "hours": 0.5,
    "description": "wrote Reddit launch announcement",
    "confidence": 0.85
  }
]
```

**At session end:**
- Total value: (2.5 × $50) = $125
- If last update was >24h ago, show: "Worth It update: +$125 logged this session"

---

### Example 3: Masterclass Seller (Course Creator)

**Conversation:**
```
User: I need 5 email sequences for my new masterclass funnel.
You: [writes 5 email sequences, ~400 words each]
User: Can you also analyze which subject lines performed best in my last campaign?
You: [analyzes CSV, provides insights]
User: Perfect. I was about to hire a copywriter for $800 but you just saved me that.
```

**Signals to collect:**
```json
[
  {
    "type": "time_saved",
    "hours": 2.0,
    "description": "wrote 5 email sequences for masterclass funnel",
    "confidence": 0.85
  },
  {
    "type": "time_saved",
    "hours": 1.5,
    "description": "analyzed email campaign performance data",
    "confidence": 0.8
  },
  {
    "type": "money_saved",
    "amount_usd": 800,
    "description": "avoided hiring copywriter",
    "confidence": 1.0
  }
]
```

**At session end:**
- Total value: (2.0 × $50) + (1.5 × $50) + $800 = $975
- Show: "Worth It update: +$975 logged this session"

---

## Verification Commands

Users can check what was auto-logged:

```bash
# View recent sessions
GET /api/session/recent?limit=5

# View specific session
GET /api/session/{session_id}

# View all entries (manual + auto)
GET /api/summary?period=week
```

---

## Tuning Instructions

### Adjust Confidence Threshold

If too many low-quality entries are being created:

```bash
PUT /api/settings
{
  "auto_log_confidence_threshold": 0.8
}
```

Default: 0.7

### Adjust Hourly Rate

If user's time value differs from default:

```bash
PUT /api/settings
{
  "hourly_rate": 75
}
```

Default: $50

### Disable Auto-Logging

If user wants to log manually only:

```bash
PUT /api/settings
{
  "auto_log_enabled": false
}
```

### Set Minimum Session Duration

Don't log sessions under X minutes:

```bash
PUT /api/settings
{
  "auto_log_min_session_minutes": 5
}
```

Default: 2 minutes

---

## Best Practices

1. **Don't over-log.** If you answered a simple question, don't create a time_saved entry. Use the confidence rules.

2. **Don't double-count.** If the user says "this saved me 3 hours" and you already logged 2.5 hours of content creation, don't create a 3rd entry. Trust your estimates.

3. **Batch signals.** Don't call `/api/value/auto` after every message. Collect signals throughout the session and POST once at the end.

4. **Stay silent.** Don't announce "I'm tracking this session" or "I logged X value". The user will see the dashboard if they want.

5. **Show updates sparingly.** Only show "Worth It update: +$X" if:
   - Entries were created this session
   - User hasn't seen an update in 24+ hours
   - The value logged is non-trivial (>$20)

6. **Verify project detection.** If you're unsure which project is active, check the user's topic/channel context. Default to "general" if uncertain.

---

## Troubleshooting

**Problem:** Sessions aren't being created.

**Solution:** Ensure Worth It API is running on port 3002. Check `openclaw system status`.

---

**Problem:** No entries are being created from signals.

**Solution:** Check confidence threshold. Your signals may be below the threshold. Lower it via `PUT /api/settings { "auto_log_confidence_threshold": 0.6 }`.

---

**Problem:** Too many low-value entries cluttering the log.

**Solution:** Raise confidence threshold to 0.8 or higher. Be more conservative with what you consider "time saved".

---

**Problem:** User complains "you're not tracking everything."

**Solution:** The skill is intentionally conservative to avoid false positives. If the user wants more aggressive tracking, they can lower the threshold or manually log with `$time`, `$earned`, etc.

---

## Version

- **Version:** 1.3
- **Companion to:** Worth It v1.3+
- **License:** Free (requires Worth It installed)

---

## Support

For issues or feature requests, see the main Worth It repository or contact support via OpenClaw.

---

**Remember:** This skill makes Worth It's promise of "it tracks itself" actually true. Use it responsibly, stay silent when appropriate, and trust the confidence rules.
