---
name: seomatic-approval-workflow
description: Operate SEOmatic's human-gated execution loop from chat - inspect staged proposals with full evidence, record the user's approve/dismiss decisions, watch execution, and undo with rollback if needed. Use when the user wants to review pending SEO work, approve tasks, check what the agent did, or revert a change.
version: 1.0.0
license: MIT
homepage: https://app.seomatic.ai
metadata:
  paperclip:
    requirements:
      env: []
      binaries: []
      mcp: [seomatic]
  openclaw:
    requires:
      mcp: [seomatic]
  hermes:
    requires_mcp_servers: [seomatic]
mcp:
  servers:
    seomatic:
      url: https://app.seomatic.ai/api/mcp
      transport: streamable-http
      auth: oauth
      setup: 'Add the SEOmatic MCP server (OAuth, or a Bearer smk_ API key from https://app.seomatic.ai/dashboard/settings?tab=ai-agents). Free tier covers every read in this skill.'
tools:
  - task_manage
  - campaign_manage
  - get_task_rollback
---

# Approval workflow

> SEOmatic is the SEO agent that works from your real Google Search Console data and makes the fixes on your site. Fixes you ask for here wait for your approval. By default SEOmatic's own agent also ships small, undoable fixes by itself. Every change can be rolled back.

Cost model first: EVERYTHING in this loop is free except execution itself
(a title/meta/H1 fix is typically a few hundred credits, stated per tool).
Recording decisions, executing and rolling back need a paid plan (the
`agents:act` scope); on a free key those actions are locked and say which
plan includes them.
Inspecting tasks, evidence and statuses NEVER triggers re-analysis.

1. **Inspect**: `task_manage` list (filter status proposed), then get for
   full evidence - rationale, GSC numbers behind it, exactly what will
   change. Show the user the evidence, not just titles.
2. **Record the decision**: relay the evidence, then `task_manage` action
   `decide` to record what the USER decided - never approve on your own
   judgment. (Inline Approve/Dismiss cards exist on the dashboard and in
   chat, but the card tool is not exposed over MCP, so an MCP client relays
   the evidence and records the user's answer instead.)
3. **Destructive types** (noindex, redirects): these remove pages from the
   index or reroute equity - fast to apply, weeks to reverse. Require the
   user to explicitly confirm after seeing the exact URL and consequence;
   only then pass confirmDestructive.
4. **Execution**: approved auto-executable tasks dispatch within seconds
   (the decide response says whether they did). Poll get for the outcome;
   a HELD result means the safety reviewer staged it - show the staged
   content, and only an explicit user go releases it.
5. **Verify**: report from the evidence block what actually changed
   (before/after), never from assumption.
6. **Undo**: if the user reports a bad change, call get_task_rollback
   FIRST - every live edit stores the full pre-edit state; original
   content is never lost. Never offer invented replacement copy.
