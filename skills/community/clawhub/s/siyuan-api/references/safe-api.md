# SiYuan Safe API Reference

This file is the default reference for the published `siyuan-api` skill.
It intentionally lists only the safer, in-scope API families for local note management.

## In Scope

### Notebook

- `/api/notebook/lsNotebooks`
- `/api/notebook/openNotebook`
- `/api/notebook/closeNotebook`
- `/api/notebook/createNotebook`
- `/api/notebook/removeNotebook`
- `/api/notebook/renameNotebook`

### Document and File Tree

- `/api/filetree/createDocWithMd`
- `/api/filetree/renameDoc`
- `/api/filetree/renameDocByID`
- `/api/filetree/removeDoc`
- `/api/filetree/removeDocByID`
- `/api/filetree/moveDocs`
- `/api/filetree/moveDocsByID`
- `/api/filetree/getHPathByPath`
- `/api/filetree/getHPathByID`
- `/api/filetree/getPathByID`
- `/api/filetree/getIDsByHPath`

### Block

- `/api/block/insertBlock`
- `/api/block/prependBlock`
- `/api/block/appendBlock`
- `/api/block/updateBlock`
- `/api/block/deleteBlock`
- `/api/block/moveBlock`
- `/api/block/getBlockInfo`
- `/api/block/getBlockAttrs`
- `/api/block/setBlockAttrs`

### Database / Attribute View

Use these for SiYuan database tables and database row/cell updates.

- `/api/av/getAttributeView`
- `/api/av/renderAttributeView`
- `/api/av/getAttributeViewKeys`
- `/api/av/getAttributeViewKeysByAvID`
- `/api/av/getAttributeViewKeysByID`
- `/api/av/setAttributeViewBlockAttr`
- `/api/av/batchSetAttributeViewBlockAttrs`

Allowed use:

- inspect a database schema and field IDs
- find a row/item by primary block value
- update clearly requested cells in an existing row
- batch update a small set of cells in one database

Avoid:

- broad or unreviewed database rewrites
- deleting database rows or keys unless the user explicitly asks
- deprecated `rowID` request fields; use `itemID`

Notes:

- Databases are Attribute Views; the database ID is the Attribute View ID (`avID`).
- Row updates require the row item's `itemID`, which is usually the `blockID` of the primary `block` value in `av.keyValues`.
- `renderAttributeView` is display-oriented. Grouped tables may have empty top-level `view.rows`; inspect `view.groups[*].rows` or use `getAttributeView` for storage-oriented lookup.
- Database cell text does not reliably support Markdown tables. Use newline-separated lines for multiple records or structured notes inside one field.
- Common update value shapes are `{ "text": { "content": "..." } }`, `{ "url": { "content": "https://..." } }`, `{ "number": { "content": 1, "isNotEmpty": true } }`, `{ "checkbox": { "checked": true } }`, and `{ "mSelect": [{ "content": "bulk", "color": "1" }] }`.

### Asset

- `/api/asset/upload`

### Export

- `/api/export/exportMdContent`

### Limited SQL

- `/api/query/sql`

Allowed use:

- read-oriented discovery
- small result sets
- metadata inspection

Avoid:

- mutation-heavy SQL
- large unbounded scans
- using SQL when a notebook/document/block API already exists

### Workspace File APIs

- `/api/file/getFile`
- `/api/file/putFile`
- `/api/file/removeFile`
- `/api/file/renameFile`
- `/api/file/readDir`

Use these only when the task is clearly about SiYuan workspace content or assets.

## Out of Scope

Do not use these APIs via this published skill:

- `/api/network/forwardProxy`
- `/api/convert/pandoc`

Also avoid any endpoint intended for:

- outbound internet proxying
- external command-style conversion
- broad system administration
- behavior outside local SiYuan workspace management

## Operating Rules

- Only target a local SiYuan server
- Never expose the API token
- Prefer structured APIs over raw file access
- Ask for confirmation before destructive file or document deletion
- Stay within the user's SiYuan workspace and note-management intent
