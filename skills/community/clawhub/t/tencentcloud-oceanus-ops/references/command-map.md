# Command Map — Intent to Command Routing

Quick lookup from user intent to the correct CLI command.

## High-Frequency Intents

| User Intent (用户意图) | Command | Safety Level |
|------------------------|---------|-------------|
| 创建 SQL 作业 / create SQL job | `create_job --name <n> --job_type 1 --confirm` | Mutation |
| 创建 JAR 作业 / create JAR job | `create_job --name <n> --job_type 2 --confirm` | Mutation |
| 查看作业列表 / list jobs | `describe_jobs --category folderName` | Read |
| 查看指定作业 / get job details | `describe_job_detail --job_id <id>` | Read |
| 查询地域列表 / list regions | `describe_regions` | Read |
| 查询工作空间 / list workspaces | `describe_workspaces` | Read |
| 查询集群列表 / list clusters | `describe_clusters --workspace_id <id>` | Read |
| 查询作业配置 / get job config | `describe_job_configs --job_id <id>` | Read |
| 查询变量列表 / list variables | `describe_variables --workspace_id <id> [--name <substring>]` | Read |
| 修改草稿 (SQL) / modify SQL draft | `modify_draft --job_id <id> --job_type 1 --sql <sql> [--resource_refs <json>]` | Write |
| 修改草稿 (JAR) / modify JAR draft | `modify_draft --job_id <id> --job_type 2 --entrypoint_class <cls> [--resource_refs <json>]` | Write |
| SQL 语法检查 / check SQL | `check_sql --job_id <id> --sql <sql>` | Read |
| 发布新版本 / publish config version | `create_job_config --job_id <id> --job_type <1\|2> --confirm` | Mutation |
| 启动作业 / run job | `run_jobs --job_id <id> --confirm` | Mutation |
| 停止作业 / stop job | `stop_jobs --job_id <id> --confirm` | Destructive |
| 查询依赖列表 / list resources | `describe_tree_resources` | Read |
| 查询 catalog 列表 / list catalogs | `describe_catalogs --workspace_id <id>` | Read |
| 查询默认 catalog 表 / browse default catalog | `describe_meta_catalogs --workspace_id <id>` | Read |
| 查询默认 catalog 表详情 / default catalog table detail | `describe_meta_table --table_id <id> --workspace_id <id>` | Read |
| 查询外部 catalog 数据库 / external catalog databases | `describe_external_meta_databases --catalog_id <id> --cluster_id <id> --flink_version <ver> --workspace_id <id>` | Read |
| 查询外部 catalog 表 / external catalog tables | `describe_external_meta_tables --catalog_id <id> --database_name <name> --cluster_id <id> --flink_version <ver> --workspace_id <id>` | Read |
| 创建依赖资源 / create resource | `create_resource --name <n> --resource_type <1\|2> --confirm` | Mutation |
| 上传依赖 / upload resource | `upload_resource --resource_id <id> --file <path> --confirm` | Mutation |
| 获取上传链接 / get upload URL | `create_presigned_url --file_name <name>` | Read |
| 创建资源版本 / create version | `create_resource_config --resource_id <id>` | Mutation |
| 创建文件夹 / create folder | `create_folder --folder_name <name> --confirm` | Mutation |
| 查询作业事件 / job events | `describe_job_events --job_id <id>` | Read |
| 查询作业事件详情 / job event details | `describe_job_events --job_id <id> --running_order_ids <ids>` | Read |
| 查询作业日志 / job running log | `describe_job_running_log --job_id <id>` | Read |
| 查询作业日志内容 / job log content | `describe_job_running_log --job_id <id> --running_order_id <id> --container <name>` | Read |
| 查询COS日志文件 / COS log files | `describe_job_log_cos_files --job_id <id> --running_order_id <id>` | Read |
| 下载作业日志 / download job log | `describe_job_log_cos_files --job_id <id> --running_order_id <id>` | Read |

## Parameter Auto-Resolution

The `create_job` command supports automatic parameter resolution:

| Parameter | Input Formats | Default |
|-----------|--------------|---------|
| `--region` | 中文名("广州"), ap-xxx | ap-guangzhou |
| `--workspace_id` or `--workspace_name` | 名称("default"), space-xxx | "default" |
| `--cluster_id` or `--cluster_name` | 名称, cluster-xxx | 列出候选供用户选择 |
| `--flink_version` | e.g. Flink-1.16 | Flink-1.16 |
| `--jdk_version` | e.g. 8, 11 | 8 |

### Cluster Selection Flow

When `--cluster_id` / `--cluster_name` is not provided:
1. Query clusters bound to the resolved workspace
2. Filter by status=running AND free_cu >= min_cu
3. **List candidates for user to choose** (NOT auto-select)
4. If no candidates: suggest switching workspace or binding new cluster

## Disambiguation Rules

1. **"工作空间"** in Oceanus context means the Flink workspace (space-xxxx), not a generic project space.
2. **"集群"** refers to Oceanus dedicated/shared clusters, not Kubernetes clusters or EMR clusters.
3. **"创建作业"** must always pass `--job_type` explicitly: `--job_type 1` for SQL, `--job_type 2` for JAR. The CLI does **not** default to SQL or infer the type from other flags. If the user does not say SQL or JAR, ASK before executing.
4. **"配置"** in job context means JobConfig (code + resources + parameters), not infrastructure configuration.
5. **"JAR作业"** or **"jar作业"** implies `--job_type 2`. JAR jobs require `--entrypoint_class` and `--resource_refs` instead of SQL code, and the `--resource_refs` array MUST contain exactly one entry with `Type=1` (MAIN). 其余辅助 jar 用 `Type=0` (DEPENDENCY_JAR)，配置文件用 `Type=2` (DEPENDENCY)。If the user does not designate which jar is the main program, ASK them to choose before executing.
6. **"发布"** for JAR jobs skips SQL grammar check (CheckSqlDeepGrammar).
7. **"resource_refs"** / **"依赖引用"** is supported by both SQL and JAR jobs. `ResourceRef.Type` 按用途取值：`0` = DEPENDENCY_JAR（辅助 jar 包，非主程序）、`1` = MAIN（JAR 主程序，仅 JAR 作业且恰好一个）、`2` = DEPENDENCY（非 jar 的依赖文件，例如配置文件）。SQL 作业禁止 `Type=1`：jar 引用必须用 `Type=0`，配置文件用 `Type=2`。JAR 作业必须恰好有一个 `Type=1`，其余 jar 用 `Type=0`、配置文件用 `Type=2`。`ResourceRef.Type` is NOT the same enum as `Resource.Type` (see `references/enum-reference.md` for both enums).

## Common Argument Patterns

### Required for all commands
```
--region <region>          # e.g. ap-guangzhou, ap-beijing, or Chinese name like "广州"
```

### Recommended for most commands
```
--workspace_id <id>        # e.g. space-1327 or workspace name like "default"
```

### For mutation/destructive operations
```
--confirm                  # Required flag to bypass safety check
```

## Safety Level Definitions

| Level | Description | --confirm Required |
|-------|-------------|-------------------|
| Read | Query/list operations, no side effects | No |
| Mutation | Create/modify resources | Yes |
| Destructive | Delete/stop operations, may cause data loss | Yes (explicit intent required) |
