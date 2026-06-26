---
name: veridicusscan-mcp-analyst
description: Use when the user wants to inspect a prompt, local file, or public HTTPS URL with VeridicusScan through its MCP bridge, triage prompt-injection or hidden-instruction findings, explain coverage or redaction limits, export reports, or run runtime-defense workflows such as memory ingestion, selective disclosure, tool scoping, plan guarding, and action gating.
---

# VeridicusScan MCP Analyst

Use this skill only for the VeridicusScan MCP surface, not for changing the app code itself.

VeridicusScan is a local-first scanner and runtime-defense tool. This skill is for analyst tasks such as scanning websites, files, prompts, job-application artifacts, and agent-runtime flows through the MCP bridge.

## Preconditions

- Confirm a VeridicusScan MCP server is available in the client.
- If it is not available, say so briefly and ask the user to connect the local bridge first.
- Prefer the MCP server over shelling out to app internals when both can do the task.
- Expect one active MCP session at a time. If `open_session` returns `session_limit_reached`, tell the user another active session is still open.

## High-value use cases

- Scan a public website or candidate portfolio URL before an AI agent reads it.
- Scan a local PDF, DOCX, image, or exported text artifact before model handoff.
- Triage prompt snippets or extracted page text with `scan_text`.
- Validate agent-memory and tool-approval flows with the runtime-defense methods.

## Core workflow

1. Start with `health` or `list_methods` if availability is unclear.
2. Open a session with `open_session`.
3. Run the smallest relevant scan method:
   - `scan_url` for live public HTTPS websites
   - `scan_file` for local files
   - `scan_text` for prompts, snippets, and extracted content
4. Pull the report or scan result details the user actually needs.
   - If `scan_file` returns `default_context_mode = "sanitized_only"`, prefer `safe_context` for downstream use and make clear that report surfaces are redacted by design.
   - If `scan_url` returns `non_public_network_url`, explain that VeridicusScan intentionally blocks loopback, private-network, `.local`, `.localhost`, and resolved internal targets.
5. Summarize:
   - risk band
   - risk score
   - default context mode when present
   - findings count
   - top findings with short evidence summaries
   - coverage limits or partial-scan notes
6. Close the session when done unless the user is actively continuing a multi-step analysis.

## Reporting rules

- Be explicit about whether a result is a likely true positive, likely false positive, or uncertain.
- If the scan is partial, explain exactly what was not covered and why that matters.
- If a result is redacted or `sanitized_only`, say that explicitly instead of implying raw evidence is available.
- Distinguish structural signals from semantic injection signals.
- For benign sites, do not overclaim. Say when a hit looks like tracking, accessibility, anti-bot, or app-shell markup rather than malicious prompt injection.
- Include exact MCP error codes when they change the user outcome, for example `non_public_network_url` or `session_limit_reached`.

## Runtime-defense workflow

Use these methods when the user is evaluating agent safety rather than content scanning:

- `ingest_memory` for A1 memory ingestion
- `retrieve_memory` for A2 retrieval validation
- `selective_disclosure` and `evaluate_selective_disclosure` for disclosure quality and privacy checks
- `scope_tools` before planning or execution
- `guard_plan` before approving a plan
- `gate_action` before approving a specific tool action

Always preserve the returned tool scope and pass the authoritative scope back into `guard_plan` and `gate_action`. Do not invent or forge scope values.

Recommended ordering for tool-governance tasks:

1. `open_session`
2. `scope_tools`
3. `guard_plan`
4. `gate_action`
5. `close_session`

## Output style

- Keep summaries short and operational.
- Put findings first.
- Include exact method names when explaining how a result was obtained.
- If the user asks for verification, say which MCP method(s) you used.
- Prefer language that is useful to operators, for example security, IT, recruiting, or compliance teams, instead of purely academic scanner jargon.

## References

- Read [references/mcp-methods.md](references/mcp-methods.md) for the method map and sequencing guidance.
- Public workflow example for recruiting and job-application intake:
  [AI job application screening](https://veridicuscan.app/ai-job-application-screening)
- Public technical workflow example for MCP sessions and runtime guardrails:
  [Local MCP automation for AI agents](https://veridicuscan.app/mcp-automation)
