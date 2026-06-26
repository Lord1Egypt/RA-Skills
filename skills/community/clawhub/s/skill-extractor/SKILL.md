---
name: skill-extractor
description: "Export any installed OpenClaw skill into a shareable ZIP: detects & stages external runtime files, generates STRUCTURE.md for LLM-guided install. Reads and packages local files only — no network calls, no APIs, no external transmissions."
metadata: {"openclaw":{"emoji":"📦"}}
---

# skill-extractor

Package any installed OpenClaw skill into a clean, shareable ZIP. External runtime files referenced in SKILL.md are detected, staged under `_external/`, and documented — so a new install knows exactly where every file belongs and can reproduce full functionality.

> All file operations are local only. Nothing is transmitted anywhere. The user confirms what gets included before anything is zipped.

---

## Agent Rules

- Always list available skills before asking for selection (unless skill name is already given)
- Always work on a staging copy — never modify the original skill directory or any external paths
- **Always show the user what external files were found and get explicit confirmation before zipping**
- Files are packaged as-is — values are not modified. Inform the user that sensitive files (credentials, tokens) will be included with their real values and should be reviewed before sharing
- If an external file doesn't exist on disk yet (runtime-generated), document it as "created at runtime" — do not error
- Generate `STRUCTURE.md` inside the staging folder before zipping
- Default ZIP output: the user's Desktop — confirm with user first
- If ZIP already exists at target, overwrite it
- Clean up staging after a successful ZIP
- If any step fails, leave staging intact and report clearly

---

## Step 1 — List Available Skills

Scan all known OpenClaw skill locations (workspace skills folder, user-local skills folder, and the bundled npm package skills folder) for subdirectories that contain a `SKILL.md`. Present the list with skill name and source. Ask which to export.

---

## Step 2 — Locate Skill

Find the skill folder by name. If not found, report and stop.

---

## Step 3 — Stage Skill Files

Create a hidden temp staging folder inside the workspace named after the skill. Copy all files from the skill directory into it. Originals are never touched.

---

## Step 4 — Detect External Files

Read the SKILL.md from the original skill directory. Extract all path-like strings that begin with a user home or app-data prefix (home dir shorthands and platform app-data equivalents). Resolve each to an absolute path.

For each path:
- If it is a **file** that exists: add it to the external files list.
- If it is a **directory** that exists: add all files inside it recursively to the list.
- If it doesn't exist yet: record it as a "created at runtime" entry.

**Do not copy anything yet.** Build the list first — it goes to the user for review in the next step.

---

## Step 5 — Confirm with User

Present the user with everything that will be included in the ZIP:

1. All files from the skill directory
2. The full list of detected external files with their resolved paths

Clearly warn: **"These files will be packaged with their real values — including any credentials, tokens, or sensitive config. Review before sharing the ZIP."**

Ask: *"Proceed with packaging these files?"*

- If **yes**: stage the external files into `_external/`, mirroring the directory structure relative to the user's home, then continue.
- If **no**: abort and clean up staging. Do not create a ZIP.

---

## Step 6 — Generate STRUCTURE.md

Write `STRUCTURE.md` into the staging dir with these sections in order:

**Header** — skill name, generation timestamp, one-line purpose statement.

**Folder Layout** — ASCII tree of the staging dir. Directories before files at each level, both sorted alphabetically. Use standard tree connectors (`├──`, `└──`, `│`). Directory names end with `/`.

**File Descriptions table** — two columns: relative file path and one-line purpose. Describe each file by what it does rather than its type. Well-known skill files have fixed descriptions:

| File | Description |
|---|---|
| `SKILL.md` | Main skill instructions. The LLM agent reads this to understand purpose, setup, and usage. |
| `_meta.json` | ClawhHub registry metadata: version, owner, credential paths, persistence info. |
| `STRUCTURE.md` | This file. Auto-generated folder map and install guide. |
| Any other file | Infer purpose from filename, location, and content — describe what it does in plain English. |

**External Files table** — only if external files were detected. Three columns: file path inside the ZIP | target install path on the machine | notes. Determine the notes value by this logic:

| Condition | Notes |
|---|---|
| Path suggests credentials or config | Packaged with real values — review before sharing. |
| Path suggests a worker or background script | Extracted from SKILL.md at runtime — included here for reference. |
| Path suggests a log, pid, or state file | Runtime-generated. Recreated automatically on first run. |
| File did not exist at export time | Not present at export — created automatically when the skill runs. |
| Anything else | External runtime file. Review SKILL.md for usage. |

Follow the table with a brief note on how to place `_external/` files at their target paths on both Windows and Unix systems.

**Install Instructions** — three options:
- Option A: install via ClawhHub if the skill is published
- Option B: manual — copy the skill folder into the workspace skills directory, place any `_external/` files at their target paths, confirm with `openclaw skills list`
- Option C: local clawhub install, then handle `_external/` files manually

**Footer** — credit line linking to the skill on ClawhHub.

---

## Step 7 — Zip and Deliver

Confirm the output path with the user (default: the user's Desktop). Remove any existing ZIP at that path first. Compress the staging dir. Report the saved path and file size. Delete the staging folder.

---

## Error Reference

| Problem | Cause | Fix |
|---|---|---|
| Skill not found | Name mismatch | Check spelling; run `openclaw skills list` |
| Access denied on copy | File ownership issue | Run as admin or check permissions |
| ZIP creation fails | Disk full or missing compression support | Free space or update runtime |
| Staging not cleaned | ZIP step failed | Delete the staging folder inside the workspace manually |
| External file missing | Runtime-generated, not yet created | Safe to skip — document as "created at runtime" |
| User declined confirmation | Sensitive files flagged by user | Abort — no ZIP created, staging cleaned up |
