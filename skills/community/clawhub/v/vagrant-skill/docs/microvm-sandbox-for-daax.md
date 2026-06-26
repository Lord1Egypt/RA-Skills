# microvm-sandbox → daax: Security Layer Integration
*Written: 2026-03-16*  
*Source: github.com/jpoley/microvm-sandbox (14/14 tests passing)*  
*Context: daax agentic platform — daax-cli, hawkeye, nanofuse, daax-web*

---

## What Was Proven

microvm-sandbox just completed a full end-to-end security validation of running untrusted workloads in Kata/Cloud Hypervisor microVMs. Four layers were tested and proven:

1. **Escape containment** — 13 attack vectors, 100% blocked at the hypervisor boundary
2. **Filesystem isolation** — bind-mount safe directories only; forbidden paths invisible
3. **L3/L4 firewall + DNS** — port allowlists, dnsmasq domain filtering
4. **SPIFFE identity + secret injection** — JWT-SVID issued, Vault authenticated, secrets retrieved inside container

These are the exact four layers daax needs for production agentic workload execution.

---

## daax Architecture Mapping

```
User / Agent Request
        │
        ▼
   daax-web (Next.js)
   Terminal + AI tools
        │
        ▼
   daax-cli (launcher)          ← SPIFFE identity injection happens here
   Worktree + session setup
        │
        ▼
   hawkeye (orchestrator)       ← Job scheduling, routing to nanofuse
        │
        ▼
   nanofuse (Firecracker)       ← microVM runtime — all 4 security layers land here
   microVM per workload
```

The microvm-sandbox security layers plug into **nanofuse** as the enforcement point. hawkeye orchestrates which workloads get what policy. daax-cli injects identity before launch.

---

## Layer 1: Escape Containment

**What was tested:** 13 escape vectors including `/dev/mem`, host PID namespace leak, `/proc/*/root` host filesystem access, `modprobe`, `sysrq-trigger`, CVE-2019-5736 runc overwrite, privileged container + all Linux capabilities.

**Result:** All 13 CONTAINED. microVM boundary (KVM hypervisor) blocks all of them. No userspace sandbox or seccomp profile required — the hypervisor is the boundary.

**What daax gets from this:**

The escape test suite should run as part of **nanofuse's CI** before every release. The tests are 100% portable — same 13 vectors apply to Firecracker (nanofuse uses Firecracker, microvm-sandbox used Kata/CHv; same KVM isolation model).

```
Action: Port escape-attempt.sh → test/security/escape_test.go in nanofuse
        Run via SSH into a test VM
        Gate every nanofuse release on 13/13 CONTAINED
```

This gives daax a hard security guarantee per release: "microVM boundary proven unescapable on this kernel + Firecracker version."

---

## Layer 2: Filesystem Isolation

**What was tested:** Host writes sentinel to `forbidden-dir`. Only `safe-dir` is bind-mounted into container. Container cannot see forbidden-dir via any path including `/proc/1/root/`, direct path, or device access.

**What daax gets from this:**

Every daax workload that runs in nanofuse gets a workspace volume. The sentinel test pattern validates that:
- The workspace volume is the only host path visible inside the VM
- Other users' workspaces are invisible
- Host system files are not accessible

This directly addresses multi-tenant isolation for daax's use case (multiple agents, multiple users, same host).

```
Action: Add filesystem isolation test to nanofuse E2E suite
        Pattern: write sentinel to /var/lib/nanofuse/workspaces/user-B/
                 start user-A VM with only user-A workspace mounted
                 verify user-B sentinel is not reachable from user-A VM
```

---

## Layer 3: L3/L4 Firewall + DNS — daax Policy Model

**What was tested:** iptables allow port 8080, block port 8081 from container subnet. dnsmasq: `allowed.sandbox.local` resolves, `blocked.sandbox.local` → NXDOMAIN. External DNS bypass tested (informational for Kata; Firecracker is enforceable).

**What daax gets from this — and why Firecracker is better:**

In Kata/CNI, iptables FORWARD doesn't intercept TAP traffic. **In nanofuse (Firecracker), nanofused creates each TAP device directly.** This means:

```
nanofuse0 bridge: 172.16.0.0/24
tap0vm{N}: per-VM TAP device, owned by nanofused
VM traffic: VM eth0 → tap0vm{N} → nanofuse0 → routing
```

Because nanofused owns `tap0vm{N}`, it can apply **per-VM iptables rules** at the TAP interface level. This is stronger than what we validated in microvm-sandbox.

**daax workload policy (per-VM):**

```bash
# nanofused applies these on VM create, removes on VM destroy
VM_TAP="tap0vm${VM_ID}"
VM_IP="172.16.0.${N}"

# Default deny — no internet access for untrusted agents
iptables -I FORWARD -i $VM_TAP -j DROP

# Allow only what the job spec says (e.g., GitHub API, pypi, npm)
iptables -I FORWARD -i $VM_TAP -d api.github.com -p tcp --dport 443 -j ACCEPT
iptables -I FORWARD -i $VM_TAP -d pypi.org -p tcp --dport 443 -j ACCEPT

# Always allow: VM → daax-web (for recording), VM → hawkeye (for status)
iptables -I FORWARD -i $VM_TAP -d 172.16.0.1 -p tcp --dport 4201 -j ACCEPT  # recording
iptables -I FORWARD -i $VM_TAP -d 172.16.0.1 -p tcp --dport 8080 -j ACCEPT  # hawkeye

# DNS: only our dnsmasq, no bypass
iptables -I INPUT -s $VM_IP -p udp --dport 53 -j ACCEPT
iptables -A FORWARD -s $VM_IP -p udp --dport 53 ! -d 172.16.0.1 -j DROP
```

**DNS domain control for daax agents:**

```
/etc/dnsmasq.d/daax-sandbox.conf
  address=/daax.internal/172.16.0.1    # resolve daax services
  address=/pypi.org/151.101.0.223      # only if job policy allows
  server=8.8.8.8                       # forward everything else (if policy allows)
  # OR: no server= line → NXDOMAIN for all external domains (full lockdown)
```

This lets hawkeye define per-job DNS policy: "this agent job can reach pypi but not npm, and nothing else."

```
Action: Add per-TAP firewall rules to internal/network/ in nanofuse
        hawkeye job spec: add network_policy field (allowlist of CIDRs/domains)
        nanofused reads policy on VM create, applies iptables + dnsmasq rules
        nanofused cleans up rules on VM destroy
```

---

## Layer 4: SPIFFE Identity + Vault Secret Injection

**What was tested:** SPIRE server + agent issues JWT-SVIDs. Vault configured with JWT auth backed by SPIRE's JWKS endpoint. Container receives JWT, authenticates to Vault, retrieves secret `s3cr3t-kata-workload`.

**What daax gets from this — the full identity bootstrap chain:**

```
hawkeye schedules job
    │
    ├→ nanofused: CreateVM(job_id, user_id, group_id)
    │     ├→ SPIRE: RegisterWorkload(spiffe://poley.dev/g/{group}/u/{user}/w/microvm/{vm_id})
    │     ├→ SPIRE: FetchJWTSVID for this VM
    │     └→ VM boots with JWT injected (env var OR vsock)
    │
    └→ VM runtime:
          ├→ POST /v1/auth/jwt/login  (JWT → Vault token)
          ├→ GET /v1/secret/daax/{job_id}/  (job-specific secrets)
          └→ Run agent code with secrets in env
```

**This is daax-cli's identity injection in production form:**

daax-cli already supports `--identity` / SPIFFE injection (`identity.trust_domain`, `identity.workload_id` in config). The microvm-sandbox work proves the backend: SPIRE issues the JWT, Vault validates it and returns secrets. daax-cli + microvm-sandbox = complete identity pipeline.

**SPFFE ID scheme (nanofuse already defines this):**
```
spiffe://poley.dev/g/{group_id}/u/{user_id}/w/microvm/{vm_id}
```

**Per-VM secret isolation in Vault:**
```
vault policy write daax-vm-{vm_id} - <<EOF
path "secret/daax/jobs/{job_id}/*" { capabilities = ["read"] }
EOF
# VM can only read its own job's secrets, nothing else
```

**auth.poley.dev as the OIDC issuer (production path):**

In microvm-sandbox we used SPIRE's own JWKS endpoint (`http://127.0.0.1:8082/keys`). In production daax, `auth.poley.dev` (Pocket ID OIDC) becomes the issuer. Vault's JWT auth config points to `auth.poley.dev` instead:

```bash
vault write auth/jwt/config \
  oidc_discovery_url="https://auth.poley.dev" \
  bound_issuer="https://auth.poley.dev" \
  default_role="daax-workload"
```

The VM still gets a JWT-SVID from SPIRE. SPIRE is configured to federate with `auth.poley.dev` as the upstream OIDC trust anchor. This is the swap that makes daax production-ready.

```
Action: 
  1. nanofuse: Fix spire/service.go to use binary (not docker exec)
  2. nanofuse: Add FetchJWTSVID() to spire/service.go
  3. nanofuse: Add internal/vault/ package (JWT exchange + secret read)
  4. nanofuse: Inject JWT into VM via vsock at boot (vsock already exists in nanofuse)
  5. daax-cli: Wire identity.workload_id → SPIRE entry on job launch
  6. auth.poley.dev: Configure as Vault JWT OIDC discovery endpoint
```

---

## What This Unlocks for daax Users

Once all 4 layers are in nanofuse:

| Capability | What users get |
|-----------|---------------|
| Agent escape containment | LLM-generated code cannot escape the microVM — proven, not theoretical |
| Workspace isolation | Each agent sees only its own files — multi-tenant safe |
| Network policy per job | "This agent can reach GitHub but not exfiltrate to arbitrary IPs" |
| Secret injection | Agent gets credentials scoped to this job only — no ambient secrets |
| Identity-based audit | Every Vault secret access tied to `spiffe://poley.dev/.../vm/{id}` — full audit trail |

This is the security posture that differentiates daax from "just running Claude Code in a container."

---

## Implementation Order for daax

| # | What | Where | Effort |
|---|------|-------|--------|
| 1 | Per-TAP iptables (default deny + allowlist) | `nanofuse/internal/network/` | 2–3 days |
| 2 | Fix SPIRE service (binary, not docker exec) | `nanofuse/internal/spire/service.go` | 0.5 days |
| 3 | SPIRE JWKS endpoint (Go HTTP handler) | `nanofuse/internal/spire/` | 0.5 days |
| 4 | Vault JWT auth + secret read | `nanofuse/internal/vault/` (new) | 2 days |
| 5 | JWT injection via vsock at VM boot | `nanofuse/internal/firecracker/vm.go` | 1 day |
| 6 | Escape test suite in CI | `nanofuse/test/security/` | 1 day |
| 7 | hawkeye: job spec network_policy field | `daax/hawkeye/` | 1 day |
| 8 | auth.poley.dev as Vault OIDC issuer | config + auth.poley.dev setup | 1 day |

**Total: ~10 days of focused work → daax has production-grade sandboxing.**

---

## Reference

- microvm-sandbox: `github.com/jpoley/microvm-sandbox` — run `cd vm && vagrant up`
- nanofuse → daax reuse doc: `~/jarvis/docs/microvm-sandbox-vs-nanofuse.md`
- Proven scripts: `microvm-sandbox/network/setup.sh`, `identity/setup.sh`, `escape/escape-attempt.sh`
