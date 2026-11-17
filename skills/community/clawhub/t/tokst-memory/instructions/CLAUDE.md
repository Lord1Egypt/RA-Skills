# TokST for Claude

TokST is available through Cloud MCP. Use MCP tools for every memory and context operation.

## Work flow

1. Use `tokst_memory_get` for a known ID, `tokst_search` for a targeted historical question, and `tokst_context` for a grouped knowledge-base snapshot.
2. Search before repeating a recommendation, decision, policy, or implementation plan. Search results already include complete memory content.
3. Use `tokst_remember` only for confirmed facts, decisions, preferences, rules, or architecture that remain useful across work.
4. Use update, append, verify, supersede, archive, or restore only for the corresponding durable record.

## Memory quality

Use `fact`, `decision`, `preference`, `architecture`, or `note` for durable knowledge. The `task` type serves historical compatibility; formal assigned work belongs in a Task.

Preserve the user's working language and important tables, values, file changes, risks, and confirmed next steps. Exclude credentials, private keys, cookies, access tokens, raw reasoning, raw tool JSON, debug traces, and temporary errors.

## Scope and safety

Use the narrowest available Workspace and Atlas. The MCP connection supplies the trusted Agent identity, so never invent an authoritative source identity. Ask before a broad archive or access change. Cloud MCP does not expose permanent memory deletion. Permanent cleanup is performed by the user from the Dashboard archived view after manual confirmation.
