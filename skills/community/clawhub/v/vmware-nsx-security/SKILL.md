---
name: vmware-nsx-security
description: >
  Use this skill whenever the user needs to manage VMware NSX security — distributed firewall (DFW) policies, security groups, microsegmentation, and IDS/IPS.
  Directly handles: create/manage DFW policies and rules, security groups, VM tags, network traceflow diagnostics, IDPS profiles and status.
  Always use this skill for "create firewall rule", "set up microsegmentation", "add VM to security group", "run traceflow", "check IDS status", or any NSX security/DFW task.
  Do NOT use for NSX networking operations like segments, gateways, NAT, or routing (use vmware-nsx), or VM lifecycle (use vmware-aiops).
  For load balancing/AVI/AKO use vmware-avi.
installer:
  kind: uv
  package: vmware-nsx-security
allowed-tools:
  - Bash
metadata: {"openclaw":{"requires":{"env":["VMWARE_NSX_SECURITY_CONFIG"],"bins":["vmware-nsx-security"],"config":["~/.vmware-nsx-security/config.yaml","~/.vmware-nsx-security/.env"]},"optional":{"env":["VMWARE_<TARGET>_PASSWORD"],"bins":["vmware-policy"]},"primaryEnv":"VMWARE_NSX_SECURITY_CONFIG","homepage":"https://github.com/zw008/VMware-NSX-Security","emoji":"🔒","os":["macos","linux"]}}
compatibility: >
  vmware-policy auto-installed as Python dependency (provides @vmware_tool decorator and audit logging). All write operations audited to ~/.vmware/audit.db.
  Credentials: Each NSX Manager target requires a per-target password env var in ~/.vmware-nsx-security/.env following the pattern VMWARE_<TARGET_NAME_UPPER>_PASSWORD. Passwords are never logged or echoed.
  Destructive operations: DFW policy delete checks for active rules, security group delete checks for references. IDS/IPS config changes require double confirmation. Traceflow is read-only.
  No webhooks, no outbound network calls, no guest operations. Local only: stdio MCP + NSX Policy API (HTTPS 443).
  Transitive dependencies: Only vmware-policy (audit/policy). No post-install scripts or background services.
---

# VMware NSX Security

> **Disclaimer**: This is a community-maintained open-source project and is **not affiliated with, endorsed by, or sponsored by VMware, Inc. or Broadcom Inc.** "VMware" and "NSX" are trademarks of Broadcom. Source code is publicly auditable at [github.com/zw008/VMware-NSX-Security](https://github.com/zw008/VMware-NSX-Security) under the MIT license.

VMware NSX DFW microsegmentation and security — 21 MCP tools for distributed firewall, security groups, VM tags, Traceflow, and IDPS.

> Domain-focused security skill for NSX-T / NSX 4.x Policy API.
> **Companion skills**: [vmware-nsx](https://github.com/zw008/VMware-NSX) (networking), [vmware-aiops](https://github.com/zw008/VMware-AIops) (VM lifecycle), [vmware-monitor](https://github.com/zw008/VMware-Monitor) (read-only monitoring), [vmware-avi](https://github.com/zw008/VMware-AVI) (AVI/ALB/AKO), [vmware-harden](https://github.com/zw008/VMware-Harden) (compliance baselines).
> | [vmware-pilot](../vmware-pilot/SKILL.md) (workflow orchestration) | [vmware-policy](../vmware-policy/SKILL.md) (audit/policy)

## What This Skill Does

| Category | Tools | Count |
|----------|-------|:-----:|
| **DFW Policy** | list, get, create, update, delete, list rules | 6 |
| **DFW Rules** | create, update, delete, get stats | 4 |
| **Security Groups** | list, get, create, delete | 4 |
| **VM Tags** | list VM tags, apply tag, remove tag | 3 |
| **Traceflow** | run trace, get result | 2 |
| **IDPS** | list profiles, get status | 2 |

**Total**: 21 tools (10 read-only + 11 write)

## Quick Install

```bash
uv tool install vmware-nsx-security
vmware-nsx-security init      # guided setup: writes config + .env (chmod 600, password grep-safe), then verifies
vmware-nsx-security doctor
```

## When to Use This Skill

- List, create, or modify DFW security policies and rules
- Create security groups based on VM tags, IP ranges, or segment membership
- Apply or list NSX tags on virtual machines
- Run Traceflow to trace a packet path and diagnose drop reasons
- Check IDPS profile configuration, signature status, and global IDS settings
- Implement zero-trust microsegmentation between application tiers

**Use companion skills for**:
- NSX segments, gateways, NAT, routing, IPAM → `vmware-nsx`
- VM lifecycle, deployment, guest ops → `vmware-aiops`
- vSphere inventory, health, alarms, events → `vmware-monitor`
- Storage: iSCSI, vSAN, datastores → `vmware-storage`
- Tanzu Kubernetes → `vmware-vks`
- Load balancing, AVI/ALB, AKO, Ingress → `vmware-avi`

## Related Skills — Skill Routing

| User Intent | Recommended Skill |
|-------------|-------------------|
| NSX security: DFW rules, security groups, IDS/IPS | **vmware-nsx-security** ← this skill |
| NSX networking: segments, gateways, NAT, routing | **vmware-nsx** |
| Read-only vSphere monitoring, alarms, events | **vmware-monitor** |
| VM lifecycle, deployment, guest ops | **vmware-aiops** |
| Storage: iSCSI, vSAN, datastores | **vmware-storage** |
| Tanzu Kubernetes | **vmware-vks** |
| Multi-step workflows with approval | **vmware-pilot** |
| Compliance baselines (CIS / 等保 / PCI-DSS), drift detection, LLM remediation advisor | **vmware-harden** (`uv tool install vmware-harden`) |
| Load balancer, AVI, ALB, AKO, Ingress | **vmware-avi** (`uv tool install vmware-avi`) |
| Audit log query | **vmware-policy** (`vmware-audit` CLI) |

## Common Workflows

### Implement App-Tier Microsegmentation

**Pre-flight (judgment — DFW changes can lock everyone out)**:
- **Default-allow first**: the very first rule in any new policy must be ALLOW for management traffic (DNS, NTP, vCenter, SSH from jumphost). Without it, the moment you add a default-deny you blackhole your own access.
- Tag inventory: confirm the VMs you intend to protect actually carry the tag (`tag list <vm>`). A group based on a non-existent tag matches zero VMs — the policy will appear "applied" but enforce nothing.
- Category choice: `Application` for app-tier microseg (rules evaluated late, after Infrastructure rules pass through). Using `Emergency` for routine rules will starve real incident-response capacity.
- Stateless? Default to stateful — NSX DFW is stateful and almost no rule should be stateless. Stateless = both directions must be explicitly allowed.
- Always start with **logging enabled** on new rules; disable later once verified. Silent drops are the worst kind of bug.

**Steps**:
1. Tag the VMs first (see workflow below) — empty groups = no enforcement
2. Create groups via the `create_group` MCP tool with `tag_scope`/`tag_value` (the tag condition is matched as `"scope|tag"`, e.g. `tier|web`; note multiple criteria types — tag/IP/segment — are ORed, not ANDed)
3. `policy create app-microseg --category Application`
4. Add rules in order: ALLOW management → ALLOW intra-tier → ALLOW web→app on app-port → DROP any-any with logging
5. Verify with traceflow (see below) **before** enabling default-deny

### Apply NSX Tags to VMs

**Judgment**: tags drive group membership which drives DFW enforcement. A misspelled tag silently excludes a VM from protection. Always re-list after applying.

1. `tag list my-web-vm-01` → record the VM external ID, also see what tags already exist (avoid duplicates / typo collisions)
2. `tag apply <vm-external-id> --scope tier --value web`
3. **Verify**: `tag list my-web-vm-01` again → confirm the new tag is present AND no unexpected ones

### Trace a Packet with Traceflow

**Judgment**: traceflow is your verification mechanism for any DFW change. Run it **before** enabling deny rules and **after** every rule modification. Don't trust "looks right in the UI."

1. Get source VM's logical port ID via `vmware-nsx troubleshoot vm-segment`
2. `traceflow run <lport-id> --src-ip <src> --dst-ip <dst> --proto TCP --dst-port <port>`
3. Inspect the DFW hit chain: which rule matched, ALLOW or DROP, and at which transport node
4. **Common failure**: rule matches at category Application but is shadowed by an earlier DROP at category Environment — read the trace top-to-bottom, not just the final verdict

### Check DFW Policy Hit Counts

```bash
vmware-nsx-security policy list
vmware-nsx-security rule list <policy-id>
vmware-nsx-security rule stats <policy-id> <rule-id>
```

### Multi-Target Operations

All commands accept `--target <name>` to operate against a specific NSX Manager:

```bash
# Default target
vmware-nsx-security policy list

# Specific target
vmware-nsx-security policy list --target nsx-prod
vmware-nsx-security group list --target nsx-lab
```

## Usage Mode

| Scenario | Recommended | Why |
|----------|:-----------:|-----|
| Local/small models (Ollama, Qwen) | **CLI** | ~2K tokens vs ~8K for MCP |
| Cloud models (Claude, GPT-4o) | Either | MCP gives structured JSON I/O |
| Automated pipelines | **MCP** | Type-safe parameters, structured output |

## MCP Tools (21 — 10 read, 11 write)

All MCP tools accept an optional `target` parameter.

| Category | Tool | Type | Description |
|----------|------|:----:|-------------|
| DFW Policy | `list_dfw_policies` | Read | List all DFW security policies with category, sequence, and rule count |
| | `get_dfw_policy` | Read | Get policy details: category, stateful, locked, scope, tags |
| | `create_dfw_policy` | Write | Create a new DFW policy with category and sequence number |
| | `update_dfw_policy` | Write | Partial update: display_name, description, sequence_number, stateful |
| | `delete_dfw_policy` | Write | Delete policy — refuses if active rules exist |
| | `list_dfw_rules` | Read | List rules in a policy: action, sources, destinations, services |
| DFW Rules | `create_dfw_rule` | Write | Create rule with sources/destinations/services/action/scope |
| | `update_dfw_rule` | Write | Partial update rule fields |
| | `delete_dfw_rule` | Write | Delete a rule from a policy |
| | `get_dfw_rule_stats` | Read | Get packet/byte/session/hit counts and popularity_index for a rule |
| Security Groups | `list_groups` | Read | List all security groups with expression count |
| | `get_group` | Read | Get group details: expression criteria + up to 50 effective VM members |
| | `create_group` | Write | Create group with tag/IP/segment membership criteria (tag matched as "scope\|tag"; multiple criteria ORed) |
| | `delete_group` | Write | Delete group — refuses if referenced by DFW rules/scopes, or if the reference scan fails |
| VM Tags | `list_vm_tags` | Read | List NSX tags on a VM by display name |
| | `apply_vm_tag` | Write | Apply a scope/value tag to a VM (additive, preserves existing tags) |
| | `remove_vm_tag` | Write | Remove a scope/value tag from a VM (other tags preserved; may change dynamic group membership) |
| Traceflow | `run_traceflow` | Write | Inject probe packet; returns operation_state + hop-by-hop observations (by resource_type) + dfw_hits |
| | `get_traceflow_result` | Read | Check operation_state/observations of an existing traceflow |
| IDPS | `list_idps_profiles` | Read | List IDPS profiles with severity and filter criteria |
| | `get_idps_status` | Read | Get IDPS signature status + global IDS settings (auto_update, syslog export) |

## CLI Quick Reference

```bash
# DFW Policy
vmware-nsx-security policy list [--target <name>]
vmware-nsx-security policy get <policy-id>
vmware-nsx-security policy create <id> --name "Display Name" --category Application [--dry-run]
vmware-nsx-security policy delete <id> [--dry-run]

# DFW Rules
vmware-nsx-security rule list <policy-id>
vmware-nsx-security rule stats <policy-id> <rule-id>
vmware-nsx-security rule delete <policy-id> <rule-id> [--dry-run]

# Security Groups
vmware-nsx-security group list
vmware-nsx-security group get <group-id>
vmware-nsx-security group delete <group-id> [--dry-run]

# Tags
vmware-nsx-security tag list <vm-display-name>
vmware-nsx-security tag apply <vm-external-id> --scope env --value production [--dry-run]
vmware-nsx-security tag remove <vm-external-id> --scope env --value production [--dry-run]

# Traceflow
vmware-nsx-security traceflow run <lport-id> --src-ip &lt;src-ip&gt; --dst-ip &lt;dst-ip&gt;

# IDPS
vmware-nsx-security idps profiles
vmware-nsx-security idps status

# Diagnostics
vmware-nsx-security doctor [--skip-auth]
```

## Troubleshooting

### "Cannot delete policy — active rules exist"

`delete_dfw_policy` checks for active rules before deleting. Use `vmware-nsx-security rule list <policy-id>` to see which rules need to be removed first. Then delete each rule individually before retrying the policy deletion.

### "Cannot delete group — referenced by DFW rules"

`delete_group` scans all policies for references to the group in rule source_groups, destination_groups, and applied-to scope, plus policy-level scope. Remove the group from those references first (via `update_dfw_rule` replacing the group path with 'ANY' or another group), then retry. If the error says the reference scan itself failed, deletion was aborted as a precaution — verify NSX connectivity with `vmware-nsx-security doctor` and retry.

### "No virtual machine found with display_name"

`list_vm_tags` looks up VMs by display name via the NSX fabric API. Common causes:
1. Display name mismatch — the name in NSX Manager may differ from vCenter. Check `vmware-monitor vm list` for the exact NSX fabric display name.
2. VM not registered — newly deployed VMs may take a minute to appear in the NSX fabric.
3. Multiple VMs with the same name — use `apply_vm_tag` with the specific external_id.

### Traceflow returns empty observations

1. If `operation_state` is `IN_PROGRESS`, the trace has not finished — poll again with `get_traceflow_result <traceflow-id>`.
2. Verify the `src_lport_id` is the correct logical port attachment UUID — not the segment port path. Get it from `vmware-nsx troubleshoot vm-segment <vm>`.
3. The source VM must be powered on and connected to an NSX overlay segment.
4. If the VM is on a VLAN-backed segment, Traceflow is not supported.
5. NSX Manager requires the transport node hosting the source VM to be reachable. Check `vmware-nsx health transport-nodes`.

### DFW rule stats show zero hits

A newly created rule will have zero hit counts until traffic matches it. If expected traffic still shows zero:
1. Confirm the rule is not disabled (`disabled: false` in `list_dfw_rules` output).
2. Check that source/destination group membership is correct using `get_group`.
3. Verify rule sequence number — a lower-sequence rule with ALLOW/DROP may be matching first.

### "Password not found" error

Password variable convention: `VMWARE_NSX_SECURITY_<TARGET_UPPER>_PASSWORD`
where hyphens are replaced by underscores. For target `nsx-prod`:
`VMWARE_NSX_SECURITY_NSX_PROD_PASSWORD`. Check `~/.vmware-nsx-security/.env`.

### `invalid peer certificate: UnknownIssuer` (uvx)

Corporate TLS proxy not trusted by uv's bundled cert store. Use the v1.5.15+
single-command form `vmware-nsx-security mcp` (no PyPI re-resolve), or
`export UV_NATIVE_TLS=true` to make uv use the system cert store.

## Safety

- **Audit logging**: All write operations logged to `~/.vmware/audit.db` (SQLite WAL, via vmware-policy) with timestamp, user, target, operation, parameters, and result
- **Dependency checks**: `delete_dfw_policy` checks for active rules; `delete_group` checks for DFW rule references — prevents accidental cascade failures
- **Input validation**: All IDs validated against safe character set (alphanumerics, hyphens, underscores, dots); all text fields sanitized to strip control characters
- **Dry-run mode**: CLI write commands support `--dry-run` to preview API calls without executing
- **Double confirmation**: CLI destructive operations (delete) require two separate confirmation prompts
- **Credential safety**: Passwords loaded only from environment variables (`.env` file), never from `config.yaml`
- **No networking changes**: Cannot modify segments, gateways, NAT, or routing — that scope belongs to `vmware-nsx`
- **Prompt injection defense**: All API-sourced strings passed through `_sanitize()` before inclusion in tool output

## Setup

```bash
uv tool install vmware-nsx-security
mkdir -p ~/.vmware-nsx-security
cp config.example.yaml ~/.vmware-nsx-security/config.yaml
# Edit config.yaml with your NSX Manager targets

# Add to ~/.vmware-nsx-security/.env (create if missing, chmod 600):
# VMWARE_NSX_SECURITY_NSX_PROD_PASSWORD=<your-password>
chmod 600 ~/.vmware-nsx-security/.env

vmware-nsx-security doctor
```

> All tools are automatically audited via vmware-policy. Audit logs: `vmware-audit log --last 20`

> Full setup guide: see `references/setup-guide.md`

## Architecture

```
User (natural language)
  |
AI Agent (Claude Code / Goose / Cursor)
  | reads SKILL.md
vmware-nsx-security CLI or MCP server (stdio transport)
  | NSX Policy API (REST/JSON over HTTPS)
NSX Manager
  |
DFW Policies / Rules / Security Groups / Tags / IDPS
```

The MCP server uses stdio transport (local only, no network listener). All connections to NSX Manager use HTTPS on port 443.

## Audit & Safety

All operations are automatically audited via vmware-policy (`@vmware_tool` decorator):
- Every tool call logged to `~/.vmware/audit.db` (SQLite, framework-agnostic)
- Policy rules enforced via `~/.vmware/rules.yaml` (deny rules, maintenance windows, risk levels)
- Risk classification: each tool tagged as low/medium/high/critical
- View recent operations: `vmware-audit log --last 20`
- View denied operations: `vmware-audit log --status denied`

vmware-policy is automatically installed as a dependency — no manual setup needed.

## License

MIT — [github.com/zw008/VMware-NSX-Security](https://github.com/zw008/VMware-NSX-Security)
