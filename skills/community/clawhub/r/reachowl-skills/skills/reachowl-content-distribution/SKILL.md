---
name: reachowl-content-distribution
description: "Repurpose an article, blog post, product launch, or announcement into posts tailored to different Facebook groups and communities, then schedule them with ReachOwl's post scheduler and auto-reply to interested commenters. Use for content distribution, community marketing, launch announcements, or sharing a blog post across Facebook groups."
license: MIT
compatibility: Requires the ReachOwl MCP server (https://reachowl.com/mcp) and a connected Facebook account with synced groups in ReachOwl.
metadata:
  author: ReachOwl
  version: "1.0.0"
  homepage: https://reachowl.com
  tags: reachowl, content-distribution, content-repurposing, community-marketing, facebook-groups, launch
---

# ReachOwl Content Distribution

Turn one piece of content into native posts for each community, schedule them, and capture the people who respond.

ReachOwl's scheduler publishes to **Facebook groups**. For other platforms (LinkedIn, X, Reddit, newsletters), this skill drafts the posts for the user to publish themselves.

## Before you start

- Requires the ReachOwl MCP server connected with the user's token. If a tool reports a missing token, run the `reachowl-auth` flow.
- Get the user's approval on every post and its target groups before scheduling.

## 1. Get the source

Ask for the article text or URL (read it if you can), the goal (traffic, sign-ups, leads, awareness), and the call to action.

## 2. Pick the communities

- `list_groups { search? }` → groups synced in the user's account (name, URL, size if available).
- Group them by audience (for example "landlords", "first-time buyers", "investors").
- No suitable groups? Tell the user to join relevant groups and sync them from their connected Facebook browser.

## 3. Repurpose

For each audience cluster, write a post that fits that group:

- Lead with the value for that audience, not the headline of the article.
- Give 3–5 useful takeaways in the post itself. Most group rules punish bare link drops.
- End with a soft call to action: put the link at the end, or "comment INFO and I'll send it".
- Write 2–3 variants so groups don't see identical text.
- Keep it to roughly 80–200 words, with plain formatting.

Also draft versions for other channels if the user wants them (a LinkedIn post, an X thread, a Reddit-style post, a newsletter blurb). These are drafts for the user to publish.

## 4. Schedule (Facebook groups)

One scheduler per audience cluster (fields in `reachowl-post-scheduler`):

```json
{
  "body": {
    "name": "Rental guide – landlords",
    "executor_id": 3807,
    "team_id": 7715,
    "group_urls": ["https://www.facebook.com/groups/landlords-lahore", "https://www.facebook.com/groups/123456789"],
    "schedule_type": "interval",
    "interval": 30,
    "posts": [
      { "text": "Landlords in Lahore: 5 things that cut vacancy time in half …" },
      { "text": "Quick tips for landlords from our new guide …" }
    ]
  }
}
```

## 5. Capture responses

If the post asks people to comment a keyword, add a comment automation once the posts are live (`reachowl-comment-automations`). Use keywords like `["info", "guide", "send"]`, a public reply ("Sent!"), and a DM with the link.

To follow up with everyone who engaged, create a campaign with `audience_type: "comments"` on the post URL (`reachowl-campaigns`).

## 6. Report

`get_post_scheduler { id }` shows what has been posted and what is still queued. Summarize for the user, and offer to pause (`{ status: 0 }`) or clear the pending queue (`delete_queue_ids`).

## Rules

- Respect each group's rules on promotion. Skip groups that ban links or promotion, or use a no-link version for them.
- Space posts out (interval ≥ 15 minutes) and don't post the same content to the same group twice.
