# spex create

**PLAN only** — produces spec documents + todo list.
Does NOT write any application code.

Create a new spec with requirement analysis, detailed design,
and test plan.

## Usage

```text
/spex create [input]
```

## Inputs

- OPT: `$input` — requirement description
- Role: senior software architect; focus on requirement completeness,
  edge cases, testability

## Preconditions

- SCOPE: documents only — `spec.md`, `todo.json`, `meta.json` inside
  the spec directory. NO application code. NO existing project file
  modifications. Implementation later via `/spex apply` or
  `/spex apply-one-step`.
- Follow phases in order. Do not skip or reorder.
- Debug session: call `create-helper begin-session` before Phase 1
  `precheck`. Pre-name CLI traces go to the session log. On
  `prepare-spec` success, session content is merged into
  `<spec_dir>/debug.log` and the session file is deleted. Runtime
  does not dual-write session and spec logs. Do not call
  `mark-phase`; script anchors (`begin-session`, `prepare-spec`,
  `post-action`) are automatic.

## Execution

### Phase 1: Validate Branch

- CMD (begin create debug session; idempotent):

```bash
$spex_skill_dir/scripts/spex create-helper begin-session
```

- CMD:

```bash
$spex_skill_dir/scripts/spex create-helper precheck
```

- IF non-zero exit -> error already on stderr -> STOP
- ELSE -> continue

### Phase 2: Clarify Requirement

- IF `$input` missing/empty -> ask user to describe requirement;
  reply becomes `$input`
- Explore workspace only enough to locate relevant code + patterns for
  the spec. Identify: (1) relevant source files/locations, (2) existing
  patterns/conventions to reference, (3) dependencies touched.
  Do NOT read full file contents unless needed for the spec, dig into
  implementation details, or modify any files (`/spex apply` handles
  that).

- Clarify IF any apply:
  - Multiple viable implementation paths affect design
    (e.g. REST vs GraphQL, polling vs WebSocket)
  - Scope/boundaries unclear (modules in/out, backward compat)
  - Dependencies on other systems/features unspecified
  - Ambiguous terminology with multiple interpretations
- ELSE IF requirement already specific/unambiguous -> skip clarification.
  Do not ask just to be thorough; only when answer would
  materially change the spec.

- How to clarify:
  - Ask all questions in one message (not back-and-forth)
  - Limit 2–4 questions; prioritize those most affecting design
- After clarification (or none needed) -> `$requirement` ← complete
  unambiguous requirement -> Phase 3

### Phase 3: Generate Name and Description

- From `$requirement`, generate JSON with two fields:
  - `name`: short English (<32 bytes), `[a-z0-9-]` only, spaces -> `-`.
    Do NOT prepend date prefix.
  - `description`: brief English summary (merge commit message + PR
    description). Single line — no embedded newlines; wrapping is
    automatic.
- Example: `{"name": "add-login-api", "description": "Add user login API with JWT authentication"}`
- Parse JSON -> `$name`, `$description`

### Phase 4: Prepare Spec Directory

- CMD:

```bash
$spex_skill_dir/scripts/spex create-helper prepare-spec --description "$description" --name "$name" <<'EOF'
$requirement
EOF
```

- Script creates spec directory + `meta.json` (`prompts` = requirement,
  `description` = description). On success it merges any active
  session log into `$spec_path/debug.log`, deletes the session file,
  and clears the active pointer (merge-then-delete; no dual-write).
  Parse JSON stdout:
  - `$spec_name` ← `spec_name` (with date prefix,
    e.g. `2026-05-24-10-30-add-login-api`)
  - `$spec_path` ← `spec_path`
  - `$spec_template` ← `spec_template`
- ON_FAIL: session is left intact for retry; return to Phase 3 ->
  retry with different name
- Example JSON output:

```json
{
  "spec_name": "2026-05-24-10-30-add-login-api",
  "spec_path": "/path/to/.spex/specs/2026-05-24-10-30-add-login-api",
  "spec_template": "# [Title]\n..."
}
```

### Phase 5: Design Specification

- CHECK images from either source (ext: `.png`, `.jpg`, `.jpeg`, `.gif`,
  `.svg`, `.webp`, `.bmp`):
  - Pasted images (primary): scan conversation for markers
    (e.g. `[Image: source: <path>]`) or inline image content; extract
    absolute paths (agent-cached local dirs)
  - Explicit file paths (secondary): local image paths in `$requirement`
    with supported extension
- IF images found:
  1. `mkdir -p $spec_path/assets/`
  2. Copy each image into `$spec_path/assets/`, keep original filename
  3. In `spec.md` below, reference via `![description](assets/filename.png)`
  4. After writing `spec.md`, register in `meta.json` (example):

     ```bash
     $spex_skill_dir/scripts/spex meta-helper $spec_name prompts \
       --add-images assets/file1.png assets/file2.png
     ```

- Perform detailed requirement analysis + solution design from
  `$requirement`. Cover functional/non-functional requirements, data
  models, API contracts, error handling, edge cases.
- Using `$spec_template`, create `$spec_path/spec.md` in same language
  as user's requirement. Replace placeholder sections
  (`<!-- Replace this section with ... -->`) with analysis/design.
  Fill "User Clarification" from Phase 2. Keep Constraints as-is.
  Do not remove or modify `<!-- spex:begin:* -->` comment lines.

### Phase 6: Plan Implementation Steps

- From `$spec_path/spec.md`, break work into incremental steps.
  Each step independently committable + verifiable.
- Principles:
  - Small batches: minimal working increment per step
  - Self-contained: production code + tests in same step — never split
  - Ordered by dependency: each builds on previous; no forward refs
- Use `spex todo-helper` to build `todo.json` step by step.
  Number sequentially: `step-1`, `step-2`, etc.

- **Append** — `--details-from-stdin` + heredoc for multi-line Markdown:

```bash
$spex_skill_dir/scripts/spex todo-helper --name $spec_name append \
  --id step-1 --step-name "Short description for the step" --details-from-stdin <<'DETAILS'
Markdown-formatted description of what this step does,
including file changes, logic, and acceptance criteria.

- Create `src/auth.py` with login endpoint
- Add input validation for email and password
- Write unit tests in `tests/test_auth.py`

**Acceptance criteria**: all tests pass, endpoint returns JWT
DETAILS
```

- **Show** current steps (review before adding more):

```bash
$spex_skill_dir/scripts/spex todo-helper --name $spec_name show \
  --format markdown
```

- **Edit** (only specified fields updated):

```bash
$spex_skill_dir/scripts/spex todo-helper --name $spec_name edit \
  --id step-1 --details-from-stdin <<'DETAILS'
Updated multi-line details for this step.

- Revised implementation approach
- Added error handling requirements
DETAILS
```

- **Remove**:

```bash
$spex_skill_dir/scripts/spex todo-helper --name $spec_name remove \
  --id step-1
```

- `details` field: multi-line Markdown OK (file changes, logic,
  acceptance criteria). Use lists, bold, inline code. Do not use
  headings (`#`, `##`, etc.).

### Phase 7: Post-Action

- CMD:

```bash
$spex_skill_dir/scripts/spex create-helper post-action --name $spec_name
```

- With debug enabled, appends a post-action anchor to
  `$spec_path/debug.log` automatically (no agent `mark-phase`).
- ON_FAIL: fix JSON format in `todo.json` -> re-run until validation OK

### Phase 8: Output

- Display summary:

```text
**Spec**: `$spec_name`

- Spec: `$spec_path/spec.md`
- Todo: `$spec_path/todo.json`
- Meta: `$spec_path/meta.json`
```

### Phase 9: STOP — Do NOT Implement

- Hard STOP. Do NOT write application code, modify project files, or
  begin implementing steps in `todo.json`.
- Planning complete. Sole responsibility: produce `spec.md`,
  `todo.json`, `meta.json` inside the spec directory.
- Wait for user review -> `/spex apply` or `/spex apply-one-step`.

## STOP / Outputs

- Writes: `$spec_path/spec.md`, `$spec_path/todo.json`,
  `$spec_path/meta.json` (+ optional `assets/`)
- Phase 9 hard STOP — no application code
