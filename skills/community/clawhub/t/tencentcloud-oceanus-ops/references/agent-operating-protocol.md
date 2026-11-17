# Agent Operating Protocol

Execution protocol for AI agents using the TencentCloud Oceanus CLI skill.

## Execution Entry Point

```bash
cd <skill_directory>/scripts
python oceanus_ops.py <command> [args]
```

## Operation Classification

### Read Operations (no side effects)
- Job: `describe_jobs`, `describe_job_detail`, `describe_job_configs`, `check_sql`, `describe_job_savepoints`
- Job observability: `describe_job_events`, `describe_job_running_log`, `describe_job_log_cos_files`
- Workspace / cluster: `describe_regions`, `describe_workspaces`, `describe_clusters`, `describe_variables`
- Folder: `describe_folder`, `query_folder`
- Resource: `describe_tree_resources`, `create_presigned_url`

**Rule**: Execute immediately without confirmation.

### Mutation Operations (create/modify resources)
- Job: `create_job`, `create_job_config`, `run_jobs`, `trigger_savepoint`
- Folder: `create_folder`, `modify_folder`
- Resource: `create_resource`, `create_resource_config`, `upload_resource`

**Rule**: Require `--confirm` flag. If user gives direct imperative ("帮我创建"), treat as approved.

### Write Operations (safe, no confirmation needed)
- `modify_draft`, `check_sql`

**Rule**: Execute directly (no `--confirm`). These modify draft state but are safe / idempotent.

### Destructive Operations (delete/stop, may lose data)
- `stop_jobs`, `delete_folders`

**Rule**: Always require explicit user intent AND `--confirm` flag. State impact before execution.

## Parameter Auto-Resolution Strategy

The `create_job` command implements an automatic parameter resolution chain that reduces the information users need to provide upfront.

### Resolution Chain

```
region (中文/英文/ap-xxx) → workspace (名称/space-xxx) → cluster (名称/cluster-xxx) → version
```

### Resolution Rules

1. **Region**:
   - Not specified → default `ap-guangzhou`
   - Chinese name (e.g. "广州") → call DescribeRegionZones to resolve to `ap-guangzhou`
   - Already `ap-xxx` format → use directly

2. **Workspace**:
   - Not specified → look up workspace named "default"
   - Name provided → call DescribeWorkSpaces to resolve to `space-xxx`
   - Already `space-xxx` format → use directly (still query for cluster bindings)

3. **Cluster** (requires workspace to be resolved first):
   - Name or ID provided → match from workspace-bound clusters
   - **Not specified → DO NOT auto-select. List all eligible candidates (status=running, FreeCU >= min_cu) and ask user to choose**
   - No eligible candidates → return error with suggestions (switch workspace / bind new cluster / scale up)

4. **Version** (requires cluster to be resolved):
   - Flink version not specified → default `Flink-1.16`
   - JDK version not specified → default `8`
   - Validate against cluster's supported versions

### Agent Behavior for Cluster Selection

When `create_job` returns `needs_selection: true`:
1. Present the candidate list to the user in a readable format
2. Ask the user to choose by name or ID
3. Re-run `create_job` with the selected `--cluster_id` or `--cluster_name`

### Common Defaults
| Parameter | Default |
|-----------|---------|
| --region | ap-guangzhou |
| --cluster_type | 2 (dedicated) |
| --cu_mem | 4 |
| --output | json |

## Safety Gates

### Pre-execution Checklist
1. ✅ Region parameter present
2. ✅ Required parameters for the specific command present
3. ✅ For mutations: `--confirm` present or interactive approval obtained
4. ✅ For destructive: explicit user intent verified

### Credential Protection
- NEVER read or output environment variable values containing secrets
- NEVER embed credentials in commands or logs
- NEVER store credentials in generated files
- The CLI reads credentials internally from environment

## Standard Execution Flow

### For Read Operations
```
1. Validate required parameters
2. Execute command
3. Present result to user
```

### For Mutation Operations
```
1. Validate required parameters
2. Confirm user intent (--confirm or interactive)
3. Execute command
4. If response contains "needs_selection: true":
   a. Present the options to the user
   b. Wait for user to choose
   c. Re-run command with the selected parameters
5. Read-back verify (execute corresponding describe_* command)
6. Present result to user
```

### Handling `needs_selection` Responses

Some commands (e.g. `run_jobs` without `--run_type`) return a `needs_selection: true`
response instead of executing immediately. This means the CLI needs user input to proceed.

**Agent MUST**:
1. Present all listed `options` to the user in a clear, readable format
2. If `savepoint_candidates` are included, display them for reference
3. Wait for the user to choose an option
4. Re-execute the command with the appropriate parameters based on user's choice
5. **NEVER** silently pick an option on behalf of the user
6. **NEVER** ignore the `needs_selection` flag and proceed with a default

### For Multi-step Workflows
```
1. Execute each step in sequence
2. If a step fails, log error and CONTINUE to next step
3. Use output from previous steps as input to next
4. Report per-step results at the end
```

## Output Interpretation

### Success
```json
{
  "success": true,
  "operation": "CreateJob",
  "data": { "JobId": "cql-xxxx" },
  "request_id": "xxx-xxx"
}
```

### Error
```json
{
  "success": false,
  "operation": "CreateJob",
  "error": { "code": "ErrorCode", "message": "..." },
  "request_id": "xxx-xxx"
}
```

When error occurs:
1. Check `references/error-handling.md` for recovery strategy
2. If retryable, attempt retry with backoff
3. If not retryable, report error to user with actionable guidance
