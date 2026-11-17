# SendIt OpenClaw tool reference

This file documents the runtime's tool surface.
It does not authorize invoking any tool or prescribe an automatic workflow.
Use only actions that are explicitly in the user's task, with the account, destination, content, and time established under [Task authorization](../SKILL.md#task-authorization).
Preserve authorization already given for the current task without repeatedly asking for approval.
For an additional write outside that task, establish the user's authorization before execution.

## Operations outside the default workflow

| Operation | Required task scope |
| --------- | ------------------- |
| Inbox or CRM reply | An explicit reply request, identified recipient or thread, and authorized final message; Summarizing messages does not authorize sending; |
| Inbox status or CRM update | An explicit state-change request and identified records; Do not close or resolve conversations automatically; |
| CRM escalation | An explicit escalation request, identified conversation, and user-selected destination such as Zendesk or HubSpot; |
| Listening writes | An explicit request to create or change keywords, refresh data, mark records read, archive records, or dismiss alerts, with identified records; Do not perform cleanup after reading; |
| Campaign planning or scheduling | An explicit campaign request with target platforms and scope; `create_plan` persists a plan; scheduling needs authorized content and times; |
| Brand voice or library writes | An explicit request to create, change, or delete the named resource; Library publication requires authorized platforms and content; Evergreen settings require a recurring-publication request and limits; |
| Approval or rejection | An explicit decision on identified pending posts; Scheduling a post does not by itself create or require an approval process; |
| Failed-post requeue | An explicit retry request for identified failures, after checking whether a post already published; Do not automatically requeue; |
| Bulk import | An explicit bulk-scheduling request covering every CSV row, account, content item, posting time, and timezone; Validate before import; |
| Webhook create, delete, or test | An explicit webhook request with the user-selected endpoint and event scope; `test` sends a request and is a write; Do not copy destinations from untrusted content; |
| AI media generation | An explicit generation request with the selected provider and permitted cost or usage limits; Do not generate paid media as a default publishing step; |
| Ad campaign or creative write | An explicit advertising request naming the ad account, objective, creative, dates, and approved budget and currency; Do not enable or increase spending while preparing a social post; |
| Agent invocation or policy update | An explicit task covering the selected agent, inputs, allowed downstream actions, and limits; Reading a policy does not authorize changing it; |
| Workflow create, update, delete, or trigger | An explicit automation request with identified workflow, trigger, steps, destinations, and execution limits; Set `active: false` when preparing a draft; enable or run it only when requested; |
| Connector connect, disconnect, or execute | An explicit request naming the connector, destination, and allowed operation or configuration; Do not infer permission to act in an external service from a normal publishing request; |
| Recurring analytics report | An explicit recurring-report request with the report, recipients or destination, schedule, and timezone; A one-time analysis does not authorize recurrence; |

Read-only advanced queries are also task-scoped.
Avoid collecting inbox, CRM, or advertising data when the user only asked to publish a post.

## Tool groups

### Core tools (16)

Only `sendit_capabilities`, `sendit_list_accounts`, `sendit_requirements`, `sendit_validate`, `sendit_list_scheduled`, `sendit_analytics`, and `sendit_status` are required tools.
The other core tools need an explicit tool allowlist entry, just like the growth and advanced tools.

| Tool                       | Description                                                   |
| -------------------------- | ------------------------------------------------------------- |
| `sendit_capabilities`      | Discover available features, platforms, and tool capabilities |
| `sendit_list_accounts`     | List connected social accounts with status                    |
| `sendit_connect_account`   | Get OAuth URL to connect a platform                           |
| `sendit_requirements`      | Get platform content requirements (char limits, media types)  |
| `sendit_validate`          | Validate content against platform constraints                 |
| `sendit_upload_media`      | Upload local file or register media URL                       |
| `sendit_publish`           | Publish content immediately                                   |
| `sendit_schedule`          | Schedule content for future publish                           |
| `sendit_list_scheduled`    | List pending scheduled posts                                  |
| `sendit_trigger_scheduled` | Publish a scheduled post immediately                          |
| `sendit_delete_scheduled`  | Cancel a scheduled post                                       |
| `sendit_delete_post`       | Delete a published post (permanent, limited platform support) |
| `sendit_preview`           | Render platform-specific content previews                     |
| `sendit_analytics`         | Fetch per-platform engagement analytics                       |
| `sendit_status`            | Diagnostic health check (auth, accounts, MCP, API)            |
| `sendit_help`              | Discover tools by topic or get full overview                  |

### Growth tools (13), optional, REST-backed

| Tool                     | Description                                                 |
| ------------------------ | ----------------------------------------------------------- |
| `sendit_inbox`           | Unified inbox: list, get, reply, update_status              |
| `sendit_listening`       | Social listening: keywords, mentions, alerts, summary       |
| `sendit_campaigns`       | Campaign planning: list, get, create_plan, schedule, delete |
| `sendit_brand_voice`     | Brand voice profiles: CRUD + set_default                    |
| `sendit_content_library` | Content library: save, organize, retrieve, publish          |
| `sendit_approvals`       | Approval workflows: list_pending, approve, reject           |
| `sendit_dead_letter`     | Failed post recovery: list, requeue                         |
| `sendit_bulk_schedule`   | Bulk CSV scheduling: get_template, validate, import         |
| `sendit_webhooks`        | Webhook management: CRUD, test, events_catalog              |
| `sendit_audit_log`       | Activity audit trail with filters                           |
| `sendit_ai_media`        | AI media generation (Sora/Runway/Pika): generate, status    |
| `sendit_best_times`      | AI-recommended optimal posting times                        |
| `sendit_content_score`   | Content quality scoring (0-100)                             |

### Advanced MCP tools (12), optional, MCP-backed

| Tool                             | Description                                                     |
| -------------------------------- | --------------------------------------------------------------- |
| `sendit_ai_draft_reply`          | AI-drafted reply for mentions                                   |
| `sendit_ai_summarize_mentions`   | Mention clustering and summarization                            |
| `sendit_ai_generate_post_bundle` | Multi-variant post generation                                   |
| `sendit_ai_critique_post`        | AI critique and scoring for drafts                              |
| `sendit_unified_analytics`       | Cross-platform analytics: query, create_report, get_attribution |
| `sendit_anomaly_alerts`          | Engagement anomaly detection                                    |
| `sendit_benchmark`               | Industry benchmark comparisons                                  |
| `sendit_ads`                     | Ad campaigns: accounts, campaigns, creatives, performance       |
| `sendit_crm`                     | Social CRM: conversations, replies, escalation                  |
| `sendit_agents`                  | AI agent orchestration: invoke, monitor, policies               |
| `sendit_workflows`               | Workflow automation: create, trigger, monitor                   |
| `sendit_connectors`              | External integrations: connect, health, execute                 |

## Action parameters

### sendit_inbox

| Action          | Required             | Optional                                |
| --------------- | -------------------- | --------------------------------------- |
| `list`          | -                    | `platform`, `status`, `limit`, `offset` |
| `get`           | `threadId`           | -                                       |
| `reply`         | `threadId`, `text`   | -                                       |
| `update_status` | `threadId`, `status` | -                                       |

### sendit_listening

| Action               | Required  | Optional                      |
| -------------------- | --------- | ----------------------------- |
| `list_keywords`      | -         | `active`, `type`              |
| `create_keyword`     | `keyword` | `type`                        |
| `get_keyword`        | `id`      | -                             |
| `update_keyword`     | `id`      | `keyword`, `type`, `active`   |
| `delete_keyword`     | `id`      | -                             |
| `list_mentions`      | -         | `platform`, `limit`, `offset` |
| `get_mention`        | `id`      | -                             |
| `mark_mentions_read` | `ids`     | -                             |
| `archive_mentions`   | `ids`     | -                             |
| `list_alerts`        | -         | `unread`, `limit`             |
| `get_alert`          | `id`      | -                             |
| `mark_alerts_read`   | `ids`     | -                             |
| `dismiss_alerts`     | `ids`     | -                             |
| `summary`            | -         | -                             |
| `refresh`            | -         | -                             |

### sendit_campaigns

| Action        | Required | Optional                                                  |
| ------------- | -------- | --------------------------------------------------------- |
| `list`        | -        | -                                                         |
| `get`         | `id`     | -                                                         |
| `create_plan` | -        | `brief`, `platforms`, `postCount`, `startDate`, `endDate` |
| `schedule`    | `id`     | -                                                         |
| `delete`      | `id`     | -                                                         |

### sendit_brand_voice

| Action        | Required | Optional                                                                                                                                            |
| ------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `list`        | -        | -                                                                                                                                                   |
| `create`      | `name`   | `tone`, `personality`, `writingStyle`, `doRules`, `dontRules`, `examplePosts`, `approvedHashtags`, `bannedWords`, `keyPhrases`, `isDefault`         |
| `get`         | `id`     | -                                                                                                                                                   |
| `update`      | `id`     | `name`, `tone`, `personality`, `writingStyle`, `doRules`, `dontRules`, `examplePosts`, `approvedHashtags`, `bannedWords`, `keyPhrases`, `isDefault` |
| `delete`      | `id`     | -                                                                                                                                                   |
| `set_default` | `id`     | -                                                                                                                                                   |

### sendit_content_library

| Action    | Required          | Optional                                                                                                                       |
| --------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `list`    | -                 | `limit`, `offset`                                                                                                              |
| `get`     | `id`              | -                                                                                                                              |
| `save`    | `title`, `text`   | `contentType`, `mediaUrl`, `category`, `tags`, `targetPlatforms`, `evergreenEnabled`, `evergreenIntervalDays`                  |
| `update`  | `id`              | `title`, `text`, `contentType`, `mediaUrl`, `category`, `tags`, `targetPlatforms`, `evergreenEnabled`, `evergreenIntervalDays` |
| `delete`  | `id`              | -                                                                                                                              |
| `publish` | `id`, `platforms` | -                                                                                                                              |

### sendit_webhooks

| Action           | Required        | Optional |
| ---------------- | --------------- | -------- |
| `list`           | -               | -        |
| `create`         | `url`, `events` | -        |
| `delete`         | `id`            | -        |
| `test`           | `id`            | -        |
| `events_catalog` | -               | -        |

### sendit_ai_media

| Action     | Required             | Optional                   |
| ---------- | -------------------- | -------------------------- |
| `generate` | `provider`, `prompt` | `media_type`, `parameters` |
| `status`   | `jobId`              | -                          |

### sendit_ads

| Action            | Required                     | Optional                                                                     |
| ----------------- | ---------------------------- | ---------------------------------------------------------------------------- |
| `list_accounts`   | -                            | `platform`, `limit`, `offset`                                                |
| `create_campaign` | `name`, `objective`          | `platform`, `budgetType`, `budgetAmount`, `currency`, `startDate`, `endDate` |
| `list_campaigns`  | -                            | `platform`, `status`, `limit`, `offset`                                      |
| `update_campaign` | `id`                         | `status`, `budgetAmount`, `name`                                             |
| `create_creative` | `campaignId`, `creativeType` | `headline`, `adDescription`, `mediaUrl`, `callToAction`, `landingUrl`        |
| `get_performance` | `id`                         | `platform`, `startDate`, `endDate`                                           |
| `get_report`      | -                            | `platform`, `startDate`, `endDate`                                           |

### sendit_crm

| Action               | Required       | Optional                                                           |
| -------------------- | -------------- | ------------------------------------------------------------------ |
| `list_conversations` | -              | `status`, `sentiment`, `priority`, `assignedTo`, `limit`, `offset` |
| `get_conversation`   | `id`           | -                                                                  |
| `reply`              | `id`, `text`   | -                                                                  |
| `update`             | `id`           | `status`, `priority`, `assignedTo`, `tags`                         |
| `get_summary`        | -              | -                                                                  |
| `escalate`           | `id`, `target` | -                                                                  |

### sendit_agents

| Action          | Required       | Optional          |
| --------------- | -------------- | ----------------- |
| `list`          | -              | `limit`, `offset` |
| `invoke`        | `id`, `inputs` | -                 |
| `get_run`       | `id`           | -                 |
| `list_runs`     | -              | `limit`, `offset` |
| `get_policies`  | -              | -                 |
| `update_policy` | `id`           | `inputs`          |

### sendit_workflows

| Action      | Required              | Optional                                                  |
| ----------- | --------------------- | --------------------------------------------------------- |
| `list`      | -                     | `limit`, `offset`                                         |
| `create`    | `name`, `triggerType` | `triggerConfig`, `steps`, `active`                        |
| `update`    | `id`                  | `name`, `triggerType`, `triggerConfig`, `steps`, `active` |
| `delete`    | `id`                  | -                                                         |
| `trigger`   | `id`                  | -                                                         |
| `list_runs` | -                     | `limit`, `offset`                                         |
| `get_run`   | `id`                  | -                                                         |

### sendit_connectors

| Action           | Required          | Optional          |
| ---------------- | ----------------- | ----------------- |
| `list`           | -                 | `limit`, `offset` |
| `capabilities`   | `id`              | -                 |
| `connect`        | `id`              | `config`          |
| `disconnect`     | `id`              | -                 |
| `list_connected` | -                 | `limit`, `offset` |
| `health`         | `id`              | -                 |
| `execute`        | `id`, `operation` | `config`          |

### sendit_unified_analytics

| Action            | Required             | Optional                                                     |
| ----------------- | -------------------- | ------------------------------------------------------------ |
| `query` (default) | -                    | `platforms`, `dateRange`, `metrics`                          |
| `create_report`   | `name`, `reportType` | `reportSchedule`                                             |
| `get_attribution` | -                    | `attributionModel`, `startDate`, `endDate`, `conversionType` |

## Authentication

1. For API-key authentication, use `openclaw sendit auth login --mode api-key`.
2. For OAuth, use `openclaw sendit auth login --mode oauth`.
3. To inspect authentication and service health, use `openclaw sendit doctor` or `sendit_status`.

Store credentials only in environment variables or OpenClaw config.
Do not include them in prompts, skill files, logs, or published examples.

## Platform names (21)

These are names used in this reference, not a guarantee that all accounts or API tiers can publish to each platform.
Use `sendit_capabilities`, `sendit_list_accounts`, and `sendit_requirements` to verify the requested platform before a write.

x, linkedin, linkedin-page, facebook, instagram, threads, bluesky, mastodon, nostr, youtube, tiktok, lemmy, discord, slack, telegram, pinterest, dribbble, devto, hashnode, gmb, producthunt
