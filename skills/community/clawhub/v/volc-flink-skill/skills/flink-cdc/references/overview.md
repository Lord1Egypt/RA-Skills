# CDC overview

## What this skill covers

This skill focuses on "CDC draft/job" workflows for `volc_flink`, primarily:

- Generate CDC pipeline YAML templates (copy/paste)
- Explain important YAML options and platform constraints
- Create/publish/start/debug CDC drafts and jobs on Volcengine Flink

## Platform constraints (MUST)

- CDC draft/job type: `FLINK_CDC_JAR`
- Engine version: currently only supports `FLINK_VERSION_1_16`
- CDC version: default `v3.4`

## CLI mapping

- `volc_flink drafts create --type cdc` => `JobType = FLINK_CDC_JAR`
- CDC YAML can be provided via:
  - `--cdc "<inline-yaml>"`
  - `--cdc-file <file.yml>`
  - `--cdc-dir <dir>` (recursive `*.yml/*.yaml`)

Important: `drafts update` currently does not expose `--cdc/--cdc-file/--cdc-dir` flags, so treat update as "recreate draft with new YAML" unless the user confirms CLI version support.

## Recommended YAML structure

Prefer this structure to align with current CLI sample and job-info parsing:

```yaml
sources:
- source:
    type: mysql
    ...
sink:
  type: paimon
  ...
transform:
- source-table: db.table
  projection: "*"
route:
- source-table: db.table
  sink-table: ods_db.table
pipeline:
  name: my-cdc-job
  parallelism: 2
```

## Placeholder naming note

The templates under `assets/` intentionally use placeholders like `${mysql_server_id}` or `${mysql_tables_exclude}`.

- Treat placeholders as plain text replacement
- Placeholder names are standardized to snake_case (only lowercase letters, digits, and `_`)

## Related references

- `references/route.md`: route rules, regex matching, and pattern replacement (`replace-symbol`)
- `references/transform.md`: transform rules, projection/filter, hidden columns, soft delete (`SOFT_DELETE`)
