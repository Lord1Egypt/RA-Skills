# Observation Checklist And Report Template

## Pre-Run Checklist

- User explicitly approved dynamic execution for the specific artifact.
- Artifact identity recorded: URL, version, file size, SHA-256, signature/digest if available.
- No real keys, production `.env`, SSH credentials, browser profiles, or funded wallets are present.
- Runtime tier selected and documented.
- Command, timeout, CPU/memory/PID limits, mounts, and network mode are recorded.
- Logs directory is empty and writable before the run.

## Behavior Checklist

Record:

- Files read outside the sample directory.
- Files written, created, renamed, chmodded, or deleted.
- Child processes and shell invocations.
- Network endpoints, DNS queries, SNI names, raw IPs, and unexpected protocols.
- Downloaded files and whether execution was attempted.
- Environment variables read or printed.
- Resource behavior: CPU, memory, forks, disk writes, repeated crashes.
- Blockchain behavior: RPC methods, transaction simulation/send calls, priority fees, tips, wallet access.

## Red Flags

- Reads key material or unrelated secrets.
- Attempts persistence through cron, systemd, shell profiles, launch agents, or startup folders.
- Writes outside expected config/log/temp locations.
- Calls unknown endpoints not present in docs or config.
- Fetches and executes new artifacts.
- Requires root, privileged Docker, host networking, Docker socket, or broad host mounts.
- Sends private key material or signed transactions to a non-RPC endpoint.
- Behaves differently only when a funded wallet is present.

## Report Shape

Use this structure:

```markdown
**Scope**
Artifact, version, hash, source, command, tier, timeout.

**Confirmed Findings**
Facts directly observed in logs/traces.

**Risk Signals**
Suspicious or trust-reducing behavior that is not independently proven malicious.

**Unknowns**
What this run could not prove, including time-window, sandbox-evasion, and closed-source limits.

**Wallet/Key Exposure**
Whether key files were read, where data was sent, and whether transaction signing/broadcasting occurred.

**Operational Fit**
CPU, memory, disk, network, restart behavior, and production-host suitability.

**Recommendation**
Go/no-go, confidence level, and the next safest test tier.
```

Confidence language:

- High: repeated controlled runs, clear traces, narrow behavior, no major unobserved paths.
- Medium: useful traces but closed-source behavior, short runtime, or incomplete network visibility.
- Low: static-only, failed run, or too many unknowns to support a deployment decision.
