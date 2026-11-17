# build-profile

Use when someone asks who an account or business is and what its niche is, wants their own profile or positioning mapped, or asks who their competitors are and where the open space is.

## Goal

Say who this account or business is for, what its niche is, who it competes with and where the open space is, backed by its own posts and its competitors'.

## Steps

1. Start with the target viewer and their pain points: everything else in the profile builds on them.
2. If the account already posts, read its recent posts first (about the last 30) to see what it has been doing.
3. Find the competitor accounts in the niche from what the user says about their niche and customer. Pull in their best posts and leave out the ones unrelated to the user.
4. Describe each competitor's best posts by a short fingerprint of what they do. Judge "best" by views and outlier score.
5. Place each competitor by how broad or narrow a topic it targets, judged by views and outlier score only.
6. Compare competitors on topic, substance, audience, format and visual layout, and look for gaps where nobody is doing something the user could own.
7. Describe content as a formula: topic plus format plus visual layout. Say what the user does, what competitors do and where the open space is.
8. Look across top competitor posts for the claims they all repeat: these are the common beliefs a user could push against.
9. End with one short summary: the niche, how to position, where the open space is and how to go after it.
10. Lead with the 3 to 5 top videos for the niche or term, as many as are strong (never pad with weak ones), each with 3 or 4 points on why it worked, from what is seen, said and shown on screen. Visual hooks count as much as text hooks.
11. Add one closing line on a shared pattern only if 3 or more of the top videos show it. Don't build the answer around formats instead of individual videos.
12. Show videos from the US, Europe, Canada, Australia and New Zealand by default. When the user names a market or language, show videos from there.

## When to deviate

- Contrarian takes must be real: the user's own principles, never invented. If you don't know them, say what they could push against and leave the choice to them.
- You may suggest words or phrases the user could be known for, if they fit the content direction.

## By profile type

The user's profile type (app, service, creator, ecommerce, agency) comes from `get_profile`, or from what they tell you.

- creator: use their profile (get_profile); don't ask the user to restate their niche.
- ecommerce: keep the brand's own posts apart from creators' posts about it, and say which is which.
- agency: profile the client, not the agency.

## Tools

- `get_account` (CLI: `npx searchtok account`): the account's recent posts, usual views and best posts.
- `analyze_brand` (CLI: `npx searchtok brand`): a brand known by handle, name or website, optionally against up to 3 others.
- `find_accounts` (CLI: `npx searchtok accounts`): competitor accounts in the niche, with how reliably they get outliers.
- `search_content` (CLI: `npx searchtok search`): the niche's best posts, to find who wins in it.
- `analyze_post` (CLI: `npx searchtok post`): formats and hooks of the posts you'll describe. One post per call: run it on the 3 to 5 you'll show.

## A great answer

From a real searchtok answer to "set up our profile: we're glossier on tiktok. what's our niche and who are we up against?" (16 Oct 2026), one top video. Each point is about that video; the numbers and quotes came straight from searchtok's tools:

> **Glossier You: one for getting ready, one for touch-ups**
> - Brand post built on one hero product, the fragrance, shown in two everyday uses (7M views, 1038.6x usual views).
> - The caption frames a simple reason to own two bottles: getting ready and touching up.
> - It is the brand's own biggest spike, so the hero product is the thing to repeat.

## Don'ts

- Don't judge which topic breadth works by conversions or leads: views and outlier score only.
- Don't invent the user's beliefs or principles.
- Never show low-view videos, and never say why a video didn't work.
- Leave ads out entirely: never show one or use it as evidence.

## Plain words

- Plain words, short sentences. Describe the niche in the words creators in it use.

## Sources

This playbook paraphrases what these creators teach (it never copies their words), plus searchtok's own rules and tested examples:

- Kallaway, [7 Claude Skills So Powerful They Feel Illegal](https://www.youtube.com/watch?v=gEdt3AGLWjI)
