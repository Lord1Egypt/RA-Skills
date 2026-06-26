# COMMON.md

This document defines shared conventions across all Flink skills in this repo.
Individual skills SHOULD reference this file instead of duplicating the same rules.

## Common Conventions

### Terminology

- `project_name`: Flink project name (human-readable).
- `job_id`: Flink job/application id used by `volc_flink jobs ... -i <job_id>`.
- `job_name`: User-friendly name; MUST be resolved to `job_id` before any change.
- `draft_id`: Draft id used by `volc_flink drafts ... -i <draft_id>`.
- `draft_name`: Draft name; MUST be resolved to `draft_id` before any change.
- `resource_pool`: Resource pool name used when publishing.

### Golden Rules (MUST)

- Never request or accept plaintext AK/SK in chat.
- Never suggest using `volc_flink login --ak ... --sk ...` in examples or ask users to paste secrets into command-line arguments.
- Never run destructive or state-changing operations without explicit user confirmation.
- Never act on a job/draft that was not explicitly selected/confirmed by the user.
- When ambiguity exists (multiple matches), stop and ask the user to choose.

## Login Preflight

### Tool Presence

- If `volc_flink` is missing, route to `flink-volc` first.
- Verify with:

```bash
volc_flink --version
```

### Login State

- Check login state with:

```bash
volc_flink config show
```

- If the CLI indicates not logged in:
  - Stop the workflow.
  - Ask the user to login via interactive login (`volc_flink login`) or their approved internal method.
  - Do not ask the user to paste AK/SK into chat or into `--ak/--sk` command arguments.

## Scope & Identity (Project/Job/Draft Resolution)

### Project Selection

- If `project_name` is missing:
  - List projects: `volc_flink projects list`
  - Ask the user to choose one project.

### Job Resolution

- If `job_id` is missing but `job_name` exists:
  - Search: `volc_flink jobs list --search <keyword>`
  - If multiple matches, present a numbered list and ask the user to choose.
  - After choosing, confirm: project + job name + job id.

### Draft Resolution

- If `draft_id` is missing:
  - List drafts: `volc_flink drafts apps` (and optionally `volc_flink drafts dirs`)
  - Ask the user to choose a single draft.
  - After choosing, confirm: project + draft name + draft id.

## Risk Confirmation (Change Gate)

Any of the operations below MUST go through risk confirmation:

- `jobs stop`, `jobs restart`, `jobs rescale`
- `drafts publish`
- `drafts update`, `drafts params set`, dependency changes
- savepoint restore / delete (if supported)

### Template

Use the following template and wait for an explicit confirmation (e.g. "yes", "确认", "继续") before proceeding:

```text
⚠️ 操作风险确认

您将要执行以下操作：
- 操作类型: [创建草稿/更新草稿/发布草稿/启动任务/停止任务/重启任务/扩缩容/恢复快照/...]
- 目标对象: [project_name] / [job_name or draft_name]
- 目标 ID: [job_id or draft_id]
- 当前状态: [RUNNING/FAILED/STOPPED/...]
- 变更内容: [what will change]

潜在风险：
- [impact: downtime / delay / data loss risk / resource cost / rollback complexity]

请确认是否继续？(yes/no)
```

## Post-Op Verification (Minimal Set)

After any operation, run the minimal verification set and summarize results:

- `jobs detail -i <job_id>`: state + key config.
- `jobs events -i <job_id>` or `monitor events`: recent lifecycle events.
- `monitor logs -i <job_id> --level ERROR --lines 200`: recent errors.
- For performance/health: `jobs metrics -i <job_id>` (if applicable).

If the job transitioned to `FAILED`, immediately switch to diagnosis workflow:

- Fetch both `ERROR` and `WARN` logs.
- Check both JobManager and TaskManager logs if supported.

## Error Handling (Shared)

### Not Logged In

- Symptom: CLI says "请先登录" or returns auth errors.
- Action:
  - Stop.
  - Ask user to login via `flink-volc` guidance.

### Not Found (Job/Draft/Project)

- Symptom: "not found" / empty results.
- Action:
  - Ask for a wider search keyword or list options.
  - Do not guess.

### Timeout / Network Issues

- Symptom: command timeout, connection errors.
- Action:
  - Recommend retry with reduced scope (smaller time window for logs).
  - If persistent, ask user to check network/VPN/proxy and service status.

## Output Contract (Shared)

When you respond, prefer to include:

- Scope: `project_name`, `job_name/draft_name`, `job_id/draft_id`
- What you did (commands at a high level, not secrets)
- Result: status changes + key evidence (events/log snippets summary)
- Next step (what to do if it fails / how to validate)
