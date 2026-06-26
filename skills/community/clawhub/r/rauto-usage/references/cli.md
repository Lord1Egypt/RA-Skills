# Rauto CLI Reference (Full Examples)

Use this file when the user asks for exact CLI commands.

## Table of Contents

1. Common placeholders
2. Core execution
3. Recording and replay
4. Device/profile management
5. Template storage management
6. Saved connections and history
7. Transaction block
8. Transaction workflow
9. Multi-device orchestration
10. Backup and restore
11. Global flags

## 1) Common placeholders

- `<host>`: device IP/FQDN
- `<username>`: SSH username
- `<password>`: SSH password
- `<profile>`: device profile, e.g. `cisco`
- `<connection>`: saved connection name

## 2) Core execution

```bash
# Direct execute
rauto exec "show version" \
  --host <host> --username <username> --password <password> --ssh-port 22

# Direct execute with mode
rauto exec "show ip route" \
  --host <host> --username <username> --password <password> \
  --mode Enable

# Template dry-run preview
rauto template show_version.j2 \
  --vars ./vars.json \
  --dry-run

# Template render + execute
rauto template show_version.j2 \
  --vars ./vars.json \
  --host <host> --username <username> --password <password>

# Use saved connection
rauto exec "show ip int brief" --connection <connection>
```

## 3) Recording and replay

```bash
# Record direct execution
rauto exec "show version" \
  --host <host> --username <username> --password <password> \
  --record-file ~/.rauto/records/show_version.jsonl \
  --record-level key-events-only

# Record with full level
rauto exec "show run" \
  --host <host> --username <username> --password <password> \
  --record-file ~/.rauto/records/show_run.jsonl \
  --record-level full

# Replay inspect
rauto replay ~/.rauto/records/show_version.jsonl --list

# Replay one command
rauto replay ~/.rauto/records/show_version.jsonl \
  --command "show version" --mode Enable
```

## 4) Device/profile management

```bash
# List available profiles
rauto device list

# Show profile detail
rauto device show cisco

# Copy builtin profile to custom
rauto device copy-builtin cisco my-cisco --overwrite

# Delete custom profile
rauto device delete-custom my-cisco

# Diagnose profile
rauto device diagnose cisco
rauto device diagnose cisco --json

# Test connection
rauto connection test \
  --host <host> --username <username> --password <password> --ssh-port 22
```

## 5) Template storage management

```bash
rauto templates list
rauto templates show show_version.j2

rauto templates create show_vlan.j2 --content "show vlan"
rauto templates update show_vlan.j2 --file ./show_vlan.j2
rauto templates delete show_vlan.j2
```

## 6) Saved connections and history

```bash
# Add/update saved connection
rauto connection add lab1 \
  --host <host> --username <username> --password <password> \
  --ssh-port 22 --device-profile cisco

# List/show/delete
rauto connection list
rauto connection show lab1
rauto connection delete lab1

# Save effective connection after successful run
rauto exec "show version" \
  --host <host> --username <username> --password <password> \
  --save-connection lab1 --save-password

# History list/detail/delete
rauto history list lab1 --limit 50
rauto history list lab1 --limit 50 --json
rauto history show lab1 <history-id>
rauto history show lab1 <history-id> --json
rauto history delete lab1 <history-id>
```

## 7) Transaction block

```bash
# Per-step rollback by repeated flags
rauto tx \
  --name vlan-10-change \
  --command "interface vlan 10" \
  --command "ip address 10.0.10.1 255.255.255.0" \
  --rollback-command "no interface vlan 10" \
  --rollback-command "no ip address 10.0.10.1 255.255.255.0" \
  --mode Config \
  --host <host> --username <username> --password <password>

# Per-step rollback from file
rauto tx \
  --command "vlan 20" \
  --rollback-commands-file ./rollback.txt \
  --host <host> --username <username> --password <password>

# Whole-resource rollback
rauto tx \
  --command "vlan 30" \
  --resource-rollback-command "no vlan 30" \
  --rollback-trigger-step-index 0 \
  --host <host> --username <username> --password <password>

# Build command list from template
rauto tx \
  --template vlan_create.j2 --vars ./vars.json \
  --template-profile cisco \
  --host <host> --username <username> --password <password>

# Dry-run and JSON output
rauto tx --command "show version" --dry-run
rauto tx --command "show version" --json --host <host> --username <username> --password <password>
```

## 8) Transaction workflow

```bash
# Visualize workflow structure (ANSI colors enabled by default)
# Disable colors with: NO_COLOR=1
rauto tx-workflow ./workflow.json --view

# Dry-run (prints visual plan by default)
rauto tx-workflow ./workflow.json --dry-run

# Dry-run raw JSON
rauto tx-workflow ./workflow.json --dry-run --json

# Execute
rauto tx-workflow ./workflow.json \
  --host <host> --username <username> --password <password>

# Execute with recording
rauto tx-workflow ./workflow.json \
  --host <host> --username <username> --password <password> \
  --record-file ~/.rauto/records/tx_workflow.jsonl \
  --record-level full
```

## 9) Multi-device orchestration

```bash
# Preview orchestration structure
rauto orchestrate ./orchestration.json --view

# Dry-run normalized plan
rauto orchestrate ./orchestration.json --dry-run

# Dry-run raw JSON
rauto orchestrate ./orchestration.json --dry-run --json

# Execute a staged multi-device plan
rauto orchestrate ./orchestration.json --record-level full

# Execute with saved connection fallback defaults
rauto orchestrate ./orchestration.json --connection <connection>
```

Repo-aligned sample files:

```text
templates/examples/campus-vlan-orchestration.json
templates/examples/campus-inventory.json
templates/examples/fabric-advanced-orchestration.json
templates/examples/fabric-advanced-inventory.json
templates/examples/fabric-change-workflow.json
```

## 10) Backup and restore

```bash
# Create backup with auto timestamp filename
rauto backup create

# Create backup in custom directory (auto timestamp filename)
rauto backup create --output ./backup/

# Create backup with explicit file path
rauto backup create --output ./backup/rauto-prod.tar.gz

# List backups under ~/.rauto/backups
rauto backup list

# Restore by merge
rauto backup restore ~/.rauto/backups/rauto-backup-1234567890.tar.gz

# Restore by replace
rauto backup restore ~/.rauto/backups/rauto-backup-1234567890.tar.gz --replace
```

## 11) Global flags

```text
--host
--username
--password
--ssh-port
--enable-password
--device-profile
--template-dir
--connection
--save-connection
--save-password
```
