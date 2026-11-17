# Delete / Cleanup

Calls `scripts/delete_stack.sh` to perform full stack destruction.

---

## Invocation

```bash
bash scripts/delete_stack.sh --project-root . --yes
```

`--yes` skips CLI interactive confirmation (Agent should have already obtained user confirmation via AskUserQuestion).

---

## Execution Flow

1. Reads `.qwencloud-deploy` state file, extracts `stack_id`, `region_id`, `artifact_bucket`
2. `aliyun ros DeleteStack` initiates deletion
3. Polls `GetStack` until 404 (DELETE_COMPLETE), timeout 20 min (45 min with RDS)
4. Cleans OSS temporary bucket (`oss rm -r -f` + `oss rm -b -f`)
5. Removes local `.qwencloud-deploy` and `.qwencloud-deploy.local`

> If step 3 fails or times out (DELETE_FAILED / timeout / DeleteStack error), the script **still runs step 4 to clean the OSS bucket**,
> then prints what is left plus a "re-run this script later" hint and exits with code 2; the state file is kept so the run can be retried.

---

## Pre-deletion Confirmation (Agent MUST do)

> ⚠️ **Irreversible** — Agent must confirm via AskUserQuestion before calling:
> - Clearly state the scope (which resources will be deleted)
> - With RDS: extra warning that database data will be destroyed along with the RDS instance and cannot be recovered — recommend exporting a backup first

---

## Error Handling

| Situation | Script Behavior |
|-----------|-----------------|
| Stack already gone (404) | Treated as success, continues to OSS cleanup |
| DELETE_FAILED | Exit code 2, suggests checking `ListStackResources` for cause |
| Timeout | Exit code 2, suggests checking console |
| OSS bucket cleanup fails | Warning only, non-blocking (bucket has 7-day lifecycle auto-expiry) |

---

## Critical Rule

> 🚫 **Never manually delete individual cloud resources** (ECS, VPC, security groups, EIP, etc.).
> In full-stack mode all resources are managed by the ROS stack — just run this script; ROS automatically releases resources in dependency order.
> Manual deletion causes stack state inconsistency, orphaned resources, and deletion failures.

---

## Required State File Fields

The script reads these fields from `.qwencloud-deploy`; missing required fields abort without deleting anything:

| Field | Purpose |
|-------|---------|
| `region_id` (required) | Locate the stack's region |
| `stack_id` (required) | DeleteStack target |
| `stack_name` | Log display |
| `artifact_bucket` | OSS bucket cleanup |
| `db_engine` | Determines timeout (45 min with RDS) |
| `outputs.public_ip` | Shown in confirmation prompt |
