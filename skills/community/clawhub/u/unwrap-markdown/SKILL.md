---
name: unwrap-markdown
description: Unwrap hard-wrapped Markdown prose into one line per paragraph, while keeping code fences, tables, headings, setext headings, lists, blockquotes, hard line breaks, and YAML frontmatter intact. Use when a Markdown file was written with hard line breaks at a fixed width and needs to become one paragraph per line, when checking a folder of Markdown files for hard-wrapped prose (for CI), or when the user asks to unwrap, reflow, or un-hard-wrap Markdown. Handles CJK text without adding spaces between Chinese or Japanese characters.
---

# Unwrap Markdown

This skill joins hard-wrapped prose lines into single-line paragraphs. It keeps structure as written. Fenced code, indented code at the start of a paragraph, tables, headings, setext headings, horizontal rules, blockquotes, HTML comments, images, hard line breaks, and YAML frontmatter stay unchanged.

## When to use

- A Markdown file has prose broken at a fixed column width, and each paragraph spans several lines.
- You want a repo to follow a "one paragraph per line" rule, and you need to check it in CI.
- You want to unwrap several Markdown files in one run.

## Usage

Run the script from this skill's folder, or pass its full path. Writing requires explicit paths. The script does not scan a folder on its own when it writes.

Preview which files would change. Nothing is written:

```bash
python3 scripts/unwrap_md.py --dry-run path/to/folder
```

Unwrap one file:

```bash
python3 scripts/unwrap_md.py path/to/file.md
```

Unwrap every Markdown file in a folder. Hidden folders are skipped:

```bash
python3 scripts/unwrap_md.py path/to/folder
```

Check only. The exit code is 1 if any file still needs unwrapping:

```bash
python3 scripts/unwrap_md.py --check path/to/folder
```

`--check` and `--dry-run` with no path scan the current directory.

Exit codes: 0 means done, 1 means a file needs unwrapping (`--check` only), and 2 means a path was missing, a file was not UTF-8, or a write failed. Any file that could not be read is reported and skipped, and the other files still run.

## Procedure

1. Run `--dry-run` first to list the files that would change. Do not write yet.
2. Show the list to the owner, and confirm which files to change.
3. Run the unwrap command on the confirmed files only.
4. Run `--check` on the same files. It must exit 0.
5. Review the diff. Only prose and list-item lines should change. Code blocks, tables, headings, and frontmatter must be identical.

## Rules the script follows

- Consecutive prose lines join into one line, with a single space between them.
- Between two CJK characters, the join adds no space.
- A blank line starts a new paragraph.
- Lines inside a fenced code block are never touched.
- An indented block at the start of a paragraph is kept as code.
- An indented line after prose is a continuation, so it is joined.
- A list item and its wrapped continuation lines join into one line.
- A hard line break is kept. A line that ends with two spaces, or with a backslash, stays on its own line.
- A setext heading, a line followed by `===`, is kept as written.
- CRLF line endings are preserved.
- A file that already has one paragraph per line is reported as unchanged.

## Limits

- The script does not check meaning. It only changes line breaks.
- Only Markdown files are accepted (`.md`, `.markdown`, `.mdown`). A path to any other file type is refused with exit 2, so a script or config file is never mangled by accident.
- A line that contains a `|` character is treated as a table line. It stays on its own line and breaks the paragraph around it, so a prose line with a pipe is not unwrapped. Check these by hand.
- An HTML block that spans several lines is not recognized as a block. Its prose lines can be joined. Check these by hand.
- Deeply nested or unusual list layouts are not tested. Check these by hand.
- Trailing spaces on a single-line paragraph are removed. The diff will show this.
- Run the script in version control, or on a copy, so you can review and revert changes.
