---
name: tencentcloud-oceanus-ops
description: |
  Use for TencentCloud Oceanus (流计算 Oceanus) operations: SQL/JAR job CRUD, job config,
  run/stop jobs, dependency/resource management, job events/logs, workspace/folder ops.
  Trigger on keywords: job, 作业, workspace, 工作空间, 集群, 依赖, resource, 日志, log,
  or IDs matching space-*, cluster-*, cql-*. Also trigger when user asks to run oceanus_ops.py.
  Do NOT trigger for generic cloud tasks (CVM, COS, TKE, billing) or cluster lifecycle (create/scale/delete cluster).

license: Apache-2.0
compatibility: Requires Python 3.8+ (standard library only, no external dependencies). TencentCloud credentials via environment variables TENCENTCLOUD_SECRET_ID / TENCENTCLOUD_SECRET_KEY.
metadata:
  domain: aiops
  owner: oceanus-team
  allowed-tools: Bash Read Write
---

# TencentCloud Oceanus Ops

Operate Oceanus workspace resources via CLI:

```
python scripts/oceanus_ops.py <command> [args]
```

This file is the **navigation hub**. Detailed protocol, command catalog, enums,
and step-by-step playbooks live under `references/`. Always load the linked
reference for any non-trivial task instead of guessing.

## Mandatory Execution Rule

When this skill is triggered, you MUST execute real CLI commands using
`python scripts/oceanus_ops.py`. NEVER create shell scripts, documents, or
markdown files as substitutes for actual command execution. NEVER use `tccli`,
`kubectl`, or any other CLI — only `python scripts/oceanus_ops.py`.

Once triggered, execute a concrete CLI command immediately. Never stop at
templates, `--help` output, or pure explanation.

## Scope & Boundaries

**In scope** — Oceanus workspace operations:

- SQL jobs / JAR jobs (create, configure, publish, run, stop, savepoint)
- Workspace, folder, dependency-resource (jar/config) management
- Catalog / database / table metadata browsing
- Job observability — events, running logs, COS log files

**Out of scope** (do NOT handle):

- Cluster lifecycle (create / scale / delete cluster)
- Container or pod troubleshooting
- Other compute engines (EMR, DLC, …)
- Generic cloud infrastructure (CVM / VPC / billing)

## Trigger Conditions

Trigger this skill when the request matches Oceanus context **and** at least one of:

1. Operation keywords: `job`, `SQL作业`, `JAR作业`, `作业配置`, `workspace`,
   `工作空间`, `集群`, `folder`, `文件夹`, `依赖`, `dependency`, `resource`, `jar`,
   `配置文件`, `上传`, `事件`, `日志`, `运行日志`, `log`, `catalog`, `元数据`,
   `metadata`, `数据库`, `database`, `表`, `table`.
2. Resource ID patterns: `space-*`, `cluster-*`, `cql-*`, `folder-*`, `resource-*`.
3. Oceanus-specific verbs: create / describe / run / stop / publish a job;
   upload / version / query a resource; query job events / running log / COS files.

Do NOT trigger for generic cloud prompts without Oceanus context.

## Execution Protocol (Hard Rules)

### Region is mandatory

Every command MUST include `--region <region>`. If the user omits it, default
to `--region ap-guangzhou`. Never run a command without `--region`.

### Approval gates

| Class | Examples | Rule |
| ----- | -------- | ---- |
| Read        | `describe_*`                                        | Execute directly. |
| Write       | `modify_draft`, `check_sql`                         | Execute directly (no `--confirm` needed). These modify draft state but are safe / idempotent. |
| Mutation    | `create_job`, `run_jobs`, `create_resource`, `upload_resource`, `create_job_config` | Requires `--confirm`. Direct imperative ("帮我创建/运行") counts as approval; tentative phrasing ("能不能/先看看") requires explicit confirmation first. |
| Destructive | `stop_jobs`, `delete_folders` | Requires explicit user intent **and** `--confirm`. State the impact before executing. |

### Draft confirmation (独立门控) — CRITICAL

`create_job_config` produces a draft summary before publishing. This is a
**mandatory human-review gate** that is independent of the `--confirm`
approval gate above.

**Hard rules (NEVER violate):**

1. **NEVER pass `--skip_draft_confirm`** unless the user's message contains
   an explicit phrase such as "跳过审核", "skip review", "直接发布",
   "不用确认草稿". Implied urgency or convenience is NOT sufficient.
2. When the draft summary is displayed, you MUST present it to the user and
   **wait for explicit approval** ("确认发布", "OK", "没问题", "发布吧")
   before proceeding. Do NOT auto-approve on behalf of the user.
3. If the CLI outputs the draft to a temporary file, read and display the
   key changes (SQL diff / resource changes / config deltas) to the user.
4. Violation of this gate is a **critical protocol breach** — equivalent to
   executing a destructive operation without consent.

- `--skip_draft_confirm`: skip the review (**automation-only flag**; agent
  must NEVER use it unless user explicitly opted out of review).

### Credential safety (CRITICAL)

`TENCENTCLOUD_SECRET_ID` / `TENCENTCLOUD_SECRET_KEY` /
`TENCENTCLOUD_SECURITY_TOKEN` are secrets. Hard rules:

1. NEVER read, print, or echo their values (no `echo $TENCENTCLOUD_*`,
   `env | grep TENCENT`, `printenv`, …).
2. NEVER ask the user to paste keys into chat. Have them configure locally.
3. Never embed credentials in command arguments or generated files. The CLI
   reads them from the environment.
4. If a tool result accidentally surfaces a credential value, redact it
   (`***REDACTED***`) before quoting back to the user.
5. On `MissingCredentials` error: stop further execution, follow the OS-tailored
   setup flow in `references/credential-setup.md`, and wait for "已配置".

Full setup templates and reply boilerplate: **`references/credential-setup.md`**.

## Resources Map

### Always consult after triggering

- **`references/agent-operating-protocol.md`** — Execution flow, classification,
  output interpretation, parameter auto-resolution.
- **`references/command-map.md`** — Intent → command routing table with
  disambiguation rules.
- **`references/command-catalog.md`** — Full command list grouped by module.

### Load on demand

- **`references/credential-setup.md`** — OS-specific persistent credential
  setup; `MissingCredentials` recovery flow.
- **`references/enum-reference.md`** — Authoritative listing of every enum
  (Job Status, Job Type, Resource.Type vs ResourceRef.Type, LogCollect
  request/response sides, Run Type, Stop Type, FolderType, VariableItem.Type).
- **`references/error-handling.md`** — Recovery strategies when a CLI command
  returns `success: false` or non-zero exit.
- **`references/oceanus-product-model.md`** — Domain model
  (workspace / cluster / job / config / instance).

### Playbooks (multi-step workflows)

- **`references/playbooks/create-sql-job.md`** — SQL job: create_job →
  [upload deps] → modify_draft → check_sql → create_job_config → run_jobs.
- **`references/playbooks/create-jar-job.md`** — JAR job: upload main jar →
  create_job → modify_draft → create_job_config → run_jobs.
- **`references/playbooks/modify-job-config.md`** — Modify existing job:
  describe_job_configs → [resource changes] → modify_draft → [check_sql] →
  create_job_config.
- **`references/playbooks/job-runtime-ops.md`** — Run / stop / savepoint and
  the most common operational scenarios.
- **`references/playbooks/job-observability.md`** — Events, running log
  (CLS / ES), COS log file enumeration, "why is this job restarting" recipe.
- **`references/playbooks/dependency-management.md`** — Resource lifecycle
  (upload, version, query, folder organization).

## Common Args Cheatsheet

```
--region <region>          # required; default ap-guangzhou (Chinese name accepted: "广州")
--workspace_id <id>        # space-xxx, or workspace name like "default"
--cluster_id <id>          # cluster-xxx, or cluster name
--job_type {1|2}           # 1=SQL, 2=JAR — required for create/modify/publish job config
-o {json|table|text}       # output format, default json
--confirm                  # required for Mutation / Destructive
```

## Assets

- `scripts/oceanus_ops.py` — main CLI entry
- `scripts/client.py` — TencentCloud API client (TC3-HMAC-SHA256)
- `scripts/job_development.py` — job development atomic commands (create / describe / modify_draft / check_sql / create_job_config)
- `scripts/job_config_helpers.py` — SQL/JAR payload builders, constants, draft confirmation
- `scripts/folder_management.py` — folder CRUD operations (create / describe / query / modify / delete)
- `scripts/resource_change_ops.py` — resource change processing utilities
- `scripts/job_runtime.py` — runtime ops (run / stop / savepoint)
- `scripts/job_observability.py` — events / logs / COS log files
- `scripts/resource_management.py` — dependency resource lifecycle
- `scripts/resource_resolver.py` — region/workspace/cluster/version auto-resolution
- `scripts/resource_query.py` — `describe_regions` / `describe_workspaces` / `describe_clusters`
- `scripts/metadata_query.py` — catalog/database/table metadata browsing (`describe_catalogs` / `describe_meta_catalogs` / `describe_meta_table` / `describe_external_meta_databases` / `describe_external_meta_tables`)
- `scripts/unit_test.py` — offline unit tests for pure-logic helpers (no network / no credentials). Run via `python scripts/unit_test.py` or `python -m unittest discover -s scripts -p 'unit_test.py' -v`.
- `scripts/e2e_test.py` — end-to-end CLI tests; requires `TENCENTCLOUD_SECRET_ID` / `TENCENTCLOUD_SECRET_KEY`.
- `assets/requirements.txt` — Python dependencies (currently none — stdlib only)
