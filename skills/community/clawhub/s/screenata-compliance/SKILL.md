---
name: screenata-compliance
description: Manage SOC 2, HIPAA, ISO 27001, and ISO 42001 compliance with Screenata. Use for workspace readiness, failing security tests, evidence collection, policy drafting, risk review, and audit preparation through Screenata's hosted MCP tools. Requires a Screenata account and authorized MCP connection. General framework explanations do not require Screenata tools.
license: MIT
---

# Screenata compliance

Use Screenata's live workspace data to answer compliance questions and carry out authorized work. Screenata prepares the program and evidence; the user's auditor issues the audit report or certification. Do not describe a readiness score or passing check as certification.

## Connect and identify the workspace

This skill supplies instructions, not an MCP connection. If Screenata tools are unavailable, guide the user to add a remote MCP server named `screenata` at `https://api.screenata.com/mcp`, using Streamable HTTP and OAuth. They sign in and select a workspace in the browser. The client must support remote MCP and OAuth discovery. Installation of this skill does not authorize scans, uploads, or workspace changes.

Call `screenata_whoami` and name the workspace before reading its compliance data or making changes. To switch workspaces, reconnect and choose the intended workspace on the consent screen. If sign-in fails, stop workspace operations until it succeeds. Never ask the user to paste tokens or provider credentials into chat.

Discover the connected server's current tool schemas; tool names may be prefixed by the client. Use their returned fields and constraints rather than guessing arguments. If a tool reports a missing scope, name it and ask the user to reconnect with that permission. Do not retry an unchanged permission failure.

## Choose the right read operation

| User request | Tools and interpretation |
| --- | --- |
| Overall compliance readiness | `screenata_status`, then `screenata_next_actions`. |
| Automated infrastructure results | `screenata_assess`. This is an automated check score, not audit readiness. |
| Audit blockers | `screenata_audit_check`, then `screenata_gaps` for missing or stale evidence. |
| Failing checks | `screenata_tests` with `check_result: FAIL`; use `fixable: true` to find actionable tests. Read detail before proposing a fix. |
| Framework controls | `screenata_controls` with the requested `framework`, and `cycle` when audit conclusions are needed. |
| Policies and claims | `screenata_policies`, then `screenata_policy_detail` for a chosen policy. |
| Risk register | `screenata_risks`; follow pagination and use the returned rating/status enums. |
| Policy or procedure questions | `search_workspace_docs`, then `get_document_by_title` when a title is known. |

For SOC 2, HIPAA, ISO 27001, and ISO 42001, framework slugs are `soc-2`, `hipaa`, `iso-27001`, and `iso-42001`. A framework slug is not an audit cycle ID. Resolve the requested framework's cycle from `screenata_status`, then pass its actual ID to cycle-specific calls. Lead with that cycle's score; label any workspace-wide score separately. Offer one prioritized next action unless the user requests a broader plan.

Name tests by their returned `TEST-nnn` code and controls by their returned display code and title. Do not invent codes or use internal `SC-` identifiers as display codes. Link returned `url`, `testUrl`, or `auditCycleUrl` values verbatim. Follow pagination when completeness matters, and disclose any unread pages or unavailable data.

## Fix a failing test

1. Read `screenata_test_detail`. Explain the failed check, affected resources, and the cause. Resolve questions that change the fix before preparing it. For multiple targets, identify the target with the user; never silently select the first resource.
2. Use the returned `applyPath` and `terminalPath` to choose the action. An integration or authentication failure requires reconnecting the integration, not changing infrastructure. `integration_blocked` does not mean ready to execute.
3. For `applyPath: screenata`, call `screenata_test_remedy_prepare` with the exact returned `targetRef` as `target`. Show the plan, side effects, and rollback information. Only after the user approves that concrete plan, call `screenata_test_remedy_execute` with the unchanged `plan`, `plan_hash`, and same target.
4. For `applyPath: agent`, use the returned guidance to prepare a local CLI, API, or infrastructure-as-code change. Verify that its account and resource match the target. Present the exact change, effects, and revert plan for approval before applying it. For `manual`, give the human steps and wait; enrolling an MFA device cannot be replaced by attaching an enforcement policy. If the test has no check-backed fix, collect evidence instead.
5. Verify the affected target with `screenata_test_run`, using `wait: true` and the same target. If the run remains in progress, use `screenata_test_run_status`. A successful API call or applied change is not a passing check. Report the returned result exactly, including other resources still failing.
6. Compare readiness before and after using `screenata_status` for the same cycle. Report an unchanged score when that is what the service returns. Link the test and run evidence; do not duplicate native check proof as a text evidence submission without a separate need and authorization.

Read the initial cycle score before applying the change if a before/after comparison is needed. `screenata_test_remedy_undo` changes infrastructure too: show the rollback's effect and obtain approval before using it. Never set a test's status directly or claim an upload made it pass.

## Draft a policy from the user's operations

Start with `screenata_policy_questions`. Ask only unanswered questions, at most four at a time, and explain which requirement each serves. Record answers with `screenata_policy_answer` only when the user actually supplied them. Do not infer an attestation from code, a recommendation, or an unanswered question.

Before `screenata_policy_draft`, summarize the recorded answers and obtain approval to create the draft. For an approved or imported policy, explicitly explain that drafting replaces current content; use `replace: true` only after that replacement is approved. Use `force: true` only when the user explicitly asks to draft with incomplete answers, and disclose the unattested items. The user reviews and approves the draft in Screenata; never approve it on their behalf.

## Collect evidence, scan, and assign work

Find the intended test with `screenata_tests` or `screenata_test_detail` before submission. `screenata_submit_evidence` accepts redacted text, such as configuration exports or verified command output, tied to a specific test. Screenshots and PDFs use the Screenata portal or a separately installed Screenata CLI. Do not invent evidence, fabricate a missing procedure, or assert an unverified fix.

For `screenata_scan`, confirm the intended provider and account and that its integration is connected. `screenata_assess` reads existing assessment results; it does not authorize a new scan. Use `screenata_assess_state` only to record the user's actual choice to skip or reconsider a provider.

For `screenata_assign_task`, confirm the test and intended assignee. Explain the concrete change before every write, obtain authorization for it, and use `dry_run` where available. Existing authorization covers only the action and targets the user approved.

## Data handling and reporting

Keep cloud-provider sign-in in the browser or local tooling. Do not request, retrieve, submit, or process patient records, payment card data, government identifiers, authentication secrets, or provider credentials through these tools. HIPAA workflows concern technical controls and procedures, not patient records. Do not open an existing document described as containing restricted data; ask for redacted configuration or aggregate evidence instead.

Report verified outcomes and partial failures precisely. A successful upload can still need review. Never approve a policy, accept a risk, or claim compliance on the user's behalf. When suggesting another action, wait for authorization before starting a new scan, upload, or change. General framework education needs no workspace access.

Product and account access: [Screenata](https://screenata.com) and [Screenata app](https://app.screenata.com). Connection guide and current tool overview: [Screenata MCP](https://github.com/Screenata/screenata-mcp).
