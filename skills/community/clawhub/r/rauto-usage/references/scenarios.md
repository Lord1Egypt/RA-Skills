# Rauto Usage Scenarios

Use these scenarios as ready-to-run examples or checklists. Each scenario includes CLI and Web UI steps when applicable.

## Table of Contents

1. Batch configuration change with rollback (Tx block)
2. Connection test + save connection
3. Template render preview and execute
4. Diagnose profile and fix issues
5. Recording and replay for troubleshooting
6. Tx workflow for multi-block change
7. Manage templates (create/update/delete)
8. Manage profiles (copy builtin to custom)
9. Use saved connection to execute
10. Use interactive session in Web
11. Transaction failure compensation strategy (workflow)
12. Vendor-specific rollback examples
13. Cross-device orchestration (batch execution)
14. Phased rollout / canary execution
15. Post-failure downgrade strategy
16. Cross-device rollback consistency check
17. Cross-device comparison template
18. Quick verification checklist (post-change)
19. Backup and restore playbook

## 1) Batch configuration change with rollback (Tx block)

### CLI

1. Prepare commands:
```
rauto tx \
  --command "set interfaces ge-0/0/1 unit 0 family inet address 10.0.0.2/24" \
  --command "set interfaces ge-0/0/2 unit 0 family inet address 10.0.1.2/24" \
  --rollback-command "delete interfaces ge-0/0/1 unit 0 family inet address 10.0.0.2/24" \
  --rollback-command "delete interfaces ge-0/0/2 unit 0 family inet address 10.0.1.2/24" \
  --mode "Config"
```
2. Preview plan first:
```
rauto tx --dry-run ...same args...
```
3. Use `--rollback-on-failure` if you want a failed step to roll itself back.

### Web UI

1. Operations → Transaction Block.
2. Paste commands, choose rollback policy `per_step`, fill rollback commands.
3. Click “Preview Tx Plan”, then “Execute Tx Block”.

## 2) Connection test + save connection

### CLI

1. Test connection:
```
rauto connection test --host <ip> --username <user> --password <pass>
```
2. Save connection:
```
rauto connection add <name> --host <ip> --username <user> --password <pass> --ssh-port 22
```

### Web UI

1. Fill Connection Defaults (host/port/user/pass/profile).
2. Click “Test Connection”.
3. Enter a saved connection name and click “Save”.

## 3) Template render preview and execute

### CLI

```
rauto template <template-name> --vars /path/to/vars.json --dry-run
rauto template <template-name> --vars /path/to/vars.json
```

### Web UI

1. Operations → Execute → Template Render + Execute.
2. Select template, fill vars JSON.
3. Click “Preview Render”, then “Run Template”.

## 4) Diagnose profile and fix issues

### CLI

```
rauto device diagnose <profile> --json
```
Inspect `unreachable_states`, `dead_end_states`, and missing edge lists.

### Web UI

1. Prompt Profiles → Diagnose.
2. Choose profile, click “Diagnose”.
3. Use built-in profile as baseline; edit custom profile in “Edit” tab.

## 5) Recording & replay for troubleshooting

### CLI

```
rauto exec "show version" --record-file ./session.jsonl --record-level key-events-only
rauto replay ./session.jsonl --list
rauto replay ./session.jsonl --command "show version" --mode Enable
```

### Web UI

1. Execute any command with recording enabled.
2. Open Recording drawer (REC floating button).
3. Use List/Raw view, filters; click “Use in Replay”.
4. Replay tab → List Records / Replay Command.

## 6) Tx workflow for multi-block change

### CLI

1. Build `workflow.json` (TxWorkflow format).
2. Preview:
```
rauto tx-workflow workflow.json --dry-run
```
3. Execute:
```
rauto tx-workflow workflow.json
```

### Web UI

1. Operations → Transaction Block → Tx Workflow.
2. Build blocks in builder; export JSON.
3. Preview workflow and execute.

## 7) Manage templates (create/update/delete)

### CLI

```
rauto templates create my.tpl --file ./my.tpl
rauto templates update my.tpl --content "show version"
rauto templates delete my.tpl
```

### Web UI

1. Template Manager → choose or input name.
2. Edit content, click Save / Delete.

## 8) Manage profiles (copy builtin → custom)

### CLI

```
rauto device copy-builtin cisco my-cisco --overwrite
rauto device show my-cisco
```

### Web UI

1. Prompt Profiles → Built-in → Load → Copy to custom.
2. Edit fields and Save.

## 9) Use saved connection to execute

### CLI

```
rauto exec "show ip int brief" --connection <name>
```

### Web UI

1. Select saved connection from dropdown.
2. Execute commands; history is stored under that connection.

## 10) Use interactive session in Web

1. Interactive tab → Start Session.
2. Send commands iteratively.
3. Stop Session to finalize history/recording.

## 11) Transaction failure compensation strategy (workflow)

Use this when you need “all-or-nothing” semantics across multiple blocks.

### CLI

1. Build `workflow.json` with ordered blocks, and explicit rollback policy per block.
2. Prefer explicit rollback commands for ambiguous vendor syntax.
3. Preview the workflow plan:
```
rauto tx-workflow workflow.json --dry-run
```
4. Execute:
```
rauto tx-workflow workflow.json
```

### Web UI

1. Operations → Transaction Block → Tx Workflow.
2. Add blocks in order; set rollback policy for each block.
3. Use “Preview Workflow” to validate rollback plan.
4. Execute workflow.

## 11.1) Orchestration deep dive (multi-block)

Use this pattern when you need dependent changes across blocks (e.g., address → service → policy).

### Design rules

1. **Order blocks from lowest-risk to highest-impact**: e.g., create objects → bind policy → activate.
2. **Use explicit rollback for ambiguous syntax**: avoid heuristic rollback for policy or ACL changes.
3. **Choose rollback policy per block**:
   - `per_step` for list-like changes (multiple small commands).
   - `whole_resource` for atomic-style objects that can be deleted in one command.
4. **Set `trigger_step_index`** when using whole-resource rollback to ensure rollback only runs after a successful creation step.
5. **Always dry-run first**, then execute with recording enabled.

### Web (Builder) example

1. Create Block A (objects)
   - Rollback: `per_step`
2. Create Block B (services)
   - Rollback: `per_step`
3. Create Block C (policy)
   - Rollback: `whole_resource`
   - `trigger_step_index`: 0
4. Preview Workflow → Execute Workflow.

## 11.2) Complex orchestration examples

### Example A: Firewall publish (address/service/policy)

**Block 1: Address objects**
```
set address-book global address WEB01 10.0.10.10/32
set address-book global address WEB02 10.0.10.11/32
```
Rollback (per-step):
```
delete address-book global address WEB01
delete address-book global address WEB02
```

**Block 2: Service objects**
```
set applications application APP_HTTP protocol tcp destination-port 80
set applications application APP_HTTPS protocol tcp destination-port 443
```
Rollback (per-step):
```
delete applications application APP_HTTP
delete applications application APP_HTTPS
```

**Block 3: Policy**
```
set security policies from-zone trust to-zone untrust policy web-out match source-address WEB01
set security policies from-zone trust to-zone untrust policy web-out match destination-address any
set security policies from-zone trust to-zone untrust policy web-out match application APP_HTTP
set security policies from-zone trust to-zone untrust policy web-out then permit
```
Rollback (whole-resource):
```
delete security policies from-zone trust to-zone untrust policy web-out
```

### Example B: VLAN + SVI + routing update

**Block 1: VLAN**
```
vlan 20
 name USERS
```
Rollback (whole-resource): `no vlan 20`

**Block 2: SVI**
```
interface Vlan20
 ip address 10.20.0.1/24
```
Rollback (whole-resource): `no interface Vlan20`

**Block 3: Routing**
```
ip route 10.20.0.0/24 10.0.0.1
```
Rollback (per-step): `no ip route 10.20.0.0/24 10.0.0.1`

### Example C: ACL + interface binding

**Block 1: ACL**
```
ip access-list extended WEB_OUT
 permit tcp any any eq 80
 permit tcp any any eq 443
```
Rollback (whole-resource): `no ip access-list extended WEB_OUT`

**Block 2: Interface bind**
```
interface GigabitEthernet0/1
 ip access-group WEB_OUT out
```
Rollback (per-step): `interface GigabitEthernet0/1\n no ip access-group WEB_OUT out`

### Example D: BGP neighbor add/remove

**Block 1: Neighbor**
```
router bgp 65001
 neighbor 10.1.1.2 remote-as 65002
 neighbor 10.1.1.2 description PEER-1
```
Rollback (whole-resource): `router bgp 65001\n no neighbor 10.1.1.2`

**Block 2: Policy**
```
route-map RM-OUT permit 10
 match ip address prefix-list PL-OUT
```
Rollback (whole-resource): `no route-map RM-OUT`

## 12) Vendor-specific rollback examples

### Cisco-style (Enable/Config)

Commands:
```
interface Vlan10
 ip address 10.10.10.1 255.255.255.0
```

Per-step rollback:
```
no interface Vlan10
```

### Juniper-style (set/delete)

Commands:
```
set interfaces ge-0/0/1 unit 0 family inet address 10.0.0.2/24
```

Per-step rollback:
```
delete interfaces ge-0/0/1 unit 0 family inet address 10.0.0.2/24
```

### Generic heuristic (no-prefix)

Rule: prefix `no ` for config lines that support negation. Use explicit rollback when unsure.

### Huawei-style (undo)

Commands:
```
interface Vlanif10
 ip address 10.10.10.1 255.255.255.0
```

Per-step rollback:
```
undo interface Vlanif10
```

### Arista EOS-style (no)

Commands:
```
interface Vlan10
 ip address 10.10.10.1/24
```

Per-step rollback:
```
no interface Vlan10
```

### Nokia SR OS-style (no / undo)

Commands:
```
configure router interface "to-core" address 10.0.0.1/24
```

Per-step rollback (example):
```
configure router no interface "to-core"
```

## 13) Cross-device orchestration (batch execution)

Use this when the same change must be applied across multiple devices.

### CLI pattern (`rauto orchestrate`)

```
rauto orchestrate ./orchestration.json --dry-run
rauto orchestrate ./orchestration.json --record-level full
```

Typical plan design:

1. Stage 1: serial rollout for core devices
2. Stage 2: parallel rollout for access devices
3. Reuse `target_groups` and `inventory_file` when the same target sets are used repeatedly
4. Reuse `tx_workflow` for device-internal multi-block changes and `tx_block` for smaller templated changes

### Web pattern

1. Operations -> Tx -> Orchestrate
2. Paste orchestration JSON and optional `base_dir`
3. Preview the plan first
4. Execute orchestration
5. Inspect stage/target result cards and detail views

## 14) Phased rollout / canary execution

Use this when you need a small blast radius before full rollout.

1. **Canary set** (2–3 devices):
   - Run `orchestrate` against a small target group and verify output + history.
2. **Expand** to 25–50% of devices:
   - Expand the inventory group or target list; compare stage and target status.
3. **Full rollout** if no issues detected.

Tips:
- Use recording level `key-events-only` for routine phases, `full` for first canary.
- Keep rollback commands ready and validated before expanding.

## 15) Post-failure downgrade strategy

Use this when a block/workflow fails and you need a safe fallback plan.

1. **Stop further execution** (fail-fast enabled).
2. **Review rollback results**:
   - Check `rollback_attempted` and `rollback_succeeded`.
   - Inspect `rollback_errors` for command failures.
3. **Decide fallback**:
   - If rollback succeeded: re-run after fixing commands or profile.
   - If rollback partially failed: apply explicit rollback commands manually.
4. **Record the remediation**:
   - Save session recording for audit.

## 16) Cross-device rollback consistency check

Use this after multi-device rollouts.

1. Compare history drawer results per device:
   - success status, rollback status, error patterns.
2. Re-run diagnostics or targeted rollback workflows on devices with anomalies.
3. Reconcile state manually where rollback or execution diverged.

## 17) Cross-device comparison template

Use this simple template to track outcomes per device during rollout.

```
Device: <name>
Connection: <saved-connection>
Operation: <exec|template|tx_block|tx_workflow>
Result: <success|failed>
Rollback: <attempted|skipped> / <succeeded|failed>
Notes: <errors or observations>
```

### Markdown table version

| Device | Connection | Operation | Result | Rollback Attempted | Rollback Result | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| edge-1 | prod-edge-1 | orchestrate_tx_workflow | success | attempted | succeeded | - |
| edge-2 | prod-edge-2 | orchestrate_tx_block | failed | attempted | failed | rollback command error |

### JSON template

```
{
  "device": "<name>",
  "connection": "<saved-connection>",
  "operation": "orchestrate_tx_workflow",
  "result": "success",
  "rollback_attempted": true,
  "rollback_result": "succeeded",
  "notes": ""
}
```

## 18) Quick verification checklist (post-change)

Use this checklist after a multi-block workflow:

1. Verify expected interfaces/routes/policies exist.
2. Confirm no orphaned objects remain.
3. Check device prompt/mode and state machine alignment.
4. Review history entries for errors and partial rollbacks.

## 19) Backup and restore playbook

Use this before major rollout or migration.

### CLI

1. Create backup with auto timestamp name:
```
rauto backup create
```
2. Optionally create backup in a custom directory:
```
rauto backup create --output ./backup/
```
3. List backups:
```
rauto backup list
```
4. Restore by merge:
```
rauto backup restore ~/.rauto/backups/rauto-backup-1234567890.tar.gz
```
5. Restore by replace (destructive):
```
rauto backup restore ~/.rauto/backups/rauto-backup-1234567890.tar.gz --replace
```

### Web UI

1. Open Backup tab.
2. Click `Create`.
3. Select backup row.
4. Prefer `Restore (Merge)` first.
5. Use `Restore (Replace)` only when full replacement is intended.
