---
name: WorkOS
description: Connect OpenClaw and other AI agents to WorkOS — a self-hosted workspace platform with documents, databases, tasks, meeting transcription, and sharing. Exposes 60+ tools through a remote MCP server with OAuth 2.1.
version: 1.0.0
metadata:
  openclaw:
    skillKey: workos
    homepage: https://workos.no/for-agenter
    emoji: "🧠"
    requires:
      env: []
      bins: []
---

# WorkOS

WorkOS is a self-hosted, AI-integrated workspace platform (a Notion
alternative) that exposes its full data model through a remote MCP server.
Use this skill whenever the user talks about their **documents, pages, wiki,
databases, tasks, meetings, transcripts**, or wants the agent to **create,
update, or search** their content on `workos.no`.

## When to use WorkOS

Reach for this skill when the user:

- Refers to "my wiki", "my workspace", "my page", "my database", "my tasks", "my meetings", "my notes".
- Says things like "create a new page about …", "add a task", "update the status field on row X", "find the document about …".
- Wants to search or fetch existing content on workos.no.
- Asks about transcripts, summaries, or attendees from meetings.
- Wants to share a page externally or manage access.

If the user has not yet connected the WorkOS MCP server, **set up the
connection first** (see `docs/connect.md`).

## Connection — once per agent

The WorkOS MCP server lives at:

```
https://workos.no/api/mcp
```

- **Transport:** Streamable HTTP (JSON-RPC 2.0). Not SSE.
- **Auth:** OAuth 2.1 with PKCE — fully automatic via client discovery.
- **Scopes:** `read`, `write`.

OpenClaw and other MCP clients are configured with the URL above and let the
OAuth flow happen in the system browser. Per-client setup is in
[`docs/connect.md`](docs/connect.md). Important: older Cline versions must
set `"type": "streamableHttp"` — the server does not support SSE.

## What the agent can do

After connecting, the server exposes ~60 tools grouped as follows:

| Area | Example tools | Use for |
|---|---|---|
| Account | `get_me`, `list_workspaces`, `get_workspace` | Identity and workspace context |
| Pages | `create_page`, `get_page`, `update_page`, `archive_page`, `restore_page`, `delete_page`, `move_page`, `search_pages`, `list_pages` | Documents, wiki, notes |
| Page blocks | `append_blocks`, `insert_blocks_after`, `update_block`, `delete_blocks` | Granular editing |
| Page groups | `create_page_group`, `update_page_group`, `delete_page_group`, `reorder_page_groups`, `list_page_groups` | Sidebar organization |
| Databases | `list_databases`, `create_database`, `get_database`, `update_database`, `delete_database` | Structured data |
| Properties | `add_db_property`, `update_db_property`, `remove_db_property`, `reorder_db_properties` | Schema |
| Rows | `list_db_rows`, `create_db_row`, `update_db_cell`, `delete_db_row`, `move_db_row` | Content |
| Views | `list_db_views`, `create_db_view`, `update_db_view`, `delete_db_view` | Table / board / list |
| Meetings | `create_meeting`, `append_transcript`, `generate_meeting_summary`, `list_meeting_templates` | Transcription + AI summary |
| Comments | `create_comment`, `update_comment`, `resolve_comment`, `list_comments`, `delete_comment` | Discussion |
| Sharing | `create_share_link`, `list_share_links`, `revoke_share_link` | External links |
| Files | `upload_image` | Image uploads |

The full catalog is in [`docs/tools.md`](docs/tools.md). Always call
`tools/list` after `initialize` to get the authoritative, current set.

## Workflow patterns

Common flows (full examples in [`docs/workflows.md`](docs/workflows.md)):

1. **Search → fetch → show**: `search_pages` → `get_page` → present content.
2. **Create page with structure**: `create_page` (with the right `workspaceId`
   and `pageGroupId`) → `append_blocks` for content.
3. **Database update**: `list_databases` → `list_db_rows` (filtered) →
   `update_db_cell` per row.
4. **Meeting flow**: `create_meeting` → `append_transcript` (in chunks) →
   `generate_meeting_summary`.
5. **Safe edits**: fetch existing content before overwriting, and confirm
   destructive operations (delete, archive) with the user.

## Rules and expectations

- **Workspace context first.** If the user has not specified a workspace,
  call `list_workspaces` and ask which one is active before writing data.
- **Never guess IDs.** Always fetch them from a list/search call.
- **Write conservatively.** Prefer `update_*` over delete-and-recreate.
  Confirm deletes/archives before running them.
- **Mirror the user's language.** WorkOS users are often Norwegian; mirror
  whatever language the user is writing in for new pages and comments.
- **Respect roles.** `read` scope only allows fetching. If a write tool
  returns 403, tell the user they lack `write` access in the workspace.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| 401 from `/api/mcp` | Token expired or missing | The client should refresh automatically; otherwise remove the server and re-add it |
| 405 on GET | Client is trying SSE | Use Streamable HTTP — set `type: streamableHttp` (Cline) or upgrade the client |
| Empty workspace list | User is not a member of any workspace | Have the user create or join a workspace at workos.no first |
| 403 on write tools | Missing `write` scope | Re-run the OAuth flow with `read write` |

More in [`docs/connect.md`](docs/connect.md) under "Troubleshooting".

## Links

- For agents (public docs): https://workos.no/for-agenter
- Homepage: https://workos.no
- Support: hello@workos.no
