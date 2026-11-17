---
name: social-media-scraper
description: Scrape public social media data through ToolRouter's MCP server - profiles, posts, videos, comments, search and trends from TikTok, Instagram, YouTube, X/Twitter, Facebook, LinkedIn, Reddit, Threads, Bluesky, Pinterest, Twitch and more. Use when the user wants follower counts, a creator's recent posts, video metrics, comments, hashtag or keyword search, or competitor social monitoring.
metadata: {"homepage":"https://toolrouter.com/tools/social-media-content","openclaw":{"emoji":"📱","requires":{"bins":[],"env":[]}}}
---

# Social Media Scraper

Pull structured public data from social platforms with one MCP connection: no scraper to host, no proxy pool, no per-platform API keys. Every call returns JSON with handles, captions, dates, media URLs and engagement counts.

## Installation

Install with `pnpm dlx skills add Humanleap/agent-skills --skill social-media-scraper`. Connect the client's remote MCP server to `https://api.toolrouter.com/mcp` (Claude: Customize → Connectors → Add custom connector; Claude Code: `claude mcp add toolrouter -- npx -y toolrouter-mcp`). Setup: https://toolrouter.com/docs/markdown/quickstart.

## Hard Rules

1. **Public data only.** These operations read public profiles, posts and ads. Never try to reach private accounts, DMs or logged-in-only content.
2. **Use the exact operation.** Pick the `tool` and `skill` below, or call `discover` with the job. Never invent an input field.
3. **Scope before you pull.** Each call is billed. Fetch one profile or one feed, check it answers the question, then widen.
4. **Report what the data says.** Quote counts and dates from the response. An empty result is a coverage limit, not proof an account or post does not exist.

## Authentication and Cost

The server provisions an anonymous account on first use. Paid calls need credits: if `use_tool` returns a claim link, give it to the user so they can sign in and add credits. Most social calls cost $0.005; `discover` shows the live price for each operation.

## Core Workflow

1. **Identify the target.** A handle (`duolingo`), a post URL, or a search query.
2. **Profile first.** `social-profiles` gives followers, post count and bio for one cheap call.
3. **Then content.** `social-media-content` returns the latest posts or videos with per-post metrics.
4. **Then conversation.** `social-reader` reads comments, searches posts and lists trending topics.
5. **Summarise.** Return a table (date, caption, views, likes, comments, URL) and the takeaway the user asked for.

## Essential Operations

| Job | `tool` | `skill` | Input |
|---|---|---|---|
| TikTok profile and follower count | `social-profiles` | `get_tiktok_profile` | `{"handle":"duolingo"}` |
| Instagram profile | `social-profiles` | `get_instagram_profile` | `{"handle":"nike"}` |
| YouTube channel stats | `social-profiles` | `get_youtube_channel` | `{"handle":"mkbhd"}` |
| X/Twitter profile | `social-profiles` | `get_twitter_profile` | `{"handle":"openai"}` |
| LinkedIn company page | `social-profiles` | `get_linkedin_company` | `{"url":"https://www.linkedin.com/company/notionhq"}` |
| Subreddit stats | `social-profiles` | `get_reddit_subreddit` | `{"subreddit":"SaaS"}` |
| Latest TikTok videos | `social-media-content` | `get_tiktok_videos` | `{"handle":"duolingo"}` |
| One TikTok video | `social-media-content` | `get_tiktok_video` | `{"url":"https://www.tiktok.com/@user/video/123"}` |
| Instagram posts or reels | `social-media-content` | `get_instagram_posts` / `get_instagram_reels` | `{"handle":"nike"}` |
| YouTube videos or shorts | `social-media-content` | `get_youtube_videos` / `get_youtube_shorts` | `{"handle":"mkbhd"}` |
| Tweets from an account | `social-media-content` | `get_twitter_tweets` | `{"handle":"openai"}` |
| LinkedIn company posts | `social-media-content` | `get_linkedin_company_posts` | `{"url":"https://www.linkedin.com/company/notionhq"}` |
| Facebook page posts | `social-media-content` | `get_facebook_posts` | `{"url":"https://www.facebook.com/NotionHQ"}` |
| Pinterest pin or board | `social-media-content` | `get_pinterest_pin` / `get_pinterest_board` | `{"url":"https://www.pinterest.com/pin/123"}` |
| Comments (TikTok, YouTube, Instagram, Facebook, Reddit, X, Threads) | `social-reader` | `read_comments` | `{"url":"<post url>"}` |
| TikTok keyword search | `social-media-search` | `search_tiktok_keywords` | `{"query":"protein snacks"}` |
| TikTok hashtag | `social-media-search` | `search_tiktok_hashtags` | `{"hashtag":"booktok"}` |
| Reddit search | `social-media-search` | `search_reddit` | `{"query":"best crm for startups"}` |
| Inside one subreddit | `social-media-search` | `search_reddit_subreddit` | `{"subreddit":"SaaS","query":"pricing","sort":"top","timeframe":"month"}` |
| Instagram reels search | `social-media-search` | `search_instagram_reels` | `{"query":"pilates"}` |
| YouTube search | `social-media-search` | `search_youtube` | `{"query":"notion tutorial"}` |
| Trending on TikTok or YouTube Shorts | `social-reader` | `get_trending` | `{"platform":"tiktok","trending_type":"hashtags","country":"GB","period":"7"}` |

Call these through `use_tool` with `tool`, `skill` and `input`. Run `discover` with a query such as "tiktok followers" to see the full list, including Threads, Bluesky, Twitch, Kick, Snapchat and Truth Social.

## Common Patterns

- **Creator vetting:** profile → latest videos → median views over the last 10 posts → engagement rate (likes + comments ÷ views). Flag accounts whose views swing wildly between posts.
- **Competitor content audit:** latest posts for 3 to 5 competitor handles on one platform, then group by format and hook, and rank by views.
- **Audience research:** `search_reddit` or `search_reddit_subreddit` for the pain point, then `read_comments` on the top threads; quote real phrasing.
- **Trend spotting:** `search_tiktok_hashtags` or `search_tiktok_keywords`, sorted by recency and views, then pull the top videos with `get_tiktok_video`.
- **Ad + organic picture:** pair this skill with `ad-library-scraper` to see what a brand pays to promote next to what it posts.

## Gotchas

- Feed calls return a page of recent items (TikTok returns about 10 videos). Responses can be large: ask for one handle at a time and summarise before pulling more.
- Handles go without `@`. Facebook, LinkedIn and Pinterest operations take full URLs, not handles.
- Counts are live at call time; say when you pulled them.
- Private, deleted or region-locked content returns empty or an error. Report it; do not retry the same input in a loop.

## Quick Reference

**Connect → handle or URL → profile → posts → comments/search → table with dates and metrics.**

More: https://toolrouter.com/tools/social-media-content · https://toolrouter.com/tools/social-profiles · https://toolrouter.com/tools/social-media-search
