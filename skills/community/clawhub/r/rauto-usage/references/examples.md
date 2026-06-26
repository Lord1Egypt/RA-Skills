# Rauto Execution-Style Prompt Examples (EN)

Use these as few-shot examples for action-first agent behavior.
Default output shape after execution:

```text
Operation: <what was done>
Command: <exact rauto command>
Result: <key outcome>
Notes: <risk/error/follow-up>
```

## Table of Contents

1. Basic execution
2. Templates
3. Saved connections
4. Profiles and templates management
5. Tx block/workflow orchestration
6. Multi-device orchestration
7. Recording/replay/history
8. Web-first requests
9. Backup and restore

## 1) Basic execution

### Example 1.1

User ask:
```text
Run one show command on my device.
```

Execution-style answer:
```text
Operation: Execute direct command on target device
Command: rauto exec "show version" --host <host> --username <username> --password <password>
Result: Command executed; captured version output from device
Notes: If connection fails, verify SSH port/profile credentials
```

### Example 1.2

User ask:
```text
Run it in Enable mode.
```

Execution-style answer:
```text
Operation: Execute direct command with explicit mode
Command: rauto exec "show ip route" --host <host> --username <username> --password <password> --mode Enable
Result: Command executed in Enable mode
Notes: If mode mismatch appears, verify profile prompt/state mapping
```

## 2) Templates

### Example 2.1

User ask:
```text
Preview template output first.
```

Execution-style answer:
```text
Operation: Render template without device execution
Command: rauto template show_vlan.j2 --vars ./vars.json --dry-run
Result: Template rendered successfully; no commands sent to device
Notes: Review rendered commands before live execution
```

### Example 2.2

User ask:
```text
Now execute the rendered template.
```

Execution-style answer:
```text
Operation: Render and execute template on target device
Command: rauto template show_vlan.j2 --vars ./vars.json --host <host> --username <username> --password <password>
Result: Template commands executed on target
Notes: Add recording flags if audit/replay is required
```

## 3) Saved connections

### Example 3.1

User ask:
```text
Save this connection and reuse it.
```

Execution-style answer:
```text
Operation: Save connection profile and run command by profile name
Command: rauto connection add lab1 --host <host> --username <username> --password <password> --ssh-port 22 --device-profile cisco
Result: Saved connection lab1
Notes: Reuse with: rauto exec "show version" --connection lab1
```

### Example 3.2

User ask:
```text
Show history for that saved connection.
```

Execution-style answer:
```text
Operation: Query connection-scoped execution history
Command: rauto history list lab1 --limit 50
Result: Returned recent history entries for lab1
Notes: Use history show with an entry ID for event-level detail
```

## 4) Profiles and templates management

### Example 4.1

User ask:
```text
Copy builtin cisco profile to a custom one.
```

Execution-style answer:
```text
Operation: Duplicate builtin profile to custom profile
Command: rauto device copy-builtin cisco my-cisco --overwrite
Result: Custom profile my-cisco created/updated
Notes: Inspect with: rauto device show my-cisco
```

### Example 4.2

User ask:
```text
Create or update a template for me.
```

Execution-style answer:
```text
Operation: Create/update command template
Command: rauto templates create my_show.j2 --content "show version"
Result: Template created (or use update command if exists)
Notes: Update form: rauto templates update my_show.j2 --file ./my_show.j2
```

## 5) Tx block/workflow orchestration

### Example 5.1

User ask:
```text
Run a tx block with per-step rollback.
```

Execution-style answer:
```text
Operation: Execute tx block with explicit per-step rollback
Command: rauto tx --name vlan10 --command "interface vlan 10" --command "ip address 10.0.10.1 255.255.255.0" --rollback-command "no interface vlan 10" --rollback-command "no ip address 10.0.10.1 255.255.255.0" --host <host> --username <username> --password <password>
Result: Tx block executed with rollback policy per_step
Notes: Use --dry-run first when changing production config
```

### Example 5.2

User ask:
```text
Preview workflow then run it.
```

Execution-style answer:
```text
Operation: Dry-run then execute tx workflow
Command: rauto tx-workflow ./workflow.json --dry-run
Result: Workflow plan validated
Notes: Execute after review: rauto tx-workflow ./workflow.json --host <host> --username <username> --password <password>
```

### Example 5.3

User ask:
```text
Which rollback mode should I pick?
```

Execution-style answer:
```text
Operation: Provide rollback policy recommendation
Command: (no command; policy guidance)
Result: per_step for explicit per-command undo, whole_resource for single-resource undo command
Notes: Prefer preview before execution and explicit rollback commands for ambiguous syntax
```

### Example 5.4

User ask:
```text
Give me a detailed whole-resource rollback tx example with trigger step.
```

Execution-style answer:
```text
Operation: Execute tx block with whole-resource rollback and trigger control
Command: rauto tx --name fw-policy-publish --command "set security policies from-zone trust to-zone untrust policy allow-web match source-address WEB01" --command "set security policies from-zone trust to-zone untrust policy allow-web match destination-address any" --command "set security policies from-zone trust to-zone untrust policy allow-web then permit" --resource-rollback-command "delete security policies from-zone trust to-zone untrust policy allow-web" --rollback-trigger-step-index 0 --mode Config --host <host> --username <username> --password <password>
Result: Tx block executed under whole_resource rollback strategy
Notes: Preview first with --dry-run; use explicit rollback command for policy-like resources
```

### Example 5.5

User ask:
```text
Use rollback commands from file/JSON for per-step tx execution.
```

Execution-style answer:
```text
Operation: Execute tx block with external rollback list
Command: rauto tx --name vlan-batch --command "interface vlan 10" --command "ip address 10.0.10.1 255.255.255.0" --rollback-commands-file ./rollback.txt --rollback-on-failure --mode Config --host <host> --username <username> --password <password>
Result: Tx executed with per-step rollback commands loaded from file
Notes: Alternative JSON input: --rollback-commands-json ./rollback.json ; empty rollback lines are allowed and will be skipped
```

### Example 5.6

User ask:
```text
I need a full tx-workflow run sequence (preview + execute + recording).
```

Execution-style answer:
```text
Operation: Preview and execute tx workflow with recording
Command: rauto tx-workflow ./workflow.json --dry-run
Result: Workflow structure validated before execution
Notes: Execute with recording: rauto tx-workflow ./workflow.json --host <host> --username <username> --password <password> --record-file ~/.rauto/records/tx_workflow.jsonl --record-level key-events-only
```

### Example 5.7

User ask:
```text
I need multi-block orchestration with compensation rollback if a later block fails.
```

Execution-style answer:
```text
Operation: Preview and execute multi-block tx workflow with compensation rollback visibility
Command: rauto tx-workflow ./workflow.json --dry-run
Result: Workflow and rollback plan validated before live execution
Notes: Execute with audit trail: rauto tx-workflow ./workflow.json --connection <connection> --record-file ~/.rauto/records/fw_publish.jsonl --record-level key-events-only ; then verify rollback_attempted/rollback_succeeded/rollback_errors in output
```

### Example 5.8

User ask:
```text
Generate deployment commands for me.
```

Execution-style answer:
```text
Operation: Propose rollback-capable deployment plan (not executed yet)
Planned Command: rauto tx-workflow ./workflow.json --connection <connection>
Result: Change plan prepared with rollback path; waiting for human confirmation
Notes: Preview first: rauto tx-workflow ./workflow.json --dry-run ; execute only after explicit confirmation
```

## 6) Multi-device orchestration

### Example 6.1

User ask:
```text
Preview this multi-device rollout before I execute it.
```

Execution-style answer:
```text
Operation: Preview multi-device orchestration plan
Command: rauto orchestrate ./orchestration.json --dry-run
Result: Orchestration plan validated and normalized
Notes: Use `--view` for terminal structure view; execute only after confirmation
```

### Example 6.2

User ask:
```text
Run this staged rollout across my saved connections.
```

Execution-style answer:
```text
Operation: Execute staged multi-device orchestration
Command: rauto orchestrate ./orchestration.json --record-level full
Result: Stage-by-stage execution started across target devices
Notes: Prefer inventory/groups and inspect per-stage/per-target results after completion
```

### Example 6.3

User ask:
```text
Give me an orchestration JSON with inventory groups for core and access.
```

Execution-style answer:
```text
Operation: Provide runnable multi-device orchestration template
Command: (no command; JSON generation task)
Result: Prepared `orchestration.json` plus `inventory.json` using `target_groups`
Notes: Load `references/orchestration-json-template.md`; preview with `rauto orchestrate ./orchestration.json --dry-run`
```

### Example 6.4

User ask:
```text
How do I run orchestration from the web UI?
```

Execution-style answer:
```text
Operation: Web orchestration guidance
Command: (web UI operation)
Result: Path: Operations -> Tx -> Orchestrate
Notes: Paste JSON, optionally set `base_dir`, then use Preview Orchestration / Execute Orchestration
```

### Example 6.5

User ask:
```text
Review the risk of this orchestration before you run it.
```

Execution-style answer:
```text
Operation: Orchestration risk review
Command: rauto orchestrate ./orchestration.json --dry-run
Result: Plan validated; reviewed target scope, concurrency, fail_fast, and rollback boundary
Notes: Load `references/orchestration-risk-check.md`; require confirmation before live execution
```

## 7) Recording/replay/history

### Example 7.1

User ask:
```text
Record this run and replay later.
```

Execution-style answer:
```text
Operation: Execute with recording and list replayable entries
Command: rauto exec "show version" --host <host> --username <username> --password <password> --record-file ~/.rauto/records/show_version.jsonl --record-level key-events-only
Result: Recording file generated
Notes: Replay list: rauto replay ~/.rauto/records/show_version.jsonl --list
```

### Example 7.2

User ask:
```text
Why replay cannot find my command?
```

Execution-style answer:
```text
Operation: Replay troubleshooting
Command: rauto replay ~/.rauto/records/show_version.jsonl --list
Result: Listed recorded command strings/modes to verify exact match
Notes: Command text and optional mode must match replay query
```

### Example 7.3

User ask:
```text
Show event-level detail for one history entry under a saved connection.
```

Execution-style answer:
```text
Operation: Query history then inspect one event-level entry
Command: rauto history list lab1 --limit 50
Result: Returned ordered history entries with IDs
Notes: Detail view: rauto history show lab1 <history-id> ; machine-readable: rauto history show lab1 <history-id> --json
```

### Example 7.4

User ask:
```text
Give me an auditable execution chain for a saved connection.
```

Execution-style answer:
```text
Operation: Execute, persist record, inspect connection history, and replay
Command: rauto exec "show version" --connection lab1 --record-file ~/.rauto/records/lab1_show_version.jsonl --record-level key-events-only
Result: Command executed with durable recording and connection-bound history entry
Notes: Continue with: rauto history list lab1 --limit 20 ; rauto history show lab1 <history-id> ; rauto replay ~/.rauto/records/lab1_show_version.jsonl --list
```

## 8) Web-first requests

### Example 8.1

User ask:
```text
Start web UI and tell me where to run template execution.
```

Execution-style answer:
```text
Operation: Start web service and provide exact UI path
Command: rauto web --bind 127.0.0.1 --port 3000
Result: Web UI started at http://127.0.0.1:3000
Notes: Use Operations -> Template Render + Execute -> Preview Render -> Run Template
```

### Example 8.2

User ask:
```text
How to run interactive mode in web?
```

Execution-style answer:
```text
Operation: Web interactive session guidance
Command: (web UI operation)
Result: Path: Interactive tab -> Start Session -> Send -> Stop Session
Notes: Ensure valid connection context before starting session
```

## 9) Backup and restore

### Example 9.1

User ask:
```text
Backup all rauto data now.
```

Execution-style answer:
```text
Operation: Create runtime data backup
Command: rauto backup create
Result: Backup archive created under ~/.rauto/backups with timestamp filename
Notes: List backups with: rauto backup list
```

### Example 9.2

User ask:
```text
Use my directory but auto-generate backup filename.
```

Execution-style answer:
```text
Operation: Create backup in custom directory with auto timestamp filename
Command: rauto backup create --output ./backup/
Result: Backup created as ./backup/rauto-backup-<timestamp>.tar.gz
Notes: If output is a file path, that exact filename is used
```

### Example 9.3

User ask:
```text
Restore safely; when should replace be used?
```

Execution-style answer:
```text
Operation: Restore backup in merge/replace modes
Command: rauto backup restore ~/.rauto/backups/rauto-backup-1234567890.tar.gz
Result: Merge restore completed
Notes: Use --replace only for full replacement: rauto backup restore ~/.rauto/backups/rauto-backup-1234567890.tar.gz --replace
```
