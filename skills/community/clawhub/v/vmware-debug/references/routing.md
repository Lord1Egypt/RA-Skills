# Symptom → Signal → Skill Routing

The catalogue debug uses to turn "something is wrong" into concrete next steps.
Keep this in sync with `_CATEGORY_SIGNATURES` in `vmware_debug/ops/timeline.py`
(a regression test asserts the two match).

| Category | Keyword signatures (sample) | Pull signals from | Fix via |
|---|---|---|---|
| **storage** | datastore, scsi, latency, vsan, apd, pdl, no space, vmfs, iscsi | vmware-storage, vmware-log-insight (vmkernel scsi/apd) | aiops / pilot |
| **network** | vmotion, uplink, link down, mtu, firewall, dfw, segment, tier-0, bgp | vmware-nsx, vmware-nsx-security (traceflow, DFW hits) | pilot |
| **compute** | cpu ready, memory, balloon, swap, contention, numa | vmware-aria (metrics + anomalies) | pilot (rightsizing) |
| **ha_drs** | ha, high availability, drs, failover, admission control, isolation | vmware-monitor, vmware-aiops (cluster) | pilot |
| **power_lifecycle** | power on/off, failed to start, boot, vmx, ovf, clone, snapshot | vmware-aiops (task status, snapshot tree), vmware-monitor | aiops |
| **auth** | login, authentication, denied, 401, 403, token, certificate, tls | config/.env, target cert + time sync | config fix |
| **platform** | vpxd, hostd, service restart, crash, 503, not responding, disconnected | vmware-monitor (connection/service), vmware-log-insight (vpxd/hostd) | pilot |

## Remediation handoff (advisor → executor)

Debug never executes. It mirrors the `vmware-harden → vmware-pilot` pattern:

- **Single, low-risk fix** → call the matching **vmware-aiops** tool (own double-confirm).
- **Multi-step / approval / cross-skill** → submit the proposed plan to **vmware-pilot**:
  state machine + approval gate + rollback + audit all live there.

## Adding a new symptom category

1. Add a `(name, keywords, suggested_check)` tuple to `_CATEGORY_SIGNATURES`.
2. Add the matching row to the table above.
3. Add a focused unit test in `tests/test_timeline.py` (a sample text → expected category).
4. Add a playbook under `references/playbooks/` if the investigation is non-obvious.
