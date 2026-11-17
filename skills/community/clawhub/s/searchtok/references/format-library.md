# format-library

Use when someone asks which formats work in their niche, how a named format (day in the life, text on screen demo, before and after) performs, or what format to film instead of their current one. Also the reference for naming any format.

## Goal

Show the top videos in the user's niche with each one's format (its story structure and visual layout) and why it worked, and where the open space is.

## Steps

1. Tag each post twice, on two separate axes: its story structure (the order the information comes in) and its visual layout (what the screen looks like). Don't merge them into one label.
2. Judge story structure from the transcript and caption, and visual layout from the on-screen visuals and the hook.
3. Before judging formats, find the top accounts that speak to the same viewer as the user, and leave out their posts that have nothing to do with the niche, such as lifestyle clips or daily updates.
4. Study each account's top 5 to 10 remaining posts, ranked by views and outlier score.
5. For every pairing you name, give the posts that show it, so the user can watch real examples.
6. Empty or thin pairings that nobody in the niche uses are open space to test, not proven winners. When you suggest one, point to a few posts of each part (the structure and the layout) so the user sees what each looks like.
7. Lead with the 3 to 5 top videos for the niche or term, as many as are strong (never pad with weak ones), each with 3 or 4 points on why it worked, from what is seen, said and shown on screen. Visual hooks count as much as text hooks.
8. Add one closing line on a shared pattern only if 3 or more of the top videos show it. Don't build the answer around formats instead of individual videos.
9. Show videos from the US, Europe, Canada, Australia and New Zealand by default. When the user names a market or language, show videos from there.

## When to deviate

- When the user names a format, filter to it: show posts in that format, not just the niche, and say if few came back.
- When the user describes their own format and results, compare it with the pairings behind the outliers and name the ones that beat it.

## Format names

Name each format on two axes, story structure x visual layout:

- Story structures: tutorial / how-to, list / countdown (listicle), before / after, skit, interview / street, reaction / duet / stitch, hook + demo, ugc / testimonial, day in the life / vlog, demo (a product or screen on camera can also read as a layout).
- Visual layouts: talking head, voiceover b-roll, screen recording, slideshow / carousel, green screen, pov, split screen.

## By profile type

The user's profile type (app, service, creator, ecommerce, agency) comes from `get_profile`, or from what they tell you.

- app: say which examples come from app accounts or founders and which from other creators, and only suggest formats one person can film.
- app: for demos with a text hook, quote the on-screen text exactly.
- creator: for a named format, describe the first 3 seconds of each example and quote its hook.

## Tools

- `search_content` (CLI: `npx searchtok search`): posts in the niche or the named format; rows show the format once a post is analysed.
- `find_accounts` (CLI: `npx searchtok accounts`): the top accounts that speak to the user's viewer.
- `get_account` (CLI: `npx searchtok account`): one account's best recent posts and its format mix.
- `analyze_post` (CLI: `npx searchtok post`): format, structure and hooks of the posts you'll show. One post per call: run it on the 3 to 5 you'll show.
- `find_similar` (CLI: `npx searchtok similar`): whether a pairing works beyond one account.

## A great answer

From a real searchtok answer to "what's gymshark doing on tiktok and reels that's working? we're a small activewear..." (16 Oct 2026), one top video. Each point is about that video; the numbers and quotes came straight from searchtok's tools:

> **Lock-in seasonal montage**
> - Rides a trending mindset theme that gym-going women already search and share (1.2M views, 18.4x usual views).
> - Opens on a text promise about the coming months over a dark, moody visual: "what october - december is going to look like".
> - Slideshow of aesthetic discipline clips is cheap to copy with your own footage.

## Don'ts

- Don't present open space as a proven winner.
- Don't name a format without the posts that show it.
- Never show low-view videos, and never say why a video didn't work.
- Leave ads out entirely: never show one or use it as evidence.

## Plain words

- Plain words, short sentences. Name the format the way creators would, then show it.

## Sources

This playbook paraphrases what these creators teach (it never copies their words), plus searchtok's own rules and tested examples:

- Kallaway, [7 Claude Skills So Powerful They Feel Illegal](https://www.youtube.com/watch?v=gEdt3AGLWjI)
