# Command Reference

All commands: `node index.js {command} [args]`

**Prerequisite**: cwd must be the skill directory (where `index.js` is located).

---

## Read Commands

### search — Search notes

```bash
node index.js search {keyword} [limit] [type]
```

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| keyword | Yes | | Search term |
| limit | No | 20 | Result count (1-200) |
| type | No | all | `p` paragraph `h` heading `l` list `c` code `d` document `t` table |

Flexible parameter order: `search "AI" 10 h` or `search "AI" h` (omit limit to use default 20)

**Returns**: Formatted text, one result per line with block ID, content, type, time

---

### search-md — Search with Markdown output

```bash
node index.js search-md {keyword} [limit] [type]
```

Same parameters as `search`. **Returns**: Full Markdown page format

---

### open-doc — Open document

```bash
node index.js open-doc {docID} [readable|patchable] [--full] [--cursor {blockID}] [--limit-chars {N}] [--limit-blocks {N}]
```

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| docID | Yes | | Document block ID |
| view | No | readable | `readable` = clean Markdown; `patchable` = PMF format |
| --full | No | | Skip truncation/pagination, output full document |
| --cursor | No | | Patchable pagination start block ID |
| --limit-chars | No | 15000 | Readable view character truncation threshold (1000-1000000) |
| --limit-blocks | No | 50 | Patchable view blocks per page (5-10000) |

**Returns**:
- `readable`: YAML header + Markdown body. Long docs auto-truncate to `--limit-chars` with heading outline
- `patchable`: PMF format with block IDs. Long docs auto-paginate, header includes `partial=true next_cursor={blockID}`

**Side effect**: Marks document as "read" and records version snapshot (satisfies write precondition)

**Environment variables**:
- `SIYUAN_OPEN_DOC_CHAR_LIMIT`: Override default character truncation threshold
- `SIYUAN_OPEN_DOC_BLOCK_PAGE_SIZE`: Override default blocks per page

---

### open-section — Read section

```bash
node index.js open-section {headingBlockID} [readable|patchable]
```

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| headingBlockID | Yes | | Must be a heading block (type=h) |
| view | No | readable | `readable` = Markdown; `patchable` = PMF format |

**Returns**:
- `readable`: YAML header (with scope: section) + Markdown of all blocks under the heading
- `patchable`: PMF format (header has `partial=true section={headingBlockID}`)

**Side effect**: Marks document as "read"

**Note**: Patchable PMF is marked `partial=true`, cannot be used for apply-patch. Use `replace-section` or `update-block` for editing.

---

### search-in-doc — Search within document

```bash
node index.js search-in-doc {docID} {keyword} [limit]
```

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| docID | Yes | | Document to search |
| keyword | Yes | | Search keyword |
| limit | No | 20 | Result count (1-200) |

**Returns**: Formatted text with block ID, content, type, time

Ideal for quickly locating content in long documents without reading the whole thing.

---

### notebooks — List notebooks

```bash
node index.js notebooks
```

No parameters. **Returns**: Numbered list with notebook name, ID, closed status

---

### docs — List documents

```bash
node index.js docs [notebookID] [limit]
```

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| notebookID | No | all | Filter by notebook |
| limit | No | 200 | Result count (1-2000) |

**Returns**: Formatted text with document ID (e.g., `[20260206204419-vgvxojw]`)

---

### headings — Document headings

```bash
node index.js headings {docID} [level]
```

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| docID | Yes | | |
| level | No | all | `h1`/`h2`/`h3`/`h4`/`h5`/`h6` (string format, not number) |

---

### blocks — Document child blocks

```bash
node index.js blocks {docID} [type]
```

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| docID | Yes | | |
| type | No | all | `p`/`h`/`l`/`t`/`c` etc. |

**Returns**: Formatted text with block ID (e.g., `[20260206204442-j76ycfo]`), usable as anchors for append-block / insert-block.

Image blocks are marked with `[img]` in the summary.

---

### Other read commands

| Command | Signature | Description |
|---------|-----------|-------------|
| `doc-children` | `{notebookID} [path]` | List child documents |
| `doc-tree` | `{notebookID} [path] [depth]` | Document tree (default depth 4) |
| `doc-tree-id` | `{docID} [depth]` | Document tree by doc ID |
| `tag` | `{tagName}` | Search by tag |
| `backlinks` | `{blockID}` | Backlinks |
| `tasks` | `[status] [days]` | Tasks (`[ ]`/`[x]`/`[-]`, default 7 days) |
| `daily` | `{start} {end}` | Daily Notes (YYYYMMDD) |
| `attr` | `{name} [value]` | Query by attribute (`custom-` prefix for custom attrs) |
| `bookmarks` | `[name]` | Bookmarks |
| `random` | `{docID}` | Random heading |
| `recent` | `[days] [type]` | Recent changes (default 7 days) |
| `unreferenced` | `{notebookID}` | Unreferenced documents |
| `check` | | Connection check |
| `version` | | Kernel version |
| `version-check` | | Skill version check |

---

## Write Commands

**All write commands require**:
1. `SIYUAN_ENABLE_WRITE=true` (env var or command prefix)
2. Prior `open-doc` or `open-section` of the target document
3. Document must not have been modified by another client since reading

**Exceptions**: `create-doc` and `rename-doc` do not require prior `open-doc`

---

### create-doc — Create document

```bash
SIYUAN_ENABLE_WRITE=true node index.js create-doc {notebookID} {title}
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| notebookID | Yes | Target notebook |
| title | Yes | Document title |
| stdin | No | Initial content (Markdown via stdin) |

```bash
# Empty document
SIYUAN_ENABLE_WRITE=true node index.js create-doc "notebookID" "My Doc"

# With initial content
printf '## Section 1\nContent' | SIYUAN_ENABLE_WRITE=true node index.js create-doc "notebookID" "My Doc"
```

---

### rename-doc — Rename document

```bash
SIYUAN_ENABLE_WRITE=true node index.js rename-doc {docID} {newTitle}
```

Automatically resolves notebook and path from doc ID.

---

### update-block — Update block content (auto-split support)

```bash
printf 'new content' | SIYUAN_ENABLE_WRITE=true node index.js update-block {blockID}
```

Content via stdin only. If content parses as multiple blocks, automatically performs "first block update + subsequent inserts" with post-write verification.

---

### delete-block — Delete single block

```bash
SIYUAN_ENABLE_WRITE=true node index.js delete-block {blockID}
```

---

### append-block — Append content

```bash
printf 'content' | SIYUAN_ENABLE_WRITE=true node index.js append-block {parentID}
```

`parentID` can be a document ID (append to end) or heading block ID (append to section).

---

### insert-block — Insert at position

```bash
printf 'content' | SIYUAN_ENABLE_WRITE=true node index.js insert-block --before {blockID}
printf 'content' | SIYUAN_ENABLE_WRITE=true node index.js insert-block --after {blockID}
printf 'content' | SIYUAN_ENABLE_WRITE=true node index.js insert-block --parent {blockID}
```

Three anchor modes: `--before` (insert before), `--after` (insert after), `--parent` (append as child).

---

### replace-section — Replace section content

```bash
printf 'new content' | SIYUAN_ENABLE_WRITE=true node index.js replace-section {headingID}
SIYUAN_ENABLE_WRITE=true node index.js replace-section {headingID} --clear
```

Deletes all blocks under the heading, then appends new content. **The heading block itself is preserved** — do not repeat the heading in your new content.

---

### apply-patch — Apply PMF patch

```bash
cat /tmp/doc.pmf | SIYUAN_ENABLE_WRITE=true node index.js apply-patch {docID}
```

Supports: update / delete / reorder / insert. PMF must be complete (missing blocks = deletion). Partial PMF is rejected.

See [[PMF Spec]] for details.

---

### move-docs-by-id — Move documents

```bash
SIYUAN_ENABLE_WRITE=true node index.js move-docs-by-id {targetID} {sourceIDs}
```

Requires prior `open-doc` of target AND all source documents.

---

## JS API (node -e / script)

For operations not covered by CLI, or for batch editing multiple blocks in a single process.

### Function Signatures

**⚠️ JS API 签名与 CLI 参数不同，不要混淆。**

| Function | Signature | Description |
|----------|-----------|-------------|
| `openDocument` | `(docId: string, mode: 'readable'\|'patchable') → Promise` | 读取文档（标记已读，刷新版本号） |
| `updateBlock` | `(id: string, markdown: string) → Promise` | 更新块内容。**仅 2 个参数**，不要传 dataType |
| `deleteBlock` | `(id: string) → Promise` | 删除单个块 |
| `insertBlock` | `(markdown: string, anchors: { previousID?, nextID?, parentID? }) → Promise` | 在锚点位置插入。锚点参数名是 `previousID`/`nextID`/`parentID`，**不是** `after`/`before`/`parent` |
| `appendMarkdownToBlock` | `(parentID: string, markdown: string) → Promise` | 在父块末尾追加内容 |
| `executeSiyuanQuery` | `(sql: string) → Promise<Array>` | 执行 SQL 查询 |
| `getChildBlocks` | `(id: string) → Promise<Array>` | 获取子块列表 |
| `createDocWithMd` | `(notebookID: string, path: string, markdown: string) → Promise` | 创建文档（path 决定标题） |
| `formatResults` | `(rows: Array) → string` | 格式化查询结果为文本 |

### Common Gotchas

1. **`updateBlock` 只有 2 个参数** `(id, markdown)`。不要写 `updateBlock(id, 'markdown', content)` — 这会把字符串 `'markdown'` 当作内容写入，**破坏块数据**
2. **`insertBlock` 的锚点参数名** 是 SiYuan API 原生的 `previousID`/`nextID`/`parentID`，不是 CLI 的 `--after`/`--before`/`--parent`
3. **写入前必须 `openDocument`** 刷新版本号。在同一进程内连续写入时，每次写入前都要调用
4. **所有写入函数** 需要环境变量 `SIYUAN_ENABLE_WRITE=true`

### Examples

```bash
# SQL query
node -e "const s = require('./index.js'); s.executeSiyuanQuery('SELECT * FROM blocks WHERE type=\"d\" LIMIT 5').then(r => console.log(s.formatResults(r)));"

# Get child blocks
node -e "const s = require('./index.js'); s.getChildBlocks('docID').then(r => console.log(JSON.stringify(r, null, 2)));"

# Create sub-document
SIYUAN_ENABLE_WRITE=true node -e "const s = require('./index.js'); s.createDocWithMd('notebookID', '/Parent/ChildTitle', '# Content').then(r => console.log(JSON.stringify(r)));"

# Batch edit (single process, sequential)
SIYUAN_ENABLE_WRITE=true node -e "
const s = require('./index.js');
(async () => {
  await s.openDocument('docID', 'readable');
  await s.updateBlock('blockID1', '新内容1');
  await s.openDocument('docID', 'readable');
  await s.updateBlock('blockID2', '新内容2');
  await s.openDocument('docID', 'readable');
  await s.insertBlock('插入内容', { previousID: 'anchorID' });
  console.log('All done');
})();
"
```
