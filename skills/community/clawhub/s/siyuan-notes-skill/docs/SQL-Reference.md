# SQL Reference

SiYuan uses SQLite. Default query limit: 64 rows.

## Main Tables

### blocks — All content blocks

| Field | Type | Description |
|-------|------|-------------|
| id | TEXT | Block ID `YYYYMMDDHHmmss-xxxxxxx` |
| parent_id | TEXT | Parent container ID |
| root_id | TEXT | Document root ID |
| hash | TEXT | Content hash |
| box | TEXT | Notebook ID |
| path | TEXT | Document path |
| hpath | TEXT | Human-readable path |
| name | TEXT | Block name |
| alias | TEXT | Alias |
| memo | TEXT | Memo |
| tag | TEXT | Tags (comma-separated) |
| content | TEXT | Plain text content |
| fcontent | TEXT | Formatted content |
| markdown | TEXT | Markdown content |
| length | INTEGER | Content length |
| type | TEXT | Block type |
| subtype | TEXT | Subtype |
| ial | TEXT | Inline attributes |
| sort | INTEGER | Sort order |
| created | TEXT | Creation time `YYYYMMDDHHmmss` |
| updated | TEXT | Update time `YYYYMMDDHHmmss` |

**Block types** (from SiYuan kernel `treenode/node.go`):

| Code | Node Type | Description |
|------|-----------|-------------|
| `d` | NodeDocument | Document |
| `h` | NodeHeading | Heading |
| `p` | NodeParagraph | Paragraph |
| `l` | NodeList | List (container) |
| `i` | NodeListItem | List item (container) |
| `c` | NodeCodeBlock | Code block |
| `m` | NodeMathBlock | Math block |
| `t` | NodeTable | **Table** (atomic block; internal cells have no block ID) |
| `b` | NodeBlockquote | Blockquote (container) |
| `s` | NodeSuperBlock | Super block (container) |
| `tb` | NodeThematicBreak | **Thematic break** (`---`). ⚠️ NOT "table body"! |
| `html` | NodeHTMLBlock | HTML block |
| `av` | NodeAttributeView | Attribute view (database) |

**Heading subtypes**: `h1`, `h2`, `h3`, `h4`, `h5`, `h6`

**List subtypes**: `u` unordered, `t` todo, `o` ordered

---

### refs — Block references (links)

| Field | Description |
|-------|-------------|
| id | Reference ID |
| block_id | Source block |
| root_id | Source document |
| box | Notebook |
| path | Document path |
| def_block_id | Definition block (target) |
| def_block_root_id | Definition document |
| def_block_box | Definition notebook |
| def_block_path | Definition path |

---

### attributes — Custom attributes

| Field | Description |
|-------|-------------|
| id | Attribute ID |
| block_id | Block ID |
| root_id | Document ID |
| box | Notebook |
| path | Document path |
| name | Attribute name |
| value | Attribute value |
| type | `block` |
| block_type | Block type |

---

## Query Examples

### Find documents by title

```sql
SELECT id, content, hpath, updated
FROM blocks
WHERE type = 'd' AND content LIKE '%Project Summary%'
ORDER BY updated DESC
LIMIT 10
```

### Find headings in document

```sql
SELECT id, content, subtype, updated
FROM blocks
WHERE root_id = 'docID' AND type = 'h'
ORDER BY sort ASC
```

### Find recent blocks

```sql
SELECT id, type, content, updated
FROM blocks
WHERE type != 'd'
ORDER BY updated DESC
LIMIT 20
```

### Find blocks created today

```sql
SELECT * FROM blocks
WHERE created >= strftime('%Y%m%d%H%M%S', 'now', 'start of day', 'localtime')
ORDER BY created DESC
```

### Find blocks by date range

```sql
SELECT * FROM blocks
WHERE created BETWEEN '20250101000000' AND '20250131235959'
ORDER BY created DESC
```

### Find backlinks

```sql
SELECT * FROM refs
WHERE def_block_id = 'blockID'
```

### Find references from a block

```sql
SELECT * FROM refs
WHERE block_id = 'blockID'
```

### Find blocks by attribute

```sql
SELECT b.* FROM blocks b
JOIN attributes a ON b.id = a.block_id
WHERE a.name = 'custom-priority' AND a.value = 'high'
```

### Find untagged documents

```sql
SELECT id, content, hpath
FROM blocks
WHERE type = 'd' AND (tag = '' OR tag IS NULL)
```

### Content length statistics

```sql
SELECT type, COUNT(*), AVG(length), SUM(length)
FROM blocks
GROUP BY type
ORDER BY COUNT(*) DESC
```

---

## JS API

```javascript
const s = require('./index.js');

// Execute query
s.executeSiyuanQuery('SELECT * FROM blocks WHERE type="d" LIMIT 5')
  .then(rows => console.log(s.formatResults(rows)));
```

---

## Time Format

All timestamps: `YYYYMMDDHHmmss` (14 digits, no separators)

SQLite functions:
- `strftime('%Y%m%d%H%M%S', 'now', 'localtime')` — current time
- `strftime('%Y%m%d%H%M%S', 'now', 'start of day', 'localtime')` — start of today
- `strftime('%Y%m%d%H%M%S', 'now', '-7 days', 'localtime')` — 7 days ago
