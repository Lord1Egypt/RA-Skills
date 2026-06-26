---
name: sendit-openclaw
description: Execute SendIt social publishing workflows in OpenClaw using the official @senditapp/openclaw plugin tools.
metadata:
  openclaw:
    skillKey: sendit-openclaw
    requires:
      config:
        - plugins.entries.sendit.enabled
    install:
      - id: sendit-plugin
        kind: npm
        package: '@senditapp/openclaw'
        label: Install @senditapp/openclaw
---

# SendIt OpenClaw Orchestrator

Use only prefixed SendIt plugin tools from `@senditapp/openclaw`.

## Tool Groups

**Core (16):** sendit_capabilities, sendit_list_accounts, sendit_connect_account, sendit_requirements, sendit_validate, sendit_upload_media, sendit_publish, sendit_schedule, sendit_list_scheduled, sendit_trigger_scheduled, sendit_delete_scheduled, sendit_delete_post, sendit_preview, sendit_analytics, sendit_status, sendit_help

**Growth (13):** sendit_inbox, sendit_listening, sendit_campaigns, sendit_brand_voice, sendit_content_library, sendit_approvals, sendit_dead_letter, sendit_bulk_schedule, sendit_webhooks, sendit_audit_log, sendit_ai_media, sendit_best_times, sendit_content_score

**Advanced MCP (12):** sendit_ai_draft_reply, sendit_ai_summarize_mentions, sendit_ai_generate_post_bundle, sendit_ai_critique_post, sendit_unified_analytics, sendit_anomaly_alerts, sendit_benchmark, sendit_ads, sendit_crm, sendit_agents, sendit_workflows, sendit_connectors

## Workflow 1: Connect Accounts

1. Call `sendit_status` to check current integration health.
2. Call `sendit_capabilities`.
3. Call `sendit_list_accounts`.
4. For each missing platform call `sendit_connect_account` with `platform`.
5. Ask user to complete OAuth URLs.
6. Re-run `sendit_list_accounts` and confirm connected state.

## Workflow 2: Publish or Schedule

1. Call `sendit_requirements` for target platforms.
2. Call `sendit_validate` with `platforms` and `content`.
3. If local media is present call `sendit_upload_media` first.
4. Call `sendit_preview` to visualize how content will appear.
5. For immediate posting call `sendit_publish`.
6. For delayed posting call `sendit_best_times` then `sendit_schedule`.
7. If needed call `sendit_list_scheduled`, `sendit_trigger_scheduled`, or `sendit_delete_scheduled`.

## Workflow 3: Inbox + Listening Loop

1. Call `sendit_inbox` with `action="list"`.
2. For thread follow-ups call `sendit_inbox` with `action="get"`.
3. For replies call `sendit_inbox` with `action="reply"`.
4. Monitor listening data with `sendit_listening` actions (`list_mentions`, `list_alerts`, `summary`).
5. Keep hygiene with `sendit_listening` actions `mark_mentions_read`, `archive_mentions`, `mark_alerts_read`, and `dismiss_alerts`.

## Workflow 4: Campaign Planning

1. Call `sendit_campaigns` with `action="create_plan"`.
2. Inspect outputs via `sendit_campaigns` with `action="list"`.
3. View details with `sendit_campaigns` with `action="get"`.
4. Schedule selected campaign with `sendit_campaigns` and `action="schedule"`.
5. Validate execution through `sendit_list_scheduled` and `sendit_analytics`.

## Workflow 5: Advanced AI Optimization

1. Use `sendit_ai_generate_post_bundle` to generate variants.
2. Use `sendit_ai_critique_post` to score a candidate draft.
3. Use `sendit_content_score` for quantitative scoring.
4. Use `sendit_ai_summarize_mentions` to capture audience themes.
5. Use `sendit_ai_draft_reply` to draft sensitive mention responses.
6. Publish finalized content with `sendit_publish` or `sendit_schedule`.

## Workflow 6: Analytics Intelligence

1. Call `sendit_unified_analytics` for cross-platform overview.
2. Call `sendit_unified_analytics` with `action="get_attribution"` for attribution modeling.
3. Call `sendit_best_times` for optimal posting windows per platform.
4. Call `sendit_anomaly_alerts` to detect engagement anomalies.
5. Call `sendit_benchmark` to compare against industry benchmarks.
6. Use `sendit_content_score` to evaluate draft quality pre-publish.
7. Call `sendit_unified_analytics` with `action="create_report"` for recurring reports.

## Workflow 7: Content Library Management

1. Call `sendit_content_library` with `action="list"` to browse saved content.
2. Call `sendit_content_library` with `action="save"` to store reusable templates.
3. Call `sendit_content_library` with `action="get"` to retrieve a saved piece.
4. Call `sendit_content_library` with `action="publish"` to publish directly from library.
5. Or use retrieved content with `sendit_publish` or `sendit_schedule`.

## Workflow 8: Approval Workflows

1. Create content via `sendit_schedule` (posts in "pending approval" state).
2. Call `sendit_approvals` with `action="list_pending"` to review the queue.
3. Call `sendit_approvals` with `action="approve"` or `action="reject"`.
4. Approved posts proceed to their scheduled time.

## Workflow 9: Failed Post Recovery

1. Call `sendit_dead_letter` with `action="list"` to view failed posts.
2. Investigate failure reasons in the response data.
3. Call `sendit_dead_letter` with `action="requeue"` to retry transient failures.

## Workflow 10: Bulk Operations

1. Call `sendit_bulk_schedule` with `action="get_template"` for the CSV format.
2. Prepare CSV content matching the template.
3. Call `sendit_bulk_schedule` with `action="validate"` to check the CSV.
4. Call `sendit_bulk_schedule` with `action="import"` to create all posts.

## Workflow 11: Ad Campaign Management

1. Call `sendit_ads` with `action="list_accounts"` to view ad accounts.
2. Call `sendit_ads` with `action="create_campaign"` to set up a campaign.
3. Call `sendit_ads` with `action="create_creative"` to add creatives.
4. Call `sendit_ads` with `action="get_performance"` to track results.
5. Call `sendit_ads` with `action="get_report"` for unified reporting.

## Workflow 12: CRM Engagement

1. Call `sendit_crm` with `action="list_conversations"` to view threads.
2. Call `sendit_crm` with `action="get_conversation"` for details.
3. Call `sendit_crm` with `action="reply"` to respond.
4. Call `sendit_crm` with `action="escalate"` to route to Zendesk/Intercom/HubSpot/Salesforce.
5. Call `sendit_crm` with `action="get_summary"` for inbox metrics.

## Workflow 13: Workflow Automation

1. Call `sendit_workflows` with `action="list"` to view existing workflows.
2. Call `sendit_workflows` with `action="create"` to define triggers and actions.
3. Call `sendit_workflows` with `action="trigger"` to run manually.
4. Call `sendit_workflows` with `action="list_runs"` to monitor execution.

## Workflow 14: Troubleshooting

1. Call `sendit_status` first — it returns auth validity, account count, MCP availability, and API health in one call.
2. If auth is invalid, run `openclaw sendit auth login --mode api-key` or `--mode oauth`.
3. Run `openclaw sendit doctor` for deeper connectivity diagnostics.
4. Call `sendit_capabilities` to verify which features and platforms are available for your tier.
5. Use `sendit_help` with a topic to find the right tool for your task.

## Guardrails

- Do not call unprefixed SendIt MCP tools directly.
- Validate before writing when uncertain.
- Call `sendit_status` first when encountering errors or starting a new session.
- Prefer `sendit_capabilities` when behavior differs across environments.
- If a MCP AI tool returns unavailable, proceed with REST-core workflows and surface the fallback reason.
- Use `sendit_content_score` and `sendit_ai_critique_post` before high-stakes publishes.
- Check `sendit_best_times` before scheduling for maximum engagement.
- Use `sendit_preview` before publishing to verify content rendering.
- Use `sendit_delete_post` with caution — deletion is permanent and platform support varies.
