---
name: x-hots
version: 2.0.1
description: Fetch trending topics from X (Twitter). Analyze user interests from natural language, retrieve top hot topics per domain, and summarize background, key opinions, and controversies.
---

# X (Twitter) Hot Topics Fetcher

Primary source = logged-in browser on x.com (full index, engagement-ranked Top search + Explore trending).
Fallback = X API free-tier search, which **systematically misses viral tweets** (verified 2026-10-19: a 740K-view tweet was absent from `search_recent` results while low-engagement residue ranked top). Never use API search alone to claim what is "hot".

## Prerequisites

### Browser source (primary; no credentials needed)
- OpenClaw browser tool with a logged-in x.com session (session cookies persist in the managed browser profile).
- Session check: `browser action=tabs`; reuse or open tab label `x-login` at `https://x.com/home`. Logged-in = title `(N) Home / X` plus timeline cards. Landing/login page = session expired → restore the session first (cookie import or the assisted-browser-login skill); do not fetch while logged out.
- Cloudflare "Performing security verification" page: retry the same navigation up to 3 times (~5–10 s apart); it usually clears once `cf_clearance` is set. Still blocked after retries → go to fallback.

### API fallback (credentials OPTIONAL)
- `pip3 install tweepy` (only needed for fallback).
- Env `X_BEARER_TOKEN` — **optional**: required only if the browser source fails and API fallback is desired. If unset and the browser fails, report both sources down; never present API-only output as the complete hot-topic picture.

## Workflow

### Step 1: Parse interest domains
| Domain | Keywords |
|---|---|
| International Politics | politics, geopolitics, diplomacy, sanctions, war, NATO, UN |
| Economy & Finance | economy, stock market, tariff, trade, inflation, crypto, bitcoin |
| Technology | AI, LLM, GPT, tech, chip, semiconductor, Apple, Google, Microsoft |
| Sports | football, World Cup, NBA, Olympics, FIFA |
| Entertainment | movie, music, celebrity, Netflix, Disney |
| Society | climate, health, education, protest, human rights |

Rules: explicit domain → its keywords; specific topic → that topic's keywords; nothing identifiable → generic hot set via browser Top search (`trending OR breaking OR viral OR news`) plus Explore trending. Pick 2–3 keywords per domain.

### Step 2: Browser fetch (primary)
**2a Today's trends:** navigate `https://x.com/explore/tabs/trending`, then evaluate:
` () => Array.from(document.querySelectorAll('[data-testid="trend"]')).map(e => e.innerText.replace(/\n/g, ' | ')) `

**2b Keyword Top search:** navigate `https://x.com/search?q=<urlencoded>&f=top`. Operators: `since:YYYY-MM-DD`, `until:`, `min_faves:N`, `min_retweets:N`, `lang:xx`, OR/parentheses. For "today/recent" asks default to `since:` = yesterday. Wait for `article[data-testid="tweet"]`, then evaluate:
```js
() => Array.from(document.querySelectorAll('article[data-testid="tweet"]')).slice(0, 10).map(a => {
  const g = s => { const e = a.querySelector(s); return e ? (e.getAttribute('datetime') || e.getAttribute('href') || e.innerText.replace(/\s+/g, ' ').slice(0, 160)) : null; };
  const labels = Array.from((a.querySelector('[role="group"]') || a).querySelectorAll('[aria-label]')).map(e => e.getAttribute('aria-label'));
  return { who: g('[data-testid="User-Name"]'), when: g('time'), text: g('[data-testid="tweetText"]'), stats: labels.slice(0, 5), url: g('a[href*="/status/"]') };
})
```
Stat aria-labels read: "N replies", "N reposts" (= RT + quotes), "N likes", "N views".

**2c Exact metrics for a known tweet:** open its status URL (same extraction), or API `GET /2/tweets/:id?tweet.fields=public_metrics` (per-ID metrics verified accurate vs web).

### Step 3: Fallback — API search (only if Step 2 unavailable / blocked / empty)
If `X_BEARER_TOKEN` is set:
```bash
cd <this skill dir> && python3 scripts/x_hots.py '["kw1", "kw2"]'
```
Label such results as API-fallback in the answer (partial-index caveat). 429 → wait 15 min or skip fallback. Token unset → report the browser failure; do not fabricate.

### Step 4: Analyze and present
Rank by engagement (likes + reposts + replies; views as tiebreak). Per topic give: 📌 Background (origin, timeline, key actors) · 💬 Popular opinions (supporters / opponents / neutral) · ⚔️ Key controversies (where stances diverge). Present as `## 🔥 [Domain] Hot Topics` with `### Topic N` blocks.

## Pitfalls (verified 2026-10-19)
- Web "reposts" = RT + QT; web "views" ≈ API `impression_count`.
- v1.1 `verify_credentials` is deprecated (404); check login state via Home title/timeline instead.
- Free-tier `search_recent`: partial index, relevancy-sorted, 7-day window, 10 req/15 min → returns low-engagement residue; cross-validated on France riots / stock market / AI.
- CF challenge: retry navigation several times before concluding "blocked".

## Error handling
- Not logged in → restore session, retry once.
- CF loop after 3 retries → Step 3.
- Both sources down → state it explicitly with reasons; never serve stale or API-only data as complete.
