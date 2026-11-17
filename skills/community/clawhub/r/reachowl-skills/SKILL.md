---
name: reachowl
description: "ReachOwl social media marketing automation for Facebook, Instagram, and WhatsApp: social listening, signal-based prospecting, cold DM campaigns, WhatsApp marketing, Facebook group posting, comment-to-DM automations, Instagram growth, lead finding, and CRM follow-ups through the ReachOwl MCP server. Use when the user mentions ReachOwl or wants to automate Facebook, Instagram, or WhatsApp marketing and doesn't name a specific ReachOwl feature."
license: MIT
compatibility: Requires the ReachOwl MCP server (https://reachowl.com/mcp) and a ReachOwl account.
metadata:
  author: ReachOwl
  version: "1.0.0"
  homepage: https://reachowl.com
  tags: reachowl, facebook-marketing, instagram-marketing, whatsapp-marketing, social-listening, marketing-automation, lead-generation
---

# ReachOwl

[ReachOwl](https://reachowl.com) runs marketing actions from the user's own connected Facebook, Instagram, and WhatsApp accounts. This skill routes a request to the right ReachOwl skill.

## Before you start

1. The ReachOwl MCP server must be connected: `https://reachowl.com/mcp`. Setup: <https://github.com/SaaSBakers/reachowl-skills#setup>.
2. Authenticate with `reachowl-auth` (`auth_status` → `set_token` if needed → `get_user`).
3. Connected social accounts come from `list_app_states`. Their ids are the `executor_id` values most tools need.

## Pick the skill

| The user wants to… | Skill |
|--------------------|-------|
| Connect or verify their ReachOwl account | `reachowl-auth` |
| Monitor keywords and discussions (Facebook groups, Instagram, Reddit, Quora) | `reachowl-mentions` |
| Find people who just posted a need and reach out | `reachowl-signal-outreach` |
| DM group members, post commenters, followers, or a list | `reachowl-campaigns` |
| Run a WhatsApp campaign | `reachowl-whatsapp-marketing` |
| Turn an article or announcement into community posts | `reachowl-content-distribution` |
| Schedule posts to Facebook groups | `reachowl-post-scheduler` |
| Auto-reply and DM people who comment a keyword | `reachowl-comment-automations` |
| Grow an Instagram profile | `reachowl-profile-growth` |
| Scrape leads from websites and import them | `reachowl-lead-finder` |
| See leads and add notes | `reachowl-contacts` |
| Retry a failed or stuck message | `reachowl-queues` |
| Manage pipeline stages and templates | `reachowl-stages-templates` |
| See connected accounts or manage teammates | `reachowl-team-accounts` |
| Send events to Slack, Zapier, n8n, or a CRM | `reachowl-webhooks` |
| Anything else in the V1 API | `reachowl-api` |

## Rules for every ReachOwl task

- Confirm with the user before anything that sends messages, posts publicly, or starts a campaign. Create things paused (`status: 0`) and switch them on after approval.
- Use public URLs (Facebook group URLs, post URLs, profile URLs) rather than internal ids.
- Add contacts to an existing campaign with `add_campaign_contacts`; never create a new campaign just to upload a list.
- Connected accounts and browsers are read-only through the API. Connecting accounts and activating WhatsApp happen in the ReachOwl app.
- Leave `team_id` out of list calls. Get it from `get_user` when a create call needs it.
- Toggle campaigns and schedulers with `status: 0 | 1`, comment automations with `"active" | "paused"`, and growth plans with `"running" | "paused"`.
