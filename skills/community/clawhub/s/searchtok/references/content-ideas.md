# content-ideas

Use when someone asks what to post, for content ideas, or for "<niche> content ideas". The answer is real posts to copy from their niche, not advice.

## Goal

Give the user ideas they can film, each built on real posts from their niche that beat their account's usual views, with the topic, hook and format to take from them.

## Steps

1. "<niche> content ideas" means examples: the niche's own posts, ranked by outlier score, not coaches' or marketers' advice about the niche. Look for advice videos only when the user asks for tips or advice.
2. Judge outliers by the outlier score only (views against the account's usual views), never by a multiple of followers.
3. Search the niche, its subtopics and the job title as keywords. Favour posts from the last year, the more recent the better.
4. For each idea, say its topic, the hook to take (quoted from the post), the value, the script structure, the call to action and the format.
5. Mix hooks from different posts so an idea doesn't copy one creator. The topic and hook can come from others; the substance should come from the user's own knowledge or story.
6. Read a viral outlier's transcript for its structure. List, ranking and story structures carry over to other niches.
7. Vary the formats you suggest: sitting and talking to camera is often dull.
8. Lead with the 3 to 5 top videos for the niche or term, as many as are strong (never pad with weak ones), each with 3 or 4 points on why it worked, from what is seen, said and shown on screen. Visual hooks count as much as text hooks.
9. Add one closing line on a shared pattern only if 3 or more of the top videos show it. Don't build the answer around formats instead of individual videos.
10. Show videos from the US, Europe, Canada, Australia and New Zealand by default. When the user names a market or language, show videos from there.

## When to deviate

- New or established account changes the mix. For a new account with no winners yet: about 90% proven outlier ideas from the niche and 10% new experiments. For an established one: about 70% proven niche ideas, 20% doubling down on its own winners, 10% new.
- Doubling down means keeping a winner the same and changing only the value, or only the filming format.
- Topic breadth: map ideas from the exact audience (the centre) out to ideas for anyone. Judge which breadth gets reach from the profile's own posts or close competitors, on views and outlier score only. Skip the broadest ring: it brings unqualified viewers to a narrow niche.
- One starting mix for every seven videos: three for the exact audience, two a step wider, two wider again. It's a starting point to test, not a rule for every niche.
- Suggest untried swaps: keep a working topic and change the format or layout, or the reverse, and point to what competitors do that the profile doesn't.
- Only suggest a contrarian angle the business owner really holds. Don't force one, and never invent their beliefs.

## By profile type

The user's profile type (app, service, creator, ecommerce, agency) comes from `get_profile`, or from what they tell you.

- app: only formats one person can film, and say which examples come from app accounts or founders.
- service: the business's own posts (a realtor's tours, an accountant's tax tips), not coaches telling them what to post.
- creator: use their profile (get_profile). Don't ask the user to restate their niche.
- agency: ideas for the client's niche that can be shot at the client's place in one visit.

## Tools

- `search_content` (CLI: `npx searchtok search`): the niche's posts by outlier score, in the words creators use.
- Yourself, from the rows: drop advice and posts that only match the words.
- `get_account` (CLI: `npx searchtok account`): the user's own or a competitor's best posts, for doubling down and swaps.
- `analyze_post` (CLI: `npx searchtok post`): hooks, formats and structure of the posts behind each idea. One post per call: run it on the 3 to 5 you'll show.

## A great answer

From a real searchtok answer to "realtor content ideas" (16 Oct 2026), one top video and the pattern line. Each point is about that video; the numbers and quotes came straight from searchtok's tools:

> **listing walkthrough of a North Carolina home**
> - Opens with a welcome and the full property address, so local buyers know right away what home it is (1.4M views, 671x usual views).
> - It's a plain listing tour, so the home is the draw and a small account can copy it.
> - Caption leads with the listing details, which fits a goal of more listings and buyer leads.
>
> Pattern: Each top video is a tour of a specific home or community, with the place and key details given in the caption.

## Don'ts

- Don't judge ideas on conversions or watch time: searchtok can't see them. Views and outlier scores only.
- Don't write or improve a hook. Quote real ones by reference.
- Never show low-view videos, and never say why a video didn't work.
- Leave ads out entirely: never show one or use it as evidence.

## Plain words

- Plain words, short sentences. Each idea says what to film and why it fits this user.

## Sources

This playbook paraphrases what these creators teach (it never copies their words), plus searchtok's own rules and tested examples:

- Personal Brand Launch, [How to Create a Month Worth of Content in 60 Minutes](https://www.youtube.com/watch?v=TpTY6hFJbic)
- Kallaway, [7 Claude Skills So Powerful They Feel Illegal](https://www.youtube.com/watch?v=gEdt3AGLWjI)
- Kallaway, [5 Claude Skills To Grow Faster Than 99% of People on Social Media](https://www.youtube.com/watch?v=Cnk9NQ8JpCs)
