---
name: reachowl-campaigns
description: "Create, list, start, pause, update, and delete ReachOwl outreach campaigns for Facebook, Instagram, and WhatsApp (cold DMs, friend requests, follow-ups, auto comment replies), and upload leads into an existing campaign. Use for Facebook group or post commenter outreach, Instagram follower or hashtag outreach, WhatsApp bulk messaging, or importing a contact list into a ReachOwl campaign."
license: MIT
compatibility: Requires the ReachOwl MCP server (https://reachowl.com/mcp) and a connected Facebook, Instagram, or WhatsApp account in ReachOwl.
metadata:
  author: ReachOwl
  version: "1.1.0"
  homepage: https://reachowl.com
  tags: reachowl, facebook-marketing, instagram-dm, whatsapp-marketing, cold-outreach, lead-generation, campaigns
---

# ReachOwl Campaigns

A campaign pulls an audience (group members, post commenters, followers, a CSV, …) and runs an action on each person (DM, friend request, comment reply) from the user's connected account.

## Before you start

- Requires the ReachOwl MCP server connected with the user's token. If a tool reports a missing token, run the `reachowl-auth` flow.
- Confirm the audience, message text, and daily limit with the user before creating a campaign with `status: 1` (it starts sending).

## MCP tools

| Tool | Purpose |
|------|---------|
| `list_campaigns` | `{ platform?, page?, per_page? }` — omit `team_id` |
| `get_campaign` | `{ id }` |
| `create_campaign` | `{ body }` — create a **new** campaign only |
| `update_campaign` | `{ id, body }` — partial; `{ status: 1 }` start, `{ status: 0 }` pause |
| `delete_campaign` | `{ id }` |
| `add_campaign_contacts` | `{ campaign_id, audience: [...] }` — upload leads to an **existing** campaign (max 500 rows per call) |
| `list_app_states` | Connected accounts → `executor_ids` |

## Never

- Never call `create_campaign` to upload contacts. "Add these leads to campaign 18312" → `add_campaign_contacts`.

## Create a campaign

1. `get_user` → `team_id`.
2. `list_app_states` → pick connected account ids for the platform → `executor_ids` (and `executor_id` = first id).
3. Choose `platform` + `audience_type` + `action_type`:

| platform | audience_type | `post_url` value | typical action_type |
|----------|---------------|------------------|---------------------|
| facebook | `group` | `https://www.facebook.com/groups/…` | `messages`, `friend_request` |
| facebook | `comments`, `reactions` | full post or ad URL | `messages`, `comments` (auto-reply) |
| facebook | `comments_video` | Facebook video URL | `messages` |
| facebook | `friends` | profile URL | `messages`, `unfriend_friend` |
| facebook | `pending_friend_requests`, `suggestions` | none | `cancel_friend_request`, `messages`, `friend_request` |
| instagram | `followers`, `following` | username or profile URL | `messages`, `friend_request` (follow) |
| instagram | `comments` | `https://www.instagram.com/p/…` | `messages`, `comments` |
| instagram | `location`, `hashtag` | location URL or hashtag | `messages`, `friend_request` |
| whatsapp | `group` | WhatsApp group id from the synced browser | `messages` |
| any | `file_upload` | none; add contacts after create | `messages` |

4. Call `create_campaign { body }`. Runnable minimum: `name`, `platform`, `audience_type`, `action_type`, `executor_ids`, `executor_id`, `post_url` (when the table needs one), and `messages` when `action_type` is `messages`.

```json
{
  "body": {
    "name": "Post commenters DM",
    "team_id": 7715,
    "platform": "facebook",
    "audience_type": "comments",
    "action_type": "messages",
    "post_url": "https://www.facebook.com/groups/123/posts/456/",
    "executor_id": 3807,
    "executor_ids": [3807],
    "limit": 30,
    "status": 0,
    "messages": [
      { "text": ["Hi {{first_name}}, saw your comment on the post — happy to help.", "Hey {{first_name}}! Thanks for commenting."], "delay": 0 },
      { "text": ["Just checking in, {{first_name}} — any questions?"], "delay": 1440 }
    ]
  }
}
```

- `messages[]` are sequence steps; `delay` is minutes after the previous step. Each `text[]` holds spin variants (one is picked per contact).
- Placeholders: `{{name}}`, `{{first_name}}`, plus any custom key you put in contact `variables` (for example `{{area}}`).
- Useful optional fields: `limit` (daily cap, default 30), `skip_duplicate`, `audience_keywords` / `exclude_keywords` (bio filters), `comment_keywords`, `countries`, `schedule: [{ day, start_time, end_time }]`, `clone_from` (copy an existing campaign).
- Create with `status: 0`, show the user a summary, then `update_campaign { id, body: { status: 1 } }` once they confirm.

## Add contacts to an existing campaign

```json
{
  "campaign_id": 18312,
  "audience": [
    { "name": "Ali Khan", "phone": "923001234567", "area": "DHA Lahore" },
    { "name": "Sara", "profile_url": "https://www.facebook.com/sara.example" }
  ]
}
```

- WhatsApp: pass `phone` (digits with country code); the tool builds `member_id` (`923001234567@c.us`) and `profile_url` (`https://wa.me/923001234567`).
- Facebook / Instagram: pass `profile_url` and/or `member_id`. Rows with neither are skipped.
- Any extra field (like `area`) becomes a message variable (`{{area}}`).
- Over 500 rows: split into batches of 500.
- Verify with `get_campaign` or `list_contacts { campaign_id }`.

## WhatsApp notes

- `platform: "whatsapp"`, `action_type: "messages"`, `audience_type: "group"` or `"file_upload"`.
- WhatsApp must be activated on the Browsers page in the ReachOwl app first; check `list_app_states` for a `whatsapp` account.
- For a full WhatsApp flow, see `reachowl-whatsapp-marketing`.

## Errors

- `422` on group or post audiences: the group is not synced in the user's account. Ask them to sync groups from their connected Facebook browser, then check `list_groups`.
