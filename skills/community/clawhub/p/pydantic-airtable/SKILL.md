---
name: pydantic-airtable-api
description: Manage Airtable tables and records via the pydantic-airtable Python library. Use when creating, listing, updating, deleting, or inspecting Airtable records or tables; syncing a Pydantic model to Airtable; validating schema against a model; or writing Python code that uses AirtableModel, AirtableManager, or AirtableClient.
metadata:
  openclaw:
    requires:
      bins: [python3]
      env:
        - AIRTABLE_ACCESS_TOKEN
        - AIRTABLE_BASE_ID
    install:
      - id: pydantic-airtable
        kind: pip
        package: pydantic-airtable
        label: Install pydantic-airtable
---

# Pydantic Airtable API

Use this skill for **practical Airtable management** through `pydantic-airtable`.

Keep `SKILL.md` focused on workflow. Read `references/api-surface.md` only when exact method names or signatures matter.

## Setup

Install the library if needed:

```bash
pip install pydantic-airtable
```

Provide credentials via environment:

```bash
export AIRTABLE_ACCESS_TOKEN="pat..."
export AIRTABLE_BASE_ID="app..."
```

Most bundled scripts also accept `--table` and optional `--base-id` overrides.

## Safety notes

- Use a **scoped Airtable token** with the least privileges needed.
- Prefer a **test base** before pointing the scripts at production data.
- `scripts/model_ops.py --module ./path.py` will **import and execute** that Python module. Only use it with trusted local code.
- `--fields`, `--records`, and `--updates` accept `@file.json`, which reads local files from disk. Inspect those files before passing them in.
- Installing `pydantic-airtable` is normal for this skill, but use a virtualenv/container if you want tighter isolation.

## Choose the right layer

- Use **`AirtableManager`** for base, table, schema, and direct record operations.
- Use **`AirtableClient`** for low-level record APIs and batch record operations.
- Use **`AirtableModel`** when the user wants typed Pydantic models with CRUD helpers.

For exact method coverage, read `references/api-surface.md`.

## Default workflow

1. Confirm credentials are present.
2. For one-off operational tasks, prefer the scripts in `scripts/`.
3. For reusable application code, prefer `AirtableModel` or `AirtableManager` snippets.
4. For schema-sensitive work, validate or sync before writing a lot of data.
5. Catch Airtable-specific exceptions around networked operations.

## Bundled scripts

### `scripts/manage_records.py`

Use for record CRUD without rewriting the same setup code.

Supported actions:

- `list`
- `get`
- `create`
- `update`
- `delete`
- `batch-create`
- `batch-update`

Examples:

```bash
python scripts/manage_records.py list --table Tasks --max-records 10
python scripts/manage_records.py get --table Tasks --record-id rec123
python scripts/manage_records.py create --table Tasks --fields '{"Name":"Ship it","Status":"Open"}'
python scripts/manage_records.py update --table Tasks --record-id rec123 --fields '{"Status":"Done"}'
python scripts/manage_records.py delete --table Tasks --record-id rec123
python scripts/manage_records.py batch-create --table Tasks --records '[{"Name":"A"},{"Name":"B"}]'
```

### `scripts/manage_tables.py`

Use for schema and table operations.

Supported actions:

- `list-bases`
- `base-schema`
- `table-schema`
- `create-table`
- `update-table`
- `delete-table`

Examples:

```bash
python scripts/manage_tables.py list-bases
python scripts/manage_tables.py base-schema
python scripts/manage_tables.py table-schema --table Tasks
python scripts/manage_tables.py create-table --name Tasks --fields '[{"name":"Name","type":"singleLineText"}]'
python scripts/manage_tables.py update-table --table-id tbl123 --updates '{"name":"Tasks Archive"}'
python scripts/manage_tables.py delete-table --table-id tbl123
```

### `scripts/model_ops.py`

Use when the task is explicitly model-driven.

Supported actions:

- `create-table-from-model`
- `sync-model`
- `validate-model`

The model file must expose a class by name.

Examples:

```bash
python scripts/model_ops.py validate-model --module ./task_model.py --class-name Task
python scripts/model_ops.py sync-model --module ./task_model.py --class-name Task --create-missing-fields
```

## Practical guidance

- Prefer `AirtableManager` for table creation, schema inspection, and record CRUD across named tables.
- Prefer `AirtableClient` when the user needs direct record listing or batch writes against a single configured table.
- Prefer `AirtableModel` when the task should stay type-safe and reusable in app code.
- If the user asks to "manage Airtable" without specifying code output, use the scripts first.
- If a field payload is large or repetitive, write it to a JSON file and pass `@file.json` to the script arguments that accept JSON input.

## JSON input rule for scripts

For `--fields`, `--records`, and `--updates`:

- pass inline JSON like `'{"Name":"Task"}'`, or
- pass `@path/to/file.json` to load JSON from disk.

## Exceptions

Catch and surface:

- `ConfigurationError` for missing credentials/config
- `RecordNotFoundError` for missing records
- `APIError` for Airtable API failures
- `ValidationError` for model/schema mismatches
- `AirtableError` as a final fallback
