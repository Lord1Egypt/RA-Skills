# Playbook: Modify Job Config (Update → Publish New Version)

Workflow for modifying an existing job's configuration and publishing a new version.

## Prerequisites

- An existing job (`cql-xxx`) with at least one published config version
- (Optional) Local files to add/update as dependency resources

## Workflow Overview

```
describe_job_configs → [resource changes] → modify_draft → describe_job_configs(draft) → [check_sql] → create_job_config
```

Each step is an independent atomic command.

> **Flow control** (SQL jobs): After `modify_draft`, show the draft summary for human review via `describe_job_configs --only_draft`. Only proceed to `check_sql` after user confirms draft is correct. If check fails, loop back to `modify_draft`. Only after check passes, proceed to `create_job_config`.

---

## Scenario 1: Pure Code Change (No Resource Changes)

### SQL Job — Update SQL Code

```bash
# 1. Get current published config (for reference)
python scripts/oceanus_ops.py describe_job_configs \
  --job_id cql-xxx \
  --region ap-guangzhou \
  --workspace_id space-xxx

# 2. Modify draft with new SQL
python scripts/oceanus_ops.py modify_draft \
  --job_id cql-xxx \
  --job_type 1 \
  --sql_file /path/to/updated_job.sql \
  --region ap-guangzhou \
  --workspace_id space-xxx

# 3. Review draft — present summary to user for confirmation
python scripts/oceanus_ops.py describe_job_configs \
  --job_id cql-xxx \
  --only_draft \
  --region ap-guangzhou \
  --workspace_id space-xxx
# → If user requests changes, loop back to step 2

# 4. Check SQL grammar (only after user confirms draft)
python scripts/oceanus_ops.py check_sql \
  --job_id cql-xxx \
  --sql_file /path/to/updated_job.sql \
  --region ap-guangzhou \
  --workspace_id space-xxx
# → If check fails, loop back to step 2 → 3 → 4

# 5. Publish new version (only after check passes)
python scripts/oceanus_ops.py create_job_config \
  --job_id cql-xxx \
  --job_type 1 \
  --region ap-guangzhou \
  --workspace_id space-xxx \
  --confirm
```

### JAR Job — Update Main Class or Args

```bash
# 1. Modify draft with new config
python scripts/oceanus_ops.py modify_draft \
  --job_id cql-xxx \
  --job_type 2 \
  --entrypoint_class com.example.NewMainClass \
  --program_args "-newArg value" \
  --region ap-guangzhou \
  --workspace_id space-xxx

# 2. Publish new version
python scripts/oceanus_ops.py create_job_config \
  --job_id cql-xxx \
  --job_type 2 \
  --region ap-guangzhou \
  --workspace_id space-xxx \
  --confirm
```

---

## Scenario 2: Add New Resources

Add a UDF jar and config file to an existing SQL job:

```bash
# 1. Upload new UDF jar
python scripts/oceanus_ops.py create_presigned_url \
  --file_name my-udf.jar --region ap-guangzhou
curl -X PUT -T /path/to/my-udf.jar "<Location>"
python scripts/oceanus_ops.py create_resource \
  --name my-udf.jar --resource_type 1 \
  --bucket <Bucket> --cos_path <Key> --cos_region ap-guangzhou \
  --region ap-guangzhou --workspace_id space-xxx --confirm
# → resource-udf, Version 1

# 2. Upload config file
python scripts/oceanus_ops.py create_presigned_url \
  --file_name app.properties --region ap-guangzhou
curl -X PUT -T /path/to/app.properties "<Location>"
python scripts/oceanus_ops.py create_resource \
  --name app.properties --resource_type 2 \
  --bucket <Bucket> --cos_path <Key> --cos_region ap-guangzhou \
  --region ap-guangzhou --workspace_id space-xxx --confirm
# → resource-cfg, Version 1

# 3. Get current resource refs from published config
python scripts/oceanus_ops.py describe_job_configs \
  --job_id cql-xxx --region ap-guangzhou --workspace_id space-xxx
# → Note existing ResourceRefs array

# 4. Modify draft: include existing refs + new refs
python scripts/oceanus_ops.py modify_draft \
  --job_id cql-xxx \
  --job_type 1 \
  --sql_file /path/to/job.sql \
  --resource_refs '[...existing refs..., {"ResourceId":"resource-udf","Type":0,"Version":1}, {"ResourceId":"resource-cfg","Type":2,"Version":1}]' \
  --region ap-guangzhou --workspace_id space-xxx

# 5. Review draft → Check SQL → Publish
python scripts/oceanus_ops.py describe_job_configs \
  --job_id cql-xxx --only_draft \
  --region ap-guangzhou --workspace_id space-xxx
# → Confirm draft with user, then:

python scripts/oceanus_ops.py check_sql \
  --job_id cql-xxx --sql_file /path/to/job.sql \
  --region ap-guangzhou --workspace_id space-xxx
# → If fails, loop back to step 4

python scripts/oceanus_ops.py create_job_config \
  --job_id cql-xxx --job_type 1 \
  --region ap-guangzhou --workspace_id space-xxx --confirm
```

---

## Scenario 3: Update Existing Resource (New Version)

Upload a new version of an existing resource:

```bash
# 1. Upload new file version
python scripts/oceanus_ops.py upload_resource \
  --resource_id resource-xxx \
  --file /path/to/my-udf-v2.jar \
  --region ap-guangzhou \
  --confirm
# → Returns new Version number (e.g. 2)

# 2. Get current refs
python scripts/oceanus_ops.py describe_job_configs \
  --job_id cql-xxx --region ap-guangzhou --workspace_id space-xxx
# → Find the entry with ResourceId=resource-xxx, update its Version

# 3. Modify draft with updated version number in resource_refs
python scripts/oceanus_ops.py modify_draft \
  --job_id cql-xxx --job_type 1 \
  --sql_file /path/to/job.sql \
  --resource_refs '[{"ResourceId":"resource-xxx","Type":0,"Version":2}, ...]' \
  --region ap-guangzhou --workspace_id space-xxx

# 4. Check SQL + Publish
python scripts/oceanus_ops.py check_sql \
  --job_id cql-xxx --sql_file /path/to/job.sql \
  --region ap-guangzhou --workspace_id space-xxx

python scripts/oceanus_ops.py create_job_config \
  --job_id cql-xxx --job_type 1 \
  --region ap-guangzhou --workspace_id space-xxx --confirm
```

---

## Scenario 4: Remove Resources

Remove resources from the job (resources themselves are NOT deleted):

```bash
# 1. Get current refs
python scripts/oceanus_ops.py describe_job_configs \
  --job_id cql-xxx --region ap-guangzhou --workspace_id space-xxx
# → Note full ResourceRefs, remove unwanted entries

# 2. Modify draft with filtered resource_refs (excluding removed ones)
python scripts/oceanus_ops.py modify_draft \
  --job_id cql-xxx --job_type 1 \
  --sql_file /path/to/job.sql \
  --resource_refs '[...remaining refs only...]' \
  --region ap-guangzhou --workspace_id space-xxx

# 3. Check SQL + Publish
python scripts/oceanus_ops.py check_sql \
  --job_id cql-xxx --sql_file /path/to/job.sql \
  --region ap-guangzhou --workspace_id space-xxx

python scripts/oceanus_ops.py create_job_config \
  --job_id cql-xxx --job_type 1 \
  --region ap-guangzhou --workspace_id space-xxx --confirm
```

---

## Scenario 5: Config Parameter Overrides

Override FlinkVersion, JdkVersion, or DefaultParallelism when publishing:

```bash
python scripts/oceanus_ops.py create_job_config \
  --job_id cql-xxx \
  --job_type 1 \
  --flink_version Flink-1.17 \
  --jdk_version 11 \
  --default_parallelism 4 \
  --remark "Upgrade to Flink 1.17" \
  --region ap-guangzhou \
  --workspace_id space-xxx \
  --confirm
```

If not specified, values are inherited from the current draft.

---

## Draft Confirmation

`create_job_config` displays a draft summary before publishing:
- Job type, Flink/JDK version, parallelism
- SQL code preview or JAR config (EntrypointClass/ProgramArgs)
- Complete ResourceRefs list

The agent must present this summary to the user and wait for approval before proceeding. Use `--skip_draft_confirm` only when user explicitly opts out of review.

---

## ResourceRefs Rules

**SQL jobs:** Type=0 for jars, Type=2 for configs. **Type=1 forbidden.**

**JAR jobs:** Exactly one Type=1 (MAIN). Type=0 for auxiliary jars. Type=2 for configs.

`--resource_refs` in `modify_draft` does a **full override** — always pass the complete final array.

---

## Common Errors

| Error | Cause | Fix |
|---|---|---|
| `DraftNotFound` | No draft prepared | Run `modify_draft` first |
| `SqlGrammarFailed` | SQL syntax error | Fix SQL, re-run `check_sql` |
| `ValidationError: Type=1 forbidden for SQL` | Wrong ResourceRef.Type | Use Type=0/2 for SQL jobs |
| `main ResourceRefs count 0 invalid` | JAR job missing MAIN entry | Add Type=1 entry |
