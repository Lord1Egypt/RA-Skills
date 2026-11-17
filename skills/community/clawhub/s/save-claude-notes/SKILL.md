---
name: save-claude-notes
description: Save the latest/current Claude Code Q&A to a local Markdown note. Use for /save-claude-notes, 保存笔记, save note, or configuring the notes directory.
---

# Save Claude Notes

Save the most recent substantive user question and assistant answer as Markdown.

## Default behavior

Prefer `--latest`; it reads the latest Q&A from the Claude Code transcript so long answers are not repeated in tool input.

`--latest` discovers transcripts from `~/.claude/projects` using the current working directory. If discovery fails or captures the wrong turn, retry with `SAVE_NOTE_CWD="PROJECT_PATH"` or `--transcript PATH` before falling back to explicit content input.

## Three supported user commands

### 1. Save to configured daily note

User says:

```text
/save-claude-notes
```

Run:

```bash
~/.claude/skills/save-claude-notes/scripts/save-claude-notes.sh --latest
```

This appends to `<notesDir>/YYYY-MM-DD.md`, where `notesDir` comes from `~/.claude/save-claude-notes/config.json` or defaults to `~/claude-notes`.

### 2. Save to an exact `.md` file

User says a target ending in `.md`, for example:

```text
/save-claude-notes 保存到 D:\xiao\WuKong\空.md
```

Run:

```bash
~/.claude/skills/save-claude-notes/scripts/save-claude-notes.sh --latest --output-file "D:/xiao/WuKong/空.md"
```

Treat `.md` paths as exact files; do not ask whether it is a directory. The script currently accepts any non-empty path, but prefer `.md` / `.markdown` files to avoid writing notes into non-note files.

### 3. Save to a folder directory

User says a target directory, for example:

```text
/save-claude-notes 保存到 D:\xiao\WuKong\
```

Run:

```bash
~/.claude/skills/save-claude-notes/scripts/save-claude-notes.sh --latest --notes-dir "D:/xiao/WuKong"
```

This appends to `D:/xiao/WuKong/YYYY-MM-DD.md` and does not change the default config.

## Fallback order

Use only one Q&A source mode per save; do not combine `--latest` with explicit question/answer inputs.

If `--latest` fails or selects the wrong Q&A, try in this order:

1. `SAVE_NOTE_CWD="PROJECT_PATH" ... --latest`
2. `--latest --transcript PATH`
3. `--question-file PATH --answer-file PATH` for long content
4. stdin JSON only for short content

stdin JSON repeats the full Q&A in tool input, so it costs more tokens for long answers.

## Configure default notes directory

Only when the user asks to change the default directory, write this JSON to `~/.claude/save-claude-notes/config.json`:

```json
{"notesDir":"TARGET_DIRECTORY"}
```

Do not modify the config for one-off saves.

## Safety

- Preserve Markdown formatting.
- Multi-line user questions are preserved after the generated title; redact sensitive context before saving.
- If the script refuses suspected secrets, ask the user to redact or explicitly confirm `SAVE_NOTE_ALLOW_SECRETS=1`.
- This skill is manual; automatic capture requires a separate hook/wrapper.
- Detailed docs live in `README.md`; avoid loading them unless needed.
