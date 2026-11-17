# Reporting RAGFlow results

Use this reference when summarizing operational results. Match the user's requested format; keep raw `--json` for automation or when explicitly requested.

- **Resources:** report the name, exact ID when needed for a subsequent action, and the affected dataset/document/session. Distinguish the returned page count from the server's total; do not present one page as a complete inventory.
- **Retrieval:** report source filenames and relevant excerpts with server similarity scores. Preserve the 0–1 scale or explicitly label a percentage conversion. `chunks.length` is the returned count; `total` is the server total. Empty results do not prove the source lacks the information.
- **Parsing:** preserve `UNSTART`, `RUNNING`, `CANCEL`, `DONE`, `FAIL`, or `SCHEDULE` as returned. A submitted task is not a completed parse. Report failures and timeouts with the affected IDs.
- **Models:** include provider and instance, and use the returned `identifier` for follow-up operations. `configured` means present in the catalog, not a verified working connection.
- **Files:** report saved path, MIME type, and size. Do not paste base64 file content into a normal user-facing response.
- **Graphs:** distinguish total entities/relations from returned entities/relations; filtering or limits can make these counts differ.
- **Chat and agents:** present the answer and actual returned citations. Retain session IDs for continuation. Do not invent references when none were returned.
- **Errors:** report the failed operation, server code/message, relevant target, and a specific next step. Do not claim success after an error or conceal partial failures.
- **Secrets and embeds:** omit API keys, provider credentials, token/beta values, and URLs or HTML containing `auth=` unless the user explicitly requests those values. Describe the chat/agent, mode, session, and whether embed setup succeeded.
