---
name: ultrahuman-biodata-assistant
description: Use the Ultrahuman MCP to answer questions about sleep, recovery, readiness, daily metrics, morning brief, ring data, glucose, and metabolic health. Use this skill whenever the user asks about their Ultrahuman data, last night's sleep, recovery score, HRV, steps, glucose, metabolic score, readiness, or wants a "morning brief" or comparison over several days—even if they don't say "Ultrahuman" explicitly.
created: 2026-03-16
updated: 2026-03-16
---

# Ultrahuman bio-data assistant

This skill guides you to use the **Ultrahuman MCP** tools to fetch and present daily bio metrics (sleep, recovery, HR, HRV, steps, glucose, metabolic score, etc.) in clear workflows. Use it whenever the user cares about sleep quality, recovery, readiness, or daily health metrics from their ring/CGM data.

## Prerequisites

- The **ultrahuman_mcp** MCP server must be available and configured (ULTRAHUMAN_TOKEN and ULTRAHUMAN_EMAIL in the environment, or user provides email for the request).
- For date-based queries, resolve "today" / "yesterday" to the correct **YYYY-MM-DD** date (prefer the user's local date when possible, or state which date you used).

## Workflows

### 1. Morning brief

User asks for a summary of their night or "how did I sleep" or "morning brief".

1. Call **ultrahuman_get_daily_metrics** with the user's email (from context or env) and the relevant date (e.g. yesterday for "last night").
2. From the response, surface: **Sleep score**, **Recovery score**, **Resting HR**, **HRV**, **Steps** (if available). Optionally total sleep time and sleep efficiency from sleep details.
3. Reply with a short executive summary first, then a compact metrics section. Keep it scannable.

### 2. Recovery check

User asks "how was my recovery?" or "am I ready to train?".

1. Call **ultrahuman_get_daily_metrics** for the date in question.
2. Focus on: **Recovery score**, **HRV**, **Sleep score**, and **Resting HR**. If the API returns recovery_index or movement_index, include them.
3. Give a one-line readiness takeaway (e.g. "Recovery looks good" / "Consider a lighter day") based on the numbers—descriptive only, not medical advice. For interpretation heuristics, see **references/interpretation.md** when needed.

### 3. Multi-day trend (e.g. last 3 or 7 days)

User asks to compare sleep or recovery over several days.

1. Call **ultrahuman_get_daily_metrics** once per day (same email, date for each).
2. Summarize in a short table or bullet list: date, sleep score, recovery score, and 1–2 other key metrics (e.g. HRV, steps).
3. Add a brief trend line (e.g. "Sleep scores improved over the week") without over-interpreting.

## Patterns

- **Dates:** Always use **YYYY-MM-DD**. For "today" / "yesterday", compute the date; if timezone is ambiguous, state which date you used.
- **Email:** Use the email from environment (ULTRAHUMAN_EMAIL) or from the user's message. If neither is available, ask once for the Ultrahuman account email.
- **Structure answers:** Lead with a one- or two-sentence summary, then metrics (and optional short recommendations). Avoid raw JSON unless the user asked for data export.
- **Tone:** Descriptive and supportive. Use phrases like "your ring data shows …", "according to your metrics …". Do **not** give medical diagnoses or treatment advice.
- **Missing data:** If the API returns no data for a date, say so clearly and suggest checking the date or that data may still be processing.

## Output format

Use this structure for morning briefs and recovery summaries:

1. **Summary** – One or two sentences (sleep/recovery headline).
2. **Metrics** – Key numbers (sleep score, recovery, HR, HRV, steps; add glucose/metabolic if present).
3. **Recommendations** (optional) – Only generic, non-medical tips (e.g. "Earlier bedtime may help sleep consistency") when relevant.

## References (load when needed)

- **references/metrics_glossary.md** – Definitions and units for Sleep Score, Recovery Index, HRV, Metabolic Score, Time in Target, etc.
- **references/interpretation.md** – Heuristics for "good" vs "pay attention" ranges (e.g. recovery, sleep efficiency, glucose variability). Use for context only; not medical guidance.

When the user asks what a metric means or how to read their numbers, load the glossary. When you need to judge "how good" a value is, use the interpretation reference.
