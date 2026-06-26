# Multi-Device Orchestration JSON Templates (EN)

Use this file when the agent needs to provide a runnable `orchestration.json` for `rauto orchestrate`.

Before proposing live execution, pair this file with `references/orchestration-risk-check.md`.

## Table of Contents

1. Minimal staged orchestration
2. Inventory + group orchestration
3. Advanced staged rollout
4. Run commands
5. Repo sample files
6. Pre-flight review

## 1) Minimal staged orchestration

Use this when the user wants the smallest practical multi-device plan without inventory groups.

```json
{
  "name": "campus-vlan-rollout",
  "fail_fast": true,
  "stages": [
    {
      "name": "core",
      "strategy": "serial",
      "targets": ["core-01", "core-02"],
      "action": {
        "kind": "tx_workflow",
        "workflow_file": "./core-vlan-workflow.json"
      }
    },
    {
      "name": "access",
      "strategy": "parallel",
      "max_parallel": 10,
      "targets": [
        {
          "connection": "sw-01",
          "vars": {
            "hostname": "sw-01",
            "vlans": [
              { "id": 120, "name": "STAFF" }
            ]
          }
        },
        {
          "connection": "sw-02",
          "vars": {
            "hostname": "sw-02",
            "vlans": [
              { "id": 120, "name": "STAFF" }
            ]
          }
        }
      ],
      "action": {
        "kind": "tx_block",
        "name": "access-vlan",
        "template": "configure_vlan.j2",
        "mode": "Config"
      }
    }
  ]
}
```

## 2) Inventory + group orchestration

Use this when the user wants reusable target groups and defaults inheritance.

`orchestration.json`:

```json
{
  "name": "campus-vlan-rollout",
  "fail_fast": true,
  "inventory_file": "./campus-inventory.json",
  "stages": [
    {
      "name": "core",
      "strategy": "serial",
      "target_groups": ["core"],
      "action": {
        "kind": "tx_workflow",
        "workflow_file": "./core-vlan-workflow.json"
      }
    },
    {
      "name": "access",
      "strategy": "parallel",
      "max_parallel": 20,
      "target_groups": ["access"],
      "action": {
        "kind": "tx_block",
        "template": "configure_vlan.j2",
        "mode": "Config"
      }
    }
  ]
}
```

`inventory.json`:

```json
{
  "defaults": {
    "username": "ops",
    "port": 22,
    "device_profile": "cisco",
    "vars": {
      "tenant": "campus-a"
    }
  },
  "groups": {
    "core": [
      { "connection": "core-01", "vars": { "hostname": "core-01" } },
      { "connection": "core-02", "vars": { "hostname": "core-02" } }
    ],
    "access": {
      "defaults": {
        "vars": {
          "vlans": [
            { "id": 120, "name": "STAFF" }
          ]
        }
      },
      "targets": [
        { "connection": "sw-01", "vars": { "hostname": "sw-01" } },
        { "connection": "sw-02", "vars": { "hostname": "sw-02" } }
      ]
    }
  }
}
```

## 3) Advanced staged rollout

Use this when the user needs:
- serial + parallel stages
- stage-level `fail_fast` override
- `target_groups` plus inline `targets`
- `tx_workflow` and `tx_block` mixed in one plan

Prefer the repo samples instead of retyping:
- `templates/examples/fabric-advanced-orchestration.json`
- `templates/examples/fabric-advanced-inventory.json`
- `templates/examples/fabric-change-workflow.json`

## 4) Run commands

```bash
# View normalized plan
rauto orchestrate ./orchestration.json --view

# Dry-run
rauto orchestrate ./orchestration.json --dry-run

# Dry-run raw JSON
rauto orchestrate ./orchestration.json --dry-run --json

# Execute
rauto orchestrate ./orchestration.json --record-level full

# Execute by reusing a saved connection as fallback defaults when needed
rauto orchestrate ./orchestration.json --connection <connection>
```

## 5) Repo sample files

Use these directly when the user is working in this repo:

- `templates/examples/core-vlan-workflow.json`
- `templates/examples/campus-vlan-orchestration.json`
- `templates/examples/campus-inventory.json`
- `templates/examples/fabric-change-workflow.json`
- `templates/examples/fabric-advanced-orchestration.json`
- `templates/examples/fabric-advanced-inventory.json`

## 6) Pre-flight review

Before live execution:
- run `rauto orchestrate ./orchestration.json --dry-run`
- review `references/orchestration-risk-check.md`
