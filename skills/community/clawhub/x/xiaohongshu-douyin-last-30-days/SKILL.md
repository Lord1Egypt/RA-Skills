---
name: xiaohongshu-douyin-last-30-days
description: "近30天小红书 / 抖音在说什么 (Last 30 days on Xiaohongshu & Douyin). 给一个话题、产品、品牌或人名，搜小红书和抖音最近 30 天（可调）发的帖子，读出每条里说的话（视频口播、图上的字）和点赞、评论、收藏数，按互动排序，交给 agent 写一份带出处的简报：大家在说什么、谁说的、哪天、多少人赞。用于做选题、看产品口碑、会前查一个话题。英文社区（Reddit、X、YouTube）有开源技能 last30days 在做；这个只做小红书和抖音。搜索找到的是网页已收录的帖子，通常只有几条，不是全量。不登录平台、不要 Cookie。需要 LinkDigest API Key（注册送 10 积分）。"
version: 1.0.0
homepage: https://linkdigest.dev/zh/docs?ref=skill-xiaohongshu-douyin-last-30-days
metadata: {"openclaw":{"requires":{"anyBins":["python3"]},"primaryEnv":"LINKDIGEST_API_KEY","envVars":[{"name":"LINKDIGEST_API_KEY","required":true,"description":"LinkDigest API Key（ld_live_ 开头），在 https://linkdigest.dev/signin?ref=skill-xiaohongshu-douyin-last-30-days&next=/app/keys 创建，注册送 10 积分"}],"homepage":"https://linkdigest.dev/zh/docs?ref=skill-xiaohongshu-douyin-last-30-days"}}
required_environment_variables:
  - name: LINKDIGEST_API_KEY
    prompt: "LinkDigest API key (starts with ld_live_)"
    help: "https://linkdigest.dev/signin?ref=skill-xiaohongshu-douyin-last-30-days&next=/app/keys"
    required_for: "searching Xiaohongshu and Douyin and reading the posts; sign-up gives 10 free credits, no card"
---
# 近 30 天，小红书和抖音在说什么 (the last 30 days on Xiaohongshu and Douyin)

For English-language communities there are skills that gather a month of discussion from Reddit, X and YouTube. Chinese discussion mostly happens on two apps a server cannot simply open: a Xiaohongshu note is images with the text drawn on them, a Douyin video has no captions. This skill finds the recent posts on a topic, reads what each one says, and hands the agent an evidence pack to write from.

## One command

```bash
export LINKDIGEST_API_KEY=ld_live_...   # https://linkdigest.dev/signin?ref=skill-xiaohongshu-douyin-last-30-days&next=/app/keys
python3 {baseDir}/scripts/last30.py "Claude Code"
```

| Option | Does |
| --- | --- |
| `--days 14` | The window, 1 to 365 days. Default 30. |
| `--read 4` | How many of the newest posts to read. Default 6. `0` lists what was found and reads nothing. |
| `--platforms douyin` | One platform. Default is both, `xiaohongshu,douyin`. |
| `--max-credits 6` | The most one read may cost; a dearer post is skipped and not charged. Default 8. |
| `--format json` | The pack as data. |

Each post's date comes from its own id, so the window is exact. Posts are read newest first, taking turns between the two platforms. Douyin videos are read for speech only (the cheapest read).

## What comes back

A Markdown pack, most-engaged first (likes + 2 × comments + saves + shares):

- a header that says how many posts each search found and how many fell inside the window;
- per post: title, author, date, the like / comment / save / share counts, the link, up to four key points, and two or three lines quoted from the speech (with `[mm:ss]`) or from the images;
- the posts that could not be read, each with the reason;
- the links that were found but not read.

## Writing the brief (for the agent)

1. Start with the numbers from the header: which platforms were searched, how many posts were inside the window, how many were read. Three posts are three posts. Never present them as "the internet" or "everyone".
2. Group what the posts say into themes. Every claim names the post it comes from by number, with its date and its like count, and quotes a line when one is there.
3. Order themes by engagement, and say when one post dominates (a note with ten thousand likes next to two with a few hundred).
4. Name what is missing: a platform that returned nothing, posts outside the window, a side of the topic nobody covered.
5. Offer the next step: a wider window (`--days 90`), a more specific wording, or reading the remaining links.
6. Say what the run cost (the header has the credits).

Do not add what the posts did not say, and do not fill a thin result with general knowledge. A short honest brief is the right answer to a thin search.

## What to expect, measured

Run on 2026-11-26 for "Claude Code", 30 days: Xiaohongshu search found 7 posts, 3 inside the window; Douyin found 1, 0 inside. The 3 were read in about two and a half minutes for 17 credits in all. The most-engaged had 10,400 likes, 535 comments and 16,900 saves.

That is typical. The search goes through what the open web has indexed, so it returns a handful of posts, the newest ones can be days late, and a narrow topic can return none. This skill is a way to read the best of what is findable, not a census.

## Price

A search that finds posts is 4 credits per platform; one that finds nothing is free. Each read is priced like any other: an image note from 1 credit, a video 1 credit plus 1 per started minute (speech only on Douyin: 1 per started 2 minutes). A post someone already read is 0. Sign-up gives 10 credits once; top-ups are one-time and never expire: 50 credits ¥9.9 (支付宝) / $1.50, 250 credits ¥36 / $5.

## Limits

- Xiaohongshu and Douyin only. No Bilibili or Weibo search.
- Notes Xiaohongshu shows only inside its app, deleted posts and private posts cannot be read; they are listed under 没读成的 and cost nothing.
- Counts are as of the read. Speech recognition can misspell names and numbers: check them before quoting.
- No account, cookie or login is used, and nothing is posted or downloaded.

## Privacy

Only the topic and the links go to linkdigest.dev. https://linkdigest.dev/privacy · Remote MCP: `https://linkdigest.dev/mcp` (`search_links`, `digest_url`) · support@linkdigest.dev
