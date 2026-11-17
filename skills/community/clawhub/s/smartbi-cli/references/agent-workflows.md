# Agent workflow export and modification

Resolve `<PYTHON>` to an available Python 3 interpreter and `<SKILL_DIR>` to this Skill's absolute directory. Wrapped POSIX examples show argument grouping; adapt continuation characters to the current shell.

## Capability boundary

The standard `aichat` CLI currently exposes Agent discovery and execution but not the full workflow graph lifecycle. Confirm this with `smartbi list --profile <PROFILE> --domain aichat --agent` in the target installation before using internal APIs.

The following internal SmartBI internal contracts are source-confirmed but not stable public SDK commitments:

| Action | Method and path |
| --- | --- |
| Get Agent | `GET /smartbi/smartbix/api/dataagent/graph/{id}` |
| Search Agent graphs | `POST /smartbi/smartbix/api/dataagent/graphs` |
| Create Agent | `POST /smartbi/smartbix/api/dataagent/graph/create/{parentId}` |
| Update Agent | `POST /smartbi/smartbix/api/dataagent/graph/update` |
| Download definition | `GET /smartbi/smartbix/api/dataagent/define/download/{id}` |
| Upload definition | `POST /smartbi/smartbix/api/dataagent/define/upload` |

The raw workflow ID is used here. Remove only the leading `customagent_` that `queryRpc` adds; do not otherwise transform the ID.

## Authentication

Internal calls require an authenticated SmartBI session with `AI_AGENT` permissions. Put the complete header value in an environment variable supplied through a secure channel, for example:

```bash
export SMARTBI_SESSION_COOKIE='<secret value>'
```

Pass only the environment variable name to the helper:

```bash
--header-env Cookie=SMARTBI_SESSION_COOKIE
```

Never place the value in command history, request JSON, source control, or logs.

## Export

```bash
<PYTHON> <SKILL_DIR>/scripts/smartbi_internal.py \
  --base-url <BASE_URL> \
  --header-env Cookie=SMARTBI_SESSION_COOKIE \
  agent-get \
  --agent-id <RAW_AGENT_ID> \
  --output <EXPORTED_AGENT_JSON>
```

The command reports the graph SHA-256 and node/link counts without printing the full definition.

## Modify safely

Start from the exported object. Preserve every unknown graph field. Change only the required nodes, ports, links, prompts, or settings. Before applying:

- parse `define` as JSON;
- verify every link source/target node exists;
- verify referenced input/output port IDs exist on the corresponding nodes;
- keep node IDs stable unless a new node is genuinely required;
- give each new node and port a collision-free ID;
- ensure finish nodes do not wait for mutually exclusive branches;
- do not put secrets into prompts, node inputs, or settings.

First run a dry-run:

```bash
<PYTHON> <SKILL_DIR>/scripts/smartbi_internal.py \
  --base-url <BASE_URL> \
  --header-env Cookie=SMARTBI_SESSION_COOKIE \
  agent-update \
  --agent-id <RAW_AGENT_ID> \
  --file <CANDIDATE_OR_PATCH_JSON> \
  --backup-dir <BACKUP_DIR>
```

Review `changed_fields`, node/link counts, and `current_sha256`. Apply exactly once using that hash:

```bash
<PYTHON> <SKILL_DIR>/scripts/smartbi_internal.py \
  --base-url <BASE_URL> \
  --header-env Cookie=SMARTBI_SESSION_COOKIE \
  agent-update \
  --agent-id <RAW_AGENT_ID> \
  --file <CANDIDATE_OR_PATCH_JSON> \
  --backup-dir <BACKUP_DIR> \
  --expect-sha256 <CURRENT_SHA256> \
  --apply
```

The helper rejects a stale hash, writes a timestamped backup before mutation, updates once, and reads back all editable fields. It has no delete or rollback command; rollback is an explicit update using the reviewed backup.

## Create

Creation requires a confirmed catalog parent ID and `AI_AGENT / EDIT` permission:

```bash
<PYTHON> <SKILL_DIR>/scripts/smartbi_internal.py \
  --base-url <BASE_URL> \
  --header-env Cookie=SMARTBI_SESSION_COOKIE \
  agent-create \
  --parent-id <CATALOG_PARENT_ID> \
  --file <AGENT_JSON>
```

This is a dry-run. Add `--apply` only after reviewing the name, alias, node/link counts, parent, tool bindings, and permissions. Creation does not imply publication or visibility in `getAgentItems`; deployment relations differ by SmartBI version and must be discovered and verified separately.

## Verification

After update or creation:

1. export/read back the Agent;
2. confirm Provider and Tool IDs still exist;
3. call `aichat.getAgentItems` and `getAgentCard` when applicable;
4. create a fresh conversation rather than reusing cached execution state;
5. test both success and failure branches;
6. inspect rounds and chat logs;
7. retain the backup and evidence manifest until acceptance.
