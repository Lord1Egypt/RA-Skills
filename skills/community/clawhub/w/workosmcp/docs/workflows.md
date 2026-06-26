# Example flows

Practical patterns for common tasks. All examples assume OAuth has completed
and the MCP client has access to the tools.

## 1. Search → fetch → show

User asks: *"What did I write about the onboarding process?"*

```
search_pages({ query: "onboarding", workspaceId })
→ pick the top hit
get_page({ pageId })
→ present title + relevant excerpt
```

## 2. Create a page with structure

User asks: *"Create a page about the Q2 plan in the Strategy group."*

```
list_workspaces()                                  # confirm workspace
list_page_groups({ workspaceId })                  # find the "Strategy" id
create_page({ workspaceId, pageGroupId, title: "Q2 plan" })
append_blocks({ pageId, blocks: [
  { type: "heading", level: 1, text: "Q2 plan" },
  { type: "paragraph", text: "..." },
  { type: "bulletListItem", text: "Goal 1" },
  ...
]})
```

## 3. Update rows in a database

User asks: *"Mark all open tasks from last week as overdue."*

```
list_databases({ workspaceId })                    # find "Tasks"
get_database({ databaseId })                       # find property ids for Status, Due
list_db_rows({
  databaseId,
  filter: { and: [
    { property: statusId, equals: "OPEN" },
    { property: dueId, before: "2026-04-21" },
  ]},
  limit: 100,
})
for each row:
  update_db_cell({ rowId: row.id, propertyId: statusId, value: "OVERDUE" })
```

Confirm the count with the user before running mass updates.

## 4. Meeting flow

User has a meeting recording and wants a summary:

```
create_meeting({ workspaceId, title, startedAt })
# Send the transcript in chunks for larger recordings:
for each chunk:
  append_transcript({ meetingId, segments: [...] })
list_meeting_templates({ workspaceId })            # pick "Standup" or "Sales call"
generate_meeting_summary({ meetingId, templateId })
# The result is added as blocks on the linked page.
```

## 5. Safe edits to an existing page

Before overwriting:

```
get_page({ pageId })                               # load current blocks
# Show the user a diff or change suggestion
# After confirmation:
update_block({ blockId, ... }) or append_blocks(...)
```

Prefer `update_block` over `delete_blocks` + `append_blocks`.

## 6. Share a page externally

```
create_share_link({
  pageId,
  expiresAt: "2026-05-01T00:00:00Z",
  password: null,         # or string
})
→ returns { url, token }
# Show the URL to the user. Use revoke_share_link({ linkId }) to disable.
```

## 7. Image in a page

```
upload_image({ workspaceId, filename, dataBase64 })
→ { url }
append_blocks({ pageId, blocks: [
  { type: "image", url, caption: "..." }
]})
```

## General rules

1. **Fetch IDs from list/search calls**, never guess.
2. **Confirm destructive actions** (delete, archive, revoke) explicitly.
3. **Mirror the user's language** — many WorkOS users write in Norwegian.
4. **Tell the user what you did**: after a write, give a short confirmation
   with a page/row ID or URL.
