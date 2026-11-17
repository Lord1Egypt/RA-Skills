---
name: reviewing-email-performance
description: "Reports how the user's Sendly email performed: sends, opens, bounces, campaign stats, a single email's history, and how close the project is to its sending limits. Use when the user asks 'how did my emails do this week', 'did anything bounce', 'what is my open rate', 'how did the newsletter perform', 'what happened to this email', 'how close are we to our sending limit', or wants an email analytics report. Read-only."
---

# Sendly email performance

Read Sendly's analytics and delivery history and turn them into a short, honest report. Read only.

## Connecting and calling the tools

Every tool in this skill comes from the `sendly` MCP server, the Sendly connector, and is written here as `sendly:<tool>`.

- **Tools listed by name:** call them directly, for example `sendly:list_contacts`.
- **Only `sendly:search_tools` and `sendly:execute_typescript` listed (Code Mode, the default):** call `sendly:search_tools` first, then call each tool inside `sendly:execute_typescript` as `external_<tool>` (for example `external_list_contacts`); the program must `return` its result. Scopes, confirmations and gates are identical on both surfaces.
- **"Tool not found":** switch to the Code Mode route instead of retrying the direct call. If `sendly:search_tools` does not return the tool either, its OAuth scope was not granted; the user reconnects Sendly and approves that scope.
- **No `sendly` tools at all:** Sendly is not connected yet. Install the Sendly power, which adds the server; it signs in with OAuth on first use.

## Tools you will use

- `sendly:view_analytics`: sent, delivered, opened, and bounced counts for a time window.
- `sendly:list_emails`: individual emails with status. Use it to name the emails behind a number.
- `sendly:get_email`: one email's delivery history (for example queued, then sent).
- `sendly:list_campaigns`, `sendly:get_campaign_stats`: the list of campaigns and the stats for one campaign.
- `sendly:get_usage`: the project's sending counters against its daily and monthly caps.

## Workflow

1. Agree the window (default: the last 7 days). Call `sendly:view_analytics` for it.
2. Report sent, delivered, opened, and bounced, with the bounce rate.
3. If anything bounced, call `sendly:list_emails` for the window and list the bounced emails with recipient and time. For one the user picks, call `sendly:get_email` and show its delivery history.
4. If the user asks about a campaign, call `sendly:list_campaigns` to find it, then `sendly:get_campaign_stats`.
5. Call `sendly:get_usage` and state how much of today's and this month's sending cap is used.
6. Close with at most three concrete next steps drawn from the numbers. For bounces or low delivery, offer the `checking-email-deliverability` skill.

## Rules

- Only report numbers the tools returned. If a metric is not in the response, say it is not available.
- Do not compare against industry benchmarks; there are none in the data.
- This skill only reads. Never call a send, create, update, or delete tool from it, such as `sendly:send_email`, `sendly:send_campaign`, `sendly:update_campaign`, or `sendly:delete_campaign`.
