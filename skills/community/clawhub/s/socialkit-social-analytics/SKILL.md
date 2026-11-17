---
name: socialkit-social-analytics
description: Collects engagement metrics (views, likes, comments, shares, reactions) for everything the user published with these skills on YouTube, Facebook, Instagram, Threads and other connected platforms, and writes one report. Use when the user asks how their posts or videos are performing, wants a social media report, or compares platforms.
license: MIT
metadata:
  author: Ahmad Hussain
  requires: socialkit-social-core
---

# Social analytics

Read-only. Works from the publish records in each post folder and YouTube project, so
it covers what was published with this package.

## Steps

1. Ask which folder holds the user's posts and projects (the root).
2. Run `node scripts/analytics.mjs --root <folder>`. It writes `report.md` and `report.json`.
3. Summarise: top posts per platform, what changed since the last report if one exists,
   and posts whose metrics could not be read and why.

## Rules

- Report numbers exactly as returned. Do not compute a cross-platform engagement score;
  platforms count differently.
- Missing permissions (Instagram insights, Threads metrics) need socialkit-meta-auth with
  `--with-engagement`; say so instead of guessing numbers.

## Failure handling

- Per-post errors are listed in the report; one failing platform does not stop the rest.
- `YT_QUOTA_EXCEEDED`: quota resets at midnight Pacific Time.
