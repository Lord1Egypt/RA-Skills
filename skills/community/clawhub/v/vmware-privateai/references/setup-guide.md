# vmware-privateai — Setup Guide

> **Disclaimer**: Community-maintained open-source project, **not affiliated with, endorsed by, or
> sponsored by VMware, Inc., Broadcom Inc., or NVIDIA Corporation.** "VMware", "vSphere", and "VCF" are
> trademarks of Broadcom; "NVIDIA" and "vGPU" are trademarks of NVIDIA. Source is publicly auditable
> under the MIT license.

Install, credential, and MCP-client configuration for vmware-privateai, plus the Security section.

## 1. Install

```bash
uv tool install vmware-privateai==2.5.3       # isolated tool env; puts vmware-privateai on PATH
vmware-privateai version
```

Requires Python 3.11+ (the MCP server is reflected by FastMCP/Pydantic; older interpreters can raise on
PEP 604 unions — 踩坑 #33). Runtime deps: pyvmomi, httpx, typer, rich, pyyaml, python-dotenv, mcp, and
`vmware-policy` (the family audit/policy harness, installed automatically).

## 2. Configure targets

Create `~/.vmware-privateai/config.yaml`:

```yaml
targets:
  - name: vc-prod
    host: vcenter-prod.example.com
    username: administrator@vsphere.local   # optional; env var overrides this
    type: vcenter                            # or esxi
    port: 443
    verify_ssl: true
    environment: production                  # optional label for policy scoping

# Optional — only needed for the pais model-list / kb-list tools:
pais:
  endpoint: https://pais.example.com         # base URL; the /api/v1 prefix is added by the client
  verify_ssl: true
```

The first target is the default (used when `--target` / the `target` MCP arg is omitted).

## 3. Credentials — never in config files

Passwords and the PAIS bearer token live only in `~/.vmware-privateai/.env`:

```bash
mkdir -p ~/.vmware-privateai
(
  umask 077
  set -C  # Refuse existing files; edit an existing .env locally instead
  cat > ~/.vmware-privateai/.env <<'EOF'
VMWARE_PRIVATEAI_VC_PROD_PASSWORD=REPLACE_IN_LOCAL_EDITOR
VMWARE_PRIVATEAI_PAIS_TOKEN=REPLACE_IN_LOCAL_EDITOR
EOF
)
# Before continuing, edit .env locally; never type live secrets into shell commands.
```

This writes placeholders only. Enter passwords or tokens using a local editor after creation; do not paste live credentials into terminal commands, chat or commits. If the file exists, the command refuses to overwrite it; edit the existing file after checking its permissions are `600`.

- **Per-target password**: `VMWARE_PRIVATEAI_<TARGET>_PASSWORD`, where `<TARGET>` is the target `name`
  upper-cased with `-` replaced by `_` (so target `vc-prod` → `VMWARE_PRIVATEAI_VC_PROD_PASSWORD`).
- **Optional username override**: `VMWARE_PRIVATEAI_<TARGET>_USERNAME` wins over `config.yaml` (resolved
  together with the password on every call, so a rotating sidecar never splits the pair).
- **PAIS token**: `VMWARE_PRIVATEAI_PAIS_TOKEN` — a short-lived OIDC/OAuth2 bearer token from your
  Identity Provider (the PAIS API uses `Authorization: Bearer <token>`). It is a secret and is
  obfuscated to `b64:` at rest exactly like a password.
- **Secret manager**: any of these vars can be injected from Vault / CyberArk / AWS Secrets Manager /
  a Kubernetes Secret instead of `.env` — the code reads the environment either way.

On load, plaintext `*_PASSWORD` / `*_TOKEN` values in `.env` are auto-rewritten to grep-safe `b64:`
form (obfuscation, not encryption — it defeats casual grep / shoulder-surfing, not a determined reader).

## 4. MCP client configuration

Preferred (installed console script — no `uvx` network re-resolve, works through enterprise TLS
proxies, 踩坑 #25):

```json
{
  "mcpServers": {
    "vmware-privateai": {
      "command": "vmware-privateai",
      "args": ["mcp"],
      "env": { "VMWARE_PRIVATEAI_CONFIG": "~/.vmware-privateai/config.yaml" }
    }
  }
}
```

Fallback (`uvx` — re-resolves from PyPI each start; if your network runs a TLS MitM proxy, add
`"UV_NATIVE_TLS": "true"` to `env`):

```json
{
  "mcpServers": {
    "vmware-privateai": {
      "command": "uvx",
      "args": ["--from", "vmware-privateai==2.5.3", "vmware-privateai-mcp"],
      "env": { "VMWARE_PRIVATEAI_CONFIG": "~/.vmware-privateai/config.yaml" }
    }
  }
}
```

This layout works with any MCP-compatible client (Claude Desktop, Claude Code, Goose, etc.).

## Limiting which tools are offered

By default the MCP server offers every tool. To offer only read tools, start it with `--expose read`, or set
`VMWARE_PRIVATEAI_MCP_EXPOSE=read` in the MCP client's `env` block (useful when the client launches `vmware-privateai mcp` itself). To offer
chosen write tools as well, add `--allow-write` with a comma-separated list (or `VMWARE_PRIVATEAI_MCP_ALLOW_WRITE`):

```bash
vmware-privateai mcp --expose read --allow-write assign_vgpu
```

- A read tool is one annotated `readOnlyHint: true`; every other tool counts as a write.
- An unknown setting, or a name that is not a write tool of this server, stops the server before it serves (exit
  code 2), so it never offers more than you asked for. Pre-2.0 tool names are accepted.
- With `--expose read`, the server prints one line to stderr saying what it exposes.
- Flags and environment variables are not mixed: if either flag is given, both environment variables are
  ignored, so a leftover `_ALLOW_WRITE` in the shell cannot widen `--expose read`. A blank flag value counts as
  not given.
- A tool that runs other steps (a plan, workflow or batch tool) carries every write it can execute, including
  writes this setting hides. Expose such a tool only if you would expose those writes too.
- A launcher that imports the server object can call
  `vmware_policy.exposure.restrict_tools(mcp, skill="privateai", expose="read", allow_write=[...])` before running it,
  instead of editing the SDK's tool registry.
- This limits what clients are offered. It is **not** authorization: whether a call may change anything is decided by
  the account's permissions, and deny rules in `~/.vmware/rules.yaml` still apply to every exposed tool.
- An agent that can run shell commands can also reach the platform without MCP (SSH, curl, govc, PowerCLI). So
  the service account itself must be least-privilege: exposure and deny rules are guardrails, not the boundary.

## Serving MCP over HTTPS

By default the MCP server speaks stdio to one local client. To let clients on other machines reach it, serve it over
HTTPS. Every caller then needs a bearer token.

```bash
vmware-audit token create alice                      # prints the token once; give it to alice
vmware-privateai mcp --transport https --host 0.0.0.0 --port 8443 \
    --cert /etc/vmware-mcp/server.pem --key /etc/vmware-mcp/server-key.pem \
    --public-name mcp.example.com
```

- Clients connect to `https://mcp.example.com:8443/mcp` and send `Authorization: Bearer <token>`.
- `--public-name` lists every host name clients use (comma-separated); requests for any other Host or Origin are
  refused. Use a certificate your clients trust for those names.
- Behind a reverse proxy that terminates TLS (Nginx, HAProxy) on the same machine, use
  `--transport http --host 127.0.0.1 --public-name mcp.example.com` (the names the proxy forwards in `Host`), and
  have the proxy pass the `Authorization` header through.
- Behind a load balancer or gateway on another machine, keep `--transport https` (a self-signed certificate is
  fine: the balancer is the client that has to trust it), list in `--public-name` the host name the balancer sends
  as `Host`, and have it forward `Authorization`. Point its health probe at `GET /healthz`: it needs no token, returns
  only `{"status": "ok"}` and accepts any `Host` (vmware-policy ≥ 1.23.0). Every other path still needs the token.
- Correlation: each audit row stores the caller's `traceparent` trace-id, else its `X-Request-ID` /
  `X-Correlation-ID`. Have the agent platform send one, and `vmware-audit log --correlation-id ID` lists the calls
  behind one platform request.
- Tools that read or write files on this server (here: `verify_pais_bundle` manifests) never touch its configuration, tokens, audit log or
  TLS key, and over the network they are off unless `VMWARE_MCP_FILE_ROOT` names a directory for them
  (vmware-policy ≥ 1.23.1).
- `vmware-audit token list` / `token revoke NAME` manage callers; a revoked token is refused from its next request.
  Replace a leaked token under a new name.
- The server will not start without at least one token, and checks before it binds that unauthenticated requests
  are refused.
- Each audit row records the caller as `token:<name>`. Calls run side by side, also on the same target: the server keeps up to `VMWARE_MCP_POOL_SIZE` (default 2) sessions per target, each one a login on that target, and a call waits at most 300 s for a free session (vmware-policy ≥ 1.22.0).
- **Everyone who can reach the endpoint acts with this server's account.** Tokens identify callers; they grant
  nothing on the platform. Run one endpoint per privilege level (for example a read-only account behind
  `--expose read`, and a separate endpoint for operators).
- **Several people or roles on one endpoint:** run `vmware-audit roles enable` once, then give each token a role (`vmware-audit token create NAME --role reader`, or a role in `roles.yaml` naming tools and targets; vmware-policy ≥ 1.24.0). A role limits what the token may call on this endpoint; it cannot grant more than the account has. See vmware-policy's README, "Roles for network callers".

## 5. Verify

```bash
vmware-privateai gpu host-list             # lists hosts that have a GPU
vmware-privateai vgpu profile-list         # the assignable vGPU profile catalog
vmware-privateai pais model-list           # PAIS served models (if configured)
```

A teaching error here names exactly what to fix (missing password, unresolvable host, TLS, missing PAIS
endpoint/token) — follow the message.

## Security

> **Disclaimer**: not affiliated with, endorsed by, or sponsored by VMware, Inc., Broadcom Inc., or
> NVIDIA Corporation. See the full policy in the repo-root `SECURITY.md`.

1. **Source Code** — https://github.com/vmware-skills/VMware-PrivateAI (MIT), publicly auditable.
2. **Config File Contents** — `config.yaml` holds only target host/username/port and the
   `pais.endpoint`. No passwords, no tokens. Secrets live in `~/.vmware-privateai/.env` (chmod 600,
   `b64:` obfuscated at rest).
3. **Webhook Data Scope** — none. No webhooks and no outbound network calls except to the configured
   vCenter/ESXi targets and the PAIS endpoint.
4. **TLS Verification** — on by default. `verify_ssl: false` (per target) and `pais.verify_ssl: false`
   are intended only for self-signed lab certificates.
5. **Prompt Injection Protection** — all vSphere-supplied and PAIS-supplied text (device / vendor / VM
   / vGPU-profile names, PAIS model ids, and knowledge-base descriptions — the highest-value injection
   surface here) passes through `vmware_policy.sanitize()` (≤500-char truncation + C0/C1 control-char
   stripping) before it reaches the model.
6. **Least Privilege** — read-vs-write authorization is delegated to the vCenter service account's RBAC
   role: a read-only account refuses `assign_vgpu`'s ReconfigVM at vCenter, un-bypassably (the one place
   the control cannot be stepped around by a shell). Recommend a dedicated service account scoped to the
   GPU clusters. All writes are recorded to `~/.vmware/audit.db` (and the CLI companion
   `~/.vmware-privateai/audit.log`).

### Static analysis

```bash
uvx bandit==1.9.4 -r vmware_privateai/            # target: 0 Medium+ issues
```
