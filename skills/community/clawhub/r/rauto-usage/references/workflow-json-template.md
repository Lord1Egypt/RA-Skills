# Tx Workflow JSON Templates (EN)

Use this file when the agent needs to provide a runnable `workflow.json`.

## Table of Contents

1. Minimal runnable workflow (per_step)
2. Whole-resource rollback template (with trigger_step_index)
3. Cisco workflow template (VLAN + SVI)
4. Juniper workflow template (security policy)
5. Huawei workflow template (ACL rule)
6. Multi-block compensation workflow (advanced)

## 1) Minimal runnable workflow (per_step)

This is the smallest practical structure for `rauto tx-workflow`.

```json
{
  "name": "minimal-vlan-workflow",
  "fail_fast": true,
  "blocks": [
    {
      "name": "vlan-10",
      "kind": "config",
      "fail_fast": true,
      "rollback_policy": "per_step",
      "steps": [
        {
          "mode": "Config",
          "command": "vlan 10",
          "timeout_secs": 10,
          "rollback_command": "no vlan 10",
          "rollback_on_failure": false
        },
        {
          "mode": "Config",
          "command": "name USERS",
          "timeout_secs": 10,
          "rollback_command": "no name USERS",
          "rollback_on_failure": false
        }
      ]
    }
  ]
}
```

Run:

```bash
rauto tx-workflow ./workflow.json --dry-run
rauto tx-workflow ./workflow.json --connection <connection>
```

## 2) Whole-resource rollback template (with trigger_step_index)

Use this for object-like resources that should be rolled back as one unit.

```json
{
  "name": "policy-publish-workflow",
  "fail_fast": true,
  "blocks": [
    {
      "name": "publish-policy",
      "kind": "config",
      "fail_fast": true,
      "rollback_policy": {
        "whole_resource": {
          "mode": "Config",
          "undo_command": "delete security policies from-zone trust to-zone untrust policy allow-web",
          "timeout_secs": 10,
          "trigger_step_index": 0
        }
      },
      "steps": [
        {
          "mode": "Config",
          "command": "set security policies from-zone trust to-zone untrust policy allow-web match source-address WEB01",
          "timeout_secs": 10,
          "rollback_command": null,
          "rollback_on_failure": false
        },
        {
          "mode": "Config",
          "command": "set security policies from-zone trust to-zone untrust policy allow-web then permit",
          "timeout_secs": 10,
          "rollback_command": null,
          "rollback_on_failure": false
        }
      ]
    }
  ]
}
```

Run with recording:

```bash
rauto tx-workflow ./workflow.json \
  --connection <connection> \
  --record-file ~/.rauto/records/tx_workflow.jsonl \
  --record-level key-events-only
```

## 3) Cisco workflow template (VLAN + SVI)

Use this for Cisco IOS/IOS-XE style interface provisioning with per-step rollback.

```json
{
  "name": "cisco-vlan-svi-workflow",
  "fail_fast": true,
  "blocks": [
    {
      "name": "create-vlan-120",
      "kind": "config",
      "fail_fast": true,
      "rollback_policy": "per_step",
      "steps": [
        {
          "mode": "Config",
          "command": "vlan 120",
          "timeout_secs": 10,
          "rollback_command": "no vlan 120",
          "rollback_on_failure": true
        },
        {
          "mode": "Config",
          "command": "name USERS_120",
          "timeout_secs": 10,
          "rollback_command": "no name USERS_120",
          "rollback_on_failure": false
        }
      ]
    },
    {
      "name": "create-svi-120",
      "kind": "config",
      "fail_fast": true,
      "rollback_policy": "per_step",
      "steps": [
        {
          "mode": "Config",
          "command": "interface vlan 120",
          "timeout_secs": 10,
          "rollback_command": "no interface vlan 120",
          "rollback_on_failure": true
        },
        {
          "mode": "Config",
          "command": "ip address 10.120.0.1 255.255.255.0",
          "timeout_secs": 10,
          "rollback_command": "no ip address 10.120.0.1 255.255.255.0",
          "rollback_on_failure": false
        },
        {
          "mode": "Config",
          "command": "no shutdown",
          "timeout_secs": 10,
          "rollback_command": "shutdown",
          "rollback_on_failure": false
        }
      ]
    }
  ]
}
```

Run:

```bash
rauto tx-workflow ./workflow.json --dry-run
rauto tx-workflow ./workflow.json --connection <connection>
```

## 4) Juniper workflow template (security policy)

Use whole-resource rollback for policy objects where a single delete command can cleanly undo all set commands.

```json
{
  "name": "juniper-policy-workflow",
  "fail_fast": true,
  "blocks": [
    {
      "name": "publish-allow-web-policy",
      "kind": "config",
      "fail_fast": true,
      "rollback_policy": {
        "whole_resource": {
          "mode": "Config",
          "undo_command": "delete security policies from-zone trust to-zone untrust policy allow-web",
          "timeout_secs": 10,
          "trigger_step_index": 0
        }
      },
      "steps": [
        {
          "mode": "Config",
          "command": "set security policies from-zone trust to-zone untrust policy allow-web match source-address WEB01",
          "timeout_secs": 10,
          "rollback_command": null,
          "rollback_on_failure": false
        },
        {
          "mode": "Config",
          "command": "set security policies from-zone trust to-zone untrust policy allow-web match destination-address any",
          "timeout_secs": 10,
          "rollback_command": null,
          "rollback_on_failure": false
        },
        {
          "mode": "Config",
          "command": "set security policies from-zone trust to-zone untrust policy allow-web then permit",
          "timeout_secs": 10,
          "rollback_command": null,
          "rollback_on_failure": false
        }
      ]
    }
  ]
}
```

Run:

```bash
rauto tx-workflow ./workflow.json --dry-run
rauto tx-workflow ./workflow.json --connection <connection> --record-level key-events-only
```

## 5) Huawei workflow template (ACL rule)

Use this for ACL rule publishing with explicit per-step rollback.

```json
{
  "name": "huawei-acl-workflow",
  "fail_fast": true,
  "blocks": [
    {
      "name": "acl-3001-publish",
      "kind": "config",
      "fail_fast": true,
      "rollback_policy": "per_step",
      "steps": [
        {
          "mode": "Config",
          "command": "acl number 3001",
          "timeout_secs": 10,
          "rollback_command": "undo acl 3001",
          "rollback_on_failure": true
        },
        {
          "mode": "Config",
          "command": "rule 5 permit ip source 10.10.10.0 0.0.0.255 destination 172.16.10.0 0.0.0.255",
          "timeout_secs": 10,
          "rollback_command": "undo rule 5",
          "rollback_on_failure": false
        },
        {
          "mode": "Config",
          "command": "quit",
          "timeout_secs": 10,
          "rollback_command": null,
          "rollback_on_failure": false
        }
      ]
    }
  ]
}
```

Run:

```bash
rauto tx-workflow ./workflow.json --dry-run
rauto tx-workflow ./workflow.json --host <host> --username <username> --password <password> --device-profile huawei
```

## 6) Multi-block compensation workflow (advanced)

Use this for multi-resource publishing where later block failure should trigger compensation rollback of previously committed blocks.

```json
{
  "name": "firewall-publish-workflow",
  "fail_fast": true,
  "blocks": [
    {
      "name": "address-book-block",
      "kind": "config",
      "fail_fast": true,
      "rollback_policy": {
        "whole_resource": {
          "mode": "Config",
          "undo_command": "delete security address-book global address WEB01 10.10.10.10/32",
          "timeout_secs": 10,
          "trigger_step_index": 0
        }
      },
      "steps": [
        {
          "mode": "Config",
          "command": "set security address-book global address WEB01 10.10.10.10/32",
          "timeout_secs": 10,
          "rollback_command": null,
          "rollback_on_failure": false
        }
      ]
    },
    {
      "name": "service-block",
      "kind": "config",
      "fail_fast": true,
      "rollback_policy": {
        "whole_resource": {
          "mode": "Config",
          "undo_command": "delete applications application APP-WEB-8443",
          "timeout_secs": 10,
          "trigger_step_index": 0
        }
      },
      "steps": [
        {
          "mode": "Config",
          "command": "set applications application APP-WEB-8443 protocol tcp destination-port 8443",
          "timeout_secs": 10,
          "rollback_command": null,
          "rollback_on_failure": false
        }
      ]
    },
    {
      "name": "policy-block",
      "kind": "config",
      "fail_fast": true,
      "rollback_policy": "per_step",
      "steps": [
        {
          "mode": "Config",
          "command": "set security policies from-zone trust to-zone untrust policy allow-web match source-address WEB01",
          "timeout_secs": 10,
          "rollback_command": "delete security policies from-zone trust to-zone untrust policy allow-web match source-address WEB01",
          "rollback_on_failure": true
        },
        {
          "mode": "Config",
          "command": "set security policies from-zone trust to-zone untrust policy allow-web match application APP-WEB-8443",
          "timeout_secs": 10,
          "rollback_command": "delete security policies from-zone trust to-zone untrust policy allow-web match application APP-WEB-8443",
          "rollback_on_failure": true
        },
        {
          "mode": "Config",
          "command": "set security policies from-zone trust to-zone untrust policy allow-web then permit",
          "timeout_secs": 10,
          "rollback_command": "delete security policies from-zone trust to-zone untrust policy allow-web then permit",
          "rollback_on_failure": true
        }
      ]
    }
  ]
}
```

Run:

```bash
rauto tx-workflow ./workflow.json --dry-run
rauto tx-workflow ./workflow.json --connection <connection> --record-file ~/.rauto/records/fw_publish.jsonl --record-level key-events-only
```

Validation focus after run:

1. Check workflow output for `rollback_attempted`, `rollback_succeeded`, and `rollback_errors`.
2. If failed in `policy-block`, verify compensation rollback was triggered for committed `address-book-block` and `service-block`.
3. Use `rauto replay ~/.rauto/records/fw_publish.jsonl --list` for audit.
