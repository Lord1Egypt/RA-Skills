---
name: remote-jobs-finder
version: 1.6.0
description: Fully conversational remote job finder for WhatsApp powered by Remote Rocketship. Uses rr_jobs_search tool (server-side RR_API_KEY) and supports pagination ("20 more").
---

# Remote Rocketship × OpenClaw Skill (Natural Language Job Finder)

Use this skill whenever a user asks (in normal chat) to find remote jobs, browse opportunities, or set up an ongoing job search. This integration is powered by Remote Rocketship (https://www.remoterocketship.com).

Github repo: https://github.com/Lior539/openclaw-remote-jobs-finder

**UX rule:** fully conversational. Do not tell the user to run CLIs, use slash commands, or visit dashboards.

---

## Fetching jobs (MANDATORY)

When the user wants real job listings, you MUST call the OpenClaw tool `rr_jobs_search`.

Hard rules:
- Do NOT ask the user to run any CLI.
- Do NOT claim you can’t fetch listings (you can).
- Do NOT attempt raw HTTP calls from the model.

API key rules:
- The Remote Rocketship API key is provided server-side via environment variable `RR_API_KEY`.
- Never ask the user to paste secrets in WhatsApp.

Example call:
```json
{
  "filters": {
    "page": 1,
    "itemsPerPage": 20,
    "jobTitleFilters": ["Product Manager"],
    "locationFilters": ["United Kingdom"]
  },
  "includeJobDescription": false
}
```

---

## When to Trigger

Trigger on messages like:
- “Help me find a remote job”
- “Find me remote Product Manager roles”
- “Show me remote jobs in the UK”
- “Any new backend roles since yesterday?”
- “Send me 20 more”
- “Set this up to check every hour”

---

## Conversation Flow

### A) Onboarding (keep it short)
Ask only what you need. Prefer 1–3 quick questions, then fetch.

1) Role / direction (required)
- “What kind of roles are you looking for? (job titles, function, seniority)”

2) Location eligibility (required)
- “Where can you legally work from? (country / region)”

3) Must-haves & deal-breakers (optional, single combined question)
- “Any must-haves (salary/industry/async) or deal-breakers?”

4) Monitoring cadence (optional)
- “Want me to check for new matches on a schedule (hourly/daily/off)?”

If the user doesn’t want to answer everything, proceed with what you have and fetch results anyway.

### B) First fetch (default)
- Default `itemsPerPage: 20` unless the user asks for a different batch size.
- Keep `includeJobDescription: false` unless the user asks for deeper detail.

---

## Preference Memory (important)

Maintain a simple user profile in memory so the user doesn’t need to repeat themselves:

- targetTitles: string[]
- locationFilters: string[]
- seniorityFilters: string[] (if known)
- employmentTypeFilters: string[] (if known)
- mustHaves: string[]
- dealBreakers: string[]
- rankingPreference: "best_fit" | "newest_first"
- pollingCadence: e.g. "hourly" / "daily" / "off"
- lastQueryFilters: the last `filters` object used (for “20 more”)

If the user updates anything (“Actually only contract roles”), update memory.

---

## Pagination & “20 more”

Store lightweight paging state:
- filters
- page
- itemsPerPage
- pagination.totalCount / hasNextPage

Rules:
1) When the user tweaks filters, reset `page` back to 1 and fetch again.
2) If they say “more”, “20 more”, “next page”, increment `filters.page` and call `rr_jobs_search` again with the last filters.
3) Always mention what you’re showing (e.g., “Showing 21–40 of 134”).
4) If `hasNextPage` is false, tell the user you’ve reached the end.

---

## Output formatting (WhatsApp-friendly)

For each job, show as a bulleted list:
**Role Title** — Company
- 🕒 Posted: <date and time posted, formatted nicely e.g. today @ 5:15pm, or yesterday @ 2:10pm, or 2 days ago, or 1 week ago etc. Only show time if it was today or yesterday> 
- <flag emoji> Location (remote scope)
- 💰 Salary (or “Salary undisclosed”)
- 1–2 line summary
- 🔗 Link to apply
- 🏢 Link to company homepage
- 🌐 Link to company LinkedIn:

Keep it concise. After the list, ask what to do next:
- “Want 20 more, or should I narrow by industry/seniority/salary?”

---

## OpenClaw Tool to Use (required)

Tool: `rr_jobs_search`

Parameters:
- `filters` (object): passed through to Remote Rocketship API `filters`
- `includeJobDescription` (boolean, optional; default false)

The tool performs the POST to:
`https://www.remoterocketship.com/api/openclaw/jobs`

---

## Error handling

| Status | Meaning | Agent guidance |
| --- | --- | --- |
| 401 | Missing/invalid API key | Tell the admin to set/repair `RR_API_KEY` server-side and restart the gateway. Do NOT ask the user for keys in chat. |
| 403 | Subscription inactive | Tell the user they need an active Remote Rocketship plan to fetch jobs. |
| 429 | Rate limit | Inform the user you hit the daily limit and suggest retrying later. |
| 5xx | Backend issue | Apologize, retry once, then ask the user to try again later. |

---

## Filters (common)

Common filter keys you can use inside `filters`:
- `page` (int, default 1)
- `itemsPerPage` (int, default 20, max 50)
- `jobTitleFilters` (string[])
- `locationFilters` (string[]) — use canonical values like “United Kingdom”, “Worldwide”
- `keywordFilters` (string[])
- `excludedKeywordFilters` (string[])
- `seniorityFilters` (string[]) — e.g. `["senior"]`
- `employmentTypeFilters` (string[]) — e.g. `["full-time"]`

Prefer canonical titles/locations from RR lists when possible.
