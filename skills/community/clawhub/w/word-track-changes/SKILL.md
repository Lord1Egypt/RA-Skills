---
name: word-track-changes
description: Enable Microsoft Word's Track Changes (修订模式) on documents using native OOXML elements. Supports cross-run text matching and precise paragraph-level replacement. Use when agents need to modify Word documents with tracked changes that show up as insertions (green) and deletions (red strikethrough) in Word's Review pane. Handles real-world DOCX files where text is split across multiple w:t nodes.
---

# Word Track Changes Skill

Enable native Microsoft Word Track Changes functionality using OpenXML. **Handles real-world DOCX files** where text is split across multiple `<w:t>` nodes.

## When to Use

Use this skill when you need to:
- Edit a Word document while preserving a visible record of changes
- Show insertions as green underlined text
- Show deletions as red strikethrough text
- Allow users to accept/reject changes in Word's Review pane
- Replace text that may be split across multiple `<w:r>` / `<w:t>` elements

## Quick Start

### 1. Enable Track Changes on a Document

```bash
python ~/.openclaw/skills/word-track-changes/scripts/enable_tracking.py input.docx output.docx
```

### 2. Replace Text with Revision Mark

```python
from track_changes import TrackChangesProcessor

p = TrackChangesProcessor("document.docx")
p.set_author("Agent")
p.replace_text_with_revision(
    old_text="existing text to replace",
    new_text="new text with revision mark"
)
p.save("output.docx")
p.cleanup()
```

### 3. Insert a New Paragraph with Revision Mark

```python
from track_changes import TrackChangesProcessor

p = TrackChangesProcessor("document.docx")
p.set_author("Agent")
p.insert_paragraph_after(
    search_text="text before new paragraph",
    new_text="New paragraph shown as insertion."
)
p.save("output.docx")
p.cleanup()
```

### 4. Batch Multiple Revisions

```python
from track_changes import batch_revisions

revisions = [
    {"type": "replace", "old": "old text 1", "new": "new text 1"},
    {"type": "insert_after", "search": "anchor text", "new": "inserted paragraph"},
]

batch_revisions(
    "input.docx",
    revisions,
    author="Agent",
    output_path="output.docx"
)
```

## Key Capabilities

| Capability | Description |
|------------|-------------|
| **Cross-Run Matching** | Finds text even when Word splits it across multiple `<w:t>` nodes |
| **Paragraph-Level Precision** | Only replaces the target text within its paragraph, preserving all other content |
| **Format Preservation** | Copies existing run properties (`<w:rPr>`) for consistent font/style |
| **Batch Revisions** | Apply multiple tracked changes in a single pass |
| **Track Changes Settings** | Automatically enables `trackRevisions` in `settings.xml` |

## Technical Details

### OOXML Elements Used

- `<w:ins>` — Insertion mark (green, underlined)
- `<w:del>` — Deletion mark (red strikethrough)
- `<w:delText>` — Deleted text content

### Architecture

```
DOCX (ZIP archive)
├── word/document.xml      ← Main content (modified with revision marks)
├── word/settings.xml      ← Track changes settings (updated if needed)
└── ...
```

The processor:
1. Unzips the DOCX into a temporary directory
2. Parses `word/document.xml`
3. Builds a paragraph-level text index to locate target text across split `<w:t>` nodes
4. Inserts `<w:ins>` / `<w:del>` at the exact position
5. Re-zips into a valid DOCX

## Scripts Reference

All scripts are in `scripts/` directory:

| Script | Purpose |
|--------|---------|
| `track_changes.py` | Core library with `TrackChangesProcessor` |
| `enable_tracking.py` | CLI tool to enable track changes |
| `insert_revision.py` | CLI tool to replace text with revision marks |
| `delete_revision.py` | CLI tool to mark text for deletion |
| `batch_revisions.py` | CLI tool for processing multiple revisions from stdin |

## Python API

### `TrackChangesProcessor(docx_path)`

Main class for processing a DOCX file.

#### Methods

- **`set_author(author)`** — Set the revision author name.
- **`replace_text_with_revision(old_text, new_text)`** — Replace text inside a paragraph with tracked changes. Raises `ValueError` if `old_text` is not found.
- **`insert_paragraph_after(search_text, new_text)`** — Insert a new paragraph after the paragraph containing `search_text`, marked as `<w:ins>`.
- **`enable_track_changes()`** — Update `word/settings.xml` to enable track revisions.
- **`save(output_path)`** — Write the modified DOCX.
- **`cleanup()`** — Remove temporary files.

### Helper Functions

- `enable_track_changes(input, output)`
- `insert_text_with_revision(input, search, new, author, output)`
- `mark_deletion(input, target, author, output)`
- `batch_revisions(input, revisions, author, output)`

## Example: Real-World Report Update

See `example_usage.py` for a complete working example.
