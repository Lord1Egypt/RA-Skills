# Reddit (draft only)

Generated from `docs/platforms/reddit-setup.md`; edit it there. Checked 2026-10-24.

No setup and no credentials: this skill never calls the Reddit API.

Why: since Reddit's Responsible Builder Policy (2025-11-11), API access requires explicit
approval and the developer access category is aimed at moderation. Automated posting of
similar content across subreddits is treated as spam. So the skill writes a draft that
follows the subreddit's rules and gives you a reddit.com submit link with the title and
text filled in; you review and post it yourself, then record the URL.

Sources (verify in a browser; Reddit blocks automated fetches):
- https://support.reddithelp.com/hc/en-us/articles/42728983564564-Responsible-Builder-Policy
- https://support.reddithelp.com/hc/en-us/articles/360043504051-Spam
