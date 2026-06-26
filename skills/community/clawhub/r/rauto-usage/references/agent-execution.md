# Rauto Agent Execution Playbook

Use this file when the agent should run `rauto` commands directly for the user.

## Table of Contents

1. Execution decision tree
2. Read/query operations
3. Change operations
4. Destructive operations (confirmation required)
5. Output summarization template
6. Common command templates

## 1) Execution decision tree

1. Classify user intent:
   - Query/read -> execute immediately.
   - Change/apply -> prefer `tx`/`tx-workflow`/`orchestrate` with rollback-aware planning.
   - Destructive -> require explicit confirmation.
2. Resolve connection inputs:
   - Prefer existing `--connection <name>`.
   - Else use provided host/user/password/profile/port.
   - If still missing required fields, ask only for missing fields.
3. For agent-generated change commands:
   - show planned commands + rollback path + dry-run command.
   - for `orchestrate`, also review target scope, `fail_fast`, concurrency, and rollback boundary.
   - wait for user confirmation before live execution.
4. Execute command and capture output.
5. Return concise result summary.

## 2) Read/query operations

Safe to run directly:

- `rauto device list`
- `rauto device show <name>`
- `rauto templates list`
- `rauto templates show <name>`
- `rauto connection list`
- `rauto connection show <name>`
- `rauto history list <name> --limit <N>`
- `rauto replay <record_file> --list`
- `rauto replay <record_file> --command "<cmd>" [--mode <Mode>]`
- `rauto backup list`

Read-only commands (for example `show ...`) do not need transaction wrapping.

## 3) Change operations

Default policy:

- Prefer rollback-capable execution via `rauto tx` / `rauto tx-workflow` / `rauto orchestrate`.
- If user asks for generated deployment commands, propose first and wait for confirmation.
- If user explicitly provides exact command and asks to run now, execute directly.

- `rauto tx ...`
- `rauto tx-workflow ...`
- `rauto orchestrate ...`
- `rauto connection add ...`
- `rauto templates create|update ...`
- `rauto backup create [...]`
- `rauto backup restore <archive>` (merge mode)

## 4) Destructive operations (confirmation required)

Require clear user confirmation before running:

- `rauto backup restore <archive> --replace`
- `rauto connection delete <name>`
- `rauto device delete-custom <name>`
- `rauto templates delete <name>`
- `rauto history delete <name> <id>`

If user already asks explicitly (e.g. "删除", "replace 恢复"), execute directly.

## 5) Output summarization template

After execution, report:

```text
Operation: <what was done>
Command: <exact rauto command>
Result: <success/failure + key fields>
Notes: <risk/errors/next action>
```

For query operations, include only key lines.
For change operations, include target + outcome + rollback/fallback hints when needed.

For proposed (not executed yet) config changes, report:

```text
Operation: <planned change>
Planned Command: <tx/tx-workflow command>
Rollback: <per_step or whole_resource path>
Risk Check: <why safe/unsafe>
Confirmation Needed: <yes>
```

For proposed `orchestrate` changes, prefer the orchestration-specific review from `references/orchestration-risk-check.md`.

## 6) Common command templates

When user asks for workflow JSON content, load:

- `references/workflow-json-template.md`
- `references/orchestration-json-template.md` for multi-device staged execution
- `references/orchestration-risk-check.md` before proposing or executing multi-device rollout
- For vendor-specific orchestration, use sections 3-5 in `references/workflow-json-template.md` (Cisco/Juniper/Huawei).
- For advanced compensation rollback, use section 6 in `references/workflow-json-template.md`.

### Query device profiles and templates

```bash
rauto device list
rauto templates list
```

### Execute one command via saved connection

```bash
rauto exec "show version" --connection <connection>
```

### Execute one command via direct credentials

```bash
rauto exec "show version" \
  --host <host> --username <username> --password <password> \
  --ssh-port 22 --device-profile cisco
```

### Template dry-run then execute

```bash
rauto template <template> --vars <vars.json> --dry-run
rauto template <template> --vars <vars.json> --connection <connection>
```

### Tx workflow

```bash
rauto tx-workflow <workflow.json> --dry-run
rauto tx-workflow <workflow.json> --connection <connection>
```

### Multi-device orchestration

```bash
rauto orchestrate <orchestration.json> --view
rauto orchestrate <orchestration.json> --dry-run
rauto orchestrate <orchestration.json> --record-level full
```

### Safe change sequence (recommended)

```bash
# 1) Build rollback-capable transaction/workflow
# 2) Preview first
rauto tx-workflow <workflow.json> --dry-run

# 3) Execute only after user confirmation
rauto tx-workflow <workflow.json> --connection <connection>
```

For staged multi-device rollout:

```bash
# 1) Build/validate orchestration.json (+ inventory.json when used)
rauto orchestrate <orchestration.json> --dry-run

# 2) Execute only after user confirmation
rauto orchestrate <orchestration.json> --record-level full
```

### Detailed Tx block patterns

```bash
# Per-step rollback with explicit rollback list
rauto tx \
  --name vlan-batch \
  --command "interface vlan 10" \
  --command "ip address 10.0.10.1 255.255.255.0" \
  --rollback-command "no interface vlan 10" \
  --rollback-command "no ip address 10.0.10.1 255.255.255.0" \
  --rollback-on-failure \
  --mode Config \
  --connection <connection>

# Whole-resource rollback with trigger step
rauto tx \
  --name policy-publish \
  --command "set security policies ... policy allow-web then permit" \
  --resource-rollback-command "delete security policies ... policy allow-web" \
  --rollback-trigger-step-index 0 \
  --mode Config \
  --connection <connection>
```

### Detailed Tx workflow run sequence

```bash
# 1) Preview structure and rollback planning
rauto tx-workflow <workflow.json> --dry-run

# 2) Execute with recording for audit/replay
rauto tx-workflow <workflow.json> \
  --connection <connection> \
  --record-file ~/.rauto/records/tx_workflow.jsonl \
  --record-level key-events-only
```

### Backup and restore

```bash
rauto backup create
rauto backup create --output ./backup/
rauto backup list
rauto backup restore <archive.tar.gz>
rauto backup restore <archive.tar.gz> --replace
```
