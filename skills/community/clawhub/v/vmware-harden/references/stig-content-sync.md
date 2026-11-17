# vSphere 9 STIG content sync (InSpec / Cinc Auditor)

> **Disclaimer**: This is a community-maintained open-source project and is **not
> affiliated with, endorsed by, or sponsored by VMware, Inc., Broadcom Inc., or
> DISA.** "VMware", "vSphere", and "ESXi" are trademarks of Broadcom. "STIG" is a
> DISA program. This describes a *content mapping*, not an official STIG tool.

## Why this is content, not an API

VCF Operations 9.1 **Automated Configuration Compliance (ACC)** and **Security
Posture Management (SPM)** are **UI- and schedule-driven** with a paid **Salt**
engine. They expose **no public compliance REST endpoint** — the VCF Operations
9.1 OpenAPI (343 paths) has zero Compliance / Benchmark / Baseline / Posture /
Scan / Remediation classes. There is nothing to wrap.

The published vSphere STIG is distributed as **downloadable open-source content**,
not an API:

- **MITRE InSpec / Cinc Auditor** profiles (the machine-readable control set)
- Ansible + PowerCLI remediation playbooks
- SAF (Security Automation Framework) tooling

harden therefore integrates by **content sync**: aligning its own rule catalog
with those profiles. The built-in `vsphere-stig-v9-subset` baseline is the
hand-curated result for a representative host advanced-setting control set.

## Routing: harden vs VCF Operations SPM/ACC

| Need | Use |
|------|-----|
| Continuous, fleet-wide enforcement + automated remediation | **VCF Operations SPM/ACC (UI)** |
| API-scriptable, DuckDB-persisted, cross-target **point-in-time scan** + drift | **vmware-harden** |

harden does not replace SPM/ACC; it is the scriptable scanner that fits CI /
agent workflows where a UI does not.

## The mapping mechanism

Each InSpec/Cinc control asserts an ESXi **advanced setting** has an expected
value. The mapping is mechanical:

1. Pull the official vSphere STIG InSpec/Cinc profile from a verified source:
   - `https://github.com/vmware/dod-compliance-and-automation`
   - `https://github.com/vmware/vcf-security-and-compliance-guidelines`
2. For each control, read its advanced-setting key and expected value
   (e.g. `Security.AccountLockFailures <= 3`).
3. Emit an equivalent harden rule: a declarative SQL `check` against the DuckDB
   twin's `nodes.attrs`, plus `remediation` guidance. Reuse an existing `attrs`
   key when a sibling CIS/SCG rule already covers the same setting so the two
   never diverge.

Example — the InSpec control for `Security.AccountLockFailures` becomes:

```yaml
- id: stig-esxi9-account-lock-failures
  title: "Ensure host account lockout triggers after at most 3 failed logins (Security.AccountLockFailures)"
  severity: medium
  category: auth
  check:
    type: query
    sql: |
      SELECT id, name FROM nodes
      WHERE type = 'host'
        AND CAST(json_extract(attrs, '$.account_lock_failures') AS INTEGER) > 3
```

## Rule naming honesty

Rule ids use harden's own `stig-esxi9-<control>` namespace. They are **not**
invented DISA V-IDs / STIG-IDs (`ESXI-90-000xxx`) — those exact numeric
identifiers must be cross-referenced from the published STIG XCCDF. Each rule
instead names its **advanced-setting key**, which is the stable, public,
verifiable control surface. `tests/eval/regression/test_stig_baseline.py` asserts
every cited setting is in the verified set in
`tests/eval/spec/vcf91_compliance.py`, so a hallucinated control fails CI.

## Automated importer — deferred

A full `import_inspec_profile()` that parses an InSpec profile and emits a
baseline YAML is **deferred**. It is a content transform (no network/API
dependency), safe to build later. Today, hand-author or override baseline YAML
under `~/.vmware-harden/baselines/` and load it with
`vmware-harden baseline import <file>`. The stub lives at
`vmware_harden/baselines/stig.py::import_inspec_profile`.

## Scan it

```bash
vmware-harden stig controls                       # list the controls
vmware-harden stig sync-info                       # this routing, as JSON
vmware-harden scan --baseline vsphere-stig-v9-subset --target <vcenter>
```
