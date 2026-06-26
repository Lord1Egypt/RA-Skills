# Error Recovery

| Error | Cause | Recovery |
|-------|-------|----------|
| `invalid ID argument` | Block ID doesn't exist or wrong format | Re-export `open-doc ... patchable --full`, verify block IDs before submitting |
| Document cleared | Submitted incomplete PMF, missing blocks treated as deletion | Use `open-doc ... patchable --full` to re-export full PMF and restore |
| Write guard error | No prior open-doc / open-section or read mark expired | Run `open-doc "docID" readable` (or `open-section`) then retry |
| Version conflict | Document modified by another client after read | `open-doc "docID" readable` to get latest version, then retry |
| PMF version conflict | Document modified after PMF export | `open-doc "docID" patchable --full` to re-export, save with `tee` |
| partial PMF rejected | Paginated/section PMF is incomplete | Use `update-block` for single-block edit, or `open-section` + `replace-section` for section edit |
| Read-only mode | Missing `SIYUAN_ENABLE_WRITE=true` | Add `SIYUAN_ENABLE_WRITE=true` prefix |
| Document title "Untitled" | `createDocWithMd` path parameter determines title | Use `create-doc` CLI (auto-sets title) or `rename-doc` to fix |
| Connection failed | SiYuan not running / wrong port / token | `node index.js check` to verify |
| Search returns empty | Keyword too short / no matches | Use `search-in-doc` to limit scope, or expand keyword context |
| Parallel write version conflict | Multiple independent Bash commands writing to the same document | Use a single JS script with sequential writes (see Pattern 8 in SKILL.md), or re-run `open-doc` before each write |
| `updateBlock` writes literal "markdown" | Called JS API with 3 args: `updateBlock(id, 'markdown', content)` | **`updateBlock` takes only 2 args**: `updateBlock(id, markdownContent)`. The string `'markdown'` was treated as content. Fix: delete corrupted block, re-insert correct content |
| `insertBlock 需要至少一个锚点参数` | Used wrong parameter names like `{ after: id }` | Use SiYuan native names: `{ previousID: id }` (insert after), `{ nextID: id }` (insert before), `{ parentID: id }` (append as child) |
