---
name: viral-content-research
description: Research what content is actually going viral in a niche, topic or competitor set, and turn it into evidence-backed patterns (hooks, titles, formats, angles) plus ready-to-use content ideas. Uses the YouTube Data API through a bundled script for verified numbers, and WebSearch/WebFetch for Reddit, X, news and other web signals. Use this skill whenever the user asks what is trending or viral, what is working in a niche, which videos are outperforming, for content/video/Shorts/Reels/TikTok ideas backed by data, for hook or title research, or for competitor content analysis, even if they never say "viral research" (for example "what is going viral", "what is working in my niche", "give me video ideas that will actually perform").
---

# Viral Content Research

Goal: find what is **outperforming its own baseline** in a niche right now, explain **why**, and turn that into specific content the user can make. Raw view counts mislead (a huge channel gets big views on any upload), so everything below is built around *relative* performance, with evidence the user can click and check.

## Inputs

Needed: niche or topic, platform(s) (default: YouTube + web), audience region/language, time window (default 30 days, use 90 for evergreen niches), and the goal (ideas, hooks, competitor analysis). If something is missing, pick a sensible default, state it in one line at the top of the report, and proceed. Ask only when the niche itself is unknown.

## Two research lanes

**Lane A: YouTube, verified numbers.** Use `scripts/yt_research.py` (stdlib only, needs `YOUTUBE_API_KEY`).

```bash
python scripts/yt_research.py search -q "query one" -q "query two" --days 30 --region PK --lang en --max 30 --out research/yt
python scripts/yt_research.py trending --region PK --category 28
python scripts/yt_research.py stats <url-or-id> <url-or-id>
python scripts/yt_research.py comments <url-or-id> --max 50
```

Each `search` query costs 100 quota units of the free 10,000/day, everything else about 1 unit, and the script prints what it used. So plan 4 to 8 well-chosen queries instead of 30 sloppy ones. Run `python scripts/yt_research.py --help` for all flags (`--order date` is useful as a control group, see the analysis reference).

**Lane B: the wider web.** Use WebSearch and WebFetch for Reddit threads, X posts, news, newsletters and other platforms, where the API gives nothing. Read `references/web-research.md` before starting this lane; it covers query patterns and how to label confidence, because TikTok and Instagram numbers are rarely verifiable.

Run both lanes in parallel when subagents are available (one per lane or platform). Otherwise plan the queries first, then run them back to back.

## The metric: what counts as "viral"

The script gives every video these fields:

- `outlier_x`: views divided by the median views of that channel's recent uploads, with the median floored at `--min-baseline` (default 1,000) so tiny channels do not produce 40,000x "outliers". This is the main signal. 3x is notable, 5x or more is a real outlier. Rows marked `*` (`baseline_floored`) come from small channels: treat them as weaker evidence.
- `views_per_day`: velocity. Separates rising topics from old hits that merely accumulated views.
- `views_per_sub`: a cheap fallback when baseline data is missing.
- `like_rate_pct`, `comment_rate_pct`: depth of reaction, useful as a tiebreaker.

State which definition you used in the report. Never call something "viral" on absolute views alone.

## Workflow

1. **Plan queries.** Mix the core topic, problem-phrased searches ("how to ..."), format-phrased searches ("... in 60 seconds", "... vs ..."), beginner vs advanced, and a local-language variant if the audience is not English-speaking.
2. **Collect** with both lanes. Save raw output (JSON/CSV) so the user can inspect it.
3. **Shortlist.** Keep outliers (`outlier_x` of 3 or more, or very high `views_per_day`). Drop what the user cannot replicate: news spikes, celebrity or music uploads, giveaways, one-off events. Note when you drop something and why.
4. **Dissect the top 10 to 15.** Follow `references/analysis-framework.md`: title formula, hook type, format and length, angle, emotional driver. Do this from the data you have (title, duration, tags, description, comments), and say plainly when you could not see something such as a thumbnail or the first seconds of the video.
5. **Mine audience language.** Pull comments for the top 3 to 5 videos. Note recurring questions, objections and phrases; they are the best source of hooks that speak the audience's own words.
6. **Check timing.** Many outliers on the same angle in the last two weeks means saturated. A few, from small channels, with high velocity, means rising. Say which.
7. **Synthesize.** Turn patterns into ideas. Each idea needs a hook, an angle, a format, linked evidence, and why it fits this user. Ideas must be transformations of a pattern, not clones of a specific video.
8. **Deliver** using `references/report-template.md`: a short report plus the raw CSV. If the session offers a document artifact type, put the report there; otherwise write a markdown file.

## Honesty rules (why the report is trustworthy)

- Every pattern cites at least 3 videos from at least 3 different channels, and says "k of n top videos". One channel repeating itself is a habit, not a pattern.
- Label numbers: **verified** (API, with pull date), **page-visible** (fetched page with figure and date), **unverified** (snippet or secondhand). Do not mix them in one table without the label.
- Never invent a metric. If a field is missing (hidden likes, hidden subscribers), leave it blank.
- Paraphrase source text; keep any quote under 15 words. The goal is insight, not a copy of someone else's script.
- Report the method (queries, window, region, date pulled) so the research can be repeated.

## If something fails

- **No API key.** Tell the user how to get one: Google Cloud Console, create a project, enable "YouTube Data API v3", create an API key (free). Meanwhile continue with Lane B alone and label the report as unverified. If the user pastes a key, pass it inline for that command (`YOUTUBE_API_KEY=... python ...`); never write it into a file, the report or memory.
- **Network blocked or proxy error** from the script: say so in one line, continue with Lane B, and offer to give the user the exact command to run on their own machine.
- **Quota exceeded:** report what was collected, state that coverage is partial, and suggest resuming after the daily reset.
- **Thin results:** widen the window, relax region or language, or use broader queries before concluding there is nothing.

## References

- `references/analysis-framework.md`: hook taxonomy, title formulas, validation rules, control-group check, saturation test.
- `references/web-research.md`: Lane B query patterns, source confidence labels, platform limits.
- `references/report-template.md`: the report structure and length guidance.
