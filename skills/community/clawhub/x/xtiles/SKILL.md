---
name: xtiles
description: Create and manage structured visual pages, projects, tiles, tasks and workflows in xTiles via MCP.
homepage: https://xtiles.app
license: MIT-0
metadata:
  openclaw:
    category: productivity
    tags: [notes, tasks, projects, visual-workspace, mcp]
---

# xTiles

xTiles is a visual workspace for notes, projects, and tasks. This skill connects
the hosted xTiles MCP server and tells the agent when and how to use its tools.

## Setup (one-time)

Connect the remote xTiles MCP server, then sign in via OAuth:

    openclaw mcp add xtiles \
      --url https://mcp.xtiles.app/mcp \
      --transport streamable-http \
      --auth oauth
    openclaw mcp login xtiles
    openclaw mcp doctor xtiles --probe

Once connected, the xTiles tools become available to the agent.

## Authentication

- Flow: OAuth 2.0 authorization_code + PKCE (S256); Dynamic Client Registration supported.
- The connector operates only on the signed-in user's own xTiles workspace.
- Legacy: xTiles Personal Access Tokens (`xt_…`) are also accepted as bearer tokens.

## When to use

Use these tools when the user wants to read or edit their xTiles workspace:

- **projects** — create and manage projects
- **pages** — create and manage structured visual pages
- **tiles** — add and edit content tiles on a page
- **layout** — arrange the visual layout of a page
- **tasks** — create and manage tasks
- **collections** — group and organize items
- **planner** — planning / calendar views
- **workflows** — run multi-step content workflows
- **structure-information** — inspect the structure of a page/project
- **users** — current user context

## Write operations

Most tools are read-only. Some tools change the user's real xTiles workspace:
`create_*` add new projects, pages, tiles, or tasks; `update_task`,
`patch_view_content`, `set_page_description` and `set_page_layout` overwrite
existing content; and `delete_tasks` permanently removes tasks (irreversible).
Confirm intent before destructive actions and operate only on the resources the
user asked about.

## Notes for the agent

- For any task involving due dates or relative dates ("tomorrow", "next Monday",
  "end of week"), call `xtiles_get_user_timezone` first and resolve dates against
  the returned IANA timezone before creating or updating tasks.
- Before assembling a multi-step process by hand (setup, recurring digest/brief,
  onboarding, "have xTiles do X for me"), call `xtiles_list_workflows` first to
  check for a prepared recipe, then follow it via `xtiles_get_workflow`.
- Call `tools/list` on the endpoint for the exact tool names, parameters and JSON
  schemas — this skill lists capability groups, not individual tool signatures.
