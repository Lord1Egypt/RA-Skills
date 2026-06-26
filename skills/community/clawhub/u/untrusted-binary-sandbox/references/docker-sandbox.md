# Docker And VM Sandbox Reference

## Tier Selection

Use the weakest tier that answers the question.

- Tier 0, static only: source/archive inspection, hashes, strings, scripts/config review. Use this when the user has not approved execution.
- Tier 1, offline container: no network, read-only root, non-root user, short timeout, syscall/file tracing.
- Tier 2, internal mock network: internal Docker network only, mock RPC/API endpoints, DNS logging, no internet route.
- Tier 3, controlled egress: sacrificial VM preferred, egress allowlist, DNS/SNI/flow logging, no funded wallet.
- Tier 4, live tiny-fund test: sacrificial VM/VPS, explicit approval, tiny throwaway wallet, hard spend caps, short window.

Docker is a containment layer, not a malware analysis boundary. Use a VM or disposable VPS for hostile samples, kernel exploit risk, or anything requiring live funds.

## Minimum Container Guardrails

Use these unless the sample cannot start and there is a documented reason to loosen one guardrail:

```yaml
services:
  sample:
    user: "10001:10001"
    read_only: true
    network_mode: "none"
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
    pids_limit: 128
    mem_limit: 768m
    cpus: "1.0"
    tmpfs:
      - /tmp:rw,nosuid,nodev,noexec,size=128m
    volumes:
      - ./artifact:/work/artifact:ro
      - ./config:/work/config:ro
      - ./logs:/logs:rw
```

Never add `privileged: true`, `network_mode: host`, `/var/run/docker.sock`, `/`, `$HOME`, SSH directories, browser profiles, production `.env`, cloud credentials, or funded wallet mounts.

## Instrumentation Commands

Inside Linux containers, prefer:

```bash
timeout 180 strace -f -yy -s 256 -o /logs/strace.log ./sample config.toml
find /work /tmp -xdev -type f -printf '%p %s %TY-%Tm-%Td %TH:%TM:%TS\n' > /logs/files-after.txt
ps auxww > /logs/ps-after.txt
```

For ELF inspection, prefer:

```bash
sha256sum sample
file sample
readelf -h sample
readelf -d sample || true
objdump -p sample || true
strings -a -n 8 sample | sort -u > strings.txt
```

Avoid `ldd` on untrusted ELF files. It can invoke the dynamic loader and has historically been unsafe for hostile samples.

For JARs:

```bash
sha256sum sample.jar
jar tf sample.jar > jar-contents.txt
unzip -p sample.jar META-INF/MANIFEST.MF || true
strings -a -n 8 sample.jar | sort -u > jar-strings.txt
```

## Controlled Network Pattern

For Tier 2, use an internal Docker network:

```yaml
networks:
  sandbox_net:
    internal: true

services:
  rpc-mock:
    image: python:3.12-slim
    networks: [sandbox_net]
    volumes:
      - ./mock-rpc:/mock-rpc:ro
    working_dir: /mock-rpc
    command: ["python", "server.py"]

  sample:
    networks: [sandbox_net]
```

Point the sample's RPC URL at `http://rpc-mock:8899`. Any internet access attempt should fail. If broad DNS or internet access is still observed, the sandbox is misconfigured.

For Tier 3, prefer a disposable VM with host firewall rules. Docker-only egress controls are easier to misconfigure, especially if the daemon or host networking is exposed.

## Evidence Preservation

For each run, store:

- Artifact path, source URL, size, SHA-256, and timestamp.
- Exact command, image digest/base image, Docker Compose file, environment variables, and config redactions.
- `strace.log`, process list, file tree before/after, network logs, stdout/stderr, resource stats.
- Any downloaded secondary payloads with hashes, without executing them.
