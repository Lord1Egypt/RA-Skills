# whats-working

Use when someone asks what's working, blowing up or trending in their niche right now, or wants the niche's best posts to copy. The default when no other skill fits a niche question.

## Goal

Show the posts in the user's niche that beat their own account's usual views right now, and why each one worked, so the user picks what to copy.

## Steps

1. Show the niche's own posts, ranked by outlier score, not coaches' or marketers' advice about the niche. Look for advice videos only when the user asks for tips or advice.
2. Study creators who talk to the same audience as the user, not just the biggest accounts. Leave out their posts that are off the user's topic, such as lifestyle clips or daily updates.
3. Include small creators who grew fast recently, not only big names.
4. Rank by outlier score (views against the account's usual views) and keep the posts that beat it. Every post keeps its link so it can be watched.
5. Prefer recent posts. One source used the last seven days and a 25,000 view floor: treat the floor as an example and fit it to the niche's size.
6. Check whether the winners post series: a daily count with a goal, progress updates toward one goal, or a lesson series. Name the series type when you find one.
7. Look for creators remaking their own outlier with small changes (a new value, the same format with other parts changed, the same content in a new format). A repeated hit shows what is working.
8. If a pairing of format and layout has no strong posts in the niche, you may name it as open space to test, never as a proven winner.
9. Lead with the 3 to 5 top videos for the niche or term, as many as are strong (never pad with weak ones), each with 3 or 4 points on why it worked, from what is seen, said and shown on screen. Visual hooks count as much as text hooks.
10. Add one closing line on a shared pattern only if 3 or more of the top videos show it. Don't build the answer around formats instead of individual videos.
11. Show videos from the US, Europe, Canada, Australia and New Zealand by default. When the user names a market or language, show videos from there.

## When to deviate

- Very uneven views on one account (15k on one post, 500k on another) point to a one-off hit, not a pattern. Steady views mean people follow the creator.
- A creator who looks like an overnight success has often posted for years: say if recent growth seems to come from one change, such as starting a series.
- When the user names competitors, check those accounts' recent posts first, then search the niche.

## By profile type

The user's profile type (app, service, creator, ecommerce, agency) comes from `get_profile`, or from what they tell you.

- app: the niche's own posts include app accounts and their founders (demos, builds, streak screens), not general productivity advice.
- service: the business's own posts first. For a local question, include local guide creators too and say which is which.
- creator: search and answer in the profile's language, and quote hooks in the original language.
- ecommerce: sales aren't public. Say so plainly and rank by outlier score instead.
- agency: answer for the client's niche, with things the client can film, and say how many examples come from their area.

## Tools

- `search_content` (CLI: `npx searchtok search`): the niche's posts, ranked by outlier score. Two or three versions of the query at once.
- Yourself, from the rows: drop posts that only match the words.
- `get_account` (CLI: `npx searchtok account`): one creator's usual views, consistency and best recent posts.
- `find_similar` (CLI: `npx searchtok similar`): whether a pattern holds beyond one account.
- `analyze_post` (CLI: `npx searchtok post`): the hooks and formats of the posts you'll show. One post per call: run it on the 3 to 5 you'll show.

## A great answer

From a real searchtok answer to "ok so i launched my budgeting app about 3 months ago and i've been posting on tiktok..." (16 Oct 2026), one top video and the pattern line. Each point is about that video; the numbers and quotes came straight from searchtok's tools:

> **17-year-old budgets his paycheck on camera**
> - Opens on his age and job, which is a first-paycheck situation your audience shares: "I'm 17 and I work 30+ hours a week." (4.2M views, 2208.5x usual views).
> - Plain bedroom, raw phone footage, so anyone can film it.
> - Real dollar amounts for each bucket (car, gas, subscriptions), then the money left to spend as the payoff.
> - The on-screen title tells you the whole video in one line: "Budget My Paycheck With Me As A 17 yr old Working 30+ hours a week".
>
> Pattern: The top videos put a person on camera with real money details or a personal take, and the app comes second.

## Don'ts

- Don't call a post an outlier on raw views or follower count: judge it against its own account's usual views.
- Don't claim a post drove sales, downloads or leads: only public stats are visible.
- Don't write or improve a hook. Quote real ones by reference, or none.
- Never show low-view videos, and never say why a video didn't work.
- Leave ads out entirely: never show one or use it as evidence.

## Plain words

- Plain words, short sentences. Say what to copy and why it fits this user.

## Sources

This playbook paraphrases what these creators teach (it never copies their words), plus searchtok's own rules and tested examples:

- Kallaway, [7 Claude Skills So Powerful They Feel Illegal](https://www.youtube.com/watch?v=gEdt3AGLWjI)
- Personal Brand Launch, [I Studied the Top 100 Fastest Growing Creators From This Year, Here's How to Actually Grow on IG.](https://www.youtube.com/watch?v=UM2Vv_3-ODA)
- Kallaway, [5 Claude Skills To Grow Faster Than 99% of People on Social Media](https://www.youtube.com/watch?v=Cnk9NQ8JpCs)
