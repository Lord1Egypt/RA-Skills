# microvm-sandbox → nanofuse: Reuse Analysis
*Written: 2026-03-16*  
*Source: microvm-sandbox eval (github.com/jpoley/microvm-sandbox)*  
*Target: nanofuse (github.com/peregrinesummit/nanofuse)*

---

## TL;DR

microvm-sandbox proved out 4 security layers (escape containment, filesystem isolation, L3/L4 firewall + DNS, SPIFFE + Vault) against a Kata/Cloud Hypervisor stack. nanofuse is Firecracker-based but shares the same fundamentals. **5 of the 6 components are directly reusable** — one (DNS bypass enforcement) is actually *easier* in nanofuse because Firecracker's TAP networking is more controllable than Kata's.

---

## Architecture Comparison

| Dimension | microvm-sandbox | nanofuse |
|-----------|----------------|---------|
| Hypervisor | Kata Containers (wraps CHv/FC) | Firecracker directly (Jailer) |
| OCI interface | containerd / nerdctl | Custom daemon (nanofused) |
| Network bridge | 10.4.0.0/24 (CNI) | 172.16.0.0/24 (nanofuse0) |
| Language | Bash scripts | Go |
| SPIRE | Working setup (server+agent+JWKS) | Partial (spire/service.go, CLI-only) |
| Firewall | iptables ACCEPT/REJECT by port | Not implemented (future-fw.md exists) |
| DNS control | dnsmasq (allow/block domains) | Not implemented |
| Escape tests | 13 vectors, all contained | Not implemented |
| Identity → secrets | SPIFFE JWT → Vault KV | Not implemented |
| Test automation | `vagrant up` → all tests | Ad-hoc E2E scripts |

---

## Component-by-Component Reuse

---

### 1. Escape Test Suite → nanofuse Integration Tests

**Status in nanofuse:** Absent. No escape testing exists.  
**Status in microvm-sandbox:** 13 vectors, 100% contained, automated.

**What to port:**

The `escape-attempt.sh` test logic should become nanofuse's security regression test suite. Every vector that was verified contained in Kata applies equally to Firecracker — Firecracker's isolation model is the same (separate kernel + KVM hypervisor boundary).

| Vector | Test in microvm-sandbox | nanofuse equivalent |
|--------|------------------------|-------------------|
| PID namespace | `/proc/1/comm` ≠ host systemd | Same test in VM console |
| Host filesystem | Sentinel file not visible via `/proc/*/root` | Mount a sentinel file host-side, check from VM |
| `/dev/mem` / `/dev/kmem` | `dd if=/dev/mem` blocked | Same |
| Block device | No host disk visible | Same — Firecracker presents only virtual vda |
| `modprobe` | Blocked | Same — Firecracker doesn't expose module loading |
| CVE-2019-5736 | Host jailer binary not visible | Even stronger in Firecracker: jailer runs as separate UID |
| Network namespace | No virbr0/docker0 visible | Same — TAP device only |
| `sysrq-trigger` | Blocked | Same |
| Privileged caps scope | All caps scoped to guest VM | Same — SYS_ADMIN in VM can't reach host |

**Action:** Create `test/escape/` in nanofuse — Go test file that SSHs into a running VM and executes each escape vector. Can reuse the bash logic verbatim as a heredoc or embedded script.

---

### 2. SPIRE Configuration → Replace Docker Exec with Direct Binary

**Status in nanofuse:** `internal/spire/service.go` exists but uses `docker exec <container> spire-server entry create` — couples SPIRE to a running Docker container. No JWKS endpoint. No Vault integration.  
**Status in microvm-sandbox:** Working SPIRE server + agent (binaries, not containers), JWKS HTTP endpoint, Vault JWT auth backed by SPIRE bundle.

**What's directly reusable:**

```
microvm-sandbox/identity/setup.sh → nanofuse SPIRE bootstrap script
```

Key config patterns:
- SPIRE server trust domain: `sandbox.local` → `poley.dev` (nanofuse already uses this)
- SPIRE server bind port: 8083 (avoid conflicts)
- Agent join token flow: works cleanly without Docker
- Workload entry format: `spiffe://poley.dev/g/{group}/u/{user}/w/microvm/{vm-id}` (nanofuse's own SPIFFE ID scheme)
- JWKS endpoint: Python HTTP server exposing `spire-server bundle show -format jwks` — enables Vault JWT auth

**nanofuse's existing `spire/service.go`:**
- `BuildSPIFFEID` — good, keep as-is
- `RegisterWorkload` — currently calls `docker exec spire-server ...` — replace with `exec.Command("/opt/spire/bin/spire-server", "entry", "create", ...)` pointing at the binary directly
- Missing: `FetchJWTSVID` method (fetches JWT-SVID from workload socket for injection into VMs)

**Add to nanofuse spire/service.go:**
```go
// FetchJWTSVID fetches a JWT-SVID for the given SPIFFE ID to inject into a microVM.
// Uses spire-agent CLI: spire-agent api fetch jwt -audience vault -socketPath <sock>
func (s *Service) FetchJWTSVID(ctx context.Context, audience string) (string, error)
```

---

### 3. Vault JWT Auth → Secret Injection Pipeline

**Status in nanofuse:** Not implemented. No secret injection into VMs.  
**Status in microvm-sandbox:** Working end-to-end — SPIFFE JWT → Vault auth → KV secret retrieved inside container.

**The pattern (directly applicable to nanofuse):**

```
nanofused creates VM
  → SPIRE RegisterWorkload for this VM's SPIFFE ID
  → Fetch JWT-SVID on host (FetchJWTSVID)
  → Pass JWT as env var OR write to vsock at boot
  └→ VM bootstraps: uses JWT to call Vault API
       → Gets Vault token
       → Reads secrets for this workload
```

**Vault setup from microvm-sandbox (verbatim for nanofuse):**
```bash
vault auth enable jwt
vault write auth/jwt/config \
  jwks_url="http://127.0.0.1:8082/keys" \
  bound_issuer="http://127.0.0.1:8082" \
  default_role="nanofuse-workload"

vault write auth/jwt/role/nanofuse-workload \
  role_type="jwt" \
  bound_subject="spiffe://poley.dev/..." \
  bound_audiences="TESTING" \
  user_claim="sub" \
  policies="nanofuse-workload"
```

**Where to put this in nanofuse:** `scripts/dev-vault-setup.sh` + document in `docs/VAULT_INTEGRATION.md`. The Go side goes in a new `internal/vault/` package (client + token exchange).

---

### 4. Network Firewall (iptables) → **BETTER in nanofuse than in microvm-sandbox**

**Status in nanofuse:** Not implemented. `future-fw.md` documents the need.  
**Status in microvm-sandbox:** Working for L3/L4 (port allow/reject) but DNS bypass via 8.8.8.8 was NOT enforceable because Kata TAP networking bypasses host FORWARD chain.

**Why nanofuse can do better:**

Nanofuse directly controls the TAP device for each Firecracker VM. The TAP device (`tap0vmX`) is created by nanofused. Traffic from the VM goes:
```
VM eth0 → tap0vmX (host) → nanofuse0 bridge → routing
```

Because nanofuse controls the TAP creation, it can apply **per-VM iptables rules** anchored to the TAP interface, which is *not possible* with Kata's CNI-managed TAP devices.

**Rules to port from microvm-sandbox/network/setup.sh:**

```bash
# Per-VM firewall (replace subnet rule with per-TAP interface rule)
VM_TAP="tap0vm${VM_ID}"
VM_IP="172.16.0.${N}"

# Allow specific ports
iptables -I FORWARD -i $VM_TAP -p tcp --dport 443 -j ACCEPT
iptables -I FORWARD -i $VM_TAP -p tcp --dport 80 -j ACCEPT

# Block everything else from this VM
iptables -A FORWARD -i $VM_TAP -j DROP

# DNS: only allow VM to reach our dnsmasq
iptables -I INPUT -s $VM_IP -p udp --dport 53 -j ACCEPT
iptables -I FORWARD -s $VM_IP -p udp --dport 53 ! -d 172.16.0.1 -j DROP
```

This gives nanofuse true per-VM L3/L4 policy — each VM has its own allowlist. This was the limitation in microvm-sandbox (Kata shares a CNI bridge).

**dnsmasq config from microvm-sandbox is directly portable:**
- Allow list: `address=/allowed.example/172.16.0.1`
- Block list: `address=/blocked.example/` (NXDOMAIN)
- Forward everything else to 8.8.8.8

---

### 5. Filesystem Isolation Pattern → Volume Mount Validation

**Status in nanofuse:** Volume mounts exist but no enforcement tests.  
**Status in microvm-sandbox:** Proven — safe-dir mounted, forbidden-dir not visible, proc-escape via sentinel blocked.

**Direct application to nanofuse:**

When nanofused mounts a workspace volume into a Firecracker VM (via virtio-blk or virtiofs), the same test pattern applies:
1. Write a sentinel to a forbidden path on the host (not in any mount spec)
2. Start the VM
3. Verify VM cannot see the sentinel via any path (`/proc/1/root/...`, direct path, etc.)

The sentinel file approach from `escape/run-escape-tests.sh` + `filesystem/test.sh` should become part of nanofuse's `test/` directory.

---

### 6. Vagrant Test Harness → nanofuse CI Environment

**Status in nanofuse:** CI uses GitHub Actions (`.github/workflows/ci.yaml`). Local dev is complex. No nested KVM env.  
**Status in microvm-sandbox:** `vagrant up` → full nested KVM environment, all tests, single command.

**What nanofuse gets from this pattern:**

The `vm/Vagrantfile` config (nested KVM, host-passthrough, 4 vCPU, 4GB RAM) is exactly what nanofuse needs for local E2E testing of Firecracker. Currently there's no documented way to run nanofuse E2E tests locally without a bare-metal machine.

**Add to nanofuse:** `dev/Vagrantfile` using the same bento/ubuntu-24.04 + host-passthrough config, with nanofuse's setup script as the provisioner. This gives every developer a one-command local environment.

---

## Priority Order for nanofuse

Ranked by impact:

| Priority | Component | Effort | Impact |
|----------|-----------|--------|--------|
| 🔴 1 | **L3/L4 firewall (per-TAP)** | Medium (port iptables rules to Go in network package) | Security-critical, blocks production use |
| 🔴 2 | **Escape test suite** | Low (port bash → Go/SSH) | No security regression coverage today |
| 🟡 3 | **SPIRE binary (drop Docker exec)** | Low (change exec path in service.go) | Makes SPIRE usable without Docker |
| 🟡 4 | **SPIRE JWKS endpoint** | Low (add Python script or Go HTTP handler) | Enables Vault JWT auth |
| 🟡 5 | **Vault JWT auth + secret injection** | Medium (new internal/vault package) | Core daax use case |
| 🟢 6 | **DNS filtering (dnsmasq)** | Low (port setup.sh config to nanofused setup) | Important for multi-tenant isolation |
| 🟢 7 | **Vagrant dev environment** | Low (copy Vagrantfile, add nanofuse provisioner) | Dev quality of life |

---

## What microvm-sandbox Does NOT Cover for nanofuse

Things nanofuse needs that weren't in scope for the eval:

1. **Snapshot/resume** (task-011 in nanofuse backlog) — Firecracker-specific, no Kata equivalent
2. **vsock-based agent communication** — nanofuse uses vsock for recording; microvm-sandbox doesn't touch this
3. **OCI image → rootfs.ext4 pipeline** — nanofuse's image builder; microvm-sandbox uses pre-built Ubuntu images
4. **Sub-200ms boot time validation** — performance testing; not in scope for security eval
5. **Multi-VM networking (VM-to-VM)** — the `firecracker-runner-networking-extension.md` overlay network design

---

## Quick Wins (can do today)

1. **Copy SPIRE binary setup** from `microvm-sandbox/identity/setup.sh` into nanofuse's `scripts/setup-spire.sh` — removes Docker dependency
2. **Add escape tests** as `test/security/escape_test.go` — one day's work
3. **Add per-TAP iptables rules** in `internal/network/` alongside the existing bridge setup — the code pattern is proven in microvm-sandbox
4. **dnsmasq config template** — 20 lines, directly portable to nanofuse's networking setup
