---
name: tokst-memory
description: Use TokST Cloud MCP for durable memory, shared context, and governed knowledge.
description_zh: 使用 TokST 云端 MCP 管理长期记忆、共享上下文和知识治理。
description_en: Use TokST Cloud MCP for durable memory, shared context, and governed knowledge.
display_name: TokST
display_name_en: TokST
category: tools
slug: tokst-memory
displayName: TokST
version: 0.9.0
author: TokST
summary: Cloud MCP memory and shared context for people and AI agents.
license: MIT-0
---

# TokST Memory

TokST gives the connected Agent durable memory across conversations, devices,
and authorized workspaces. Use the TokST Cloud MCP connection for all memory
operations. The MCP endpoint is:

https://api.tokst.com/mcp

## Connection

Configure this URL in an MCP client that supports Streamable HTTP. Complete the
browser authorization requested by the client. Static or headless deployments
may use a TokST API key as a Bearer token.

The connected client exposes TokST tools directly. Use those tools; do not ask
the user to install a CLI for memory retrieval or memory writes.

## First-use check

1. Connect `https://api.tokst.com/mcp` and complete browser authorization.
2. Use `tokst_search` to return the title and ID for one known topic.
3. Use `tokst_remember` to save one confirmed Markdown memory with a clear
   heading.

A returned memory title and ID confirms the active Workspace and Atlas route.
Use Cloud MCP for durable knowledge.

Useful references:

- Documentation: https://tokst.com/docs
- MCP guide: https://tokst.com/docs/mcp
- Agent guide: https://tokst.com/llms.txt
- Full agent context: https://tokst.com/llms-full.txt
- MCP discovery: https://api.tokst.com/.well-known/mcp
- MCP changelog: tokst://changelog
- Skill changelog: https://tokst.com/skill-changelog.md

## Daily memory workflow

1. Call `tokst_memory_get` when the memory ID is already known.
2. Call `tokst_search` for a historical fact, decision, preference, constraint, or project topic. Its results already contain complete memory content; use that content directly unless a specific ID needs sensitive-read confirmation.
3. Call `tokst_context` when work needs a structured knowledge-base snapshot. It groups current records by type; it does not replace a targeted search.
4. Solve calculations, translation, rewriting, and questions fully answered by the current input without a memory call.
5. Write only confirmed long-term facts, decisions, preferences, rules, and architecture with `tokst_remember`.
6. Update or archive superseded records with their existing memory ID.
7. Keep transient execution output outside durable memory; extract only confirmed long-term knowledge.

Use the narrowest Workspace and Atlas that matches the user’s request. The
service applies the authenticated user and Agent identity; clients must not
invent an authoritative identity.

## What belongs in durable memory

| Type | Store |
|---|---|
| fact | Stable project, user, infrastructure, or operational facts |
| decision | Approved choices, rationale, and constraints |
| preference | Durable user or team preferences |
| architecture | Components, data flow, interfaces, and operational constraints |
| note | Reusable context outside the typed categories |
| task | Historical compatibility records only |

Write every formal durable memory in Markdown by default. Use a clear `#`
heading, then concise sections or bullets for facts, decisions, constraints,
and next steps. Use tables for comparable structured data. Preserve the working
language. Retain material facts, values, file changes, confirmed risks, and
concrete next steps.

## Data quality rules

Store a record after the result is confirmed. A good record states the result,
the scope, the supporting evidence, and the effective constraint.

Keep these categories outside durable memory:

- Secrets, passwords, API keys, private keys, cookies, and access tokens.
- Raw chain-of-thought, full terminal logs, raw tool JSON, and debug traces.
- Transient network failures, quota errors, retries, and duplicate output.
- Guesses presented as confirmed facts.

Preserve user-authorized business and personal information needed by the record.
Ordinary memory writes skip automatic sensitive-content classification. Keep
credentials in a secret manager and store an access reference when useful.
Optional encrypted sensitive storage is disabled by default; the workspace owner
can enable it in Dashboard Settings for explicitly selected manual records.
For a deterministic write refusal, report the error once. Preserve the original
source and avoid repeated probe writes or rephrasing that loses information.

Cloud MCP accepts up to 512 KiB of UTF-8 Markdown for one memory. Successful
writes return the saved byte count. Use `tokst_memory_update` to revise any
combination of title, content, and tags. Attach original sources with
`tokst_attach_file`: provide a ChatGPT file or a public HTTPS URL up to 100 MB.
Local paths and `file://` URLs require the Dashboard attachment panel.

## Safe mutation rules

Read and search before modifying existing records. Confirm the intended
Workspace, Atlas, or memory ID before a broad archive operation.

Use update, archive, restore, and audit tools to preserve traceability. Cloud
MCP does not expose permanent memory deletion. Permanent cleanup is performed
only by the user from the Dashboard archived view after manual confirmation.

## Error recovery

| Condition | Agent action |
|---|---|
| OAuth authorization required | Present the MCP client authorization step and wait for completion. |
| Invalid or expired credential | Ask the user to reconnect or refresh the credential. |
| Permission rejection | Confirm Workspace, Atlas, role, and target resource. |
| Rate limit or temporary server failure | Respect Retry-After when present. Retry one safe read once; do not retry a write before checking its result. |
| Interrupted write | Search the target knowledge base first. Reuse an existing matching result and avoid duplicate writes. |
| `content_too_large` | Attach the source file and save a complete Markdown summary with its source link. |
| Attachment failure | Read the returned stage and action. Fix the URL, authorization, upload, or confirmation issue once before retrying. |

Return concise, user-facing outcomes. Include relevant memory or evidence IDs
when they help the user inspect the work.
