# competitor watch

Every Monday at 9am, check up to 5 competitor accounts and report their new posts that got 3x or more their usual views, with each hook quoted exactly.

**Costs** about 3 credits per account (15 a week for 5), plus 6 for each new outlier it reads. `get_account` looks at each account's best recent posts, so a new post shows up once it's among them.

## The prompt

Replace the brackets with the accounts (`@handle` for TikTok, or a profile link for Instagram), then copy it.

```text
Use searchtok (its MCP tools, or the searchtok CLI if that's what you have) to check these accounts: [@COMPETITOR_1], [@COMPETITOR_2], [@COMPETITOR_3], [@COMPETITOR_4], [@COMPETITOR_5].

1. For each account, call get_account (CLI: npx searchtok account <@handle|url> [--platform tiktok|instagram]).
2. From its top_outliers, keep only posts from the last 7 days with an outlier_score of 3 or more.
3. For each post you keep, call analyze_post (CLI: npx searchtok post <url>) to read its hooks.

Report by account, newest post first. For each post: its link, views, outlier score with its outlier_explained line, the hook quoted exactly as searchtok returned it, and one line on why it worked from what's seen, said and on screen. If an account has nothing new at 3x or more, say so in one line. Don't pad with weaker posts and don't explain why other posts did badly. End with each account's searchtok link and the credits used.
```

## Schedule it

**OpenClaw.** With this skill installed, from a terminal:

```bash
openclaw cron create "0 9 * * 1" "Run the searchtok competitor watch recipe (recipes/competitor-watch.md in the searchtok skill) for [@COMPETITOR_1], [@COMPETITOR_2], [@COMPETITOR_3], [@COMPETITOR_4], [@COMPETITOR_5] and send me the report." --name "searchtok competitor watch" --session isolated --announce
```

Or tell your OpenClaw agent: "every Monday at 9am, run this:" followed by the prompt.

**Claude Code.** For a weekly check that runs without your laptop, type `/schedule`, ask for every Monday at 9am, and paste the prompt. The scheduled run needs searchtok connected as a connector. To check daily while you work (it stops when the session closes, or after 7 days):

```text
/loop 1d Run the searchtok competitor watch recipe for [@COMPETITOR_1], [@COMPETITOR_2], [@COMPETITOR_3], [@COMPETITOR_4], [@COMPETITOR_5], looking at the last day instead of the last 7.
```

**ChatGPT.** In a chat with searchtok connected, send "Every Monday at 9am:" followed by the prompt. ChatGPT turns it into a scheduled task. Check that the first run called searchtok's tools. If it answered without them, scheduled tasks on your ChatGPT plan may not be able to use connectors.
