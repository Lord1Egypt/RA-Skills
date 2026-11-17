---
name: submit-check
description: "Find students who haven't submitted artifacts by matching filenames against a class manifest."
---

# Submit Check

Check which students are missing from an artifact submission folder.

## How it works

- Student manifest CSV files live in `manifests/` inside this skill directory.
- Each CSV = one class, filename = class name (e.g. `CS101.csv`).
- CSV columns: `code`, `name` (header required, case-insensitive).
- Artifact filenames are scanned and matched against student codes and/or names.

## When user asks to check submissions

1. Get the **class name** and **artifact folder path** from the user.
2. Locate the manifest: `manifests/<CLASS_NAME>.csv` inside this skill directory.
   - Resolve the skill directory as the parent of this SKILL.md.
3. Run the check script:

```bash
python <SKILL_DIR>/scripts/check.py \
  --manifest <SKILL_DIR>/manifests/<CLASS_NAME>.csv \
  --artifacts "<artifact_folder_path_or_text_file>"
```

The `--artifacts` flag accepts **two modes**:
- **Folder path** (default): scans all files in the directory and matches their filenames.
- **Text file path**: if the path points to a regular file (not a directory), each non-empty line is treated as an artifact filename. This is useful when you already have a list of submitted filenames (e.g. exported from an LMS or copied from a chat log) and don't need to scan a folder.

4. If the class manifest doesn't exist, list available manifests and ask the user to provide or create one.
5. Present the results: total students, submitted count, and the list of missing students.

## Manifest format

```csv
code,name
2024001,张三
2024002,李四
```

- `code`: student ID / student number
- `name`: student name (Chinese or English)
- One file per class, named after the class.

## Matching logic

- **code**: exact substring match in filename (case-insensitive, word-boundary aware)
- **name**: full name match with flexible separators (spaces → `_`, `-`, or nothing)
- **both** (default): match against code OR name
- User can override with `--match-field code|name|both`

## Examples

User: "Check submissions for class CS201 in /tmp/homework3"

→ Run: `python .../scripts/check.py --manifest .../manifests/CS201.csv --artifacts /tmp/homework3`

Output shows missing students list.

---

User: "Check submissions for CS201, here's the file list: /tmp/submitted.txt"

→ Run: `python .../scripts/check.py --manifest .../manifests/CS201.csv --artifacts /tmp/submitted.txt`

The text file contains one filename per line, e.g.:
```
2024001_张三_homework3.pdf
2024002_李四-hw3.pdf
作业_2024003_王五.docx
```

Output shows missing students list.
