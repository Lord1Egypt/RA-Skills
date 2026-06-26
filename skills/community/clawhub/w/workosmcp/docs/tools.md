# Tool catalog

Always call `tools/list` after `initialize` for the authoritative list — the
table below may lag. Tools are grouped by topic.

## Account and workspace

| Tool | Purpose |
|---|---|
| `get_me` | Logged-in user (id, name, email, role) |
| `list_workspaces` | All workspaces the user belongs to |
| `get_workspace` | Detailed info about one workspace |
| `list_workspace_members` | Members and roles |

## Pages (documents, wiki, notes)

| Tool | Purpose |
|---|---|
| `list_pages` | Pages in a workspace or group |
| `search_pages` | Full-text search |
| `get_page` | Fetch one page with blocks |
| `create_page` | Create page (workspaceId, optional pageGroupId, parentPageId) |
| `update_page` | Change title, icon, group |
| `move_page` | Move between groups / hierarchy |
| `archive_page` | Soft delete (recoverable) |
| `restore_page` | Restore archived |
| `delete_page` | Permanent delete |

## Page blocks (content)

| Tool | Purpose |
|---|---|
| `append_blocks` | Append blocks to the end of a page |
| `insert_blocks_after` | Insert after a given block ID |
| `update_block` | Edit one block |
| `delete_blocks` | Delete multiple blocks |

Blocks use the BlockNote schema (heading, paragraph, bulletListItem,
numberedListItem, table, code, image, …). Call `get_page` to inspect the
current structure before editing.

## Page groups (sidebar organization)

| Tool | Purpose |
|---|---|
| `list_page_groups` | Groups in a workspace |
| `create_page_group` | New group |
| `update_page_group` | Name / icon |
| `delete_page_group` | Delete (pages move to ungrouped) |
| `reorder_page_groups` | Change order |

## Databases

| Tool | Purpose |
|---|---|
| `list_databases` | Databases in a workspace |
| `create_database` | New database (with starting schema) |
| `get_database` | Schema + views |
| `update_database` | Name, description |
| `delete_database` | Delete |

### Properties

| Tool | Purpose |
|---|---|
| `add_db_property` | New property (TITLE, TEXT, NUMBER, SELECT, MULTI_SELECT, DATE, CHECKBOX, URL, EMAIL, PHONE, USER, RELATION, FILE) |
| `update_db_property` | Rename / config |
| `remove_db_property` | Delete property |
| `reorder_db_properties` | Reorder |

### Rows

| Tool | Purpose |
|---|---|
| `list_db_rows` | Fetch rows (filter, sort, pagination) |
| `create_db_row` | New row |
| `update_db_cell` | Set value in one cell |
| `delete_db_row` | Delete row |
| `move_db_row` | Move between databases / position |

### Views

| Tool | Purpose |
|---|---|
| `list_db_views` | Views in a database |
| `create_db_view` | New TABLE / BOARD / LIST / GALLERY view |
| `update_db_view` | Filters, sort, visible properties |
| `delete_db_view` | Delete view |

### Import

| Tool | Purpose |
|---|---|
| `import_table_to_database` | Convert a block-level table into a database |

## Meetings

| Tool | Purpose |
|---|---|
| `list_meeting_templates` | Templates for transcription / summary |
| `create_meeting` | New meeting (linked to a page) |
| `append_transcript` | Append transcript segments |
| `generate_meeting_summary` | AI summary using a template |

## Comments

| Tool | Purpose |
|---|---|
| `list_comments` | Comments on page / block / row |
| `create_comment` | New comment (starts a thread) |
| `update_comment` | Edit |
| `resolve_comment` | Mark as resolved |
| `delete_comment` | Delete |

## Sharing

| Tool | Purpose |
|---|---|
| `list_share_links` | Active external links |
| `create_share_link` | New link (read-only / password / expiry) |
| `revoke_share_link` | Disable a link |

## Files

| Tool | Purpose |
|---|---|
| `upload_image` | Upload an image for use in blocks (returns URL) |

## Conventions

- **IDs** are strings (cuid). Never construct them by hand.
- **`workspaceId`** is required on most write tools. Get it from
  `list_workspaces` or context.
- **Dates** are ISO-8601 in UTC.
- **Pagination** uses `cursor` (opaque) + `limit` (default 50, max 100).
- **Errors** follow JSON-RPC: `error.code` and `error.message`. Common
  codes: -32601 (unknown method), -32602 (bad params), -32603 (internal
  error), 401 (unauthorized), 403 (missing scope/role).
