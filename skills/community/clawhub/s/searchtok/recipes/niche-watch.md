# niche watch

Every Monday at 9am, find the posts from the last 7 days that beat their account's usual views in your niche, with why each one worked.

**Costs** about 20 credits for the search, plus 6 for each top post it reads (up to 5).

## The prompt

Replace the bracket with your niche, in the words people would search on TikTok ("dentist", "habit tracker app", "dog grooming"), then copy it.

```text
Use searchtok (its MCP tools, or the searchtok CLI if that's what you have) to see what's working in [YOUR NICHE] this week.

1. Call search_content with the query "[YOUR NICHE]" and timeframe 7d (CLI: npx searchtok search "[YOUR NICHE]" --timeframe 7d).
2. Keep the niche's own posts, not ads and not advice videos about the niche. Pick the 3 to 5 with the highest outlier score, only as many as are strong.
3. Call analyze_post on each (CLI: npx searchtok post <url>).

For each post: its link, views, outlier score with its outlier_explained line, the hook quoted exactly as searchtok returned it, and 3 or 4 short bullets on why it worked from what's seen, said and on screen. Add one line on a shared pattern only if 3 or more of them show it. Say what was searched (the searched list) and give the search's searchtok link. If nothing beat its account's usual views this week, say so.
```

## Schedule it

**OpenClaw.** With this skill installed, from a terminal:

```bash
openclaw cron create "0 9 * * 1" "Run the searchtok niche watch recipe (recipes/niche-watch.md in the searchtok skill) for [YOUR NICHE] and send me the report." --name "searchtok niche watch" --session isolated --announce
```

Or tell your OpenClaw agent: "every Monday at 9am, run this:" followed by the prompt.

**Claude Code.** For a weekly check that runs without your laptop, type `/schedule`, ask for every Monday at 9am, and paste the prompt. The scheduled run needs searchtok connected as a connector. To check daily while you work (it stops when the session closes, or after 7 days):

```text
/loop 1d Run the searchtok niche watch recipe for [YOUR NICHE].
```

**ChatGPT.** In a chat with searchtok connected, send "Every Monday at 9am:" followed by the prompt. ChatGPT turns it into a scheduled task. Check that the first run called searchtok's tools. If it answered without them, scheduled tasks on your ChatGPT plan may not be able to use connectors.
