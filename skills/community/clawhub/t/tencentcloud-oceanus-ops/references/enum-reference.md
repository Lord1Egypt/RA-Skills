# Enum Reference

Authoritative listing of every enum used by the Oceanus CLI / API surface,
with explicit notes on *similar-looking* enums that must NOT be mixed.

## Job Status (`JobItem.Status`)

Returned by `DescribeJobs` / `DescribeJobsExists` / `DescribeJobDetail`.

| Code | Description | 中文 |
| ---- | ----------- | ---- |
| 1 | Uninitialized — just created, not yet configured | 未初始化 |
| 2 | Unpublished — has draft, no published version    | 未发布 |
| 3 | In progress — start/stop in flight              | 操作中 |
| 4 | Running — healthy execution                     | 运行中 |
| 5 | Stopped                                         | 停止 |
| 6 | Paused                                          | 暂停 |
| 7 | Finished (batch jobs)                           | 完成 |

Runtime preconditions:

- `run_jobs`: requires a published config version (auto-checked via `DescribeJobConfigs`).
- `stop_jobs`: requires status ∈ {3, 4}.
- `trigger_savepoint`: requires status = 4.

## Job Type (`--job_type`)

Required for `create_job`, `modify_draft`, `create_job_config`.

| Value | Meaning |
| ----- | ------- |
| 1 | SQL job |
| 2 | JAR job |

The CLI does **not** infer SQL vs JAR from `--entrypoint_class` /
`--resource_refs` / `--program_args`; the agent MUST decide up front.

## Folder Type (`FolderType`)

| Value | Meaning |
| ----- | ------- |
| 0 | Job folder (default) |
| 1 | Dependency-resource folder |

## Resource.Type vs ResourceRef.Type (DO NOT MIX)

These two `Type` fields look similar but live on different objects and use
different value spaces. The CLI validates them strictly.

### `Resource.Type` — describes the artifact itself

Set when **uploading** a resource: `create_resource --resource_type ...`.

| Value | Meaning |
| ----- | ------- |
| 1 | jar package (`RESOURCE_TYPE_JAR`) |
| 2 | config / dependency file (`RESOURCE_TYPE_DEPENDENCY`, e.g. `.properties`) |

### `ResourceRef.Type` — describes how a job *consumes* a resource

Set in the `ResourceRefs` array of `ModifyDraftConfig` / `CreateJobConfig`.
Authoritative backend definition:

```
RESOURCE_REF_USAGE_TYPE_MAIN           = 1
RESOURCE_REF_USAGE_TYPE_DEPENDENCY     = 2
RESOURCE_REF_USAGE_TYPE_DEPENDENCY_JAR = 0
```

| Value | Constant | Meaning | Constraints |
| ----- | -------- | ------- | ----------- |
| 0 | `DEPENDENCY_JAR` | 辅助 jar 包（**非主程序**），例如 UDF jar、connector jar、其它依赖 jar | SQL / JAR 作业引用 **jar 包** 时统一使用 |
| 1 | `MAIN`           | JAR 作业的主程序包 | **仅 JAR 作业**，**恰好一个** 条目；SQL 作业不允许 |
| 2 | `DEPENDENCY`     | 非 jar 的依赖文件（配置文件、资源文件，例如 `.properties` / `.json` / `.conf`） | SQL / JAR 作业引用 **配置文件** 时使用 |

**单个条目 Type 的决策树**：

- 它是 JAR 作业的"主程序包"？→ `Type=1` (MAIN)
- 它是一个 jar 包（非主程序）？→ `Type=0` (DEPENDENCY_JAR)
- 它是配置文件 / 非 jar 资源？→ `Type=2` (DEPENDENCY)

Concretely:

- 一个 UDF jar：上传时 `Resource.Type=1` (jar 包)，作业中引用时
  `ResourceRef.Type=0` (DEPENDENCY_JAR)。
- 一个 `.properties` 配置：上传时 `Resource.Type=2` (配置文件)，作业中
  引用时 `ResourceRef.Type=2` (DEPENDENCY)。
- 一个 JAR 作业的主程序包：上传时 `Resource.Type=1` (jar 包)，作业中
  引用时 `ResourceRef.Type=1` (MAIN)。

`Resource.Type` 与 `ResourceRef.Type` 是 **两个不同的枚举**，不能直接
相互替换。CLI 严格校验：

- JAR 作业必须恰好一个 `Type=1` (MAIN)，0 或 ≥2 个都会被拒绝。
- SQL 作业的 `ResourceRefs` 中出现 `Type=1` 会被立即拒绝。

If the user describes a JAR job but does not say which uploaded jar is the
main program, the CLI fails fast with a `ValidationError`. The agent MUST
ask the user to designate one jar as the main package and emit `Type=1`
for it;其余 jar 用 `Type=0` (DEPENDENCY_JAR)，配置文件用 `Type=2`
(DEPENDENCY)。

## LogCollect — RESPONSE side (DO NOT MIX with the request enum below)

Used by:

- `JobConfig.LogCollect` — returned by `DescribeJobConfigs`
- `JobInstance.JobCollectType` — returned by `DescribeJobRunningLog` (instance list)

Both fields share **the same enum**:

| Value | Constant | Meaning |
| ----- | -------- | ------- |
| 0 | `JobLogCollectDisabled`         | 不采集 |
| 1 | `JobLogCollectEnabled`          | 采集到 CLS |
| 2 | `JobLogCollectHistoryDisabled`  | 历史禁用（兼容旧值，等同于 0） |
| 3 | `JobLogCollectHistoryEnabled`   | 历史启用（兼容旧值，等同于 1） |
| 4 | `JobLogCollectEnabledOnCos`     | 采集到 COS |
| 5 | `JobLogCollectEnabledOnES`      | 采集到 ES |

For COS-collected logs (`4`), use `describe_job_log_cos_files` to enumerate
files and obtain presigned download URLs.

## LogCollectType — REQUEST side

Accepted by `ModifyJobConfig` / `CreateJobConfig` / `ModifyDraftConfig` as
the `LogCollectType` field on the request payload.

| Value | Constant | Meaning |
| ----- | -------- | ------- |
| 2 | `JobLogCollectTypeCLS` | Collect to CLS |
| 3 | `JobLogCollectTypeCOS` | Collect to COS |
| 4 | `JobLogCollectTypeES`  | Collect to ES |

> ⚠️ This is a **different** numbering from the response-side `LogCollect`
> field above. Do NOT translate one to the other directly:
>
> | Intent       | Request `LogCollectType` | Response `LogCollect` / `JobCollectType` |
> | ------------ | ------------------------ | ---------------------------------------- |
> | Disable      | (omit)                   | 0 (or 2 for legacy) |
> | CLS          | 2                        | 1 (or 3 for legacy) |
> | COS          | 3                        | 4 |
> | ES           | 4                        | 5 |

## Run Type (`run_jobs --run_type`)

| Value | Meaning | Required extras |
| ----- | ------- | --------------- |
| 1 | Start from latest state (default) | — |
| 2 | Restore from Savepoint **path**    | `--savepoint_path` |
| 3 | Restore from Savepoint **ID**      | `--savepoint_id` |
| 4 | Start from specific timestamp     | `--custom_timestamp` (ms) |

## Stop Type (`stop_jobs --stop_type`)

| Value | Meaning |
| ----- | ------- |
| 1 | Stop immediately (default) |
| 2 | Trigger a savepoint, then stop (recommended for production) |

## Variable Type (`VariableItem.Type`)

Returned by `describe_variables`. Matches oceanus-galileo
`constants.go` (`VARIABLE_TYPE_*`).

| Value | Constant | Meaning |
| ----- | -------- | ------- |
| 1 | `VISIBLE` | 明文变量，`Value` 字段直接可读 |
| 2 | `HIDDEN`  | 隐藏 / 密文变量，后端会把 `Value` 置为空字符串再返回 — 仅元数据可见 |
| 3 | `SYSTEM`  | 系统内置变量（如 `SYSTEM_VARIABLE_JOB_SERIAL_ID` / `SYSTEM_VARIABLE_CLUSTER_SERIAL_ID`），由后端在响应中自动追加 |

`describe_variables` 在 CLI 层附带 `TypeName` 字段（`VISIBLE` /
`HIDDEN` / `SYSTEM` / `UNKNOWN`），方便 agent 直接判读。在 SQL WITH
子句里通过 `${VarName}` 占位符引用；运行时由后端做模板替换。隐藏型
变量适合用于密码 / 密钥；系统变量在作业实际运行时会被替换为当时的
JobId / ClusterId。

> 注意：后端 `DescribeVariablesReq.SerialIds` 字段在 service 实现中
> 未被使用，CLI 故意不暴露该参数。要按名字筛选请使用 `--name <substring>`
> （后端会执行 SQL LIKE `%v%` 模糊匹配；`%` 字符会被后端拒绝，`_`
> 字符会被自动转义。）

## Catalog Type (`CatalogItem.Type`)

Returned by `describe_catalogs`. Determines which API set to use for browsing
databases and tables within the catalog.

| Value | Constant | Meaning | Query Commands |
| ----- | -------- | ------- | -------------- |
| 0 | `OCEANUS` | 默认内置 catalog（Oceanus Metastore） | `describe_meta_catalogs` / `describe_meta_table` (同步) |
| 1 | `HIVE`    | Hive Metastore catalog | `describe_external_meta_databases` / `describe_external_meta_tables` (异步) |
| 2 | `MYSQL`   | MySQL catalog | `describe_external_meta_databases` / `describe_external_meta_tables` (异步) |
| 3 | `PAIMON`  | Paimon catalog | `describe_external_meta_databases` / `describe_external_meta_tables` (异步) |

**Routing rule:**
- Type = 0 → use `describe_meta_catalogs` (sync, fast)
- Type ≠ 0 → use `describe_external_meta_databases` / `describe_external_meta_tables`
  (async, requires cluster, may take 10-60s)

**Async query flow for external catalogs (type ≠ 0):**
1. CLI sends request with `IsAsync=1`
2. Backend returns `AsyncTaskId` + `AsyncStatus=0` (processing)
3. CLI polls with same params + `AsyncTaskId` until `AsyncStatus=1` (done)
4. Exponential backoff: 1s → 1.5s → 2.25s → ... → max 5s, up to 30 retries (~60s)

## Metadata Table Variable Type (`MetadataV1.Variables[i].type`)

写入 `ProgramArgs.Metadata`（base64 JSON）时每个 variable 条目上的
`type` 字段，**与上面的 `VariableItem.Type` 不是同一枚举**。它来自
oceanus-galileo `constants.go` 的 `METADATA_TABLE_VARIABLE_TYPE_*`：

| Value | Constant | 适用 |
| ----- | -------- | ---- |
| 1 | `META_TABLE`     | 引用了元数据表（metastore）—— 当前 CLI 不构造此类型 |
| 2 | `TEMPORAL_TABLE` | 内联 `CREATE [TEMPORARY] TABLE ... WITH (...)` 中引用变量的最常见情况 |
| 3 | `CDAS`           | `CREATE CATALOG` / `CREATE DATABASE AS` 中引用变量 |

CLI 自动构造 Metadata 时一律使用 `type=2` (TEMPORAL_TABLE)，因为
`modify_draft` 流程仅扫描内联 `CREATE [TEMPORARY] TABLE`
块。详见 `references/playbooks/create-sql-job.md` 的 *Variable Metadata*
小节。
