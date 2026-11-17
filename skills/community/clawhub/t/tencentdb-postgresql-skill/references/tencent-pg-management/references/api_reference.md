# Management-plane router OpenAPI reference

## Scope

This reference maps one-sentence PostgreSQL management-plane requests to the aligned Tencent Cloud PostgreSQL OpenAPI action set. The management router must infer the real goal first, extract the minimum slot set, select the smallest matching action set, and keep write, fee-impacting, or high-risk actions behind explicit confirmation.

## Direct OpenAPI baseline

- Endpoint: `https://postgres.tencentcloudapi.com`
- Version: `2017-03-12`
- Auth: `TC3-HMAC-SHA256`
- Credentials: `SecretId` / `SecretKey` and optional temporary `Token`; read them from environment variables or other secure runtime context only
- Preferred call path: official Tencent Cloud SDK; fallback: locally generated TC3-signed HTTPS request
- Never put secrets into URLs or query parameters, and never hardcode them in source code or skill files

## Intent routing table

| Intent lane | Typical user intent | Read-only evidence actions | Write or high-risk actions |
|---|---|---|---|
| `overview` | 查看实例状态、实例列表、规格版本、任务状态、只读组现状 | `DescribeDBInstances`, `DescribeDBInstanceAttribute`, `DescribeTasks`, `DescribeReadOnlyGroups` | none |
| `instance-change` | 改名、重启、升降配、隔离、解隔离、内核升级、创建实例、创建只读实例 | `DescribeDBInstanceAttribute`, `DescribeTasks`, `DescribeReadOnlyGroups`, `DescribeRegions`, `DescribeZones`, `DescribeClasses`, `DescribeDBVersions`, `DescribeProductConfig` | `ModifyDBInstanceName`, `ModifyDBInstanceSpec`, `RestartDBInstance`, `IsolateDBInstances`, `DisIsolateDBInstances`, `UpgradeDBInstanceKernelVersion`, `CreateInstances`, `CreateReadOnlyDBInstance` |
| `backup-recovery` | 查看备份、恢复时间窗、创建基础备份、下载备份、克隆恢复 | `DescribeDBInstanceAttribute`, `DescribeTasks`, `DescribeBackupOverview`, `DescribeBaseBackups`, `DescribeLogBackups`, `DescribeAvailableRecoveryTime`, `DescribeCloneDBInstanceSpec` | `DescribeBackupDownloadURL`, `CreateBaseBackup`, `CloneDBInstance` |
| `access-security` | 账号、权限、数据库、owner、公网访问、安全组、SSL | `DescribeDBInstanceAttribute`, `DescribeTasks`, `DescribeAccounts`, `DescribeAccountPrivileges`, `DescribeDatabases`, `DescribeDatabaseObjects`, `DescribeDBInstanceSecurityGroups`, `DescribeDBInstanceSSLConfig` | `CreateAccount`, `DeleteAccount`, `ModifyAccountPrivileges`, `ResetAccountPassword`, `CreateDatabase`, `ModifyDatabaseOwner`, `OpenDBExtranetAccess`, `CloseDBExtranetAccess`, `ModifyDBInstanceSecurityGroups` |

## Routing decision order

1. **Requested outcome first**: prefer the user's actual goal over surface wording. For example, `查看状态并评估是否适合升级规格` still routes to `instance-change`, not `overview`.
2. **Affected object second**: account, database, recovery window, public access, security group, and target spec are stronger routing hints than generic verbs such as `看一下` or `检查`.
3. **Action verb third**: verbs like `重启`、`升配`、`克隆恢复`、`重置密码` confirm the lane when the target object is already clear.
4. **Operations-plane handoff**: if the request is about monitor inspection or slow SQL observation rather than management execution, stop and continue with `tencent-pg-inspection` or `tencent-pg-slowquery-diagnosis`.

## Slot checklist by lane

| Intent lane | Required slots | Common optional slots |
|---|---|---|
| `overview` | region; region-level inventory or instance ID; task goal | readonly group, task status focus |
| `instance-change` | region; existing instance ID or creation target; requested action | target spec, DB version, zone, readonly topology |
| `backup-recovery` | region; instance ID; backup or recovery goal | time window, backup type, clone target, restore point |
| `access-security` | region; instance ID; affected security object | account, database, privilege scope, security group, public-access intent, SSL |

## Routing rules

1. Infer the primary lane from the user's requested outcome, affected object, and action verb before choosing APIs.
2. Prefer the smallest action set that can answer the question; do not fetch unrelated data just because it is available.
3. Start with read-only evidence in every lane, even when the user asks for a write action.
4. If the sentence mixes multiple management lanes, split the task into staged results. Prefer one lane per execution step, and never batch multiple write actions under a single implicit approval.
5. If the request belongs to operations-plane inspection or slow SQL lookup, do not use this router; hand off to the matching operations-plane skill.

## Minimal action selection guidance

### 1. Overview lane
- Use `DescribeDBInstances` for region-level inventory or when the user has not narrowed the target.
- Use `DescribeDBInstanceAttribute` for current lifecycle state, spec, and version.
- Use `DescribeTasks` when recent or ongoing tasks matter.
- Use `DescribeReadOnlyGroups` only when readonly topology is relevant.
- Never execute write actions in this lane.

### 2. Instance-change lane
- Use `DescribeDBInstanceAttribute` and `DescribeTasks` first for all existing-instance changes.
- Use `DescribeReadOnlyGroups` when readonly topology may affect the action.
- Use `DescribeRegions`, `DescribeZones`, `DescribeClasses`, `DescribeDBVersions`, and `DescribeProductConfig` only when the requested change needs sale-option or compatibility evidence.
- Keep `ModifyDBInstanceSpec`, `CreateInstances`, and `CreateReadOnlyDBInstance` clearly marked as fee-impacting.

### 3. Backup-recovery lane
- Use `DescribeBackupOverview` first for current protection posture.
- Add `DescribeBaseBackups`, `DescribeLogBackups`, and `DescribeAvailableRecoveryTime` when recovery readiness matters.
- Use `DescribeCloneDBInstanceSpec` only for clone feasibility planning.
- Treat `DescribeBackupDownloadURL`, `CreateBaseBackup`, and `CloneDBInstance` as explicit-confirmation actions.
- When the current request is only a read-only backup-recovery query such as `DescribeAvailableRecoveryTime`, the response must still include a forward-looking warning: downstream restore / clone / backup download actions are not being executed now, remain `待确认`, and may carry data overwrite risk, access exposure risk, or fee impact.

### 4. Access-security lane
- Use `DescribeAccounts`, `DescribeAccountPrivileges`, `DescribeDatabases`, and `DescribeDatabaseObjects` according to the affected account or database scope.
- Use `DescribeDBInstanceSecurityGroups` and `DescribeDBInstanceSSLConfig` for network exposure and SSL posture.
- Keep password, privilege, public-access, and security-group changes behind explicit confirmation.

## Execution phases

### 1. Read-only evidence phase
- collect only the minimum evidence actions needed for the current lane
- summarize current facts, blockers, compatibility notes, and feasibility
- if the lane is `backup-recovery` and the current result is a recovery window or backup readiness lookup, also state that any follow-up restore / clone / backup download action is still `待确认`
- do not cross into unrelated lanes for convenience

### 2. Confirmation phase
- explicitly say the skill is waiting, using wording such as `等你确认`、`确认后我再继续`、`等你确认后我再执行`
- list the exact pending action and target scope
- explain why the pending action matters for the user's goal
- explain the expected impact, prerequisite checks, and the main risk, such as fee impact, service interruption, security exposure, wrong-target modification, or sensitive data exposure
- mark the action as `待确认`
- wait for explicit user approval before any write, fee-impacting, or high-risk call

### 3. Action execution phase
- execute only the approved action set
- keep the response tied to the approved scope
- return execution status, follow-up risks, and the next safe step

### 4. Staged multi-lane handling
- if one sentence spans multiple lanes, choose one primary lane first
- finish the current lane or stop at `待确认`
- then suggest the next lane as a separate step instead of mixing actions together

## Confirmation policy

- `ModifyDBInstanceName`: explicit confirmation required
- `ModifyDBInstanceSpec`: fee-impacting, explicit confirmation required
- `RestartDBInstance`: explicit confirmation required
- `IsolateDBInstances`: explicit confirmation required
- `DisIsolateDBInstances`: explicit confirmation required
- `UpgradeDBInstanceKernelVersion`: explicit confirmation required
- `CreateInstances`: fee-impacting, explicit confirmation required
- `CreateReadOnlyDBInstance`: fee-impacting, explicit confirmation required
- `DescribeBackupDownloadURL`: explicit confirmation required before returning or using download links
- `CreateBaseBackup`: explicit confirmation required
- `CloneDBInstance`: fee-impacting, explicit confirmation required
- `CreateAccount`: explicit confirmation required
- `DeleteAccount`: explicit confirmation required
- `ModifyAccountPrivileges`: explicit confirmation required
- `ResetAccountPassword`: explicit confirmation required
- `CreateDatabase`: explicit confirmation required
- `ModifyDatabaseOwner`: explicit confirmation required
- `OpenDBExtranetAccess`: security-impacting, explicit confirmation required
- `CloseDBExtranetAccess`: explicit confirmation required
- `ModifyDBInstanceSecurityGroups`: security-impacting, explicit confirmation required

## Output schema

### 1. Target scope
- region
- instance or creation target
- optional object such as account, database, target spec, recovery window, or security group

### 2. Recognized intent
- primary lane
- reason for routing
- requested outcome
- extracted slots that affected API selection

### 3. Current facts
- read-only evidence gathered from the routed actions
- blockers, prerequisites, or compatibility notes

### 4. Action status
- actions inspected
- actions proposed or executed
- confirmation items still pending
- explicit waiting wording when confirmation is still required
- for recovery-window lookups, downstream restore / clone / backup download actions that remain `待确认`

### 5. Safe next step
- continue read-only review
- wait for explicit approval
- state what will happen after confirmation and why that step matters
- summarize the main risk or impact of the pending action
- for recovery-window lookups, clearly say that any restore / clone / backup download continuation requires explicit confirmation first
- hand off to an operations-plane skill when the request is inspection or slow SQL only

## Guardrails

- Never call any action outside the aligned list above.
- Never skip read-only evidence before proposing or executing a write action.
- Never expose secrets, passwords, or raw download links in plain summaries.
- Keep results factual, structured, and directly tied to the detected user intent.
