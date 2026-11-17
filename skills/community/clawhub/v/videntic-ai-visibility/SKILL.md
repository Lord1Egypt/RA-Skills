---
name: videntic-ai-visibility
description: Analyze AI search visibility, competitors, mentions, citations, and Technical Audit evidence for a Videntic Project using its authenticated MCP tools. Use when the user asks about their Videntic analytics or wants evidence-based recommendations from their tracked AI responses.
license: MIT-0
metadata:
  homepage: https://videntic.com
---

# Videntic AI Visibility

[Videntic](https://videntic.com) measures how brands appear in AI responses. Use this skill with the Videntic remote MCP server at `https://mcp.videntic.com/mcp` (Streamable HTTP).

## Connect

Use an existing Videntic MCP connection. If unavailable, direct the user to add the remote URL in their client's MCP settings and complete OAuth sign-in. The user chooses the permitted Workspace and actions. This skill does not install a connector or grant access. The MCP does not accept Videntic Public API keys; do not ask users to paste credentials into chat.

Discover the connected server's tools and schemas before calling them. Respect the fields and capabilities exposed by that connection; names below identify the intended tools even when a client adds a prefix.

## Answer an analytics question

1. Resolve the Project with `list_projects`, unless its opaque `project_id` is already known. Preserve returned IDs exactly. If multiple Projects match, ask which one the user means.
2. Read `get_project_analytics` for the latest finalized Analysis. Include AI Platform or Tracked Competitor breakdowns only when useful to the question.
3. Use `list_project_analytics_history` for trends, `list_project_mentions` for brand references, and `list_project_citations` for source links. Follow returned pagination when completeness matters; use filters and bounded pages for examples.
4. Preserve metric names, denominators, time periods, and availability reasons. An unavailable metric is not zero. A Mention is a reference in response prose; a Citation is a source link. Do not use these interchangeably.
5. Report the Project, Analysis period, observed change, and evidence supporting the conclusion. Separate measured results from recommended experiments. Do not infer causation or guaranteed ranking improvements from correlation.

For deeper questions, use `get_project_topic_performance`, `get_project_provider_insights`, `get_project_competitive_signals`, or `get_project_content_gaps` as appropriate. Videntic does not supply aggregate AI prompt demand or search volume: say when these are unavailable rather than inventing estimates.

## Investigate Technical Audit findings

Start with `list_project_audit_runs`. If none exist, explain that the user needs a Technical Audit before findings are available. Otherwise read `get_project_technical_audit`, retain its Audit Run ID, and pass that `audit_id` to detail tools so findings and evidence refer to the same captured run.

Use `list_project_audit_findings`, `get_project_audit_finding`, and audited-page tools for supporting evidence. Before editing a user's repository, compare the recorded evidence with current code. A proposed Audit Fix or old Finding does not prove the current code is wrong. Report repository changes separately from verified resolution; a later comparable Audit Run is needed to establish the latter.

## Explore opportunities

Use `list_project_offpage_opportunities` for stored Off-Page Opportunities. Follow `next_after_id` when a full list is requested. A community target can be a homepage; use `engagement_targets` for exact threads and say when none are available. Priority is an ordering, not a prediction of lift. Citation records are not a substitute for opportunities.

Use `list_project_perception_questions` for Perception Questions and `list_project_prompts` for the tracked Prompt Library; these are distinct sets.

## Make requested changes

Analytics questions do not authorize writes. When the user requests a supported change, first read the target and `get_project_capabilities`. Explain material effects such as Analysis usage, draft allowance, or changed future measurements before obtaining any missing consent.

For an authorized write, use the tool's idempotency key and keep it unchanged with identical arguments across an uncertain retry. Read `get_project_operation` after an uncertain response. Report queued work as queued and preserve item-level rejections. Do not claim that a Content Draft has been published: the MCP draft tools do not publish it.

On `forbidden`, check capabilities and ask the user to reconnect with the necessary consent or obtain Project access; do not repeat the unchanged denied request. On expired authentication, use the client's OAuth reconnection flow.
