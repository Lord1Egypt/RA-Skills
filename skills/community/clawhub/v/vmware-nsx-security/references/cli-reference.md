# VMware NSX Security CLI Reference

## Global Options

| Option | Short | Description |
|--------|-------|-------------|
| `--target` | `-t` | NSX Manager target name from config (uses `default_target` if omitted) |
| `--config` | `-c` | Path to config file (overrides `VMWARE_NSX_SECURITY_CONFIG` env var) |
| `--dry-run` | | Preview API call without executing (write commands only) |
| `--help` | | Show help for any command |

---

## `policy` — DFW Policy Management

### `policy list`
List all DFW security policies.

```bash
vmware-nsx-security policy list [--target <name>]
```

Output columns: ID, Display Name, Category, Seq#, Stateful, Rules

### `policy get`
Get full details of a DFW policy.

```bash
vmware-nsx-security policy get <policy-id> [--target <name>]
```

### `policy create`
Create a new DFW security policy.

```bash
vmware-nsx-security policy create <policy-id> \
  --name "Display Name" \
  [--category Ethernet|Emergency|Infrastructure|Environment|Application] \
  [--seq <number>] \
  [--description "text"] \
  [--dry-run] \
  [--target <name>]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--name` | required | Human-readable policy name |
| `--category` | Application | Policy evaluation category (validated; Ethernet evaluated first, Application last) |
| `--seq` | 10 | Sequence number (lower = higher priority) |
| `--description` | "" | Optional description |

### `policy delete`
Delete a DFW policy (requires no active rules).

```bash
vmware-nsx-security policy delete <policy-id> [--dry-run] [--target <name>]
```

Prompts for double confirmation. Fails if the policy contains rules.

---

## `rule` — DFW Rule Management

### `rule list`
List all rules in a policy.

```bash
vmware-nsx-security rule list <policy-id> [--target <name>]
```

Output columns: ID, Display Name, Action, Direction, Disabled, Logged

### `rule stats`
Get packet/byte hit-count statistics for a rule.

```bash
vmware-nsx-security rule stats <policy-id> <rule-id> [--target <name>]
```

Output fields: `packet_count`, `byte_count`, `session_count`, `hit_count`
(summed across enforcement points), `popularity_index` (max).

### `rule delete`
Delete a DFW rule.

```bash
vmware-nsx-security rule delete <policy-id> <rule-id> [--dry-run] [--target <name>]
```

Prompts for double confirmation.

---

## `group` — Security Group Management

### `group list`
List all security groups.

```bash
vmware-nsx-security group list [--target <name>]
```

### `group get`
Get group details including membership criteria and effective VM members.

```bash
vmware-nsx-security group get <group-id> [--target <name>]
```

### `group delete`
Delete a security group (checks for DFW references first).

```bash
vmware-nsx-security group delete <group-id> [--dry-run] [--target <name>]
```

Refuses deletion if the group is referenced by any DFW rule (source,
destination, or applied-to scope) or by a policy-level scope. If the
reference scan itself fails, deletion is aborted rather than proceeding
blind.

> Group **creation** (with tag/IP/segment criteria) is exposed via the
> `create_group` MCP tool. The tag criterion is a Policy Condition with a
> pipe-delimited value `"scope|tag"`; multiple criteria are ORed.

---

## `tag` — VM NSX Tag Management

### `tag list`
List NSX tags on a VM by display name.

```bash
vmware-nsx-security tag list <vm-display-name> [--target <name>]
```

### `tag apply`
Apply an NSX tag to a VM (by external ID).

```bash
vmware-nsx-security tag apply <vm-external-id> \
  --scope <scope> \
  --value <value> \
  [--dry-run] \
  [--target <name>]
```

| Option | Description |
|--------|-------------|
| `--scope` | Tag scope (e.g. `tier`, `env`, `owner`) |
| `--value` | Tag value (e.g. `web`, `production`) |

Additive — existing tags on the VM are preserved. Uses
`POST /api/v1/fabric/virtual-machines?action=add_tags` with body
`{"external_id", "tags"}`.

### `tag remove`
Remove an NSX tag from a VM (by external ID).

```bash
vmware-nsx-security tag remove <vm-external-id> \
  --scope <scope> \
  --value <value> \
  [--dry-run] \
  [--target <name>]
```

| Option | Description |
|--------|-------------|
| `--scope` | Tag scope of the tag to remove |
| `--value` | Tag value of the tag to remove |

Removes only the exact scope/value pair; other tags are preserved. May
change dynamic security group membership immediately. Uses
`POST /api/v1/fabric/virtual-machines?action=remove_tags` with body
`{"external_id", "tags"}`.

---

## `traceflow` — Packet Tracing

### `traceflow run`
Initiate a Traceflow and wait for results.

```bash
vmware-nsx-security traceflow run <src-lport-id> \
  --src-ip <ip> \
  --dst-ip <ip> \
  [--proto TCP|UDP|ICMP] \
  [--dst-port <port>] \
  [--target <name>]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--src-ip` | required | Source IP for probe packet |
| `--dst-ip` | required | Destination IP |
| `--proto` | TCP | Protocol: TCP, UDP, or ICMP |
| `--dst-port` | 80 | Destination port (TCP/UDP) |

Output: `operation_state` (`IN_PROGRESS` / `FINISHED` / `FAILED`),
`observations` discriminated by `resource_type` (e.g.
`TraceflowObservationForwarded`, `TraceflowObservationDroppedLogical` —
Dropped* entries carry `reason` and `acl_rule_id`), and a `dfw_hits`
summary of observations that matched a DFW rule.

---

## `idps` — IDPS Operations

### `idps profiles`
List all IDPS profiles.

```bash
vmware-nsx-security idps profiles [--target <name>]
```

### `idps status`
Get IDPS signature status and global IDS settings.

```bash
vmware-nsx-security idps status [--target <name>]
```

Output: `signature_status` (scalar fields of the signature bundle status
resource — field names vary by NSX release) and `settings`
(`auto_update`, `ids_events_to_syslog`).

---

## `doctor` — Environment Diagnostics

Run pre-flight checks: config file, .env permissions, config parse, passwords, network reachability, NSX authentication, NSX version, MCP server import.

```bash
vmware-nsx-security doctor [--skip-auth] [--config <path>]
```

| Option | Description |
|--------|-------------|
| `--skip-auth` | Skip authentication tests (network check only) |
| `--config` | Override config file path |

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `VMWARE_NSX_SECURITY_CONFIG` | Path to config YAML file |
| `VMWARE_NSX_SECURITY_<TARGET>_PASSWORD` | Password for target (hyphens → underscores, uppercase) |

**Password examples**:
- Target `nsx-prod` → `VMWARE_NSX_SECURITY_NSX_PROD_PASSWORD`
- Target `nsx-lab` → `VMWARE_NSX_SECURITY_NSX_LAB_PASSWORD`
