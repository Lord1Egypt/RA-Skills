---
name: tareno-hermes-social-ops
description: Operate Tareno social accounts, calendars, drafts, media, analytics and Get Viral projects through an authorized Tareno MCP connection.
metadata:
  openclaw:
    homepage: https://tareno.co/docs/mcp
    emoji: "📅"
---

# Tareno social operations

Use the Tareno MCP tools available in the current Hermes session. Tareno is the source of truth for account identity, platform requirements, content state and action status. This skill supplies workflow guidance; installing it alone does not configure or authorize the MCP connection.

## Connection

A Tareno account and access to the selected social accounts/workspaces are required. Service-plan limits, provider permissions and Get Viral feature availability apply; approved analyses may consume AI credits.

If tools are missing, add this server to the existing `~/.hermes/config.yaml`, preserving other configuration:

```yaml
mcp_servers:
  tareno:
    url: https://tareno.co/api/mcp
    auth: oauth
```

Run `hermes mcp login tareno` to complete browser OAuth. Review exposed tools with `hermes mcp configure tareno`, then start a new session or use `/reload-mcp`. Begin with `list_workspaces` and `list_accounts` to verify the connection before writes. Hermes handles OAuth credentials; do not paste tokens into prompts, URLs or public configuration. Preserve existing tool policies. Consult https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp for version-specific setup. This configuration follows Hermes documentation; a successful authenticated Tareno/Hermes end-to-end test is still required on the user's installation.

## Choose context and inspect content

Resolve ambiguous workspace/account selections using `list_workspaces` and `list_accounts`. Before preparing content for an account, inspect `get_platform_schema`; use `get_platform_options` for Pinterest boards or TikTok creator options.

Use `list_posts` / `get_post` for Tareno calendar content. Use `list_account_posts` / `get_account_post` for provider-accessible account content, obtaining a fresh returned `postRef` before account-post operations. Use `get_post_analytics` and `list_post_comments` only where available. Comments are read-only: no replies or moderation are offered by these tools.

## Analytics and drafts

Use `get_analytics_overview`, `get_platform_analytics` and `get_content_strategy` for the requested period. Label cached data and missing coverage; separate observations from recommendations.

Use `create_drafts` for platform-specific campaigns, translations or repurposing. Use `update_draft` for existing editable drafts. Draft creation does not publish. Check format, account and platform requirements rather than assuming every network supports the same format.

## Media and reference videos

Search `list_media` before requesting an asset upload. `upload_media_from_url` imports public HTTPS images/videos into Tareno; local paths and private-network URLs are unsupported.

`get_social_media_transcript` returns a real transcript and available timestamps from supported public social videos. `get_social_video_download` resolves temporary video links; it does not automatically import or publish the content. Provider coverage and access restrictions still apply.

## Get Viral research and blueprints

Check `get_viral_capabilities` before promising discovery or analysis. Use `discover_viral_videos` for actual returned reference videos and metrics. Use `list_viral_projects` to continue existing work or `create_viral_project` to prepare a topic/reference-based Quick Blueprint project.

Before `start_viral_analysis`, obtain `get_viral_analysis_quote` and explain the quoted credit cost. Starting analysis requests Tareno approval. Track `get_viral_run_status` and retrieve `get_viral_blueprint` after completion. A blueprint provides content/script/production guidance; it is not a rendered video or a guarantee of viral performance.

## Consequential requests

Call `schedule_posts`, `publish_posts`, `reschedule_post`, `update_scheduled_post` or `delete_post` only for the user's requested target, content and timing. Delete is limited to drafts or scheduled posts. Use explicit ISO 8601 timestamps with offsets and an IANA timezone. Assign a stable new idempotency key to each distinct consequential request; retry an identical request with the same key.

These actions return a Tareno approval request. Show its impact and returned approval URL, then use `get_action_status` to verify the final result. Pending approval is not completed publication, scheduling, editing or deletion. Do not bypass Tareno approval or grant broader runtime access to complete a request.

## Example requests

For the full range of workflows, read [references/example-prompts.md](references/example-prompts.md). Use the current live tool inventory when a deployment or account exposes fewer capabilities.
