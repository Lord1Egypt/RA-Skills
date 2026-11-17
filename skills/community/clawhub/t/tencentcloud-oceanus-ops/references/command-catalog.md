# Command Catalog

Complete list of CLI commands organized by workflow module.

## job_development (作业开发 — SQL & JAR)

| Command | Description | Type | API Action |
|---------|-------------|------|------------|
| `create_job` | Create a new job. `--job_type` is REQUIRED (1=SQL, 2=JAR); auto parameter resolution for region/workspace/cluster/version | Mutation | CreateJob |
| `describe_jobs` | Query jobs in workspace (tree structure) | Read | DescribeTreeJobs |
| `describe_job_configs` | Query job configurations / draft | Read | DescribeJobConfigs |
| `modify_draft` | Modify and save draft configuration. `--job_type` is REQUIRED (1=SQL, 2=JAR); SQL writes SQL code + auto Metadata, JAR writes EntrypointClass/ProgramArgs. ResourceRefs is a top-level field for both types | Write | ModifyDraftConfig |
| `check_sql` | Run deep SQL grammar check (SQL jobs only) | Read | CheckSqlDeepGrammar |
| `create_job_config` | Publish current draft as a new version. Reads draft → shows summary → confirms → CreateJobConfig. `--job_type` is REQUIRED. Draft confirmation gate applies (see SKILL.md) | Mutation | CreateJobConfig |

### Folder Management (文件夹管理)

| Command | Description | Type | API Action |
|---------|-------------|------|------------|
| `create_folder` | Create folder (FolderType: 0=job, 1=resource) | Mutation | CreateFolder |
| `describe_folder` | Query folder details by ID | Read | DescribeFolder |
| `query_folder` | Query folder by name | Read | QueryFolder |
| `modify_folder` | Move/rename folder or move jobs | Mutation | ModifyFolder |
| `delete_folders` | Delete folders by IDs | Destructive | DeleteFolders |

## job_runtime (作业运行时)

| Command | Description | Type | API Action |
|---------|-------------|------|------------|
| `describe_job_detail` | Query job details | Read | DescribeJobDetail |
| `run_jobs` | Start/run jobs | Mutation | RunJobs |
| `stop_jobs` | Stop running jobs | Destructive | StopJobs |
| `trigger_savepoint` | Trigger a savepoint | Read | TriggerJobSavepoint |

## resource_management (依赖管理)

| Command | Description | Type | API Action |
|---------|-------------|------|------------|
| `describe_tree_resources` | Query dependency resources in tree structure | Read | DescribeTreeResources |
| `create_resource` | Create dependency resource (jar/config) | Mutation | CreateResource |
| `create_presigned_url` | Get COS presigned upload URL | Read | CreatePresignedUrl |
| `create_resource_config` | Create resource config version | Mutation | CreateResourceConfig |
| `upload_resource` | Orchestrated: presigned URL → COS upload → create version | Mutation | Multiple |

## job_observability (作业可观测)

| Command | Description | Type | API Action |
|---------|-------------|------|------------|
| `describe_job_events` | Query job events by instance (two-phase: instance list → event details) | Read | DescribeJobEvents |
| `describe_job_running_log` | Query job running logs (three-phase: instances → containers → logs) | Read | DescribeJobRunningLog |
| `describe_job_log_cos_files` | List COS log files with presigned download URLs (for COS log type) | Read | COS ListObjects |

## resource_query (资源查询)

| Command | Description | Type | API Action |
|---------|-------------|------|------------|
| `describe_regions` | List available regions | Read | DescribeRegionZones |
| `describe_workspaces` | List workspaces in a region | Read | DescribeWorkSpaces |
| `describe_clusters` | List clusters (optionally by workspace) | Read | DescribeClusters |
| `describe_variables` | List workspace variables for `${var}` substitution in SQL WITH clauses. Optional `--name` does backend LIKE `%v%` match on the variable Name column. Response includes synthetic SYSTEM variables (Type=3). VariableItem.Type: 1=VISIBLE / 2=HIDDEN (Value cleared) / 3=SYSTEM | Read | DescribeVariables |

## metadata_query (元数据 / Catalog 浏览)

| Command | Description | Type | API Action |
|---------|-------------|------|------------|
| `describe_catalogs` | List all catalogs in a workspace (includes type, name, default database). Use to discover available catalogs before browsing databases/tables | Read | DescribeCatalogs |
| `describe_meta_catalogs` | Browse default catalog (type=0, OCEANUS) tree structure: catalogs → databases → tables. Supports `--name` filter for fuzzy match | Read | DescribeMetaCatalogs |
| `describe_meta_table` | Get table details in default catalog: DDL, schema columns, properties, resource refs, version. Requires `--table_id` from describe_meta_catalogs | Read | DescribeMetaTable |
| `describe_external_meta_databases` | List databases in an external catalog (type=1 HIVE / 2 MYSQL / 3 PAIMON). Uses async polling (IsAsync=1). Requires `--catalog_id` + `--cluster_id` + `--flink_version`. WorkSpaceId required for routing | Read | DescribeExternalMetaDatabases |
| `describe_external_meta_tables` | List/detail tables in an external catalog database. Uses async polling (IsAsync=1). Requires `--catalog_id` + `--database_name` + `--cluster_id` + `--flink_version`. Optional `--table_name` for single table detail. Note: WorkSpaceId is NOT sent to this API | Read | DescribeExternalMetaTables |
