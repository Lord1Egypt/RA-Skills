# VMware NSX Security — Capabilities Reference

## Automation Level Reference

Each operation is classified by autonomy level per the Enterprise Harness Engineering framework:

| Level | Meaning | Agent autonomy | Examples in this skill |
|:-:|---|---|---|
| **L1** | Read-only, raw data | Always auto-run | `list_dfw_policies`, `get_dfw_rule`, `list_security_groups`, `list_services`, `traceflow_create`/`get`, IDS/IPS event queries |
| **L2** | Read + analysis / recommendation | Always auto-run | DFW rule conflict detection, shadowed-rule analysis, security group reference graph, traceflow path interpretation |
| **L3** | Single write — user must approve | Only after explicit confirmation; destructive ops require double-confirm + `--dry-run` | `create_dfw_policy`, `create_dfw_rule`, `delete_dfw_rule`, `create_security_group`, `delete_security_group`, IDS/IPS profile changes |
| **L4** | Multi-step plan / apply workflow | Plan generation auto; apply gated by user approval | *(roadmap — staged microsegmentation rollouts, emergency-block playbooks)* |
| **L5** | Auto-remediation from learned pattern | Pattern library only; requires `risk:low` + `reversible:true` + `repeatable:true` | *(roadmap — candidates: orphaned-SG cleanup, expired temp-block rule removal)* |

**Notes**:
- L1/L2 tools are always safe for agents to call without confirmation.
- L3 tools always pass through the `@vmware_tool` decorator: connection check → policy check → audit log → double-confirm. DFW policy delete additionally checks for active rules; SG delete checks for references.
- For Segment/Gateway/NAT (network plane) see [vmware-nsx](https://github.com/zw008/VMware-NSX).

## DFW Policy Categories

NSX DFW policies are evaluated in category order (lower category = higher priority):

| Category | Priority | Typical Use |
|----------|:--------:|-------------|
| Ethernet | 1 | Layer-2 rules (MAC-based) |
| Emergency | 2 | Incident response — block specific IPs or VMs immediately |
| Infrastructure | 3 | DNS, NTP, vCenter management traffic |
| Environment | 4 | Cross-environment rules (e.g. prod → lab) |
| Application | 5 | Application-tier microsegmentation (most common) |

`create_dfw_policy` validates the category and rejects anything outside this set.

## DFW Rule Actions

| Action | Behaviour |
|--------|-----------|
| ALLOW | Permit the traffic |
| DROP | Silently discard the packet (no RST/ICMP) |
| REJECT | Discard + send TCP RST or ICMP unreachable |
| JUMP_TO_APPLICATION | Skip to Application category rules — only valid in policies whose category is Environment |

## DFW Rule Statistics Fields

`get_dfw_rule_stats` aggregates the per-enforcement-point `RuleStatistics`
array: `packet_count`, `byte_count`, `session_count`, `hit_count` (summed)
and `popularity_index` (max). There is no `population_count` field in the
NSX API.

## Security Group Expression Types

Groups support three membership condition types:

| Type | Parameter | Example |
|------|-----------|---------|
| Tag Condition | `tag_scope` + `tag_value` | scope=tier, value=web |
| IP Address | `ip_addresses` | ['10.0.1.0/24', '10.0.2.5'] |
| Segment Path | `segment_paths` | ['/infra/segments/web-seg'] |

The tag Condition is sent as a Policy `Condition` with a pipe-delimited
`value` of `"scope|tag"` (e.g. `tier|web`; tag-only matching uses `"|tag"`).

Multiple criteria in one group are **ORed** (VM matches ANY condition):
NSX only permits AND between Conditions of the same member type, so
heterogeneous expression types (Condition vs IPAddressExpression vs
PathExpression) must join with OR.

## Traceflow Packet Types

The probe is a `FieldsPacketData` with nested `ip_header` (src_ip, dst_ip,
ttl, protocol number) and `transport_header`; `transport_type` is the L2
delivery mode (`UNICAST`), not the protocol.

| Protocol | transport_header | Notes |
|----------|------------------|-------|
| TCP | `tcp_header` (src_port, dst_port) | SYN flag set automatically |
| UDP | `udp_header` (src_port, dst_port) | |
| ICMP | `icmp_echo_request_header` | Echo request |

Completion is polled via `operation_state`: `IN_PROGRESS` → `FINISHED`
or `FAILED`.

## Traceflow Observation Types

Observations are discriminated by `resource_type`:

| resource_type | Meaning |
|---------------|---------|
| TraceflowObservationForwarded | Packet forwarded to next hop |
| TraceflowObservationDropped / TraceflowObservationDroppedLogical | Packet dropped at this component (carries `reason` + `acl_rule_id`) |
| TraceflowObservationDelivered | Packet delivered to destination |
| TraceflowObservationReceived | Packet received at a component |

Any observation carrying an `acl_rule_id` (forwarded or dropped by a DFW
rule) is also summarised in the `dfw_hits` list of the result.

## IDPS Status Output

`get_idps_status` reads two Policy API resources and returns:

- `signature_status` — scalar fields of the signature bundle status
  resource (e.g. version / update state; exact field names vary by NSX
  release, so scalars are passed through as-is)
- `settings` — `auto_update` (automatic signature updates) and
  `ids_events_to_syslog` from the global IdsSettings resource

IDPS profile `criteria` are polymorphic `filter_name`/`filter_value`
pairs (ATTACK_TYPE, ATTACK_TARGET, CVSS, PRODUCT_AFFECTED); conjunction
entries between them are always AND and are omitted from parsed output.

## IDPS Severity Levels

NSX IDPS signatures are classified by severity:

| Level | Score Range | Description |
|-------|-------------|-------------|
| CRITICAL | 9.0–10.0 | Immediate exploitation, remote code execution |
| HIGH | 7.0–8.9 | Significant risk, exploitable vulnerabilities |
| MEDIUM | 4.0–6.9 | Moderate risk, requires specific conditions |
| LOW | 0.1–3.9 | Informational, denial-of-service potential |

## NSX Tag Conventions

Best practice for NSX tag design:

| Scope | Example Values | Used For |
|-------|---------------|----------|
| `tier` | web, app, db | Application tier microsegmentation |
| `env` | prod, staging, dev | Environment separation |
| `owner` | team-a, finance | Policy ownership |
| `compliance` | pci, hipaa | Regulatory scope |

## API Endpoints Reference

| Operation | Method | Path |
|-----------|--------|------|
| List policies | GET | /policy/api/v1/infra/domains/default/security-policies |
| Get policy | GET | /policy/api/v1/infra/domains/default/security-policies/{id} |
| Create/replace policy | PUT | /policy/api/v1/infra/domains/default/security-policies/{id} |
| Update policy | PATCH | /policy/api/v1/infra/domains/default/security-policies/{id} |
| Delete policy | DELETE | /policy/api/v1/infra/domains/default/security-policies/{id} |
| List rules | GET | /policy/api/v1/infra/domains/default/security-policies/{id}/rules |
| Create/replace rule | PUT | .../rules/{rule-id} |
| Update rule | PATCH | .../rules/{rule-id} |
| Delete rule | DELETE | .../rules/{rule-id} |
| Rule statistics | GET | .../rules/{rule-id}/statistics |
| List groups | GET | /policy/api/v1/infra/domains/default/groups |
| Get group | GET | /policy/api/v1/infra/domains/default/groups/{id} |
| Create/replace group | PUT | /policy/api/v1/infra/domains/default/groups/{id} |
| Delete group | DELETE | /policy/api/v1/infra/domains/default/groups/{id} |
| Group members (VMs) | GET | /policy/api/v1/infra/domains/default/groups/{id}/members/virtual-machines |
| List VM tags | GET | /api/v1/fabric/virtual-machines?display_name={name} |
| Apply tag | POST | /api/v1/fabric/virtual-machines?action=add_tags |
| Remove tag | POST | /api/v1/fabric/virtual-machines?action=remove_tags |
| Create traceflow | POST | /api/v1/traceflows |
| Get traceflow | GET | /api/v1/traceflows/{id} |
| Traceflow observations | GET | /api/v1/traceflows/{id}/observations |
| Delete traceflow | DELETE | /api/v1/traceflows/{id} |
| IDPS profiles | GET | /policy/api/v1/infra/settings/firewall/security/intrusion-services/profiles |
| IDPS signature status | GET | /policy/api/v1/infra/settings/firewall/security/intrusion-services/signatures/status |
| IDPS settings | GET | /policy/api/v1/infra/settings/firewall/security/intrusion-services |

## NSX Version Compatibility

| NSX Version | Support Level | Notes |
|-------------|--------------|-------|
| NSX 9.1 | Full | DFW Policy API paths unchanged. VDS 7.0+ required (N-VDS removed in NSX 9 — no impact on DFW skill). |
| NSX 9.0 | Full | DFW Policy API paths unchanged. Bare-metal NSX agent removed (no impact on DFW skill — Policy API only). |
| NSX 4.2.x | Full | Latest, all DFW + Security Group + Traceflow + IDS/IPS features supported |
| NSX 4.1.x | Full | All features supported |
| NSX 4.0.x | Full | Policy API v1 fully available |
| NSX-T 3.2.x | Full | Policy API mature, all features work |
| NSX-T 3.1.x | Full | DFW Policy API stable |
| NSX-T 3.0.x | Compatible | Policy API available; some IDS/IPS endpoints introduced later |
| NSX-T 2.5.x | Limited | Policy API available but incomplete; some tools may fail |
| NSX-V (6.x) | Not supported | Completely different API (SOAP-based). Use legacy tools |

### VCF (VMware Cloud Foundation) Compatibility

| VCF Version | Bundled NSX | Support |
|-------------|-------------|---------|
| VCF 9.1 | NSX 9.1 | Full |
| VCF 9.0 | NSX 9.0 | Full |
| VCF 5.2 | NSX 4.2.x | Full |
| VCF 5.1 | NSX 4.1.x | Full |
| VCF 5.0 | NSX 4.0.x | Full |
| VCF 4.5 | NSX-T 3.2.x | Full |
| VCF 4.4 | NSX-T 3.2.x | Full |
| VCF 4.3 | NSX-T 3.1.x | Full |

**Note**: This skill uses the NSX-T Policy API only. NSX 9 changes that affect the network plane (N-VDS removal, bare-metal agent removal) do not affect DFW, Security Group, Traceflow, or IDS/IPS operations exposed by this skill.
