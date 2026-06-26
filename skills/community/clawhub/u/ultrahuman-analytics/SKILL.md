---
name: ultrahuman-analytics
description: Advanced Ultrahuman analytics, trends, predictions, and reports. Use this skill when the user asks for weekly report, 7-day summary, recovery trend, sleep consistency, metabolic week, VO2 or movement trend, deep/REM balance, tomorrow readiness, training load check, low-recovery alert, glucose spike risk, sleep-glucose link, sleep-recovery link, rest day effect, weekday vs weekend, PDF summary, coach view, monthly one-pager, best night of the week, streak, personal record, or weekly MVP. Use for any multi-day analysis, prediction, correlation, or export from Ultrahuman ring/CGM data.
created: 2026-03-16
updated: 2026-03-16
---

# Ultrahuman analytics

This skill implements **multi-day analytics, predictions, correlations, reports, and engagement** on top of Ultrahuman data. Always use the **ultrahuman_mcp** tool `ultrahuman_get_daily_metrics` once per date, then aggregate and interpret in your response. Never invent data; only use what the API returns.

## Prerequisites

- **ultrahuman_mcp** must be available. Use email from ULTRAHUMAN_EMAIL or user message.
- Dates in **YYYY-MM-DD**. For "last 7 days" compute the 7 dates ending yesterday (or today if user says "including today").
- All workflows are **read-only** and **descriptive** (no medical advice).

---

## 1. Analytics and evaluations

### 1.1 Weekly report

**Trigger:** "weekly report", "last 7 days summary", "how was my week", "week in review".

**Steps:**

1. Call **ultrahuman_get_daily_metrics** for each of the last 7 days (same email). Use `response_format: "json"` if you need to parse programmatically, or `"markdown"` and extract numbers from the summary.
2. For each day extract: sleep score, recovery score, HRV (avg), night RHR, steps. If present: metabolic_score, time_in_target, average_glucose.
3. Compute: **averages** for sleep, recovery, HRV, steps; **best night** (highest recovery or sleep score, state which date); **worst night** (lowest); **day-over-day deltas** (e.g. "Recovery improved 3 days in a row, then dropped").
4. Reply with: one short paragraph summary, then a small table (date | sleep | recovery | HRV | steps), then 1–2 bullet insights (e.g. "Best night: Wed (recovery 8). Recovery trend: improving into mid-week.").

### 1.2 Sleep consistency score

**Trigger:** "sleep consistency", "how consistent is my sleep", "sleep variability".

**Steps:**

1. Fetch **last 7–14 days** via **ultrahuman_get_daily_metrics** (one call per date).
2. From each day's sleep object get: total sleep (from quick_metrics), sleep efficiency, and if available bedtime (from details). Compute standard deviation or range for total sleep and efficiency.
3. Derive a simple "consistency" statement: e.g. "You're highly consistent (sleep within 30 min and efficiency within 5% most nights)" or "Sleep duration varied by ~1h this week – consider more consistent bedtimes."
4. No formal score required; descriptive summary is enough.

### 1.3 Recovery trend

**Trigger:** "recovery trend", "recovery over the week", "how is my recovery trending", "recovery last 14 days".

**Steps:**

1. Fetch **7 or 14 days** (one call per date).
2. Extract per day: recovery score or recovery_index, HRV avg, night_rhr avg.
3. Build a **table**: date | recovery | HRV | night RHR. Add a one-line trend: "Improving", "Declining", "Stable", or "Recovery dipped mid-week then recovered."
4. If recovery dropped for 3+ days in a row, add a short note: "Consider lighter days or more sleep" (descriptive only).

### 1.4 Metabolic week

**Trigger:** "metabolic week", "glucose this week", "time in target last 7 days", "metabolic summary".

**Steps:**

1. Fetch last **7 days**.
2. From each day get: metabolic_score, time_in_target, average_glucose, glucose_variability (if present). If a day has no CGM data, note "No CGM data for [date]."
3. Compute weekly averages for the metrics that exist. Optionally compare to the **previous 7 days** if user asked for "vs last week" (then fetch 14 days and split).
4. Reply: "Metabolic week: average time in target X%, avg glucose Y mg/dL, variability Z%. [One-line comparison if previous week requested.]"

### 1.5 VO2 and movement trend

**Trigger:** "VO2 trend", "movement this week", "activity trend", "steps and VO2".

**Steps:**

1. Fetch last **7 days**.
2. Extract: steps (avg), movement_index, vo2_max per day where available.
3. Weekly average for steps and movement_index; if vo2_max is present, note trend (up/stable/down) or latest value.
4. One sentence: "Activity trend: [up/stable/down]. Weekly avg steps: X. Movement index avg: Y."

### 1.6 Deep / REM balance

**Trigger:** "deep sleep", "REM sleep", "sleep stages", "deep vs REM".

**Steps:**

1. Fetch last **7 days** (or N user specified).
2. From each day's sleep **details.sleep_stages** get: deep_sleep %, light_sleep %, rem_sleep %, awake %.
3. Compute average % deep and average % REM over the period. Note if one is consistently low (e.g. "REM averaged 12% – some research associates higher REM with memory and mood; consider sleep consistency."). Descriptive only, no diagnosis.

---

## 2. Predictions and readiness

### 2.1 Tomorrow readiness

**Trigger:** "tomorrow readiness", "will I be ready tomorrow", "am I set for tomorrow".

**Steps:**

1. Fetch **last night's** (or the most recent night's) data with **ultrahuman_get_daily_metrics**.
2. Read: sleep score, recovery score, HRV.
3. Heuristic (descriptive only): "When recovery is above 7 and sleep above 6, your numbers typically support a solid next day. Your last night: recovery X, sleep Y – [so your numbers suggest good readiness / suggest paying attention to rest today]."
4. Do not promise outcomes; only describe what the numbers often indicate.

### 2.2 Training load check

**Trigger:** "I trained hard yesterday", "training load", "did I recover from my workout", "heavy training yesterday".

**Steps:**

1. Fetch **yesterday** and optionally **today** (or 2–3 days including the training day).
2. Compare recovery, sleep, HRV on the night *after* the training day to the user's recent baseline (e.g. 7-day average). If no baseline yet, use the same night's values only.
3. Reply: "After your training day, last night's recovery was [X]. [Compared to your recent average, that's typical / below your average – your body may need more recovery before the next hard session.]" Descriptive only.

### 2.3 Low-recovery alert

**Trigger:** "low recovery", "recovery alert", "am I overreaching", "recovery slipping".

**Steps:**

1. Fetch last **7 days**.
2. Compute 7-day average recovery (or recovery_index). Count how many of the **last 3 nights** were below that average.
3. If 2 or 3 of the last 3 nights are below average: "Last 3 nights your recovery was below your 7-day average – consider lighter days or more sleep."
4. If not, briefly summarize: "Your last 3 nights are in line with or above your weekly average."

### 2.4 Glucose spike risk (pattern)

**Trigger:** "glucose and sleep", "does sleep affect my glucose", "glucose spike risk".

**Steps:**

1. Fetch last **7–14 days**.
2. For each day: total sleep (from sleep details) or sleep score, and glucose_variability or average_glucose (if CGM data exists).
3. Split days into "shorter sleep" (e.g. &lt;6h or sleep score &lt;5) vs "longer sleep". Compute average glucose variability (or average glucose) for each group.
4. One sentence pattern: "On days when you slept under 6h, your glucose variability averaged X% vs Y% on longer-sleep days." No causation; present as observed pattern only.

---

## 3. Correlations and insights

### 3.1 Sleep–glucose link

**Trigger:** "sleep and glucose", "sleep glucose link", "how does sleep affect my glucose".

**Steps:**

1. Fetch **7–14 days**.
2. For each day: total sleep or sleep score; time_in_target and/or average_glucose.
3. Group days by e.g. "7+ hours sleep" vs "under 7 hours". Average time_in_target (and optionally average_glucose) per group.
4. Reply: "When you slept 7+ hours, time in target averaged X%. When you slept less, it averaged Y%." No causation; pattern only.

### 3.2 Sleep–recovery link

**Trigger:** "sleep recovery link", "does sleep affect recovery", "sleep efficiency and recovery".

**Steps:**

1. Fetch **7–14 days**.
2. From each day: sleep efficiency (from sleep details quick_metrics), recovery score or recovery_index.
3. Group by efficiency (e.g. ≥85% vs &lt;85%). Average recovery per group.
4. Reply: "Your recovery tends to be higher when sleep efficiency is above 85% (avg recovery X vs Y when efficiency is lower)."

### 3.3 Rest day effect

**Trigger:** "rest day", "days I didn't train", "recovery after rest".

**Steps:**

1. Fetch last **7–10 days**.
2. Use **steps** (or movement_index) as a proxy for activity: "high steps" vs "low steps" days. Define thresholds simply (e.g. above/below median steps).
3. Compare average recovery and sleep score (and HRV if you like) on "low steps" days vs "high steps" days.
4. Reply: "On lower-activity days your recovery averaged X vs Y on higher-activity days." Descriptive only.

### 3.4 Weekday vs weekend

**Trigger:** "weekday vs weekend", "weekend sleep", "do I sleep better on weekends".

**Steps:**

1. Fetch last **14 days** (to get at least two weekends).
2. Label each date as weekday (Mon–Thu) or weekend (Fri–Sun), or Mon–Fri vs Sat–Sun depending on user wording.
3. Average sleep score and recovery score for weekday vs weekend.
4. Reply: "Weekday average sleep score X, recovery Y. Weekend sleep X2, recovery Y2. [You sleep ~Z% better on weekends / similar across the week.]"

---

## 4. Reports and exports

### 4.1 PDF-ready summary

**Trigger:** "PDF summary", "export last 7 days", "report I can copy", "summary for doc".

**Steps:**

1. Fetch last **7 days** (or N requested).
2. Build a **structured Markdown or plain-text** block: title "Ultrahuman summary – [date range]"; then table with columns Date | Sleep | Recovery | HRV | Steps | [Glucose/Metabolic if present]; then one line "Trend: …".
3. Tell the user they can copy the block into a doc or export to PDF. No images; text/table only.

### 4.2 Coach view

**Trigger:** "coach view", "share with coach", "coach summary", "trainer report".

**Steps:**

1. Fetch last **7–14 days**.
2. Include only: **recovery trend** (up/down/stable), **sleep consistency** (one line), **any red flags** (e.g. "3 nights in a row below average recovery"). Optional: best night, worst night, one MVP metric.
3. Keep it short (3–5 bullets). Framed as "Summary for your coach" or "Highlights to share."

### 4.3 Monthly one-pager

**Trigger:** "monthly summary", "last month", "4 weeks", "month over month".

**Steps:**

1. Fetch last **28 days** (or 4 full weeks). Group by week (e.g. Week 1: days 1–7, Week 2: 8–14, …).
2. For each week compute: average sleep score, recovery, steps; optionally metabolic if available.
3. Output: table "Week | Sleep avg | Recovery avg | Steps avg | [Metabolic]"; then one sentence "Month over month: [improving / stable / declining]."
4. If user asked for "vs previous month", fetch 56 days and compare two 28-day blocks.

---

## 5. Fun and engagement

### 5.1 Best night of the week

**Trigger:** "best night", "best sleep this week", "top night".

**Steps:**

1. Fetch last **7 days**.
2. Pick the night with **highest recovery score** (or sleep score if recovery missing). State the date and day name.
3. Reply: "Your best night this week was [Tuesday] ([date]): recovery [X], [7h20 sleep], HRV [Y]." Include 1–2 other metrics from that night.

### 5.2 Streak counter

**Trigger:** "streak", "how many nights", "recovery streak", "sleep streak".

**Steps:**

1. Fetch last **7–14 days** (enough to count backwards).
2. From **most recent night** going backwards, count consecutive nights where recovery score ≥ 7 (or sleep score ≥ 7, if user said "sleep streak").
3. Reply: "You've had [N] nights in a row with recovery ≥ 7." Or "Your current streak is [N] nights of sleep score ≥ 7." If streak is 0, say "No streak right now – last night was below 7."

### 5.3 Personal record

**Trigger:** "personal record", "best HRV", "best sleep score", "PR this month".

**Steps:**

1. Fetch the **requested range** (e.g. last 30 days or "this month").
2. Find **max HRV** and the date; **max sleep score** and the date. If user asked for one metric only, do that one.
3. Reply: "Your highest HRV this [period] was [58] on [date]. Your best sleep score was [9] on [date]."

### 5.4 Weekly MVP metric

**Trigger:** "weekly MVP", "highlight this week", "best metric this week", "standout".

**Steps:**

1. Fetch last **7 days**.
2. Compute averages for: sleep score, sleep efficiency, recovery, HRV, steps, and if present time_in_target or metabolic_score.
3. Pick **one positive highlight** (e.g. "Sleep efficiency averaged 92%" or "Recovery averaged 7.5"). Reply: "This week's standout: [one sentence]."

---

## General rules

- **Always** use **ultrahuman_get_daily_metrics** with the user's email and correct **YYYY-MM-DD** dates. One call per date; then aggregate in your answer.
- **Never** invent or assume data. If a day has no data, say so and skip or note "No data for [date]."
- **Tone:** Descriptive and supportive. "Your data shows …", "On average …". No medical diagnosis or treatment advice.
- **Missing metrics:** If CGM or VO2 is not in the response, skip those parts and report what is available.
- **Output:** Prefer short summary first, then table or bullets, then one-line takeaway. For "export" or "PDF", output copy-paste-ready text.

Use **references/metrics_glossary.md** and **references/interpretation.md** from the **ultrahuman-biodata-assistant** skill when you need definitions or interpretation heuristics.
