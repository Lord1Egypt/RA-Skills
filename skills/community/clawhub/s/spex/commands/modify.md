# spex modify

Modify an existing specification's requirements and regenerate the
development plan.

## Usage

```text
/spex modify [spec_name] [request]
```

## Inputs

- OPT: `$spec_name`
- OPT: `$request` — modification/addition to existing spec
- Role: senior software architect; focus on incremental specification
  evolution while preserving completed work

## Preconditions

- SCOPE: updates spec documents only — `spec.md`, `todo.json`,
  `meta.json` inside the spec directory. NO application code. NO
  existing project file modifications. Implementation via
  `/spex apply` or `/spex apply-one-step`.
- Follow phases in order. Do not skip or reorder.

## Execution

### Phase 1: Resolve Spec

- CMD:

```bash
$spex_skill_dir/scripts/spex list --json "$spec_name"
```

- Parse stdout as JSON array:
  - IF single element -> set `$spec_name` / `$spec_path` from entry
  - IF multiple -> numbered `spec_name` list -> user chooses -> set
    `$spec_name` / `$spec_path` from selected entry
  - IF script exits error -> report error -> STOP

### Phase 2: Understand Context and Clarify

- IF `$request` missing/empty -> ask user what changes they want;
  full input becomes `$request`
- Read `$spec_path/spec.md` for existing requirements/design. Explore
  workspace only enough to locate relevant code + patterns referenced
  in the spec. Do NOT dig into full implementation details or modify
  files.
- `$request` is a modification/addition to the existing specification.
  Evaluate clarity:

- Clarify IF any apply:
  - Scope of change unclear (which sections affected; replace vs extend
    existing steps)
  - Multiple viable implementation paths affect design
  - Relationship to completed work unclear (preserve vs redo completed
    steps)
  - Ambiguous terminology in context of existing specification
- ELSE IF request already specific/unambiguous in current-spec context
  -> skip clarification -> Phase 3. Do not ask just to be thorough;
  only when answer would materially change the spec.

- How to clarify:
  - Ask all questions in one message (not back-and-forth)
  - Limit 2–4 questions; prioritize those most affecting design
- After clarification (or none needed) -> finalized `$request` is the
  modification request

### Phase 3: Save Request

- Record modification request in `meta.json`:

```bash
$spex_skill_dir/scripts/spex meta-helper $spec_name prompts \
  --stdin --pre-action modify <<'EOF'
$request
EOF
```

- CHECK images from either source (ext: `.png`, `.jpg`, `.jpeg`, `.gif`,
  `.svg`, `.webp`, `.bmp`):
  - Pasted images (primary): scan conversation for markers
    (e.g. `[Image: source: <path>]`) or inline image content; extract
    absolute paths (agent-cached local dirs)
  - Explicit file paths (secondary): local image paths in `$request`
    with supported extension
- IF images found:
  1. `mkdir -p $spec_path/assets/`
  2. Copy each image into `$spec_path/assets/`, keep original filename
  3. Register in `meta.json` (example):

     ```bash
     $spex_skill_dir/scripts/spex meta-helper $spec_name prompts \
       --add-images assets/file1.png assets/file2.png
     ```

  4. When updating `spec.md` in Phase 5, reference via
     `![description](assets/filename.png)` in appropriate sections

### Phase 4: Build Prompt

- CMD:

```bash
$spex_skill_dir/scripts/spex prompt modify-spec \
  --json --name $spec_name --stdin --remove-undone <<'EOF'
$request
EOF
```

- Parse JSON stdout:
  - IF non-zero exit -> report stderr -> STOP
  - ELSE -> `$modify_prompt` ← `"prompt"` field
- `--remove-undone` removes incomplete `todo.json` steps before render
  so prompt includes completed-step context only

### Phase 5: Modify spec.md

- Using `$modify_prompt`, update `$spec_path/spec.md` per prompt
  instructions
- Before writing, review current codebase structure so updated design
  integrates with existing code

### Phase 6: Build Todo Prompt

- CMD:

```bash
$spex_skill_dir/scripts/spex prompt modify-todo --json --name $spec_name
```

- Parse JSON stdout:
  - IF non-zero exit -> report stderr -> STOP
  - ELSE -> `$todo_prompt` ← `"prompt"` field

### Phase 7: Regenerate Development Steps

- Using `$todo_prompt`, follow its instructions to design and add new
  development steps to `todo.json` via `spex todo-helper`. Prompt
  already contains command syntax, planning principles, and step
  numbering rules.

### Phase 8: Post-Action

- CMD:

```bash
$spex_skill_dir/scripts/spex create-helper post-action \
  --name $spec_name --event-type modify
```

- ON_FAIL: report error -> STOP

### Phase 9: Output

- Display summary:

```text
**Spec**: `$spec_name`

- Spec: `$spec_path/spec.md`
- Todo: `$spec_path/todo.json`
- Meta: `$spec_path/meta.json`
```

### Phase 10: STOP — Do NOT Implement

- Hard STOP. Do NOT write application code, modify project files, or
  begin implementing the updated plan.
- Sole responsibility: update spec documents. Implementation via
  `/spex apply` or `/spex apply-one-step`. Wait for user review ->
  invoke those when ready.

## STOP / Outputs

- Writes: updated `$spec_path/spec.md`, `$spec_path/todo.json`,
  `$spec_path/meta.json` (+ optional `assets/`)
- Phase 10 hard STOP — no application code
