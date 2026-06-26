---
name: wiki-mcp-ops-qa-test2
description: Use when an agent should answer simple operations questions by retrieving internal wiki content through wiki MCP, and must refuse to answer when the wiki does not provide enough evidence.
---

# Wiki MCP Ops QA

## Overview

Answer simple operations questions from wiki MCP only. If the wiki does not support the answer, say so directly.

## When to Use

Use this skill for document-oriented operations questions such as:
- deployment, release, rollback, restart
- logs, alerts, SOPs, permissions
- config items, ports, environment variables

Do not use this skill for:
- live system inspection
- code investigation
- pure conceptual questions
- undocumented procedures that require inference

## Workflow

1. Decide whether the question is an operations-document question.
2. Build one to three concise search queries from the service name, system name, environment, alert name, and action.
3. Run preflight checks before first tool call.
4. Call `builtin-wiki-search-tool`.
5. Pick the most relevant one to three documents.
6. Call `builtin-wiki-document-tool` for the selected documents.
7. Extract only the content that directly answers the question.
8. Answer from that evidence only.
9. If evidence is missing, incomplete, or conflicting, refuse or answer conservatively.

## Preflight Checks

Before answering, verify:
- wiki tools are present: `builtin-wiki-search-tool`, `builtin-wiki-document-tool`
- required params are available (`keyword`, `doc_id`, optional `limit`)
- `keyword` is a plain search phrase and not an expression with format placeholders

If tool calls fail, switch to error-triage mode and do not produce undocumented runbook steps.

## Tool Calls

Use the wiki MCP tools in this order:

1. Search with `builtin-wiki-search-tool`
2. Read with `builtin-wiki-document-tool`
3. Answer only after reading the selected page content

Expected usage:
- `builtin-wiki-search-tool`
  - `keyword`: a concise operations query
  - `limit`: usually `3`, increase only if the first pass is weak
- `builtin-wiki-document-tool`
  - `doc_id`: a document id returned by the search tool

Default call pattern:
1. Build a focused `keyword`
2. Call `builtin-wiki-search-tool(keyword, limit=3)`
3. Inspect returned titles and ids
4. Call `builtin-wiki-document-tool(doc_id)` for the best match
5. If needed, read one or two more candidate pages before answering

Do not answer from search titles alone when the body is needed to support the conclusion.

## Search Rules

- Preserve service, component, system, and alert names exactly as given.
- Preserve environment labels such as `prod`, `staging`, `test`, `gray`, `canary`.
- Preserve action terms such as `restart`, `rollback`, `deploy`, `release`, `logs`, `alarm`, `SOP`.
- Remove conversational filler.
- Treat `keyword` as plain text. Do not build format strings from user input.
- If the first search is weak, retry with a narrower query or a query that emphasizes the alert name, service name, or environment.

Preferred query construction:
- restart question: `<service> restart`
- deploy question: `<service> deploy` or `<service> release`
- log question: `<service> logs`
- alert question: `<alert> SOP` or `<alert> handling`

If the user includes an environment, append it to the query.

## Result Selection Rules

- Prefer pages whose titles contain both the service or alert name and the requested action.
- Prefer runbooks, SOPs, deployment guides, and operations manuals over general introductions.
- If multiple results look similar, read the most operationally specific page first.
- If the page body does not clearly support the answer, read another candidate or refuse.

## Response Contract

Use this shape when answering:

- `Conclusion`: direct answer to the question
- `Evidence`: wiki page title and the supporting points
- `Unknown`: anything the wiki does not explicitly cover

Keep the answer short. Reuse wiki terminology where possible.

## Hard Constraints

- Do not use any source other than wiki MCP.
- Do not invent commands, steps, or explanations.
- Do not turn a weak match into a confident answer.
- Do not hide missing information.
- If multiple pages conflict, say they conflict and do not choose a side unless one page is clearly authoritative.

## Refusal Rules

Refuse or answer conservatively when:
- search returns no useful results
- titles look relevant but the page body does not support the answer
- pages are clearly incomplete or outdated
- multiple pages conflict
- the user asks for details not present in the retrieved content

Preferred wording:
- `I don't know based on the wiki results I found.`
- `The wiki does not contain enough information for a reliable answer.`
- `I found related wiki pages, but they do not explicitly describe that step.`

## Supported QA Modes

Use one of these modes based on user intent:

- Direct SOP QA:
  - user asks for exact steps such as restart, rollback, or deploy
  - return concise actionable steps only if explicitly documented
- Evidence lookup:
  - user asks where a policy, setting, or command is documented
  - prioritize page title plus exact supporting snippet
- Incident hint QA:
  - user asks how to handle an alert or common fault
  - provide only documented checks and escalation paths

Do not treat this skill as:
- real-time observability diagnosis
- shell command execution
- cross-system root-cause analysis without wiki evidence

## Tool Error Triage

If wiki tool invocation fails, classify first and report explicitly:

- DNS or network resolution errors (`lookup ... server misbehaving`, timeout):
  - state that wiki endpoint is unreachable from current runtime
  - ask for network or DNS recovery before continuing
- TLS or certificate errors (`x509`, self-signed, unknown authority):
  - state certificate trust is blocking the request
  - ask for trusted CA chain or TLS policy confirmation
- auth errors (`401`, `403`):
  - state credential is invalid, expired, or insufficiently scoped
  - ask for updated authorization configuration
- request construction errors (`%!s(MISSING)`, malformed query):
  - state query formatting is invalid
  - retry with sanitized plain-text keyword

During triage:
- do not fabricate operational steps
- provide a minimal, actionable next check list
- separate `System issue` from `Wiki evidence`

Suggested output shape for failures:
- `Status`: why the call failed
- `Impact`: what cannot be answered now
- `Next checks`: 2-4 concrete checks (network, cert, auth, query)
- `No evidence`: explicitly state no wiki evidence was retrieved

## Examples

Restart question:
- Search `service X restart`
- Call `builtin-wiki-search-tool` with that keyword
- Read the best result with `builtin-wiki-document-tool`
- Answer only if the page explicitly describes the restart path
- Otherwise say the wiki does not provide enough information

Alert handling question:
- Search `alert Y SOP` or `alert Y handling`
- Read the most relevant SOP or incident page before answering
- Summarize only the documented procedure
- Do not add remediation steps that the page does not state
