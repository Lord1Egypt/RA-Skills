# Lanhu MCP discovery notes

Session-derived notes for the xz01 workflow.

## What this Lanhu MCP exposes

The current `lanhu-mcp` service exposes project-scoped tools such as:

- `lanhu_resolve_invite_link`
- `lanhu_get_pages`
- `lanhu_get_designs`
- `lanhu_get_design_slices`
- `lanhu_get_ai_analyze_page_result`
- `lanhu_get_ai_analyze_design_result`
- `lanhu_say`, `lanhu_say_list`, `lanhu_say_detail`, `lanhu_say_edit`, `lanhu_say_delete`
- `lanhu_get_members`

## Important limitation

There is **no account-wide project enumeration tool** in this MCP setup. In practice:

- you cannot ask the MCP to list all projects owned by the account
- to inspect a project, you must start from a share/invite link or a known `tid/pid`
- once a project URL is available, use the page/design/slice tools against that specific project

## Practical workflow

1. Ask the user for a Lanhu project link when the target project is unknown.
2. If the user has only an invite/share link, resolve it first.
3. Use the resolved project URL for page/design extraction.
4. Do not promise an account-wide catalog unless the MCP gains a new tool for it later.
