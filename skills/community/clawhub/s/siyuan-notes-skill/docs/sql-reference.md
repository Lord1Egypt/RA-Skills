# SiYuan SQL Reference

SiYuan uses SQLite. Default result limit is 64 rows unless you specify `LIMIT`.

## Table: blocks

| Column | Description | Example |
|--------|-------------|---------|
| `id` | Block ID | `20210104091228-d0rzbmm` |
| `parent_id` | Parent block ID | same format |
| `root_id` | Document block ID | same format |
| `box` | Notebook ID | same format |
| `path` | File path | `/20200812220555-lj3enxa/20200825162036-4dx365o.sy` |
| `hpath` | Human-readable path | `/请从这里开始/编辑器/排版元素` |
| `name` | Block name | |
| `alias` | Block alias | |
| `memo` | Block memo | |
| `tag` | Tags | `#标签1 #标签2#` |
| `content` | Plain text (no Markdown markers) | |
| `fcontent` | First child content (containers) | |
| `markdown` | Full Markdown text | |
| `length` | Length of `markdown` | |
| `type` | Block type (see below) | `p` |
| `subtype` | Block subtype (see below) | `h2` |
| `ial` | Inline attributes | `{: id="..." updated="..."}` |
| `sort` | Sort weight (lower = earlier) | |
| `created` | Created time `YYYYMMDDHHmmss` | `20210104091228` |
| `updated` | Updated time `YYYYMMDDHHmmss` | `20210104091228` |

### Block types (`type`)

| Value | Meaning |
|-------|---------|
| `d` | Document |
| `h` | Heading |
| `p` | Paragraph |
| `l` | List |
| `i` | List item |
| `b` | Blockquote |
| `s` | Super block |
| `c` | Code block |
| `m` | Math block |
| `t` | Table |
| `av` | Attribute view (database) |

### Block subtypes (`subtype`)

- Headings: `h1` through `h6`
- Lists: `u` (unordered), `t` (task), `o` (ordered)

### Block hierarchy

- **Leaf blocks** (`p`, `h`, `c`, `m`, `t`): Contain content directly
- **Container blocks** (`l`, `i`, `b`, `s`): Contain other blocks; `parent_id` points to the container
- **Document block** (`d`): Root of a document; `root_id` points here; `content` = document title

## Table: refs

| Column | Description |
|--------|-------------|
| `id` | Reference ID |
| `def_block_id` | Referenced (target) block ID |
| `def_block_root_id` | Document ID of the referenced block |
| `def_block_path` | Document path of the referenced block |
| `block_id` | Block that contains the reference |
| `root_id` | Document ID of the referencing block |
| `box` | Notebook ID |
| `path` | Document path |
| `content` | Anchor text |

## Table: attributes

| Column | Description |
|--------|-------------|
| `id` | Attribute ID |
| `name` | Attribute name (user-defined attrs have `custom-` prefix) |
| `value` | Attribute value |
| `type` | Type (e.g. `b`) |
| `block_id` | Block ID |
| `root_id` | Document ID |
| `box` | Notebook ID |
| `path` | Document path |

## Special concepts

### Daily Notes

Daily notes are document blocks (`type='d'`) with attribute `custom-dailynote-YYYYMMDD=YYYYMMDD`. To query content *inside* a daily note, join via `root_id`.

### Bookmarks

Blocks with attribute `bookmark={name}` appear in the corresponding bookmark group.

## Query examples

```sql
-- All documents
SELECT * FROM blocks WHERE type='d'

-- H2 headings
SELECT * FROM blocks WHERE subtype='h2'

-- Sub-documents of a document
SELECT * FROM blocks WHERE path LIKE '%/{docID}/%' AND type='d'

-- Search paragraphs by keyword
SELECT * FROM blocks WHERE markdown LIKE '%关键词%' AND type='p'
ORDER BY updated DESC

-- Incomplete tasks in last 7 days
SELECT * FROM blocks
WHERE type='l' AND subtype='t'
  AND created BETWEEN strftime('%Y%m%d%H%M%S', datetime('now', '-7 day')) AND '99991231235959'
  AND markdown LIKE '* [ ] %'
  AND parent_id NOT IN (SELECT id FROM blocks WHERE subtype='t')

-- Backlinks of a block
SELECT * FROM blocks WHERE id IN (
  SELECT block_id FROM refs WHERE def_block_id='{blockID}'
) LIMIT 999

-- Daily notes in a date range
SELECT DISTINCT B.* FROM blocks AS B
JOIN attributes AS A ON B.id = A.block_id
WHERE A.name LIKE 'custom-dailynote-%' AND B.type='d'
  AND A.value BETWEEN '20231010' AND '20231013'
ORDER BY A.value DESC

-- Unreferenced documents in a notebook
SELECT * FROM blocks AS B
WHERE B.type='d' AND box='{notebookID}'
  AND B.id NOT IN (SELECT DISTINCT def_block_id FROM refs)
ORDER BY updated DESC LIMIT 128
```
