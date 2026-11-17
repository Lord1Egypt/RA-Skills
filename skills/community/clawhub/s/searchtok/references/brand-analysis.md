# brand-analysis

Use when someone names a brand, creator or competitor and asks what they post, what works for them or what changed, or wants up to 3 compared.

## Goal

Break down what one brand or creator (or up to three side by side) posts, which posts beat their own usual views and why, and what changed, so the user can copy the right things.

## Steps

1. Look at the brand's own account first and rank its posts by outlier score against its own usual views.
2. Pick a window before reading. For a competitor, use one long enough to show a pattern.
3. Break the posts down by topic, hook and format, and report which show up most among the best posts. Look for the non-obvious patterns the winners share, not only the topic.
4. Judge how broad each post's topic is against the brand's core audience, and use views and outlier score to see which breadth does best. Don't assume narrower means fewer views.
5. Name the patterns the brand could double down on.
6. Say how the brand's posts spread across breadth levels. One source suggests 3 at the core, 2 in the middle and 2 broader, none at the broadest: a starting point only, every niche differs.
7. Lead with the 3 to 5 top videos for the niche or term, as many as are strong (never pad with weak ones), each with 3 or 4 points on why it worked, from what is seen, said and shown on screen. Visual hooks count as much as text hooks.
8. Add one closing line on a shared pattern only if 3 or more of the top videos show it. Don't build the answer around formats instead of individual videos.
9. Show videos from the US, Europe, Canada, Australia and New Zealand by default. When the user names a market or language, show videos from there.

## When to deviate

- "What changed": line the posts up in time order, find where views jump from a flat run, and name the post where it began. Then compare the posts around it for what changed in topic, hook and format. Public numbers are enough to find the spike.
- For a longer history, split it into eras and say for each what changed and what stayed the same. A typical arc is broad testing, then a couple of lanes that work, then cutting what fails.
- Breakout checks matter most for small or new accounts that recently grew.
- Comparing brands: run the same analysis on each, on the same platform where possible, so the findings sit side by side.

## By profile type

The user's profile type (app, service, creator, ecommerce, agency) comes from `get_profile`, or from what they tell you.

- ecommerce: keep the brand's own posts apart from creators' posts about it, and say which is which. Public stats only: no claims about sales.
- any type: say which accounts and searches you used.

## Tools

- `analyze_brand` (CLI: `npx searchtok brand`): a brand's TikTok and Instagram from its handle, name or website, with last 30 days against the 30 before, top outlier posts and format mix; up to 3 compared.
- `get_account` (CLI: `npx searchtok account`): one account's usual views and best recent posts (cheaper when you know the handle).
- `search_content` (CLI: `npx searchtok search`): creators' posts about the brand.
- `analyze_post` (CLI: `npx searchtok post`): hooks and formats of the posts you'll show. One post per call: run it on the 3 to 5 you'll show.

## A great answer

From a real searchtok answer to "what's gymshark doing on tiktok and reels that's working? we're a small activewear..." (16 Oct 2026), one top video. Each point is about that video; the numbers and quotes came straight from searchtok's tools:

> **Onyx V1 return countdown with release date**
> - Opens on a movie-poster style group shot of athletes, so it looks like a film trailer, not an ad (1.8M views, 27.1x usual views).
> - Cinematic shots of gym wear in dramatic lighting carry the middle, so the product is shown without a sales pitch.
> - Ends by revealing the exact release date and time, which gives a clear reason to come back and buy.
> - Short on-screen title names the product and the return, so it reads with no sound.

## Don'ts

- Don't score a post without its numbers, and use public numbers only (views, likes, comments, shares, saves).
- Don't judge on conversions: searchtok can't see them.
- Don't rank a brand's posts by raw views: judge them against the brand's usual views.
- Never show low-view videos, and never say why a video didn't work.
- Leave ads out entirely: never show one or use it as evidence.

## Plain words

- Plain words, short sentences. Say what to copy from this brand and why it fits this user.

## Sources

This playbook paraphrases what these creators teach (it never copies their words), plus searchtok's own rules and tested examples:

- Kallaway, [5 Claude Skills To Grow Faster Than 99% of People on Social Media](https://www.youtube.com/watch?v=Cnk9NQ8JpCs)
- Kallaway, [7 Claude Skills So Powerful They Feel Illegal](https://www.youtube.com/watch?v=gEdt3AGLWjI)
