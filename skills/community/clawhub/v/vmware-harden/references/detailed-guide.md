> Detailed usage and architecture reference. [Quick overview](../../../README.md).


# VMware Harden

[![PyPI](https://img.shields.io/pypi/v/vmware-harden)](https://pypi.org/project/vmware-harden/) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#readme-license)

English | [中文](detailed-guide-CN.md)

Maintainer: Wei Zhou · [zhouwei008@gmail.com](mailto:zhouwei008@gmail.com)

Community-maintained open-source project; not an official VMware or Broadcom product.

[Overview](#readme-overview) · [Quick Start](#readme-quick-start) · [MCP Configuration](#readme-mcp-configuration) · [Capabilities and Workflows](#readme-capabilities-and-workflows) · [Safety and Audit](#readme-safety-and-audit) · [Troubleshooting](#readme-troubleshooting) · [Companion Skills](#readme-companion-skills) · [Reference](#readme-reference) · [License](#readme-license)

<a id="readme-overview"></a>

## Overview

Runs locally over stdio by default; configure required targets and credentials on your own machine.

> **Disclaimer**: Community-maintained open-source project. **Not affiliated with, endorsed by, or sponsored by VMware, Inc. or Broadcom Inc.** "VMware", "vSphere", "ESXi", and "NSX" are trademarks of Broadcom. Source code is publicly auditable at [github.com/vmware-skills/VMware-Harden](https://github.com/vmware-skills/VMware-Harden) under the MIT license.


AI-native VMware compliance and baseline enforcement. Sibling to the `vmware-*` skill family.

- **Read-only against vSphere**: all 8 MCP tools carry the `[READ]` marker and none mutate managed VMware infrastructure; `scan_target` writes only to the local twin DB (a cache of its own observations). See [Read-only by design](#read-only-by-design).

Container examples build a local version-tagged image and run it with `--pull=never`, avoiding registry fallback. A local version tag is not an immutable image digest.

Full agent instructions: [`skills/vmware-harden/SKILL.md`](../../../skills/vmware-harden/SKILL.md).

<a id="readme-quick-start"></a>

## Quick Start

Requires Python `>=3.10` and `uv`.

```bash
uv tool install "vmware-harden[collectors]==1.20.1"
vmware-harden --help
```

Target, credential and local data setup: [setup guide](../../../skills/vmware-harden/references/setup-guide.md).

<details>
<summary>Installation and configuration details (including offline setup)</summary>

### Quickstart

```bash
# The collectors extra is what makes `scan` work: harden reads inventory
# through vmware-aiops / vmware-storage / vmware-nsx-security, and `uv tool
# install` gives each tool its own environment — installing them separately
# puts them where harden cannot import them from.
uv tool install "vmware-harden[collectors]==1.20.1"

# Reporting on an existing twin DB needs no collectors:
#   uv tool install vmware-harden==1.20.1

# List built-in baselines
vmware-harden baseline list

# Run a scan
vmware-harden scan --target <vcenter-name> --baseline cis-vmware-esxi-8.0-subset

# Or use 等保 2.0 三级 (国内合规独家)
vmware-harden scan --target <vc> --baseline dengbao-2.0-level3-vmware

# View results
vmware-harden report
vmware-harden drift

# Generate remediation suggestions
export ANTHROPIC_API_KEY=...  # optional; falls back to mock without
vmware-harden advise --all-critical

# Web dashboard
vmware-harden web --port 8080  # → http://127.0.0.1:8080
```

#### Reading a result: violations alone are not a verdict

A rule can only judge configuration that was actually gathered, and that fails
in two independent ways. A rule whose attribute **no collector produces** is not
executed at all. A rule that *does* run can still learn nothing about one
particular host, because there the value came back absent or as the `N/A`
sentinel — an unreachable host, an account without the privilege, a setting the
ESXi build does not have. Neither is reported as passing:

```
$ vmware-harden report
No violations among the checks that could be made.

16 of 20 rules could not be evaluated — no collector provides the data they
check, so their result is unknown, not compliant. 6 of 8 per-node checks could
not be made across 2 node(s): the rules ran, but the values they read were
missing on those nodes, so those nodes are unknown rather than compliant.
Not evaluated:
  cis-esxi-2.1.1   no collector writes host.ntp_enabled
  ...
Not judged on these nodes (data missing):
  cis-esxi-2.2.1   esx-02    esxi_build
  ...
```

`--format json` returns `{"violations": [...], "coverage": {...}}`, and the MCP
tools return the same `coverage` block, so an agent reading `violations: 0`
cannot conclude "compliant" on its own. Before v1.9.0 the uncollected-attribute
rules matched zero rows and were silently counted as passes; before v1.10.0 the
per-node case was, too. See RELEASE_NOTES.md.

The two lists call for different work: the first is waiting on a collector, the
second on that node's reachability and the scanning account's privileges.


#### Offline / Air-Gapped Install (from source)

This project uses the modern PEP 517 build system (hatchling), so there is **no
`setup.py`** by design — that is expected, not a missing file. If you cloned the
source and hit `ERROR: File "setup.py" or "setup.cfg" not found ... editable mode
currently requires a setuptools-based build`, your `pip` is older than 21.3 and
cannot do an *editable* (`-e`) install with a non-setuptools backend. Editable
mode is a developer convenience, not needed to run the tool — do one of:

```bash
# From the source tree — a normal (non-editable) install builds a wheel:
pip install .              # NOT  pip install -e .

# ...or upgrade pip first, and editable works too:
pip install --upgrade pip && pip install -e .
```

For a **truly air-gapped host**, build the wheels on a connected machine and copy
them over — the target then needs no network:

```bash
# On a connected machine, collect this package + its dependencies as wheels:
pip wheel . -w dist        # → dist/*.whl   (or: uv build, for just this package)

# Copy dist/ to the air-gapped host, then install offline:
pip install --no-index --find-links dist vmware-harden
```

#### Explicit VMRC clipboard settings

The VM security pass reads the per-VM `isolation.tools.copy.disable` and
`isolation.tools.paste.disable` options. `isolation_copy_disabled` is true only when both
are explicitly true, false when either is explicitly false, and otherwise absent
(undetermined). Duplicate settings remain unknown. SCG rule `scg-vm-5`, inherited by the
v9 subset, checks this explicit configuration requirement; it does not test actual
clipboard transfer, host defaults or guest/Tools behavior. Unrelated `extraConfig`
values are not stored or returned.


</details>

<a id="readme-mcp-configuration"></a>

## MCP Configuration

Copy this configuration into your MCP client's local stdio settings. The client must be able to find `uvx`; the initial package installation requires access to a package index.

```json
{
  "mcpServers": {
    "vmware-harden": {
      "command": "uvx",
      "args": ["--from", "vmware-harden[collectors]==1.20.1", "vmware-harden-mcp"],
      "env": {
        "VMWARE_AIOPS_CONFIG": "~/.vmware-aiops/config.yaml"
      }
    }
  }
}
```

Live Harden collection reuses `~/.vmware-aiops/config.yaml`; keep `[collectors]` to install the collection dependencies.

The following sections retain preinstalled CLI alternatives and product-specific MCP options.

<details>
<summary>Preinstalled CLI and additional MCP options</summary>

### MCP server

```bash
vmware-harden mcp  # stdio MCP server (legacy alias: vmware-harden-mcp)
```

Configure your MCP client with one of `examples/mcp-configs/*.json`. 8 read-only tools: `list_baselines`, `get_baseline_rules`, `list_stig_controls`, `describe_stig_content_sync`, `list_violations`, `get_remediation`, `list_drift_events`, `scan_target`.


</details>

<a id="readme-capabilities-and-workflows"></a>

## Capabilities and Workflows

### Built-in baselines

| Baseline | Rules | Applies to | Source |
|----------|-------|-----------|--------|
| `cis-vmware-esxi-8.0-subset` | 20 | host | CIS Benchmark v1.0 |
| `vsphere-scg-v8-subset` | 15 | host, vm | [VMware vcf-security-and-compliance-guidelines](https://github.com/vmware/vcf-security-and-compliance-guidelines) |
| `dengbao-2.0-level3-vmware` | 20 | host, vm, datastore, dfw_rule | GB/T 22239-2019 三级 |
| `pci-dss-4.0-vmware` | 10 | host, dfw_rule | PCI-DSS v4.0 |
| `eu-nis2-vmware` | 12 | host, dfw_rule | EU NIS2 Directive (Articles 21/23, Annex I) |
| `bsi-itgs-basisabsicherung-vmware` | 10 | host | BSI IT-Grundschutz (OPS.1.1.4 + SYS.1.1) |
| `cis-vmware-esxi-9.0-subset` | 20 | host | Inherits `cis-vmware-esxi-8.0-subset` via `extends:` |
| `vsphere-scg-v9-subset` | 15 | host, vm | Inherits `vsphere-scg-v8-subset` via `extends:` |
| `vmsa-advisories` | 3 (one per catalogued advisory) | host, vcenter | Offline VMSA catalog — see [Known vulnerabilities](#known-vulnerabilities-vmsa) |
| `vsphere-stig-v9-subset` ⚠️ *experimental* | 12 | host | vSphere 9 STIG-aligned host advanced settings ([DoD/DISA STIG content](https://github.com/vmware/dod-compliance-and-automation)) — collector verified on ESXi 8.0.3; not yet run against 9.x |

`baseline list` returns 10 IDs: the 7 rule-bearing YAML baselines above (99 rules total), the
two v9 aliases, which carry no rules of their own and resolve to their v8 parent's, and
`vmsa-advisories`, which is generated from the advisory catalog rather than read from a file.

#### Known vulnerabilities (VMSA)

`vmsa-advisories` judges each ESXi host's and the vCenter's own version and build
against an **offline catalog of VMware security advisories** shipped in the package
(`vmware_harden/advisories/catalog.yaml`, checked against its sources on the catalog
date). One rule per advisory; each rule's text quotes the 等保 2.0 三级 control it
evidences (安全计算环境·入侵防范: find known vulnerabilities and patch them after testing).

```bash
vmware-harden scan --target prod-vc --baseline vmsa-advisories
vmware-harden report                    # each affected component: its fix, and whether the CVE is in CISA KEV
vmware-harden report --format csv > vmsa.csv
```

| Verdict | Meaning |
|---|---|
| **affected** | A violation. The evidence names the release that fixes it. |
| **fixed** | Same line, at or past the fix. |
| **unknown** | Listed per node with the reason: unreadable build, a line the advisory does not list or that was past end of support, a branch the sources disagree on, a product the catalog does not carry yet. **Never a pass.** |

A clean result means **no open advisory known as of the catalog date**, not "not
vulnerable": advisories published later are not in the catalog. Builds are compared
only within one `major.minor` line (a 7.0 U3 build can be numerically larger than an
8.0 GA build).

**How the catalog is built.** Entries record their advisory, CVE and build-number sources.
The initial catalog used NVD, CISA KEV and independent sources quoting Broadcom when its
advisory pages could not be read. VMSA-2026-0006 has now been checked directly against
Broadcom's response matrix and build KBs and covers both vCenter and ESXi. Each fixed
build is checked against `builds.yaml`; a fix can predate the consolidated advisory.

Mixed-product advisories evaluate each applicable CVE separately. Node evidence lists
affected CVEs in `cves`, individual verdicts/CVSS in `cve_results`, and `max_affected_cvss`;
fixed or other-product CVEs do not contribute to that node's KEV flag. Each rule retains
the advisory's severity. Verdicts describe build exposure; guest configuration and
exploitability require separate evidence. Missing mappings remain unknown.

The advisory coverage boundary remains **2026-10-19**. Shipped KEV flags were checked
against CISA snapshot **2026.11.06** on 2026-11-08; their provenance is separate from a
user's optional online refresh. Updating an entry does not imply that every newer
advisory has been added.

**Optional refresh.** `vmware-harden advisories update` downloads the CISA KEV feed (and, with
`--nvd`, NVD scores) into `~/.vmware-harden/advisories-cache.json`, which the catalog loader
overlays: KEV flags are only ever added, CVSS only filled where missing, and fixed builds are never
taken from it. It also lists ESXi/vCenter CVEs in KEV that no catalogued advisory covers. A failed
KEV fetch exits 1 and leaves the previous cache unchanged; an NVD record that cannot be read is
reported and does not block the KEV refresh. A running MCP server picks up a new cache on its next
call. Reports show when KEV was last checked. `vmware-harden advisories show` prints the catalog
date and the last refresh.

#### VCF 9.0 / 9.1 Compatibility

The existing baselines (`cis-vmware-esxi-8.0-subset`, `vsphere-scg-v8`, `dengbao-2.0-level3-vmware`, `pci-dss-4.0-vmware`) scan VCF 9.0 / 9.1 clusters successfully — most rules target host advanced settings stable across 8.x → 9.x. `cis-vmware-esxi-9.0-subset` and `vsphere-scg-v9-subset` ship today as `extends:` aliases of their v8 parents — same rules, a v9-named ID to scan and report under. Rules specific to 9.x will be added to them as Broadcom publishes the v9 guides.

`vsphere-stig-v9-subset` is a rule-bearing STIG-aligned baseline: 12 host advanced-setting controls (account lockout, password policy, DCUI access, shell/DCUI timeouts, MOB, guest BPDU, remote syslog) mapped to the official open-source vSphere STIG content (MITRE InSpec / Cinc Auditor). **Status: experimental.** Its checks read ESXi host advanced settings the host collector fetches via a `config.option` PropertyCollector pass. That pass **was verified end-to-end on 2026-08-13** against a live standalone **ESXi 8.0.3** (build 24280767): all 12 attributes came back populated, with values in the shapes the rules expect (`account_lock_failures=5`, `dcui_access='root'`, `password_quality_control='retry=3 min=disabled,disabled,disabled,7,7'`, `mob_enabled=False`, `syslog_remote_host=''`), and the scan raised 3 genuine violations. Still unverified, and why the status stays experimental: **ESXi 9.x**, which is what this baseline actually targets, and any vCenter-managed multi-host inventory. Treat results on 9.x as **non-authoritative**. The v1.9.0 undetermined mechanism does not cover a failed fetch on its own: it refuses a rule when *no collector declares* the attribute, a static check against the vocabulary, and these STIG attributes *are* declared, so their rules do run. If the real PropertyCollector pass comes back empty on live hardware, the attribute is simply absent and the rule again matches zero rows. **v1.10.0 catches that case** — such a host is recorded as a per-node gap (`coverage.undetermined_node_checks`) rather than a pass, so an unverified collector shows up as unjudged hosts instead of a clean report. What remains unverified is whether the pass returns the *right* values, which no coverage mechanism can tell you. The baseline's `status` field is surfaced by `list_baselines` and `describe_stig_content_sync` so a scan self-declares this caveat. It is a **content sync**, not an API wrapper — VCF Operations 9.1 Automated Configuration Compliance (ACC) / Security Posture Management (SPM) is UI- and schedule-driven and exposes **no public compliance REST API**. For continuous, fleet-wide enforcement and automated remediation, use **VCF Operations SPM/ACC (UI)**; vmware-harden is the API-scriptable, DuckDB-persisted, cross-target point-in-time scanner. See [references/stig-content-sync.md](../../../skills/vmware-harden/references/stig-content-sync.md) and inspect the catalog with `vmware-harden stig controls`.

##### Official Broadcom References

- **Security Configuration Guides**: <https://core.vmware.com/security/> — vSphere SCG v8 / future v9
- **SDKs**: <https://developer.broadcom.com/sdks> — VCF Python SDK (for fetching host config via REST)
- **CIS Benchmarks**: <https://www.cisecurity.org/cis-benchmarks/> — CIS VMware ESXi Benchmark v1.0 (8.0 / future 9.0)

### Custom baselines

```bash
vmware-harden baseline validate ./my-strict.yaml
vmware-harden baseline import ./my-strict.yaml --name my-strict-cis
vmware-harden scan --target <vc> --baseline my-strict-cis
```

YAML supports `extends:` for inheriting from a built-in baseline. See `skills/vmware-harden/references/cli-reference.md`.

<a id="readme-safety-and-audit"></a>

## Safety and Audit

### Read-Only by Design

vmware-harden is read-only against vSphere and NSX — all 8 MCP tools carry the `[READ]`
marker, and none mutate managed VMware infrastructure. `scan_target` writes only to the
local twin DB (`~/.vmware-harden/twin.duckdb`), a cache of its own observations rather than
managed infrastructure. Remediation is never applied by this skill; it is deferred to
vmware-pilot, which provides approval gating and audit trails for write operations.

### Remote access (HTTPS) and limiting tools

By default `vmware-harden mcp` speaks stdio to one local client and offers every tool. Two options change that
(vmware-policy ≥ 1.21.0).

**Serve over HTTPS** so clients on other machines can connect. Every caller needs a bearer token:

```bash
vmware-audit token create alice          # prints the token once; give it to alice
vmware-audit token list                  # names only
vmware-audit token revoke alice          # refused from its next request, no restart
vmware-harden mcp --transport https --host 0.0.0.0 --port 8443 \
    --cert /etc/vmware-mcp/server.pem --key /etc/vmware-mcp/server-key.pem \
    --public-name mcp.example.com
```

Connect a client (Claude Code shown; any MCP client that supports streamable HTTP and custom headers works):

```bash
claude mcp add --transport http vmware-harden https://mcp.example.com:8443/mcp \
    --header "Authorization: Bearer $VMWARE_MCP_TOKEN"
```

```json
{
  "mcpServers": {
    "vmware-harden": {
      "type": "http",
      "url": "https://mcp.example.com:8443/mcp",
      "headers": { "Authorization": "Bearer ${VMWARE_MCP_TOKEN}" }
    }
  }
}
```

- The server will not start without a token, refuses Host/Origin values outside `--public-name`, and checks
  before it binds that unauthenticated requests get 401. Use a certificate your clients trust for those names.
- Behind a TLS-terminating reverse proxy on the same machine use `--transport http --host 127.0.0.1
  --public-name mcp.example.com` and pass the `Authorization` header through.
- Behind a load balancer or gateway on another machine, keep `--transport https` (a self-signed certificate is
  fine), list in `--public-name` the host name the balancer sends as `Host`, and have it forward `Authorization`.
  Its health probe can use `GET /healthz`, which needs no token and returns only `{"status": "ok"}`
  (vmware-policy ≥ 1.23.0).
- Send `traceparent` or `X-Request-ID` with each request to have it stored on the audit row;
  `vmware-audit log --correlation-id ID` then finds the calls behind one platform request.
- The audit log records each caller as `token:<name>`. Calls naming different targets run in parallel; calls that
  name no target run one at a time, so name the target when several people share a server.
- **Everyone who can reach the endpoint acts with this server's account.** Tokens identify callers; they grant
  nothing on the platform. Run one endpoint per privilege level.
- **Several people or roles on one endpoint:** run `vmware-audit roles enable` once, then give each token a role (`vmware-audit token create NAME --role reader`, or a role in `roles.yaml` naming tools and targets; vmware-policy ≥ 1.24.0). A role limits what the token may call on this endpoint; it cannot grant more than the account has. For a target-limited role, `scan_target`'s target is checked against vmware-aiops' config; the datastore and DFW collectors look the same name up in vmware-storage's and vmware-nsx-security's configs, so a name must mean the same system in all three. See vmware-policy's README, "Roles for network callers".

**Limiting tools:** every tool of this server is read-only, so `--expose read` changes nothing here; it
exists for the write-capable skills. Least privilege comes from the account the server uses.

Details: `skills/vmware-harden/references/setup-guide.md` ("Serving MCP over HTTPS", "Limiting which tools are offered").

<a id="readme-troubleshooting"></a>

## Troubleshooting

For installation issues, see the installation instructions on this page. Check CLI arguments with `--help` before operating. Include only a minimal, redacted example when reporting a problem.

<a id="readme-companion-skills"></a>

## Companion Skills

The VMware Skills family contains 14 MCP servers and the shared Policy library. Choose tools by responsibility: [vmware-skills](https://github.com/vmware-skills).

### Family

- **vmware-aiops** — host inventory + ops (used by harden's HostCollector)
- **vmware-monitor** — read-only counterpart
- **vmware-storage** — datastore inventory
- **vmware-nsx-security** — DFW inventory
- **vmware-pilot** — execute remediations (writes; out of scope for harden)
- **vmware-policy** — `@vmware_tool` audit decorator

<a id="readme-reference"></a>

## Reference

Release history: [RELEASE_NOTES.md](../../../RELEASE_NOTES.md).

Read-only self-test with your own model and agent host: [model-fit self-test](https://github.com/vmware-skills/marketplace/blob/main/MODEL_FIT_SELF_TEST.md).

### GA family member (since v1.5.18)

Production-ready compliance platform with **9 built-in baselines** (CIS ESXi 8.0 + 9.0, vSphere SCG v8 + v9, **vSphere 9 STIG-aligned**, **等保 2.0 三级**, PCI-DSS 4.0, **EU NIS2**, **BSI IT-Grundschutz**) carrying **99 rules**, a **VMSA known-vulnerability check** for ESXi and vCenter builds, multi-vCenter Twin, drift detection, **LLM Remediation Advisor**, **MCP server** with 8 audited tools, web dashboard, and `vmware-harden doctor` environment diagnostics.

### Architecture

- **Estate Digital Twin** — DuckDB single file at `~/.vmware-harden/twin.duckdb`. Multi-target safe via target prefix on all node IDs.
- **Collectors** — lazy-import sibling vmware-* skills (no spawn overhead). All scans are READ; writes deferred to vmware-pilot.
- **Baseline schema** — Pydantic v2, strict (`extra="forbid"`), `extends:` inheritance, user-dir override.
- **Drift** — pure diff function with optional persistence; auto-runs after every scan.
- **Advisor** — LLM-driven Suggestion generation; Anthropic provider with prompt caching; mock fallback for tests / no-API-key environments.
- **Audit** — every MCP tool wrapped with `@vmware_tool` from family vmware-policy.
- **Web** — FastAPI + Jinja2 + Tailwind/HTMX/ECharts CDN.

### Lab regression

```bash
export VMWARE_HARDEN_LAB_TARGET=<your-vc>
pytest tests/eval/regression -v -m lab
```

### Acceptance criteria (v1.5.18 GA)

- 221 tests passing
- Bandit: 0 issues at any severity
- All 8 MCP tools audited
- SKILL.md ≤ 3000 words, family-convention compliant
- SECURITY.md with 6 elements + Broadcom disclaimer
- 9 built-in baselines (99 rules across 7 rule-bearing sets + 2 v9 aliases)
- `vmware-harden doctor` for environment diagnostics
- GA member of vmware-* family (version-aligned at 1.5.28)

### References

- Family CLAUDE.md: `CLAUDE.md` at the monorepo root

<!-- usage: remote-and-exposure -->

<a id="readme-license"></a>

## License

MIT

### DFW parent-policy evidence and validation scope

DFW rules now retain the actual parent policy `display_name` as `section_name`.
A missing parent name stays unknown; a rule's own name is not a substitute.
This makes one more built-in rule structurally evaluable, reducing the frozen
pending-rule set from 15 to 14. Per-node missing evidence is still undetermined.
Aggregate and absence checks read only the requested snapshot. Missing parent
names remain coverage gaps instead of absence findings; a measured empty DFW
inventory can still establish absence. NSX positive live validation is pending.

`posture_drift` remains an intentionally reserved, unit-tested baseline-evolution
helper; it is not a CLI/MCP feature. `diff_snapshots` is the supported pairwise
library comparison, including persistence and scan-scope tests; the CLI uses
the current drift path. Their existence does not establish dead-code defects
or justify deleting library entry points. 9.x-specific controls are not added
without an authoritative control definition and evidence source; inherited
baselines do not prove 9.x appliance validation.
