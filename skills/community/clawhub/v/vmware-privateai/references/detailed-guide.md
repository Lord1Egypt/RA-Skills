> Detailed usage and architecture reference. [Quick overview](../../../README.md).


# VMware Private AI

[![PyPI](https://img.shields.io/pypi/v/vmware-privateai)](https://pypi.org/project/vmware-privateai/) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#readme-license)

English | [中文](detailed-guide-CN.md)

Maintainer: Wei Zhou · [zhouwei008@gmail.com](mailto:zhouwei008@gmail.com)

Community-maintained open-source project; not an official VMware or Broadcom product.

[Overview](#readme-overview) · [Quick Start](#readme-quick-start) · [MCP Configuration](#readme-mcp-configuration) · [Capabilities and Workflows](#readme-capabilities-and-workflows) · [Safety and Audit](#readme-safety-and-audit) · [Troubleshooting](#readme-troubleshooting) · [Companion Skills](#readme-companion-skills) · [Reference](#readme-reference) · [License](#readme-license)

<a id="readme-overview"></a>

## Overview

Runs locally over stdio by default; configure required targets and credentials on your own machine.

The **GPU / AI-infrastructure** lens of the VMware skill family — GPU host and device inventory, vGPU consumers,
live GPU utilization, the vGPU / DirectPath profile catalog, vGPU assignment, and the models and knowledge bases
served by **Private AI Service (PAIS)** — over the **vSphere 9.x / VCF 9.1** Web Services API (pyVmomi) and the
PAIS REST API. MCP server + CLI.

> **Disclaimer**: This is a community-maintained open-source project and is **not affiliated with,
> endorsed by, or sponsored by VMware, Inc., Broadcom Inc., or NVIDIA Corporation.** "VMware", "vSphere",
> and "VCF" are trademarks of Broadcom; "NVIDIA" and "vGPU" are trademarks of NVIDIA. Source is auditable at
> [github.com/vmware-skills/VMware-PrivateAI](https://github.com/vmware-skills/VMware-PrivateAI) under the MIT license.

> **Status: beta.** Skill #15 of the family, on its own version line. Every API path is verified against official
> Broadcom/NVIDIA docs before use (see `tests/eval/spec/privateai_endpoints.py`) — no endpoints written from memory.
> GET response **field names** and some PAIS paths remain defensive and await validation on real 9.x hardware
> (see the beta caveats in `skills/vmware-privateai/SKILL.md`). Governed by the family harness (audit + policy +
> teaching errors); read/write authorization is left to the RBAC role of the vCenter service account.

Supporting commands also check GPU readiness and access, estimate model sizing locally and inspect local air-gap bundles. Local sizing does not contact a model provider or consume inference quota. Diagnostic examples shared in issues must be minimized and redacted: remove identifiers, internal addresses, sensitive hardware/capacity details and credentials.

Full agent instructions: [`skills/vmware-privateai/SKILL.md`](../../../skills/vmware-privateai/SKILL.md).

<a id="readme-quick-start"></a>

## Quick Start

Requires Python `>=3.11` and `uv`.

```bash
uv tool install vmware-privateai==2.5.4
vmware-privateai --help
```

Target, credential and local data setup: [setup guide](../../../skills/vmware-privateai/references/setup-guide.md).

<details>
<summary>Installation and configuration details (including offline setup)</summary>

### Quick Start

```bash
uv tool install vmware-privateai==2.5.4
vmware-privateai version
vmware-privateai gpu host-list        # first read command — lists the hosts that have GPUs
```

Configuration lives in `~/.vmware-privateai/config.yaml` (targets + an optional `pais:` section); passwords and the
PAIS bearer token live in `~/.vmware-privateai/.env` (chmod 600). See
`skills/vmware-privateai/references/setup-guide.md`.


</details>

<a id="readme-mcp-configuration"></a>

## MCP Configuration

Copy this configuration into your MCP client's local stdio settings. The client must be able to find `uvx`; the initial package installation requires access to a package index.

```json
{
  "mcpServers": {
    "vmware-privateai": {
      "command": "uvx",
      "args": ["--from", "vmware-privateai==2.5.4", "vmware-privateai-mcp"],
      "env": {
        "VMWARE_PRIVATEAI_CONFIG": "~/.vmware-privateai/config.yaml"
      }
    }
  }
}
```

<a id="readme-capabilities-and-workflows"></a>

## Capabilities and Workflows

### Capabilities (20 MCP tools — 19 read / 1 write)

| Category | Tools | Read/Write |
|----------|-------|:----------:|
| **GPU inventory** | host list / detail, device list, vGPU consumer list | 4 read |
| **GPU utilization** | live utilization per vGPU VM (GPU %, memory %, temperature) | 1 read |
| **GPU readiness** | per-host vGPU/PAIS readiness verdict + blocking reasons | 1 read |
| **Profile catalog** | vGPU profile list, DirectPath profile list | 2 read |
| **Profile validation** | read-only pre-check before changing a vGPU profile (power state + whether the host offers it) | 1 read |
| **vGPU assignment** | set a VM's vGPU profile (the VM must be powered off) | 1 write |
| **Private AI Service** | served models, model catalog, knowledge bases, data sources | 4 read |
| **PAIS MCP gallery** | registered MCP servers, tool approval and availability | 2 read |
| **PAIS monitoring** | cluster GPU summary (utilization/memory/temperature, hot/idle, busiest) | 1 read |
| **Sizing & air-gap** | LLM GPU/storage sizing advisor, local pais.yml mirror manifest | 2 read |
| **Access self-check** | which account the server uses and whether it holds each tool's vSphere privileges (root folder) | 1 read |

Reads are strictly non-destructive. The one write (`assign_vgpu`) previews its blast radius, refuses a powered-on
VM, **never powers a VM off itself**, double-confirms on the CLI, and is audited to `~/.vmware/audit.db`;
pre-check with `validate_vgpu_profile` first.
`assign_vgpu` takes `confirm` (default `false`). Without it the call returns `blast_radius` — the VM's name and id,
current and target profile, whether its vGPU device is edited or a new one added, power state, `blockers` and
`unmeasured` — and changes nothing. `confirm=true` is refused for a powered-on or suspended VM, a name shared by
several VMs, and a VM whose power state or devices cannot be read.
`get_pais_model_catalog` / `list_pais_data_sources` use unconfirmed PAIS control-plane paths (pitfall #36: a 404
returns a base-URL teaching hint and is not a bug); `advise_pais_sizing` / `verify_pais_bundle` need no connection
(pure computation / local file parsing).
`list_pais_mcp_servers` and `list_pais_mcp_tools` use routes documented in the
[official PAIS MCP API](https://developer.broadcom.com/xapis/vmware-private-ai-service-api/latest/mcp-servers/).
They return bounded names, availability and approval state, not server URLs,
headers or raw tool schemas. PAIS approval controls gallery visibility; the
underlying VMware Policy and product RBAC still decide what a caller may do.
These routes have not been tested against a live PAIS appliance.

### Common Workflows

**1. Find an idle GPU and change a VM's vGPU profile**
```bash
vmware-privateai gpu device-list --vendor NVIDIA   # vm_count 0 = idle
vmware-privateai gpu consumer-list                 # who holds a vGPU, with which profile
vmware-privateai vgpu profile-list --host esx-07   # profiles this host can assign
vmware-privateai gpu vgpu-assign fin-train-01 grid_a100-4c --dry-run   # preview
# power the VM off with vmware-aiops first, then:
vmware-privateai gpu vgpu-assign fin-train-01 grid_a100-4c            # double-confirm + audit
```
*Failure branch*: on "VM is powered on", power it off first with vmware-aiops `power_off_vm` (CLI:
`vmware-aiops vm power-off fin-train-01`); if the host does not offer the profile or memory is short, check the
valid profiles with `vmware-privateai gpu host-get <that host>`.

**2. Fleet-wide GPU utilization sweep**
```bash
vmware-privateai gpu utilization --top 10
```
*Failure branch*: `metrics unavailable` is not an error — the NVIDIA host GPU driver does not expose that VM's
counters. Deeper per-SM / MIG-slice telemetry is not provided by vSphere (it needs NVIDIA DCGM).

**3. See what PAIS is serving**
```bash
vmware-privateai pais model-list
vmware-privateai pais kb-list
```
*Failure branch*: HTTP 404 is usually a base-URL mismatch (the `/api/v1` prefix varies by deployment and is
unconfirmed in beta) — check `pais.endpoint`; HTTP 401/403 means `VMWARE_PRIVATEAI_PAIS_TOKEN` expired or lacks
permission — fetch a new token.

**4. Inspect PAIS MCP registrations and approvals (read-only)**
```bash
vmware-privateai pais mcp-servers
vmware-privateai pais mcp-tools --server-id <PAIS_SERVER_ID>
```
Use `--after <cursor>` when a page prints `next --after`. These commands do
not register or approve tools and cannot prove a backend caller is authorized.
Live PAIS response behavior still needs validation.

<a id="readme-safety-and-audit"></a>

## Safety and Audit

### Security

See `SECURITY.md` at the repo root. Highlights: credentials only in `.env` (chmod 600, `b64:` obfuscation); TLS
verification on by default; all vSphere/PAIS text passes `vmware_policy.sanitize()` against prompt injection;
read/write authorization is left to vCenter RBAC; `assign_vgpu` is power-off gated + double-confirmed + audited.

<!-- usage: remote-and-exposure -->

### Remote access (HTTPS) and limiting tools

By default `vmware-privateai mcp` speaks stdio to one local client and offers every tool. Two options change that
(vmware-policy ≥ 1.21.0).

**Serve over HTTPS** so clients on other machines can connect. Every caller needs a bearer token:

```bash
vmware-audit token create alice          # prints the token once; give it to alice
vmware-audit token list                  # names only
vmware-audit token revoke alice          # refused from its next request, no restart
vmware-privateai mcp --transport https --host 0.0.0.0 --port 8443 \
    --cert /etc/vmware-mcp/server.pem --key /etc/vmware-mcp/server-key.pem \
    --public-name mcp.example.com
```

Connect a client (Claude Code shown; any MCP client that supports streamable HTTP and custom headers works):

```bash
claude mcp add --transport http vmware-privateai https://mcp.example.com:8443/mcp \
    --header "Authorization: Bearer $VMWARE_MCP_TOKEN"
```

```json
{
  "mcpServers": {
    "vmware-privateai": {
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
- Tools that read or write files on this server (here: `verify_pais_bundle` manifests) never touch its configuration, tokens, audit log or
  TLS key, and over the network they are off unless `VMWARE_MCP_FILE_ROOT` names a directory for them
  (vmware-policy ≥ 1.23.1).
- The audit log records each caller as `token:<name>`. Calls run side by side, also on the same target: the server keeps up to `VMWARE_MCP_POOL_SIZE` (default 2) sessions per target, each one a login on that target, and a call waits at most 300 s for a free session (vmware-policy ≥ 1.22.0).
- **Everyone who can reach the endpoint acts with this server's account.** Tokens identify callers; they grant
  nothing on the platform. Run one endpoint per privilege level. `vmware-privateai access-info` shows which account that is and what it may do.
- **Several people or roles on one endpoint:** run `vmware-audit roles enable` once, then give each token a role (`vmware-audit token create NAME --role reader`, or a role in `roles.yaml` naming tools and targets; vmware-policy ≥ 1.24.0). A role limits what the token may call on this endpoint; it cannot grant more than the account has. See vmware-policy's README, "Roles for network callers".

**Offer only read tools, plus the writes you choose:**

```bash
vmware-privateai mcp --expose read --allow-write assign_vgpu
# or: VMWARE_PRIVATEAI_MCP_EXPOSE=read VMWARE_PRIVATEAI_MCP_ALLOW_WRITE=assign_vgpu vmware-privateai mcp
```

Tools not offered do not appear in the client's tool list. A bad value or an unknown write tool stops the server
(exit 2). This limits what clients are offered; it is not authorization, so the account itself should be
least-privilege.

Details: `skills/vmware-privateai/references/setup-guide.md` ("Serving MCP over HTTPS", "Limiting which tools are offered").

<a id="readme-troubleshooting"></a>

## Troubleshooting

### System proxy bypass

The PAIS REST client honors the operating system proxy bypass list for the configured origin.
TLS verification still follows `verify_ssl`, and CA environment settings such as `SSL_CERT_FILE` remain active.
Other origins retain their normal proxy routing.

<a id="readme-companion-skills"></a>

## Companion Skills

The VMware Skills family contains 14 MCP servers and the shared Policy library. Choose tools by responsibility: [vmware-skills](https://github.com/vmware-skills).

### Companion Skills

- [vmware-aiops](https://github.com/vmware-skills/VMware-AIops) — the vCenter VMs behind AI workloads (power/snapshot/clone/migrate)
- [vmware-vks](https://github.com/vmware-skills/VMware-VKS) — GPU-enabled Tanzu Kubernetes
- [vmware-monitor](https://github.com/vmware-skills/VMware-Monitor) — read-only vSphere health

This skill is the GPU lens over all three.

<a id="readme-reference"></a>

## Reference

Release history: [RELEASE_NOTES.md](../../../RELEASE_NOTES.md).

Read-only self-test with your own model and agent host: [model-fit self-test](https://github.com/vmware-skills/marketplace/blob/main/MODEL_FIT_SELF_TEST.md).

### Upgrading to 2.0

2.0 renamed every MCP tool it had so every name starts with a verb (e.g. `directpath_profile_list` → `list_directpath_profiles`, `gpu_consumer_list` → `list_gpu_consumers`, `gpu_device_list` → `list_gpu_devices`). The full old → new table is in
[RELEASE_NOTES.md](../../../RELEASE_NOTES.md#v200--mcp-tools-renamed-verb-first). Nothing else changes: same tools, parameters,
safety gates and CLI commands. If an agent prompt, script or `~/.vmware/rules.yaml` names a tool, update it — though deny
rules written with the old names keep working with vmware-policy ≥ 1.18 (`vmware-audit policy` lists any rule the
renames widened), and vmware-pilot ≥ 1.13 translates old names in saved workflows.
If an install older than 2.0 shares that `rules.yaml`, give it vmware-policy ≥ 1.18.2 too: it matches each rule
against both the old and the new name, so one file serves both.

<a id="readme-license"></a>

Unrecognized PAIS collection containers or non-object rows raise a readable error; they are never evidence of an empty inventory. Recognized empty arrays remain measured empty results. PAIS positive appliance validation is still pending.

## License

MIT

### PAIS gallery continuation

Gallery continuation tokens are opaque. A missing, repeated, overlong or
sanitization-changing token stops continuation with `status=partial` and
`next_after=null`; it does not establish that the registry is empty or complete.
Valid tokens are passed unchanged through query encoding. These boundaries are
covered with synthetic HTTP responses; PAIS live validation is still pending.
