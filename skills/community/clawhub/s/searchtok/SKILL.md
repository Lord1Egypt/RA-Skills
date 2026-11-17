---
name: searchtok
description: Research TikTok and Instagram Reels with searchtok. It finds outliers (posts that beat their own account's usual views), the hooks and formats behind them, the creators in a niche and what competitors post, every number worked out from real posts. Use when someone asks what's working, trending or blowing up on TikTok or Reels for a niche, app, brand or creator; wants hooks, formats, content ideas or a script structure from real posts; wants a brand or competitor broken down; wants creators in a niche or posts like one; or wants accounts or a niche checked on a schedule. Works through the searchtok MCP server or the searchtok CLI.
compatibility: Needs a searchtok plan (https://searchtok.app) and either the searchtok MCP server (https://searchtok.app/mcp) or the searchtok CLI (Node 18.18+, network access).
metadata:
  openclaw:
    homepage: https://searchtok.app
    envVars:
      - name: SEARCHTOK_API_KEY
        required: false
        description: searchtok API key for the CLI. Not needed with the MCP server or after npx searchtok auth:login.
---

# searchtok

searchtok finds the TikToks and Instagram Reels that are working in a niche: outliers (posts that got far more views than their account usually gets), their hooks and formats, and the creators behind them. Every number (views, outlier scores, usual views) is worked out by searchtok from real posts, never by a model. searchtok only sees public stats of organic posts: no sales, leads, watch time, private analytics or ads.

## Setup check (do this first)

1. **MCP.** If you have searchtok's tools (`search_content`, `get_account`... sometimes with a prefix, like `mcp__searchtok__search_content`), use them and skip the CLI.
2. **CLI.** Otherwise run `npx searchtok auth:status`. If it says `"signed_in": true`, use the CLI. If not, ask the user to run `npx searchtok auth:login` (it opens their browser), or to set `SEARCHTOK_API_KEY` to a key from https://searchtok.app/app/settings/keys. Never ask them to paste a key into the chat.
3. **Neither.** Tell the user how to connect, then stop:
   - Claude Code: `claude mcp add --transport http searchtok https://searchtok.app/mcp --header "Authorization: Bearer st_live_..."` with a key from https://searchtok.app/app/settings/keys, or leave out the header and sign in from `/mcp`.
   - Claude.ai or ChatGPT: add a custom connector with the URL `https://searchtok.app/mcp` and sign in.
   - Any other agent: the MCP URL with an `Authorization: Bearer st_live_...` header, or the CLI.
4. **Credits.** `get_usage` (CLI: `npx searchtok usage`) is free: check it before a long run. If a tool says `no_plan` or `no_credits` (CLI exit code 4), tell the user and give them its link. Don't retry.

## Tools

The MCP tools and the CLI commands are the same tools with the same credits. CLI commands print the tool's JSON on stdout (errors as JSON on stderr with a non-zero exit code); add `--help` to any command for its flags. Exit code 3 means not signed in.

| MCP tool | CLI | Credits | What it does |
|---|---|---|---|
| `search_content` | `npx searchtok search "<query>" [--platform tiktok,instagram] [--timeframe 30d] [--limit 20]` | 20 | Find the TikToks and Instagram Reels that did best for a topic or niche, ranked by outlier score (a post's views ÷ its account's usual views). |
| `find_accounts` | `npx searchtok accounts "<niche>" [--platform tiktok\|instagram]` | 15 | Find TikTok or Instagram creators and brands in a niche, with how well their posts do: followers, usual (median) views and outlier rate (how often a post gets 3x+ their usual views). |
| `get_account` | `npx searchtok account <@handle\|url> [--platform tiktok\|instagram]` | 3 | Look up one TikTok or Instagram account: profile, its usual (median) views, outlier rate, posting rate, format mix and its best recent posts by outlier score. |
| `analyze_brand` | `npx searchtok brand <url\|@handle\|name> [--compare <url\|@handle\|name> ...] [--platform tiktok\|instagram]` | 5 per brand (the brand plus each one compared) | Analyse a brand's or creator's organic TikTok and Instagram from its website, handle or name, optionally side by side with up to 3 others (compare). |
| `analyze_post` | `npx searchtok post <url\|id>` | 6 | Everything about one TikTok or Instagram post, by url or searchtok id. |
| `find_similar` | `npx searchtok similar <url\|id> [--limit 10]` | 12 | Find posts like a given TikTok or Instagram post (same topic or format), ranked by outlier score. |
| `build_profile` | `npx searchtok profile build <link\|@handle\|sentence>` | 10 | Turn one link into the user's searchtok profile: an App Store or Play link, a website, a TikTok or Instagram handle, or a sentence about the business. |
| `get_profile` | `npx searchtok profile` | free | The user's saved searchtok profile(s): what they make content for (an app, a business, a creator...), their niche, audience and language. |
| `get_usage` | `npx searchtok usage` | free | The user's searchtok plan, credits left, when they reset, and what each tool costs. |
| `research` | `npx searchtok research "<question>" [--deep] [--wait]` | 50 quick, 150 deep | Hand a whole question to searchtok's own research agent, which runs many searches and writes a checked report, every claim citing real posts. |
| `get_research` | `npx searchtok research:get <search_id> [--wait]` | free | Fetch a research run's answer by its search_id: a deep run that research started in the background, or any earlier run. |
| `content_ideas` | `npx searchtok ideas [--count 5] [--focus "<theme>"] [--profile <profile_id>]` | 150 | Content ideas for the user's profile, each built on a top video in their niche plus 2 more posts in the same format, all at 2x+ their account's usual views, with hooks quoted word for word and the beats to film. |

## How to work

- Do the thinking yourself with the fast tools, one step at a time: search_content for a niche or topic, find_accounts for creators, get_account for a known account, analyze_post for why one post worked (transcript, on-screen text, hooks), find_similar for more posts like one. Each takes about 10 to 20 seconds; call independent ones at the same time.
- When the question is about the user ('what should I post', 'for my app'), call get_profile first and search in their niche's words and language.
- research hands a whole question to searchtok's own agent. Use it only when the user asks for a full report. depth deep runs in the background: share its link, and fetch the answer later with get_research.
- With the CLI, run independent commands at the same time, and pass a row's `id` or `url` straight to `npx searchtok post` or `npx searchtok similar`.

## Evidence rules

Every answer follows these, whichever playbook you use.

- Lead with the top videos for the niche or term. For each: its link, views and outlier score, then 3 or 4 short bullets on why it worked: what's seen, said and on screen in the first seconds (visual hooks count). Call analyze_post on the top 3 to 5 to get these.
- Add a shared pattern only when 3 or more of the top videos show it.
- Only show videos that did well. Never show low-view videos or explain why something didn't work.
- Leave out ads and paid promotions.
- Default to the US and Europe. Use another market only when the user names it (search_content's region and language).
- Outlier score = the post's views divided by its account's usual (median) views. Always show it with its outlier_explained line, e.g. "41x this account's usual views (median 2.1k over its last 20 posts)".
- Quote hooks exactly as the tools return them, in quotes. Never write, translate or tidy a hook yourself.
- Link every post you mention (its url), and give the result's dashboard link so the user can open, save and share it.
- Results show credits_used and credits_left. If a tool says no_plan or no_credits, tell the user and give them its link.
- Say what you searched: the queries, platforms and timeframe (`search_content` lists them in `searched`), and which accounts you looked at.
- Quote each hook whole, as one quote: never shorten it, join two together or fix its spelling.
- Only use numbers and quotes searchtok returned. Never estimate views, scores or hooks. If a hook couldn't be read, say so.

## Playbooks

Pick the playbook that fits the question and read it before your first search. Each one is searchtok's own way of answering that kind of question: the steps, which tools to call, what a great answer looks like and what to avoid. When none fits a niche question, use whats-working.

| Playbook | Read it when |
|---|---|
| [format-library](references/format-library.md) | someone asks which formats work in their niche, how a named format (day in the life, text on screen demo, before and after) performs, or what format to film instead of their current one. Also the reference for naming any format. |
| [hook-patterns](references/hook-patterns.md) | someone asks what hooks work in their niche, for hook ideas, or how the best posts open. The answer shows the hooks of the top videos, word for word, and what's seen in their first seconds. |
| [whats-working](references/whats-working.md) | someone asks what's working, blowing up or trending in their niche right now, or wants the niche's best posts to copy. The default when no other skill fits a niche question. |
| [content-ideas](references/content-ideas.md) | someone asks what to post, for content ideas, or for "<niche> content ideas". The answer is real posts to copy from their niche, not advice. |
| [brand-analysis](references/brand-analysis.md) | someone names a brand, creator or competitor and asks what they post, what works for them or what changed, or wants up to 3 compared. |
| [script-writing](references/script-writing.md) | someone wants a script, a script structure or a story structure to film. The answer shows which structures the niche's outlier posts follow and how to fill one with their own material. |
| [build-profile](references/build-profile.md) | someone asks who an account or business is and what its niche is, wants their own profile or positioning mapped, or asks who their competitors are and where the open space is. |

## Monitoring on a schedule

searchtok doesn't send alerts. If your agent can run prompts on a schedule, these recipes do the watching. Each is a copy-paste prompt plus how to schedule it in OpenClaw, Claude Code and ChatGPT.

- [competitor watch](recipes/competitor-watch.md): Every Monday at 9am, check up to 5 competitor accounts and report their new posts that got 3x or more their usual views, with each hook quoted exactly.
- [niche watch](recipes/niche-watch.md): Every Monday at 9am, find the posts from the last 7 days that beat their account's usual views in your niche, with why each one worked.
