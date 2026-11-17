# TokST Agent Instructions

TokST uses Cloud MCP for durable memory and shared context. Use MCP tools for memory retrieval, writing, updates, archive, restore, and knowledge governance.

## Required sequence

1. Use `tokst_memory_get` for a known ID, `tokst_search` for a targeted historical question, and `tokst_context` for a grouped knowledge-base snapshot.
2. Search results already include complete memory content. Reuse returned content before issuing another read.
3. Store only confirmed long-term facts, decisions, preferences, rules, and architecture with `tokst_remember`.
4. Keep transient execution output outside durable memory and save only confirmed reusable knowledge.
5. Retain useful memory IDs in user-facing results when they support review or continuation.

## Record quality

Use Markdown when it preserves a table, procedure, configuration summary, or evidence. Keep the working language. Retain material facts, values, file changes, confirmed risks, and concrete next steps.

Keep credentials in a secret manager and store an access reference when useful. Preserve user-authorized business and personal information needed by the record. Ordinary memory writes skip automatic sensitive-content classification. Optional encrypted sensitive storage is disabled by default and can be enabled by the workspace owner in Dashboard Settings for explicitly selected manual records. Keep raw reasoning, terminal logs, raw tool JSON, debugging output, temporary failures, and duplicate fragments in diagnostics. Report deterministic write refusals once; preserve the source without probe writes or lossy rephrasing.

One Cloud MCP memory accepts up to 512 KiB of UTF-8 Markdown. Use `tokst_memory_update` to change title, content, tags, or any combination. Use `tokst_attach_file` for original source material through a ChatGPT file or public HTTPS URL up to 100 MB. Local paths and `file://` URLs are uploaded through the Dashboard attachment panel.

## Safety

Confirm the intended Workspace, Atlas, or memory ID before mutation. Require explicit user approval for access changes or broad archive. Use update, archive, restore, and audit tools to keep history traceable. Cloud MCP does not expose permanent memory deletion. Permanent cleanup is performed by the user from the Dashboard archived view after manual confirmation.
