> Detailed usage and architecture reference. [Quick overview](../../../README.md).


# VMware NSX Security

[![PyPI](https://img.shields.io/pypi/v/vmware-nsx-security)](https://pypi.org/project/vmware-nsx-security/) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#readme-license)

English | [中文](detailed-guide-CN.md)

Maintainer: Wei Zhou · [zhouwei008@gmail.com](mailto:zhouwei008@gmail.com)

Community-maintained open-source project; not an official VMware or Broadcom product.

[Overview](#readme-overview) · [Quick Start](#readme-quick-start) · [MCP Configuration](#readme-mcp-configuration) · [Capabilities and Workflows](#readme-capabilities-and-workflows) · [Safety and Audit](#readme-safety-and-audit) · [Troubleshooting](#readme-troubleshooting) · [Companion Skills](#readme-companion-skills) · [Reference](#readme-reference) · [License](#readme-license)

<a id="readme-overview"></a>

## Overview

Runs locally over stdio by default; configure required targets and credentials on your own machine.

VMware NSX DFW microsegmentation and security MCP skill — 22 tools for distributed firewall policies/rules, security groups, VM tags, the DFW exclusion list, Traceflow packet tracing, and IDPS.

> **Companion skills**: [vmware-nsx](https://github.com/vmware-skills/VMware-NSX) (networking), [vmware-aiops](https://github.com/vmware-skills/VMware-AIops) (VM lifecycle), [vmware-monitor](https://github.com/vmware-skills/VMware-Monitor) (monitoring)

MCP uses local stdio by default. Opt-in HTTPS opens the configured listener and requires TLS plus caller authentication; it is a network service, not a local-only mode. Credential examples create owner-only placeholder files without overwriting existing files; edit secrets locally.

Full agent instructions: [`skills/vmware-nsx-security/SKILL.md`](../../../skills/vmware-nsx-security/SKILL.md).

<a id="readme-quick-start"></a>

## Quick Start

Requires Python `>=3.10` and `uv`.

```bash
uv tool install vmware-nsx-security==1.17.4
vmware-nsx-security --help
```

Target, credential and local data setup: [setup guide](../../../skills/vmware-nsx-security/references/setup-guide.md).

<details>
<summary>Installation and configuration details (including offline setup)</summary>

### Quick Start

```bash
uv tool install vmware-nsx-security==1.17.4

mkdir -p ~/.vmware-nsx-security
cp config.example.yaml ~/.vmware-nsx-security/config.yaml
# Edit config.yaml with your NSX Manager host

(
  umask 077
  set -C  # Refuse existing files; edit an existing .env locally instead
  cat > ~/.vmware-nsx-security/.env <<'EOF'
VMWARE_NSX_SECURITY_NSX_PROD_PASSWORD=REPLACE_IN_LOCAL_EDITOR
EOF
)
# Before continuing, edit .env locally; never type live secrets into shell commands.

vmware-nsx-security doctor
```

This writes placeholders only. Enter passwords or tokens using a local editor after creation; do not paste live credentials into terminal commands, chat or commits. If the file exists, the command refuses to overwrite it; edit the existing file after checking its permissions are `600`.

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
pip install --no-index --find-links dist vmware-nsx-security
```


</details>

<a id="readme-mcp-configuration"></a>

## MCP Configuration

Copy this configuration into your MCP client's local stdio settings. The client must be able to find `uvx`; the initial package installation requires access to a package index.

```json
{
  "mcpServers": {
    "vmware-nsx-security": {
      "command": "uvx",
      "args": ["--from", "vmware-nsx-security==1.17.4", "vmware-nsx-security-mcp"],
      "env": {
        "VMWARE_NSX_SECURITY_CONFIG": "~/.vmware-nsx-security/config.yaml"
      }
    }
  }
}
```

The following sections retain preinstalled CLI alternatives and product-specific MCP options.

<details>
<summary>Preinstalled CLI and additional MCP options</summary>

### MCP Server Setup

**After `uv tool install vmware-nsx-security==1.17.4`, start the MCP server with one command** (v1.5.15+):

```bash
# Recommended — single command, no network re-resolve
vmware-nsx-security mcp

# With a custom config path
VMWARE_NSX_SECURITY_CONFIG=/path/to/config.yaml vmware-nsx-security mcp
```

Add to `~/.claude.json`:

```json
{
  "mcpServers": {
    "vmware-nsx-security": {
      "command": "vmware-nsx-security",
      "args": ["mcp"],
      "env": {
        "VMWARE_NSX_SECURITY_CONFIG": "~/.vmware-nsx-security/config.yaml"
      }
    }
  }
}
```

<details>
<summary>Alternative: uvx (no install) or legacy entry point</summary>

```bash
# Run without installing (requires PyPI access each launch)
uvx --from vmware-nsx-security==1.17.4 vmware-nsx-security mcp

# Legacy entry point (still works, kept for backward compatibility)
vmware-nsx-security-mcp
```

> **Behind a corporate TLS proxy?** uvx may fail with `invalid peer certificate: UnknownIssuer`.
> Use the recommended `vmware-nsx-security mcp` form above (no network needed), or set `UV_NATIVE_TLS=true`.

</details>


</details>

<a id="readme-capabilities-and-workflows"></a>

## Capabilities and Workflows

### What It Does

| Category | Tools |
|----------|-------|
| DFW Policy | list, get, create, update, delete, list rules |
| DFW Rules | create, update, delete, stats |
| Security Groups | list, get, create, delete |
| VM Tags | list tags, apply tag, remove tag |
| Traceflow | run trace, get result |
| IDPS | list profiles, signature status + settings |
| DFW Exclusions | list excluded members |

**Total: 22 MCP tools** (11 read-only + 11 write)

#### DFW exclusion list

A VM on the NSX distributed-firewall exclusion list has no DFW in its datapath: the rules that
name it exist and none of them applies. On a VCF estate the management VMs (vCenter, VCF
Operations, NSX managers) are commonly on it — one real NSX 9.1 fabric had 10 of 12 VMs excluded.
`list_dfw_exclusions` shows the list, and `list_vm_tags` / `get_group` / `list_dfw_policies` say
when a member is excluded, so "protected by DFW policy" is never reported for a VM the DFW does
not see. `dfw_excluded: null` means the list could not be read — which is not `false`.

### Common Workflows

#### Microsegment an Application

```bash
# 1. Create groups by tag — via the create_group MCP tool
#    (tag_scope=tier, tag_value=web → matched as Condition value "tier|web";
#     multiple criteria types — tag/IP/segment — are ORed)

# 2. Create DFW policy
vmware-nsx-security policy create web-app-policy --name "Web to App" --category Application
```

#### Tag a VM

```bash
# Find VM and its external ID
vmware-nsx-security tag list my-vm-01

# Apply tag using the external ID
vmware-nsx-security tag apply <external-id> --scope tier --value web
```

#### Trace a Packet

```bash
vmware-nsx-security traceflow run <src-lport-id> \
  --src-ip 10.0.1.5 --dst-ip 10.0.2.10 --proto TCP --dst-port 443
```

Output reports `operation_state` (`IN_PROGRESS`/`FINISHED`/`FAILED`),
hop-by-hop `observations` discriminated by `resource_type` (Dropped*
entries carry `reason` + `acl_rule_id`), and a `dfw_hits` summary.

<a id="readme-safety-and-audit"></a>

## Safety and Audit

### Safety

- **Dependency checks**: Cannot delete a policy with active rules, or a group referenced by DFW or gateway-firewall rules/scopes or by a parent group; group deletion aborts if the reference scan fails
- **Audit logging**: All write ops logged to `~/.vmware-nsx-security/audit.log`
- **Input validation**: IDs validated; all API text sanitized against prompt injection
- **Dry-run mode**: All CLI write commands support `--dry-run`
- **MCP delete preview**: `delete_dfw_policy`, `delete_dfw_rule` and `delete_group` preview by default — without `confirm=True` they return `blast_radius` (what would be removed, `blockers`, `unmeasured`) and delete nothing; `confirm=True` is refused while a blocker remains or a read failed
- **Credential safety**: Passwords only from env vars, never in config files

#### Companion Skills

| Skill | Scope | Tools | Install |
|-------|-------|:-----:|---------|
| **[vmware-aiops](https://github.com/vmware-skills/VMware-AIops)** ⭐ entry point | VM lifecycle, deployment, guest ops, clusters | 49 | `uv tool install vmware-aiops` |
| **[vmware-monitor](https://github.com/vmware-skills/VMware-Monitor)** | Read-only monitoring, alarms, events, VM info | 27 | `uv tool install vmware-monitor` |
| **[vmware-nsx](https://github.com/vmware-skills/VMware-NSX)** | NSX networking: segments, gateways, NAT, IPAM | 33 | `uv tool install vmware-nsx-mgmt` |
| **[vmware-storage](https://github.com/vmware-skills/VMware-Storage)** | Datastores, iSCSI, vSAN | 11 | `uv tool install vmware-storage` |
| **[vmware-vks](https://github.com/vmware-skills/VMware-VKS)** | Tanzu Namespaces, TKC cluster lifecycle | 20 | `uv tool install vmware-vks` |
| **[vmware-aria](https://github.com/vmware-skills/VMware-Aria)** | Aria Ops metrics, alerts, capacity planning | 28 | `uv tool install vmware-aria` |

### Remote access (HTTPS) and limiting tools

By default `vmware-nsx-security mcp` speaks stdio to one local client and offers every tool. Two options change that
(vmware-policy ≥ 1.21.0).

**Serve over HTTPS** so clients on other machines can connect. Every caller needs a bearer token:

```bash
vmware-audit token create alice          # prints the token once; give it to alice
vmware-audit token list                  # names only
vmware-audit token revoke alice          # refused from its next request, no restart
vmware-nsx-security mcp --transport https --host 0.0.0.0 --port 8443 \
    --cert /etc/vmware-mcp/server.pem --key /etc/vmware-mcp/server-key.pem \
    --public-name mcp.example.com
```

Connect a client (Claude Code shown; any MCP client that supports streamable HTTP and custom headers works):

```bash
claude mcp add --transport http vmware-nsx-security https://mcp.example.com:8443/mcp \
    --header "Authorization: Bearer $VMWARE_MCP_TOKEN"
```

```json
{
  "mcpServers": {
    "vmware-nsx-security": {
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
- The audit log records each caller as `token:<name>`. Calls run side by side, with or without a target: each
  target keeps up to `VMWARE_MCP_POOL_SIZE` sessions (default 2), and each session is a login on the target. A call
  that finds them all busy waits at most 300 s for one.
- **Everyone who can reach the endpoint acts with this server's account.** Tokens identify callers; they grant
  nothing on the platform. Run one endpoint per privilege level.
- **Several people or roles on one endpoint:** run `vmware-audit roles enable` once, then give each token a role (`vmware-audit token create NAME --role reader`, or a role in `roles.yaml` naming tools and targets; vmware-policy ≥ 1.24.0). A role limits what the token may call on this endpoint; it cannot grant more than the account has. See vmware-policy's README, "Roles for network callers".

**Offer only read tools, plus the writes you choose:**

```bash
vmware-nsx-security mcp --expose read --allow-write apply_vm_tag
# or: VMWARE_NSX_SECURITY_MCP_EXPOSE=read VMWARE_NSX_SECURITY_MCP_ALLOW_WRITE=apply_vm_tag vmware-nsx-security mcp
```

Tools not offered do not appear in the client's tool list. A bad value or an unknown write tool stops the server
(exit 2). This limits what clients are offered; it is not authorization, so the account itself should be
least-privilege.

Details: `skills/vmware-nsx-security/references/setup-guide.md` ("Serving MCP over HTTPS", "Limiting which tools are offered").

<a id="readme-troubleshooting"></a>

## Troubleshooting

### System proxy bypass

The NSX Manager REST client honors the operating system proxy bypass list for the configured origin.
TLS verification still follows `verify_ssl`, and CA environment settings such as `SSL_CERT_FILE` remain active.
Other origins retain their normal proxy routing.

<a id="readme-companion-skills"></a>

## Companion Skills

The VMware Skills family contains 14 MCP servers and the shared Policy library. Choose tools by responsibility: [vmware-skills](https://github.com/vmware-skills).

<a id="readme-reference"></a>

## Reference

Release history: [RELEASE_NOTES.md](../../../RELEASE_NOTES.md).

Read-only self-test with your own model and agent host: [model-fit self-test](https://github.com/vmware-skills/marketplace/blob/main/MODEL_FIT_SELF_TEST.md).

### Version Compatibility

| NSX Version | Support | Notes |
|-------------|---------|-------|
| NSX 9.1 / VCF 9.1 | ✅ Full | DFW + Security Group + Traceflow + IDS/IPS via Policy API. VDS 7.0+ required (N-VDS removed in NSX 9). |
| NSX 9.0 / VCF 9.0 | ✅ Full | Same as 9.1. Bare-metal NSX agent removed. |
| NSX 4.x / VCF 5.x | ✅ Full | All features supported. |
| NSX-T 3.2 / VCF 4.5 | ✅ Full | Policy API stable. |

##### Official Broadcom References

- **SDKs**: <https://developer.broadcom.com/sdks> — VMware NSX for Python SDK (future migration target)
- **REST APIs**: <https://developer.broadcom.com/xapis> — NSX-T Data Center REST API
- **CLI Tools**: <https://developer.broadcom.com/tools> — VCF PowerCLI 9.1

<!-- usage: remote-and-exposure -->

<a id="readme-license"></a>

## License

MIT
