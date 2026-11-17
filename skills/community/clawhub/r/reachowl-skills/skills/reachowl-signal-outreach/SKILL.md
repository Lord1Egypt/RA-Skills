---
name: reachowl-signal-outreach
description: "Signal-based prospecting with ReachOwl: find people who just posted a need ('looking for a realtor', 'can anyone recommend a CRM') in Facebook groups, Instagram, Reddit, or Quora, qualify them, and reach out with a personalized DM or reply. Use when the user wants intent-based leads, buyer-intent monitoring, to turn social listening into outreach, or to DM people who commented on or reacted to a relevant post."
license: MIT
compatibility: Requires the ReachOwl MCP server (https://reachowl.com/mcp) and a connected Facebook or Instagram account in ReachOwl for DMs.
metadata:
  author: ReachOwl
  version: "1.0.0"
  homepage: https://reachowl.com
  tags: reachowl, signal-based-marketing, intent-data, social-selling, lead-generation, social-listening, facebook-marketing
---

# ReachOwl Signal-Based Outreach

Reach people when they show a need, not from a cold list: **monitor → qualify → reach out → follow up**.

## Before you start

- Requires the ReachOwl MCP server connected with the user's token. If a tool reports a missing token, run the `reachowl-auth` flow.
- Get the user's approval on the lead list and the message before anything is sent.

## 1. Define the signal

Ask for, or propose:

- **Offer** — what the user sells and to whom.
- **Intent phrases** — what a buyer would write: "looking for…", "need a…", "any recommendations for…", "frustrated with <competitor>".
- **Where** — `facebook_groups` (which groups), `instagram`, `subreddits`, `quora`.

## 2. Monitor

Check `list_mentions` for an existing monitor. Otherwise create one with `create_or_update_mention` (fields in `reachowl-mentions`):

```json
{ "body": { "team_id": 7715, "type": "facebook_groups", "name": "Need a realtor", "keywords": ["looking for a realtor", "recommend a property dealer"], "groups": [111, 222], "executor_id": 3807, "status": 1 } }
```

New monitors fill up over time. Come back later, or add a `keyword-monitor-found-a-post` webhook (`reachowl-webhooks`) to be alerted.

## 3. Qualify

`list_mention_posts { mention_id }` returns posts with `url`, `text`, `author_name`, `author_profile_url`, and `author_id`.

Score each post and show the user a short table:

| Signal | Example |
|--------|---------|
| Strong | Clear need + timeframe or budget ("need a 3-bed rental in DHA this month") |
| Medium | General question in the right niche |
| Skip | Competitors, spam, the user's own posts, or posts older than the user cares about |

Delete noise with `delete_mention_post { id }`.

## 4. Reach out

Pick the route by where the signal came from:

**A. DM the people who posted (Facebook groups / Instagram)**

1. `list_app_states` → `executor_id` for the platform.
2. Create a holding campaign (`reachowl-campaigns`): `audience_type: "file_upload"`, `action_type: "messages"`, `status: 0`. Write a message that refers to what they asked about. Use a custom variable for the topic:

```json
{ "text": ["Hi {{first_name}}, saw your post about {{topic}} — I help with exactly that. Happy to share a few options?"], "delay": 0 }
```

3. Add the qualified authors: `add_campaign_contacts { campaign_id, audience: [{ name: author_name, profile_url: author_profile_url, topic: "a 3-bed rental in DHA" }] }`.
4. Show the user the list and message, then start: `update_campaign { id, body: { status: 1 } }`.

**B. DM everyone engaging with a hot post (Facebook / Instagram)**

When one post has many people saying "interested" or "me too", target its commenters or reactors directly: `create_campaign` with `audience_type: "comments"` (or `"reactions"`) and `post_url` set to the post. Add `comment_keywords` to keep only matching comments.

**C. Reddit / Quora**

ReachOwl can't DM on these platforms. Draft a helpful, non-salesy reply for each strong post and give the user the post `url` to answer manually.

## 5. Follow up

- Add a second message step with `delay` (minutes), such as `1440` for a day later.
- Track replies with `list_contacts { campaign_id }` and log outcomes with `add_contact_note`.
- Retry failures with `reachowl-queues`.

## Rules

- Lead with the person's need. Don't send a generic pitch.
- Keep daily `limit` modest (20–30) and add message variants.
- Never message people who are clearly not prospects (competitors, group admins announcing rules).
