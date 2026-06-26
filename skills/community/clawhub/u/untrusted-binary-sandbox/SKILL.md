---
name: untrusted-binary-sandbox
description: Use when asked to safely inspect, sandbox, detonate, run, or dynamically observe untrusted release artifacts, closed-source binaries, JARs, installers, wallet/private-key software, crypto trading bots, or suspicious GitHub releases. Provides a staged static-to-dynamic workflow with VM/Docker isolation, network controls, Solana wallet safety, tracing, evidence capture, and risk reporting.
---

# Untrusted Binary Sandbox

## Purpose

Use this skill to plan and execute controlled behavioral observation of untrusted software without trusting the software, its installer, or its documentation. Treat wallet, private-key, trading, MEV, arbitrage, and closed-source crypto tools as high-risk by default.

This skill does not prove safety. It reduces uncertainty for the exact artifact, configuration, runtime, and observation window tested.

## Non-Negotiables

- Do not run downloaded binaries, JARs, install scripts, release artifacts, or `curl | sh` flows unless the user explicitly approves dynamic execution.
- Prefer a sacrificial VM/VPS over a production host. Never mount production secrets, SSH keys, browser profiles, Docker socket, cloud credentials, or funded wallets.
- Never use a real private key during observation. Use invalid keys, empty throwaway wallets, or a tiny-fund wallet only in the final live tier after explicit approval.
- Pin artifact identity before execution: source URL, version, size, SHA-256, timestamp, and any signature/digest metadata.
- Keep confirmed findings separate from risk signals and unknowns. Report confidence level.

## Workflow

1. Scope the sample:
   Identify the artifact, claimed purpose, required command, required secrets, network endpoints, supported OS/CPU, and whether the user is asking for static analysis, dynamic observation, or production feasibility.

2. Static triage first:
   Hash the artifact, inspect archive contents, review scripts/configs, run `file`, `readelf`, `objdump`, `strings`, `jar tf`, or language-specific archive inspection as appropriate. Avoid `ldd` on untrusted ELF files; use `readelf -d` or `objdump -p` instead.

3. Choose the lowest sufficient tier:
   - Tier 0: no-run static analysis only.
   - Tier 1: offline Docker run with `network_mode: none`.
   - Tier 2: internal-only network with mock RPC/API/DNS sinks.
   - Tier 3: controlled egress with allowlisted endpoints and packet/DNS logging.
   - Tier 4: sacrificial VM/VPS with tiny-fund throwaway wallet for live behavior, only after prior tiers are clean.

4. Build containment:
   Use non-root users, `read_only` root filesystem, `cap_drop: [ALL]`, `no-new-privileges`, PID/CPU/memory limits, tmpfs for scratch, no host networking, no privileged mode, no host path mounts except read-only artifacts/config and writable logs.

5. Instrument before execution:
   Capture process tree, syscalls, opened files, filesystem writes, DNS queries, outbound connections, child processes, resource use, and any downloaded or modified files. Prefer `strace` inside Linux containers and VM-level packet capture when network is enabled.

6. Execute briefly and repeat:
   Start with short timeouts such as 60-180 seconds. Repeat with a known-bad config, mock RPC, then controlled egress. Preserve logs and hashes after each run.

7. Report with judgment:
   Summarize confirmed behavior, suspicious signals, unknowns, confidence, and a go/no-go recommendation. For wallet software, include a separate private-key exposure assessment.

## Stop Criteria

Stop and report immediately if the sample:

- Reads SSH keys, shell history, browser profiles, cloud credentials, `.env` files, unrelated wallet paths, or host-sensitive directories.
- Writes cron/systemd/profile startup hooks, modifies shell init files, changes file permissions broadly, or downloads and executes new payloads.
- Requires root, host networking, Docker socket, privileged mode, broad host mounts, or disabled sandboxing without a clear technical need.
- Connects to endpoints not declared in config/docs, especially paste sites, generic file hosts, Telegram bot APIs, raw IPs, or newly registered domains.
- Attempts to exfiltrate key material or sends transactions before the expected safe stage.

## Solana And Wallet-Specific Rules

- Never mount `~/.config/solana/id.json` or any funded wallet.
- Prefer invalid key material or an empty throwaway keypair. Do not print, transform, or store private keys in chat.
- Use a local mock RPC in Tier 2. In Tier 3, allow only explicit RPC/Jito/sender endpoints.
- Treat "encrypt your private key with this binary" as high-risk behavior, not as a safety feature.
- Measure failed transactions, priority-fee burn, Jito tips, and RPC rate-limit pressure separately from malware risk.

## Resources

- Read `references/docker-sandbox.md` when building the actual Docker or VM containment plan.
- Read `references/observation-checklist.md` when preparing the final evidence report.
- Use `scripts/scaffold_sandbox.py` to generate a local sandbox scaffold. It creates Docker Compose files and a mock Solana RPC service, but does not execute the sample by default.

**Appropriate for:** In-depth documentation, API references, database schemas, comprehensive guides, or any detailed information that Codex should reference while working.

### assets/
Files not intended to be loaded into context, but rather used within the output Codex produces.

**Examples from other skills:**
- Brand styling: PowerPoint template files (.pptx), logo files
- Frontend builder: HTML/React boilerplate project directories
- Typography: Font files (.ttf, .woff2)

**Appropriate for:** Templates, boilerplate code, document templates, images, icons, fonts, or any files meant to be copied or used in the final output.

---

**Not every skill requires all three types of resources.**
