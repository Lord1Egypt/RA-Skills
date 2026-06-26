# Initialization

One-time setup for To-Do Accelerator. Required when `todo-accelerator-config.yaml` does not exist in the agent's workspace.

## Prerequisites

1. **Python 3** with **PyYAML** installed:
   ```bash
   pip3 install PyYAML
   ```

2. A **board file path** — the `.md` file that will serve as the Kanban board. The file can be empty or non-existent; the script will populate it from the board template. If the file already contains `##` headings, the script treats it as non-empty and refuses to initialize.

## Steps

### 1. Gather information from the user

Ask the user for three paths:

| Parameter | Description |
|-----------|-------------|
| **Config file** | Where to write `todo-accelerator-config.yaml` — must be inside the agent's workspace, **not** inside the skill directory (skill updates may overwrite it) |
| **Board file** | The `.md` file to use as the Kanban board (will be created/populated if empty) |
| **Notes folder** | Where companion note files should be stored |

The template directory defaults to `<skill-dir>/assets/` which contains `note-template.md` and `board-template.md`.

### 2. Run init

```bash
python3 <skill-dir>/scripts/todo.py \
  --config <workspace>/todo-accelerator-config.yaml \
  init \
  --board "/absolute/path/to/board.md" \
  --notes-folder "/absolute/path/to/notes/" \
  --template-dir "<skill-dir>/assets"
```

The script:
- Locates `note-template.md` and `board-template.md` in the template directory
- Checks that the board file is empty (no `##` headings) — **errors if the board already contains data**
- Copies the board template to the board file path
- Creates the notes folder if it doesn't exist
- Writes `todo-accelerator-config.yaml` to the specified workspace path with relative paths
- **Errors if a config file already exists at that path** — delete it first to reinitialize

If validation fails, inform the user and ask for corrected paths.

### 3. Confirm

If the command prints "Initialized: ..." — setup is complete.

### 4. Enable heartbeat and add activity

1. **Verify heartbeat is enabled** in the OpenClaw agent configuration. If it is not enabled, enable it — without heartbeat the agent will not automatically pick up to-do items.
2. **Add the following instruction** to `HEARTBEAT.md` in the agent's workspace:

> Call `work-on-todo` from the To-Do Accelerator skill to pick up a pending to-do. Follow the returned prompt and the skill's instructions to process it.

## Template Directory Requirements

The template directory must contain two files:

### `board-template.md`
An Obsidian Kanban board template with `kanban-plugin:` in its YAML frontmatter and the required `##` column headings (Ideas, 推进中, 审阅中, Done, Archive).

### `note-template.md`
Must contain these placeholders:
- `{{targets}}` — replaced with YAML list items
- `{{requirements}}` — replaced with markdown checklist items
- `{{created_at}}` — replaced with ISO timestamp

And these section headings:
- `# What's More` — requirements checklist
- `# Target` — results and deliverables
- `# Investigation and Problems` — ongoing findings and obstacles
