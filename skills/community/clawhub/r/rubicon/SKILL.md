---
name: rubicon
description: >
  Rubicon Sentinel v2 is the no-cope geopolitical sovereignty scanner for OpenClaw.
  Inspired by Secretary Marco Rubio's Munich 2026 masterclass, it delivers real-time 8-pillar
  sovereignty scores (Economic Independence, Cultural Cohesion, Military Strength, Technological
  Sovereignty, Demographic Vitality, Energy Independence, Border Integrity, Civilizational Confidence),
  zero-chill sourced roasts, actionable Revival Playbook, trend tracking, and perfect Rubio red pills.
  Modes: Quick Scan, Deep Dive, 2030 Forecast, Roast Battle, Meme & Tweet Generator.
  Triggers: "Rubicon scan USA", "Rubicon roast EU migration", "Rubicon forecast 2030",
  "Rubicon alert Europe", "Rubicon meme", etc.
  Persistent memory + Grok Imagine-ready visuals. Built for users who want truth over comfort.
  v2 upgrades: 8-pillar index, smarter scoring rubric, expanded quotes library, visual radar matrix.
  Requires: web_search + web_fetch (image gen optional but 🔥).
  Crossed the Rubicon. No going back.

---

# Rubicon Sentinel v2 — Sovereign Forge

*The West doesn't need caretakers of its decline — it needs a forge. 8-pillar sovereignty analysis, 60+ smart queries, 40+ Rubio truth bombs. AI-powered geopolitical intelligence that hits hard and scores honest.*

No setup required. Just say **"Rubicon scan"** and it runs. Zero config. No excuses.

## Requirements
- `web_search` tool (any provider: Perplexity, Brave, etc.)
- `web_fetch` for Deep Scans only
- X/Twitter API (optional, for social sentiment — uses TWITTER_BEARER_TOKEN)
- Image generation (optional, for memes — text fallback if unavailable)

---

## 📡 Quick Scan (trigger: "Rubicon scan" or "Rubicon scan on [country]")

1. Read references/queries.md. Run 6–8 `web_search` calls from the **General / Quick Scan** section. If a specific country is given, substitute it; otherwise default to USA + EU overview.

2. Read references/scoring.md. Score each of the **8 pillars** (0–12.5 each):
   - **Economic Independence** — reshoring, supply chains, trade balance, foreign ownership
   - **Cultural Cohesion** — integration, identity, social trust, heritage education
   - **Military Strength** — spending, readiness, domestic production, alliance burden-sharing
   - **Technological Sovereignty** — chips, AI, 5G, export controls, full-stack capability
   - **Demographic Vitality** — fertility, aging, migration quality, family policy
   - **Energy Independence** — production mix, exports, grid reliability, strategic reserves
   - **Border Integrity** — enforcement, legal/illegal flows, policy effectiveness
   - **Civilizational Confidence** — national pride, heritage narrative, elite vs popular sentiment

3. Sum → **Sovereignty Score** (0–100):  🟢 80-100 Fortress | 🟡 50-79 Contested | 🔴 0-49 Crisis
   - Include trend arrows (↑/↓/→) per pillar when comparable data exists.

4. Read references/quotes.md. Pick a contextually relevant Rubio quote matching the strongest finding. Prefer Munich 2026 quotes for impact.

5. Reply with this format:

```
🏛️ RUBICON SENTINEL v2 — SOVEREIGNTY BRIEFING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 [Date] | [Country/Region] | Score: [N]/100 [emoji]

## Key Findings
- [Finding 1 — one line with source]
- [Finding 2]
- [Finding 3]
- [Finding 4]
- [Finding 5]

## 8-Pillar Breakdown
| Pillar | Score | Trend | Rationale |
|--------|-------|-------|-----------|
| Economic Independence | N/12.5 | ↑/↓/→ | ... |
| Cultural Cohesion | N/12.5 | | ... |
| Military Strength | N/12.5 | | ... |
| Technological Sovereignty | N/12.5 | | ... |
| Demographic Vitality | N/12.5 | | ... |
| Energy Independence | N/12.5 | | ... |
| Border Integrity | N/12.5 | | ... |
| Civilizational Confidence | N/12.5 | | ... |
| **TOTAL** | **N/100** | | **[emoji] [STATUS]** |

## Threat Assessment
[2-3 bullets on sovereignty risks — be specific]

## Opportunity Signals
[2-3 bullets on positive developments]

## Rubio's Word
> "[Quote]"
> — Secretary Marco Rubio

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🔬 Deep Scan (trigger: "deep Rubicon" or "deep Rubicon scan")

Same as Quick Scan, plus:
- Read references/queries.md. Use **pillar-specific** queries (1–2 per pillar) + regional alerts + forecast queries.
- `web_fetch` top 3–5 results for deeper analysis.
- If TWITTER_BEARER_TOKEN is available, run 2–3 X/Twitter queries from the queries.md X section.
- Add a **Forecast** section: 6-month and 2-year sovereignty trajectory.
- Add a **Sources** list at bottom with full URLs.

---

## 🎯 Topic Scan (trigger: "Rubicon scan on [topic]")

Replace default queries with topic-focused variants. Score only the relevant pillars (others marked N/A).
Example: "Rubicon scan on semiconductor supply chains" → queries about chip sovereignty, CHIPS Act, fab construction. Score Tech Sovereignty + Economic Independence.

---

## ⚔️ Battle Mode (trigger: "Rubicon battle [claim]")

Adversarial fact-check of a globalist or anti-sovereignty claim:
1. Use forecast/battle queries from queries.md: `"[claim] debunked OR data 2026"`
2. Find counter-evidence from 3+ sources.
3. Score the claim's validity (0–10) and deliver a Rubio-style rebuttal.
4. Format:

```
⚔️ RUBICON BATTLE MODE
━━━━━━━━━━━━━━━━━━━━━
Claim: "[the claim]"
Verdict: [🟢 TRUE / 🟡 HALF-TRUTH / 🔴 DEBUNKED]

Evidence:
- [Source 1]: [counter-point]
- [Source 2]: [counter-point]
- [Source 3]: [counter-point]

Rubio's Response:
> "[relevant quote]"
```

---

## 🌍 Country Comparison (trigger: "Rubicon compare [country A] vs [country B]")

Run parallel Quick Scans on both countries. Output side-by-side 8-pillar comparison table. Highlight where each leads and the biggest gaps.

---

## 🎨 Sovereignty Meme (trigger: "Rubicon meme")

1. If no recent scan context, run a Quick Scan first.
2. Pick the most dramatic or ironic finding.
3. Generate the meme:
   - Image prompt: `"Political meme, bold Impact font. Top: [setup]. Bottom: [punchline]. Background: [relevant imagery — eagles, factories, flags]. Style: classic internet meme, high contrast"`
   - If image generation unavailable, output as text with setup/punchline.
4. Tone: sharp, witty, pro-Western. Edgy but not offensive.

---

## 🐦 Tweet Draft (trigger: "Rubicon tweet")

Compose a tweetable summary (≤280 chars) from the latest scan:
1. If no recent scan context, run a Quick Scan first.
2. Include: Sovereignty score + emoji, one key finding, Rubio quote snippet.
3. Hashtags: #Rubicon #WesternSovereignty + 1-2 topical tags.

---

## 💬 Rubio Quote (trigger: "Rubicon quote" or "Rubio quote")

Quick-fire — no scan needed:
1. Read references/quotes.md.
2. Pick a quote matching the conversation context (or random if no context).
3. Reply:
```
🏛️ > "[Quote]"
   > — Secretary Marco Rubio
```

---

## 🚨 Rubicon Alert (trigger: "Rubicon alert")

Fast threat check:
1. Single `web_search`: `"Western sovereignty threat crisis [current month year]"`
2. Quick assessment — active crisis?
3. Reply:
```
🚨 RUBICON ALERT: [🟢 ALL CLEAR / 🟡 WATCH / 🔴 THREAT DETECTED]
[One sentence summary]
[Relevant pillar(s) affected]
```

---

## 📊 Rubicon Forecast (trigger: "Rubicon forecast [country] [year]")

Forward-looking sovereignty projection:
1. Run Deep Scan on the country.
2. Use forecast queries from queries.md.
3. Project each pillar's trajectory to target year.
4. Output forecast table with current → projected scores and key drivers.

---

## Error Handling
- If `web_search` fails: note "source unavailable", score that pillar conservatively (middle of range).
- If score is exactly 50: classify as 🟡 Contested.
- Always produce output even with partial data — state confidence level.
- If image generation unavailable for memes: fall back to text format.
- If X/Twitter API unavailable: skip social sentiment, note in output.

## References
- **references/scoring.md** — 8-pillar scoring rubric with examples and ranges
- **references/queries.md** — 60+ smart query templates by pillar, mode, and platform
- **references/quotes.md** — 40+ curated Rubio quotes by theme (sovereignty, alliances, military, civilization)
