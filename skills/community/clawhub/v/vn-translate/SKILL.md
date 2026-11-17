---
name: vn-translate
description: Translate fiction from a source language into Vietnamese using a streaming pipeline. Read raw.md in ~12 KiB chunks with RawReader, write each translated part to out/, maintain consistent proper names and forms of address, track progress in _vartemp.json, optionally index chapter titles, then merge and export EPUB.
metadata:
  version: "1.1.0"
  author: KaibaZax
---

# vn-translate — Fiction Translation to Vietnamese (v1.2 Streaming)

## Overview

This skill uses a **streaming pipeline**. It does **not** pre-split the source file into many raw part files on disk.

The workflow is:

1. Prepare `raw.md`.
2. Read approximately 12 KiB from `raw.md` with `RawReader.py`, using a byte offset.
3. Translate exactly one chunk and write it to `out/part_XXX.md`.
4. Record the completed part in `_vartemp.json`.
5. Maintain `TenRieng.md` (proper names) and `XungHo.md` (forms of address) immediately when new entries appear.
6. Maintain the optional `chapters` index in `_vartemp.json` when chapter numbering or chapter titles are known.
7. Repeat until EOF.
8. Merge the translated parts with `merge_parts.py`, or merge chapter files with `merge_chapters.py`.
9. Optionally export the result to EPUB.

## Project layout

```text
<project-dir>/
├── raw.md                 # Complete source text
├── _vartemp.json          # Translation checkpoint + part/chapter indexes
├── TenRieng.md            # Proper-name glossary
├── XungHo.md              # Forms-of-address matrix
├── out/                   # part_001.md, part_002.md, ...
├── Chapters/              # Optional: one translated file per chapter
├── Full.md / full.md      # Merged output
├── Full.epub              # EPUB output
└── assets/                # Images, if any
```

## `_vartemp.json` state

The checkpoint file is plain UTF-8 JSON. It replaces the old `_vartemp.bin` filename.

A typical state is:

```json
{
  "version": "1.2.0",
  "completed": [
    {"part": 1, "start": 0, "end": 12288},
    {"part": 2, "start": 12288, "end": 24100}
  ],
  "chapters": [
    {
      "index": 1,
      "rawIdx": 1,
      "transIdx": 1,
      "number": 1,
      "title": "Optional chapter title"
    }
  ],
  "next_offset": 24100
}
```

### State rules

- `completed` is the ordered index of translated parts.
- Each completed part stores its 1-based `part` number and source byte range `[start, end)`.
- `next_offset` is the byte offset from which the next source chunk must be read.
- `chapters` is an ordered chapter index.
- `rawIdx` is the chapter's ordinal position in the source/raw text.
- `transIdx` is the chapter's ordinal position in the translated output.
- `rawIdx` and `transIdx` may differ when chapters are omitted, merged, or otherwise remapped.
- `number` is the displayed/source chapter number.
- `title` is optional metadata used for the translated chapter heading and EPUB TOC.
- Do not invent a chapter title. If the source does not provide one and the user has not requested one, leave `title` as `null`.
- Chapter titles may be added or changed later without changing the translated prose.
- `_vartemp.json` must remain valid JSON after every progress update.

## Scripts

| Script | Purpose |
|---|---|
| `scripts/convert_to_md.py` | Convert `.txt/.epub/.docx/.html/.pdf` to Markdown |
| `scripts/RawReader.py` | Read an approximately 12 KiB chunk from `raw.md` and cut only at `\n` |
| `scripts/progress.py` | Manage `_vartemp.json`, completed-part indexes, and optional chapter indexes |
| `scripts/merge_parts.py` | Concatenate `out/part_*.md` into a full Markdown file |
| `scripts/format_output.py` | Normalize output formatting and chapter headings |
| `scripts/verify_part.py` | Perform a quick translation-part integrity check |
| `scripts/merge_chapters.py` | Merge `Chapters/` files by chapter number |
| `scripts/md2epub.py` | Convert merged Markdown to EPUB with TOC, CSS, and local images |

## Step 1 — Prepare the source

```bash
python scripts/convert_to_md.py <source_file>
# Rename or copy the resulting Markdown file to raw.md if necessary.
mkdir -p out
```

## Step 2 — Initialize the translation tables

### `TenRieng.md`

```markdown
# Proper Names

| Source Name | Vietnamese Name | Notes |
|-------------|-----------------|-------|
```

### `XungHo.md`

```markdown
# Forms of Address

Matrix: [Speaker] × [Listener], cell = `Self-reference\Address`
```

Keep these files authoritative throughout the entire translation. When a new proper name or relationship appears, update the relevant table **before translating the next part**.

## Step 3 — Translate one part at a time

### 3.1 Read the current state

```bash
python scripts/progress.py get
python scripts/progress.py next-part
python scripts/progress.py listt
```

### 3.2 Read approximately 12 KiB

```bash
OFFSET=$(python scripts/progress.py get)
PART=$(python scripts/progress.py next-part)
python scripts/RawReader.py raw.md $OFFSET 12288
```

`RawReader.py` writes:

- translated-source text to **stdout**
- metadata to **stderr**:
  - `SKIP`
  - `READ`
  - `NEXT_OFFSET`
  - `EOF`
  - `TOTAL`

Always use the returned `NEXT_OFFSET` as the end offset recorded for the completed part.

### 3.3 Translate and write `out/part_XXX.md`

For the current chunk:

- Translate the content directly.
- Write exactly one output file: `out/part_XXX.md`.
- `XXX` is a zero-padded 3-digit part number.
- Update `TenRieng.md` and `XungHo.md` immediately when new entries appear.
- Preserve paragraph boundaries: keep one blank line between paragraphs.
- Do not emit `\u3000` as indentation.
- If a chapter marker or title is known, update the chapter index in `_vartemp.json`.
- Do not process two translation parts in the same translation turn.

### 3.4 Update progress

After the translated part has been written and checked:

```bash
python scripts/progress.py add <START_OFFSET> <NEXT_OFFSET>
```

For example:

```bash
python scripts/progress.py add 12288 24100
```

To add a chapter index:

```bash
python scripts/progress.py chapter-add 3
python scripts/progress.py chapter-name 3 "The Hidden Truth"
# When raw and translated chapter positions differ:
python scripts/progress.py chapter-map 5 4 5 "The Hidden Truth"
```

List chapter indexes:

```bash
python scripts/progress.py chapter-list
```

To retranslate a part:

```bash
python scripts/progress.py remove-part 5
```

Then read the required source range again and overwrite `out/part_005.md`.

### 3.5 Continue until EOF

Repeat the one-part cycle until `EOF=1`.

## Step 4 — Merge

For ordinary streaming output:

```bash
python scripts/merge_parts.py out/ full.md
```

If the project uses one file per chapter:

```bash
python scripts/merge_chapters.py --title "Book Title"
```

Keep `rawIdx` and `transIdx` stable when chapters are remapped. `transIdx`
is the canonical translated order used for EPUB chapter filenames and TOC
entries.

## Step 5 — Normalize formatting, if needed

```bash
python scripts/format_output.py out/ titles.json
```

`titles.json` may map chapter numbers to requested titles, for example:

```json
{
  "1": "The Secret of the Parents",
  "7": "The Hidden Drive",
  "ngoai_truyen": "Extra Chapter"
}
```

## Step 6 — Export EPUB

The EPUB script uses `ebooklib` and `markdown`. It reads `_vartemp.json`
to preserve `transIdx` and requested chapter titles. Each translated chapter
is emitted as a separate `chapter_XXX.html` content document, where `XXX`
is the zero-padded `transIdx`. The EPUB NCX/Nav TOC points directly to these
chapter documents, so EReaders receive one stable TOC entry per chapter.

If the environment already uses `uv`, the dependencies can be supplied for
this command without modifying the global Python installation:

```bash
uv run --with ebooklib --with markdown python scripts/md2epub.py \
  --input Full.md \
  --output Full.epub \
  --title "Book Title" \
  --cover assets/cover.png \
  --state _vartemp.json
```

Do not install additional packages unless the user explicitly requests an environment change and the package source and requirement have been verified.

## Output format

### Proper names

```markdown
# Proper Names

| Source Name | Vietnamese Name | Notes |
|-------------|-----------------|-------|
| Alice       | Alice           | Female protagonist |
```

### Forms of address

```markdown
# Forms of Address

| Speaker \ Listener | An | Stepmother |
|--------------------|----|------------|
| An                 | -  | Con / Dì   |
| Stepmother         | Mẹ / Con | - |
```

## Placeholder and formatting protocol

| Placeholder | Meaning |
|---|---|
| `* *` | Narrative text: involuntary physical reactions, sensory details, and atmospheric descriptions. |
| `" "` | Audible dialogue spoken by `{char}` in the surrounding environment. |
| `` ` ` `` | Concealed communication: internal thought, telepathy, encrypted phone/SMS, spiritual transmission, or another secret channel that is not audible to nearby characters. Use sparingly. |

Standard output structure:

```text
# Chương N: [chapter title]

*[Physical reaction and sensory anchor first: what the body feels, smells, or hears.]*
"[Optional audible dialogue, only when the character would actually speak aloud.]"
`[Optional concealed communication — internal thought or secret channel.]`
*[Continuation of the action or a shift in attention.]*
```

## Critical rules and common failure modes

### 1. Do not duplicate the translation in hidden reasoning

**Do not write a complete translation draft in THINKING and then copy that same draft into an execution/code step.** This duplicates the content in the model context and wastes tokens.

Translate directly into the final data structure used to write the output file.

### 2. Paragraph boundaries are mandatory

The source already defines paragraph boundaries. Preserve them.

- Use one blank line between paragraphs.
- Do not merge the entire part into one large block.
- Do not create arbitrary paragraph breaks merely to make the output look shorter.

### 3. Minimal verification

After writing `out/part_XXX.md`, compare the number of non-empty paragraphs in the source chunk and translated output.

- Difference of `0` is ideal.
- Difference of `1` is acceptable because a translation may legitimately combine or split one short paragraph.
- Difference greater than `1` is a warning sign for truncation, omission, or accidental over-translation.

Do not print or reread the last three lines merely to confirm that the file was written.

### 4. Do not read a sample part only to imitate its style

Do not spend several thousand tokens rereading an old translated part just to imitate its prose style.

Use the authoritative resources instead:

- `references/thanh-ngu-va-tu-ngu.md`
- `TenRieng.md`
- `XungHo.md`

### 5. Idioms and Sino-Vietnamese terminology

Translate naturally, but preserve established Sino-Vietnamese forms for Chinese idioms and classical expressions when the reference requires them.

If a new recurring idiom or terminology is needed, add it to the appropriate reference file rather than bloating `SKILL.md`.

### 6. Formatting must be applied immediately

When writing translated output:

- Never use `\u3000` for indentation.
- Keep one blank line between paragraphs.
- Use `# Chương N: [title]` for chapters.
- Use `# Giới thiệu` for introductions.
- Use `# Ngoại truyện: [title]` when an interlude title is known.

### 7. Always read on line boundaries

`RawReader.py` is responsible for cutting the chunk at `\n`.

Never manually cut the raw chunk in the middle of a sentence or paragraph.

### 8. Translate sequentially

**One part per translation turn is mandatory.**

Do not batch two or more parts together. The intended cycle is:

```text
read one part
→ translate it
→ write out/part_XXX.md
→ verify it
→ update _vartemp.json
→ continue
```

### 9. Do not use parallel subagents for translation

Do not translate parts with parallel subagents.

Parallel translation has previously caused:

- truncated files
- inconsistent character names
- stale proper-name tables
- inconsistent forms of address
- substantially higher token usage

The main agent should translate the parts sequentially.

### 10. Zero-byte output files

If a background process creates a zero-byte Markdown output:

```bash
find out -name '*.md' -size 0 -delete
```

Remove the broken file immediately and translate that part again.

Before merging, make sure no zero-byte part remains.

### 11. Checkpoint state

Preserve these checkpoint files throughout every translation task:

- `out/`
- `_vartemp.json`
- `TenRieng.md`
- `XungHo.md`

At the beginning of each translation session, inspect:

```bash
python scripts/progress.py listt
ls out/
```

Do not restart from part 1 if the checkpoint is valid.

### 12. Token-usage diagnostics

The token dashboard may report approximately 100–160× the useful raw/output token count because the agent loop can resend the working context on each tool call.

See:

```text
references/token-usage-diagnostics.md
```

for diagnostics and interpretation.

### 13. Write the final format from the start

When continuing a translation in a new session, write the output in final format immediately.

Do not intentionally write an unformatted intermediate version and plan to fix it later.

### 14. Proper names

Add a new proper name to `TenRieng.md` the first time it appears.

Do not change a previously established translation halfway through the novel unless the user explicitly requests a terminology change.

### 15. Sensitive vocabulary

Follow:

```text
references/thanh-ngu-va-tu-ngu.md
```

For example, if the reference specifies a fixed Vietnamese term, use that exact term consistently.

### 16. Forms of address

Treat `XungHo.md` as a logical matrix.

When a new character or relationship appears:

1. Add the character to the matrix.
2. Check the speaker/listener direction.
3. Check the reciprocal form.
4. Keep the relationship consistent in subsequent parts.

### 17. UTF-8 and BOM

Markdown files may contain a UTF-8 BOM. The scripts should read such files safely.

## Safe file-writing protocol for Vietnamese/Chinese text

Do not use a shell heredoc for large Vietnamese or Chinese content. It can easily cause quoting or encoding problems.

Prefer Python `Path.write_text()`.

For content containing many double quotes, a JSON temporary file is safer:

```python
import json
from pathlib import Path

paras = ['Paragraph 1 ...', 'Paragraph 2 ...']

tmp = Path("_tmp_paras.json")
tmp.write_text(
    json.dumps(paras, ensure_ascii=False),
    encoding="utf-8",
)

paras = json.loads(tmp.read_text(encoding="utf-8"))
Path("out/part_001.md").write_text(
    "\n\n".join(paras) + "\n",
    encoding="utf-8",
)

tmp.unlink()
```

Delete temporary files immediately after the output has been written.

Do not leave `_*.json` temporary files or prompt artifacts in `_prompts/`.

## Windows path handling

- Avoid using a `workdir` containing Vietnamese characters when possible.
- Pass full paths in quotes when invoking commands.
- Windows can represent filenames in NFC or NFD forms. If a user-created directory cannot be found, enumerate the parent directory and use the actual `Path` object rather than reconstructing the name manually.
- The working directory of an execution tool may be a session directory rather than the translation project. Resolve the actual project path first and operate through `Path` objects.

## Reference material

- `references/thanh-ngu-va-tu-ngu.md` — idioms and sensitive/terminology reference
- `references/token-usage-diagnostics.md` — token-usage diagnostics
- `references/session-worked-example.md` — worked translation-session example
