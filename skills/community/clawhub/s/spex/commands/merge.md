# spex merge

Submit completed work by merging the feature branch or creating a PR.

## Usage

```text
/spex merge [spec_name] [--dry-run | -n] [--no-archive]
```

## Inputs

- OPT: `spec_name`
- OPT: `--dry-run | -n`
- OPT: `--no-archive`
- IF `spec_name` omitted -> CLI searches submittable specs (completed
  tasks + has `spex_branch` + related to current project)
  - IF exactly 1 -> auto-select
  - IF multiple -> numbered list for interactive selection

## Execution

Follow phases in order. Do not skip or reorder.

### Phase 1: Resolve Spec

- CMD:

```bash
$spex_skill_dir/scripts/spex list --json --must-done "$spec_name"
```

- Parse stdout as JSON array:
  - IF single element -> set `$spec_name` / `$spec_path` from entry
  - IF multiple -> numbered `spec_name` list -> user chooses -> set `$spec_name` / `$spec_path` from selected entry
  - IF script exits error -> report error -> STOP

### Phase 2: Validate

- Read `$spec_path/meta.json`
- IF `spex_branch` not set -> report branch management inactive -> STOP

### Phase 3: Submit

- Forward any agent-supplied Usage flags unchanged.
- CMD:

```bash
$spex_skill_dir/scripts/spex merge $spec_name [-n|--dry-run] [--no-archive]
```

- Parse JSON stdout:
  - IF `errors` non-empty -> report errors -> STOP
  - ELSE -> note `action`, `source`, `target`

### Phase 4: Output

- Display summary:

```text
**Submit**: `$spec_name`

- Action: $action
- Source branch: $source
- Target branch: $target
- Archived: $archived
```

- `$archived` = `yes` IF JSON `"archived": true` ELSE `no`

## STOP / Outputs

- Submit complete -> STOP
- Do NOT start implementing further changes
