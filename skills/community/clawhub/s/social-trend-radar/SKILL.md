---
name: social-trend-radar
description: Research public social-media and web trends, compare signals across platforms, summarize trend opportunities, and produce safe bilingual trend briefs without scraping private data or bypassing platform rules.
version: 0.1.0
homepage: https://clawhub.ai
metadata: {"openclaw":{"emoji":"📈","tags":["social-media","trends","research","marketing","content","arabic"],"requires":{"bins":["curl"]}}}
---

# Social Trend Radar

Use this skill when the user wants to discover, compare, or summarize current trends from public social platforms, news, search interest, creator communities, or niche web communities.

## Primary outcomes

Produce one of these outputs based on the user request:

1. **Trend brief** — short ranked list of current trends with evidence and recommended content angles.
2. **Platform comparison** — what is trending across TikTok, X/Twitter, Instagram, YouTube, Reddit, Google Trends, or public news.
3. **Content plan** — hooks, titles, hashtags, posting ideas, and risk notes.
4. **Arabic/English trend report** — bilingual summary for Arabic-speaking creators or brands.

## Safety and compliance rules

- Use only public pages, official APIs, RSS feeds, search results, or user-provided exports.
- Do not request or use passwords, cookies, session tokens, private API keys, or stolen data.
- Do not bypass logins, paywalls, rate limits, CAPTCHAs, robots.txt restrictions, or platform anti-scraping controls.
- Do not run obfuscated commands, downloaded scripts, cryptocurrency wallet tools, credential scanners, or browser-profile extractors.
- Never collect personal data about private individuals. Focus on aggregate trends, public creators, brands, topics, keywords, hashtags, and content formats.
- If a platform blocks automated access, stop and ask the user for an official export, API access, or public URL list.

## Recommended workflow

1. Clarify the target:
   - Platform(s): TikTok, X/Twitter, Instagram, YouTube, Reddit, Google Trends, news, forums, or all public web.
   - Market/language: global, US, GCC, Kuwait, Saudi, Arabic, English, gaming, AI, fashion, etc.
   - Time window: today, this week, last 30 days.
   - Goal: viral content, product ideas, game asset ideas, YouTube ideas, ad angles, or brand research.

2. Gather public signals:
   - Check official trending pages, platform search pages, public hashtags, RSS feeds, subreddit hot pages, news results, and Google Trends when available.
   - Save source URLs and timestamps.
   - Prefer multiple weak signals over one unsupported claim.

3. Score each trend from 1–5:
   - Velocity: is it rising now?
   - Relevance: does it fit the user’s niche?
   - Saturation: is there still room to post?
   - Monetization: can it create sales, leads, downloads, or views?
   - Risk: legal, brand safety, misinformation, privacy, or platform-policy concerns.

4. Produce the report:
   - Rank 5–10 trends.
   - Include evidence, why it matters, who should use it, content ideas, hashtags/search terms, and cautions.
   - Mark anything uncertain as uncertain.
   - Separate facts from recommendations.

## Output templates

### Quick trend brief

| Rank | Trend | Evidence | Score | Best angle | Risk |
|---:|---|---|---:|---|---|
| 1 |  |  | /5 |  |  |

After the table, add:
- **Top pick:**
- **Fast content idea:**
- **Best platform:**
- **What to avoid:**

### Full trend report

```markdown
# Trend Report: <niche/market/date>

## Executive summary
<3–5 bullets>

## Ranked trends
### 1. <trend name>
- Evidence:
- Why it is rising:
- Audience:
- Suggested content:
- Suggested hashtags/search terms:
- Monetization angle:
- Risk notes:
- Confidence: High / Medium / Low

## 7-day action plan
Day 1:
Day 2:
Day 3:
Day 4:
Day 5:
Day 6:
Day 7:

## Sources checked
- <source URL> — <timestamp>
```

### Bilingual Arabic/English mini brief

```markdown
# Trend Brief / تقرير الترندات

## English
<trend summary>

## العربية
<ملخص الترند>

## Content ideas / أفكار محتوى
1.
2.
3.

## Risk notes / ملاحظات المخاطر
-
```

## Example user prompts

- “Find trending game asset ideas for itch.io this week.”
- “Give me Arabic TikTok content trends for Kuwait restaurants.”
- “Compare what is trending in AI tools across YouTube, Reddit, and X.”
- “Make a 7-day content plan based on today’s gaming trends.”
- “Give me viral hooks for a dark fantasy pixel art asset pack.”
