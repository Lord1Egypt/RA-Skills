---
name: viralevo
description: Self-evolving viral content trend advisor. Monitors 11 platforms, predicts what to post and when, and improves its own accuracy every week automatically.
version: 0.6.4
homepage: https://github.com/0xF69/viralevo
user-invocable: true
metadata: {"openclaw":{"emoji":"📈","requires":{"bins":["node","python3"],"env":["TAVILY_API_KEY"]},"primaryEnv":"TAVILY_API_KEY","install":[{"id":"node","kind":"node","label":"Install npm dependencies (better-sqlite3, axios, dotenv)"}]}}
---

# ViralEvo — Viral Content Trend Advisor

**Version:** v0.6.4 | **Languages:** English / 中文

---

## 语言说明 / Language Support

本 Skill 完整支持中文操作。安装完成后，你可以：
- 用中文与 Agent 对话（"今天该发什么内容？"）
- 接收中文版每日报告
- 用中文关键词监控中文平台内容
- 在引导设置时选择界面语言

This skill fully supports both English and Chinese. During onboarding, the agent will ask which language you prefer.

---

## What This Skill Does

ViralEvo monitors content platforms, scores trending topics using a weighted formula, predicts lifecycle windows, and automatically adjusts its own prediction weights every week based on how accurate it was.

**Three core advantages over manual research:**

1. **Catches trends 12–48h early** — monitors signal velocity across 11 platforms simultaneously
2. **Learns from your results** — when you report your post outcomes, those signals feed back into the model
3. **Self-corrects weekly** — every Monday the system reviews its prediction errors and updates its weights automatically

---

## Quick Start

After installation, add your Tavily API key:

```bash
echo "TAVILY_API_KEY=tvly-xxxx" >> ~/.openclaw/workspace/.env
```

Then tell your agent:

```
"Start ViralEvo setup"
— or in Chinese —
"开始趋势雷达设置"
```

Or run onboarding directly:

```bash
node {baseDir}/scripts/onboarding.js
```

---

## Natural Language Triggers

When the user reports post results (e.g. "got 80k views", "效果很好"), the agent should:
1. Search for the matching topic: `python3 {baseDir}/scripts/feedback.py --search "<keyword>"`
2. Confirm the match with the user
3. Log the result: `python3 {baseDir}/scripts/feedback.py --topic-id <id> --platform <platform> --views <n>`

When the user says any of the following, the agent should run **collect → report**:

- "What should I post today?" / "今天该发什么？"
- "Any trends?" / "有什么趋势？"
- "Show me the trend report" / "给我看趋势报告"
- "What's trending in my niche?" / "我的赛道有什么热点？"

When the user says:

- "Run ViralEvo" / "运行趋势雷达" → run collect then report
- "Collect trends" / "采集趋势" → run collect only
- "Generate report" / "生成报告" → run report only
- "Weekly review" / "周度复盘" → run weekly_review
- "Show keywords" / "查看关键词" → run keywords --show

---

## Feedback Intake

When the user describes post results, **always match to a recent topic, confirm before logging**:

- "The hair clips video got 80k views on TikTok" → match topic, log: views=80000, platform=tiktok
- "那个AI文章效果很好，小红书5000收藏" → 匹配话题，记录：saves=5000, platform=xiaohongshu

Use the `/trend feedback` command or natural language — both are accepted.

---

## Available Commands

| Command | Action |
|---|---|
| `node {baseDir}/scripts/onboarding.js` | First-time setup wizard |
| `node {baseDir}/scripts/collect.js` | Fetch trend signals from all sources |
| `python3 {baseDir}/scripts/report.py` | Generate and output today's report |
| `python3 {baseDir}/scripts/verify.py --hours 24` | Verify yesterday's predictions |
| `python3 {baseDir}/scripts/verify.py --hours 72` | Verify 72h-old predictions |
| `python3 {baseDir}/scripts/weekly_review.py` | Run self-evolution (Mondays recommended) |
| `python3 {baseDir}/scripts/keywords.py --show` | View your keyword index |
| `python3 {baseDir}/scripts/keywords.py --add "term"` | Add a keyword manually |
| `python3 {baseDir}/scripts/keywords.py --remove "term"` | Remove a keyword |
| `python3 {baseDir}/setup.py` | Check all system requirements |
| `python3 {baseDir}/scripts/feedback.py --list` | List recent topics to log feedback for |
| `python3 {baseDir}/scripts/feedback.py --search "keyword"` | Find a topic by keyword |
| `python3 {baseDir}/scripts/feedback.py --topic-id <id> --platform tiktok --views 80000` | Log post performance |
| `python3 {baseDir}/db/init_db.py` | Re-initialize database (use if DB is corrupted) |
| `python3 {baseDir}/scripts/status.py` | Quick health check — config, API key, DB, recent data |

---

## System Requirements

| Requirement | Minimum | Role |
|---|---|---|
| Node.js | v18+ | Data collection, onboarding |
| Python | 3.10+ | Scoring, reports, self-evolution |
| OpenClaw | v2026.1+ | Agent runtime, scheduling |
| Tavily API Key | Free tier | Indirect platform search |

Tavily free tier = 1,000 calls/month. Single niche daily usage ≈ 60–120/month.

---

## Supported Platforms

| Platform | Method | Confidence Cap |
|---|---|---|
| HackerNews | Official Algolia API | 1.00 |
| Dev.to | Official API | 1.00 |
| Product Hunt | RSS | 1.00 |
| Reddit | JSON API (public) | 0.90 |
| YouTube | Tavily search | 0.70 |
| Twitter / X | Tavily search | 0.70 |
| Pinterest | Tavily search | 0.70 |
| LinkedIn | Tavily search | 0.70 |
| TikTok | Tavily search | 0.65 |
| Instagram | Tavily search | 0.65 |

---

## Supported Niches

AI/Tech · E-commerce · Beauty/Skincare · Fitness/Health · Finance · Gaming · Fashion/Lifestyle · Education · Real Estate · Pets · Custom (11 niches)

---

## Scoring Formula

```
Total Score =
  (Platform Signal Strength)  × W1  [default 0.25]
+ (Engagement Velocity)       × W2  [default 0.25]
+ (Cross-Platform Spread)     × W3  [default 0.20]
+ (Niche Relevance Score)     × W4  [default 0.15]
+ (Goal Alignment Score)      × W5  [default 0.15]

Constraints: W1+W2+W3+W4+W5 = 1.0 exactly
Each weight: floor=0.08, ceiling=0.45
Max change per weekly review: ±0.05 (±0.10 after algorithm change detection)
```

---

## Report Output Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔥 ViralEvo | AI/Tech | 2026-03-09 08:15
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 ACT NOW (Score > 80)
1. OpenClaw Security Issue — 135k instances exposed
   ████████████████████ 93% | Confidence: 0.85
   📅 Detected 14h ago | Source: hackernews
   ⏰ Estimated window: ~42h remaining
   🎯 Post: TODAY

🟡 PREPARE (Score 60–80)
2. OpenAI Government Surveillance Controversy
   ████████████████░░░░ 78% | Confidence: 0.74
   📅 Detected 6h ago | Source: dev.to
   ⏰ Estimated window: ~68h remaining
   🎯 Post: Tomorrow morning

🟢 EVERGREEN (Score < 60)
3. MCP Protocol Enterprise Adoption
   ████████░░░░░░░░░░░░ 44% | Confidence: 0.79
   📅 Steady growth — no spike
   ⏰ Relevant: 30d+
   🎯 Post: Any time this week

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Model Health
  Accuracy     : 58% (44 predictions)
  Sources      : 6/6 ✅
  Tavily usage : 112 / 1,000 this month
  Keyword index: 1,203 terms
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---


## Scheduling (Cron Setup)

ViralEvo runs automatically via OpenClaw's cron system. After onboarding, add these four jobs to your OpenClaw cron config.

**How to add cron jobs in OpenClaw:**

Tell your agent:
```
"Add a cron job to run ViralEvo daily at 8am"
```

Or add manually to `~/.openclaw/openclaw.json`:

```json
{
  "cron": {
    "jobs": [
      {
        "id": "viralevo-collect-report",
        "schedule": "0 8 * * *",
        "commands": [
          "node ~/.openclaw/workspace/viralevo/scripts/collect.js",
          "python3 ~/.openclaw/workspace/viralevo/scripts/report.py"
        ]
      },
      {
        "id": "viralevo-verify-24h",
        "schedule": "5 8 * * *",
        "commands": ["python3 ~/.openclaw/workspace/viralevo/scripts/verify.py --hours 24"]
      },
      {
        "id": "viralevo-verify-72h",
        "schedule": "10 8 * * *",
        "commands": ["python3 ~/.openclaw/workspace/viralevo/scripts/verify.py --hours 72"]
      },
      {
        "id": "viralevo-weekly-review",
        "schedule": "0 8 * * 1",
        "commands": ["python3 ~/.openclaw/workspace/viralevo/scripts/weekly_review.py"]
      }
    ]
  }
}
```

> See OpenClaw docs: https://docs.openclaw.ai/automation/cron-jobs

---

## OpenClaw Config (Alternative API Key Setup)

Instead of using `.env`, you can configure your Tavily key via `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "viralevo": {
        "enabled": true,
        "apiKey": "tvly-your-key-here"
      }
    }
  }
}
```

---

## Self-Evolution Loop

**Daily verification** (5 min and 65 min after your report time): re-fetches topics predicted 24h ago, compares predicted lifecycle vs actual activity, records error.

**Weekly review** (every Monday at your report time):
1. Aggregates all predictions from past 7 days
2. Calculates accuracy per platform, per topic type
3. Identifies top 3 sources of systematic error
4. Proposes weight adjustments (max ±0.05 per weight)
5. Applies new weights to config.json
6. Writes report to `reports/YYYY-MM-DD_weekly.md`
7. Auto-rolls back if accuracy drops for 2 consecutive weeks

---

## Accuracy Expectations

| Period | Expected Accuracy |
|---|---|
| Week 1–2 | 30–40% (cold start) |
| Month 2 | 55–65% |
| Month 3+ | 65–75% |
| Month 6+ | 75%+ |

Accuracy = prediction within ±20% of actual topic lifecycle.

---

## Data Location

```
~/.openclaw/workspace/viralevo/
├── config.json              ← niche, weights, schedule
├── user_profile.json        ← onboarding answers, language
├── data/
│   ├── trends.db            ← SQLite database
│   └── backups/             ← daily snapshots, 7-day retention
├── reports/                 ← daily + weekly markdown reports
└── logs/
    └── execution.log
```

---

## Privacy

All data is stored locally on your machine. The skill makes outbound network requests only to fetch public trend signals:
- HackerNews, Dev.to, Product Hunt, Reddit: public APIs, no auth required
- Tavily API: receives only search query strings — no personal data transmitted

---

## ⚠️ Disclaimers

ViralEvo provides probabilistic estimates based on publicly available signals. It does not guarantee specific outcomes in views, impressions, followers, or revenue. All predictions are directional guidance — not the sole basis for business decisions. Platform APIs change without notice.

---

## Uninstall

```bash
# Step 1: Remove skill from OpenClaw
openclaw skills remove viralevo

# Step 2: Delete local data (optional)
rm -rf ~/.openclaw/workspace/viralevo/

# Step 3: Verify
openclaw skills list
```

> If you reinstall later without deleting Step 2, ViralEvo will resume from your existing data.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| "Not configured" | Run `node {baseDir}/scripts/onboarding.js` |
| "TAVILY_API_KEY not set" | Add key to `~/.openclaw/workspace/.env` |
| No topics in report | Run `node {baseDir}/scripts/collect.js` first |
| System check | Run `python3 {baseDir}/setup.py` |
| Accuracy dropping | Run `python3 {baseDir}/scripts/weekly_review.py` manually |
| Quick diagnosis | Run `python3 {baseDir}/scripts/status.py` |
