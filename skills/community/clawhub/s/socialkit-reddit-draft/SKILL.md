---
name: socialkit-reddit-draft
description: Drafts a Reddit post for a specific subreddit that follows its rules, then gives the user a prefilled reddit.com link to review and post it themselves. Never posts automatically. Use when the user wants to share something on Reddit or a subreddit.
license: MIT
metadata:
  author: Ahmad Hussain
  platform: reddit
  requires: socialkit-social-core
---

# Reddit draft

Draft only. Reddit API access requires Reddit's approval and is aimed at moderation, and
automated posting across subreddits is treated as spam, so this skill never posts.
See [setup](references/setup.md).

## Steps

1. Ask which subreddit. Ask the user to paste the subreddit's rules (sidebar and posting
   guidelines), or read them with the user; do not scrape Reddit.
2. Create the folder: `node <socialkit-social-core>/scripts/post.mjs --init --dir rd-<slug> --platform reddit --kind <self|link>`
3. Write `post.json`: options.subreddit (no r/), options.title (300 characters), text or
   link, options.flair if the subreddit requires it, and options.rulesChecked: true once
   the rules were checked. Write for that community: no marketing tone, disclose
   affiliation if the user is promoting their own work.
4. Validate: `node scripts/draft.mjs --check --dir rd-<slug>`
5. Show: `node scripts/draft.mjs --show --dir rd-<slug>`. Give the user the `submitUrl`;
   they review and post it on reddit.com.
6. After posting, record it: `node scripts/draft.mjs --mark-posted --url <post URL> --dir rd-<slug>`

## Rules

- One subreddit per draft. Never prepare the same text for several subreddits.
- If the rules forbid self-promotion, say so and do not draft a promotional post.
