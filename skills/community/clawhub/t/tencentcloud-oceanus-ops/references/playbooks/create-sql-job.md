# Playbook: Create SQL Job

Complete workflow for creating, configuring, publishing, and running a SQL job.

## Prerequisites

- TencentCloud credentials configured (see `references/credential-setup.md`)
- Workspace ID (`space-xxx`) and a running cluster ID (`cluster-xxx`)
- SQL code ready (inline or file)
- (Optional) Pre-uploaded dependency resources if the SQL references UDF jar / config files

## Workflow Overview

```
create_job → [upload resources] → modify_draft → describe_job_configs(draft) → check_sql → create_job_config → run_jobs
```

Each step is an independent atomic command. Execute them sequentially, using the output of each step as input to the next.

> **Flow control**: After `modify_draft`, first show the draft summary for human review. Only proceed to `check_sql` after confirmation. If check fails, loop back to `modify_draft` to fix SQL, then re-confirm and re-check. Only after check passes, proceed to `create_job_config` to publish.

---

### Step 1: Create the SQL Job

```bash
python scripts/oceanus_ops.py create_job \
  --name "my_sql_job" \
  --job_type 1 \
  --region ap-guangzhou \
  --workspace_id space-xxx \
  --cluster_id cluster-xxx \
  --confirm
```

`--job_type 1` (SQL) is **required**. Note the returned `JobId` (e.g. `cql-xxx`).

---

### Step 2 (Optional): Upload Dependency Resources

Only if the SQL references UDF jars or config files:

```bash
# 1) Get presigned URL for upload
python scripts/oceanus_ops.py create_presigned_url \
  --file_name my-udf.jar --region ap-guangzhou

# 2) Upload file to COS via presigned URL
curl -X PUT -T /path/to/my-udf.jar -H "Content-Type: application/java-archive" "<Location>"

# 3) Register the resource
python scripts/oceanus_ops.py create_resource \
  --name my-udf.jar \
  --resource_type 1 \
  --bucket <Bucket> \
  --cos_path <Key> \
  --cos_region ap-guangzhou \
  --region ap-guangzhou \
  --workspace_id space-xxx \
  --confirm
# → Note ResourceId and Version
```

For config files use `--resource_type 2`.

---

### Step 2.5 (Optional): Browse Catalogs & Reference Tables

If the SQL references tables via `catalog.database.table` syntax (e.g. `SELECT * FROM my_hive.db1.orders`), browse available catalogs and tables first.

> **关键参数来源：**
> - `cluster_id`：使用**作业绑定的集群** ID（从 `describe_jobs` 返回的 `ClusterId` 获取）
> - `flink_version`：使用**作业自身的 Flink 版本**（从 `describe_jobs` 返回的 `FlinkVersion` 获取）

#### 2.5.1 List all catalogs in the workspace

```bash
python scripts/oceanus_ops.py describe_catalogs \
  --region ap-guangzhou \
  --workspace_id space-xxx
```

Note each catalog's `Name`, `Type` (0=OCEANUS, 1=HIVE, 2=MYSQL, 3=PAIMON), `SerialId`, and `FlinkVersion`.

> **⚠️ Catalog 版本过滤规则：**
>
> 返回的 catalog 列表中，只有与作业 Flink 版本匹配的 catalog 才能被引用：
> - 如果 catalog 的 `FlinkVersion` 为空（如默认 `_dc` catalog）→ **不过滤**，所有作业版本均可使用
> - 如果 catalog 的 `FlinkVersion` 非空 → 必须与作业的 `FlinkVersion` **完全一致**才能使用
>
> 例如：作业 Flink 版本为 `Flink-1.16`，则只能选择 `FlinkVersion` 为空或 `Flink-1.16` 的 catalog，
> `Flink-1.13` / `Flink-1.18` / `Flink-1.20` 的 catalog 不可使用。

#### 2.5.2a For default catalog (Type=0): Browse databases & tables

```bash
python scripts/oceanus_ops.py describe_meta_catalogs \
  --region ap-guangzhou \
  --workspace_id space-xxx
```

Get table details:

```bash
python scripts/oceanus_ops.py describe_meta_table \
  --table_id <id> \
  --region ap-guangzhou \
  --workspace_id space-xxx
```

#### 2.5.2b For external catalogs (Type=1/2/3): Browse databases & tables

External catalogs use **async queries** — the CLI automatically polls until results are ready (may take 10-60s).

`cluster_id` 和 `flink_version` 均使用作业绑定的集群和作业自身的 Flink 版本：

```bash
# List databases (cluster_id & flink_version from the job)
python scripts/oceanus_ops.py describe_external_meta_databases \
  --catalog_id <serial_id> \
  --cluster_id <job_cluster_id> \
  --flink_version <job_flink_version> \
  --region ap-guangzhou \
  --workspace_id space-xxx

# List tables in a database
python scripts/oceanus_ops.py describe_external_meta_tables \
  --catalog_id <serial_id> \
  --database_name <db_name> \
  --cluster_id <job_cluster_id> \
  --flink_version <job_flink_version> \
  --region ap-guangzhou \
  --workspace_id space-xxx

# Get single table detail
python scripts/oceanus_ops.py describe_external_meta_tables \
  --catalog_id <serial_id> \
  --database_name <db_name> \
  --table_name <table_name> \
  --cluster_id <job_cluster_id> \
  --flink_version <job_flink_version> \
  --region ap-guangzhou \
  --workspace_id space-xxx
```

#### 2.5.3 Use in SQL

Once you know the catalog/database/table structure, reference them in SQL:

```sql
-- Use catalog.database.table format
SELECT * FROM my_hive_catalog.production_db.orders;

-- Or set catalog context
USE CATALOG my_hive_catalog;
USE production_db;
SELECT * FROM orders;
```

#### 2.5.4 Pass catalog refs to modify_draft

When calling `modify_draft`, pass `--catalog_refs` so the CLI auto-builds `Metadata.catalogs` and `Metadata.referenceTables`:

```bash
python scripts/oceanus_ops.py modify_draft \
  --job_id cql-xxx \
  --job_type 1 \
  --sql_file /path/to/job.sql \
  --catalog_refs '[{"catalog":"my_hive_catalog","database":"production_db","table":"orders"}]' \
  --region ap-guangzhou \
  --workspace_id space-xxx
```

The CLI will:
1. Call `DescribeCatalogs` to get catalog config details
2. For default catalog tables: query version info via `DescribeMetaCatalogs`
3. Build `Metadata.referenceTables` and `Metadata.catalogs` in ProgramArgs

---

### Step 3: Modify Draft (Write SQL + Resource Refs)

Write SQL code into the draft. Include `--resource_refs` only if Step 2 was performed:

```bash
# Pure SQL (no resources)
python scripts/oceanus_ops.py modify_draft \
  --job_id cql-xxx \
  --job_type 1 \
  --sql_file /path/to/job.sql \
  --region ap-guangzhou \
  --workspace_id space-xxx

# SQL with resource references
python scripts/oceanus_ops.py modify_draft \
  --job_id cql-xxx \
  --job_type 1 \
  --sql_file /path/to/job.sql \
  --resource_refs '[{"ResourceId":"resource-udf","Type":0,"Version":1},{"ResourceId":"resource-cfg","Type":2,"Version":1}]' \
  --region ap-guangzhou \
  --workspace_id space-xxx
```

The CLI automatically handles:
- Base64 encoding of SQL into `ProgramArgs.SqlCode`
- `${var}` placeholder scanning → `DescribeVariables` → `Metadata` construction

---

### Step 4: Review Draft Summary

Read the draft and present the summary to the user for confirmation before proceeding to syntax check:

```bash
python scripts/oceanus_ops.py describe_job_configs \
  --job_id cql-xxx \
  --only_draft \
  --region ap-guangzhou \
  --workspace_id space-xxx
```

Present the draft content (SQL code, resource refs, params) to the user. **Only proceed to Step 5 after user confirms the draft looks correct.** If user requests changes, loop back to Step 3 (modify_draft).

---

### Step 5: Check SQL Grammar

```bash
python scripts/oceanus_ops.py check_sql \
  --job_id cql-xxx \
  --sql_file /path/to/job.sql \
  --region ap-guangzhou \
  --workspace_id space-xxx
```

`--cluster_id` is auto-resolved from the job detail. If check fails, fix the SQL and **loop back to Step 3 → Step 4 → Step 5** until check passes.

---

### Step 6: Publish New Version

```bash
python scripts/oceanus_ops.py create_job_config \
  --job_id cql-xxx \
  --job_type 1 \
  --region ap-guangzhou \
  --workspace_id space-xxx \
  --confirm
```

Only reach this step after check_sql passes. This shows a final draft summary for confirmation, then calls `CreateJobConfig`. Note the returned `Version` number.

---

### Step 7: Run the Job

```bash
python scripts/oceanus_ops.py run_jobs \
  --job_id cql-xxx \
  --region ap-guangzhou \
  --workspace_id space-xxx \
  --confirm
```

---

## ResourceRefs Format (SQL Jobs)

SQL jobs use only `Type=0` and `Type=2`:

| `ResourceRef.Type` | Meaning | Use For |
|---|---|---|
| `0` (DEPENDENCY_JAR) | Auxiliary jar (UDF / connector) | jar files |
| `2` (DEPENDENCY) | Non-jar dependency (.properties etc.) | config files |

**`Type=1` (MAIN) is forbidden for SQL jobs** — it's for JAR job main programs only.

```json
[
  { "ResourceId": "resource-udf", "Type": 0, "Version": 1 },
  { "ResourceId": "resource-cfg", "Type": 2, "Version": 1 }
]
```

> ⚠️ `ResourceRef.Type` (job config level) ≠ `Resource.Type` (upload time: 1=jar, 2=config).

---

## Variable Metadata (`${var}` Placeholders)

When SQL WITH clauses reference workspace variables (`${VAR_NAME}`), the CLI automatically:

1. Scans `CREATE [TEMPORARY] TABLE ... WITH (...)` blocks
2. Extracts `'<key>' = '${<placeholder>[:default]}'` pairs
3. Calls `DescribeVariables` to resolve each placeholder
4. Writes base64 `Metadata` into `ProgramArgs`

If a placeholder has no matching variable, a WARNING is emitted. The job publishes but **fails at runtime**. Fix by creating the variable in the workspace first.

---

## Common Errors

| Error | Cause | Fix |
|---|---|---|
| `InvalidParameterValue.JobName` | Name format invalid | Use ≤50 chars: alphanumeric, Chinese, `-_. ` |
| `InvalidParameterValue.JobNameExisted` | Duplicate name | Choose unique name |
| `ResourceNotFound.ClusterId` | Cluster not found | Check `--cluster_id` |
| `SqlGrammarFailed` | SQL syntax error | Fix SQL, re-run `check_sql` |
| `DraftNotFound` | No draft exists | Run `modify_draft` first |
| `ValidationError: Type=1 forbidden for SQL` | Wrong ResourceRef.Type | Use Type=0 for jars, Type=2 for configs |
