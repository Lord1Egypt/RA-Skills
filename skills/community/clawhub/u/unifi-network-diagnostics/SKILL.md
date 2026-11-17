---
name: unifi-network-diagnostics
description: Diagnose a private household UniFi network for Operator and discover non-secret local helper configuration. Use for Wi-Fi, internet, DNS, latency, packet loss, client connectivity, AP or switch health, gateway or WAN health, suspicious device behavior, slow network, intermittent connectivity, local UniFi helper setup, and vague network-health questions.
---

# UniFi Network Diagnostics

Operator administers a private household UniFi network. Use this skill for read-only diagnosis. Do not print, log, commit, infer, request, or embed UniFi credentials or local machine configuration.

## Safety Contract

- Use the configured read-only UniFi helper discovered by local setup. Do not assume, publish, or hard-code local helper paths.
- Run read-only diagnostics autonomously when they are relevant to the request.
- Run local helper discovery autonomously in read-only mode when the helper is not configured.
- Never run a command that changes controller, gateway, AP, switch, DNS, DHCP, firewall, Wi-Fi, client, or system state without explicit owner approval.
- Ask owner approval before writing remembered local configuration with `scripts/discover-unifi-config.sh --write`.
- Before any state-changing action, state the exact action, expected effect, risk, and rollback or stop condition, then wait for approval.
- Do not expose secrets, local paths, MAC addresses, private topology, public WAN IP addresses, tokens, cookies, API keys, or credential-like values in output.

## Baseline Workflow

1. Restate the symptom as a scope question: whole network, Wi-Fi only, one client, DNS-only, WAN-only, latency, packet loss, or suspicious behavior.
2. Run `unifi-network-diagnostics/scripts/diagnose-network.sh` unless equally current evidence is already available.
3. If the script reports no configured UniFi helper, run `unifi-network-diagnostics/scripts/discover-unifi-config.sh` to discover non-secret local configuration, or ask the owner to provide `UNIFI_HELPER` for this session.
4. Classify the evidence by layer using `references/diagnostic-model.md` when needed.
5. Separate each finding into:
   - Observation: directly measured or reported fact.
   - Inference: derived from multiple observations.
   - Hypothesis: plausible cause that still needs confirmation.
   - Conclusion: cause supported by converging evidence and no major contradiction.
6. Prefer the narrowest explanation that fits the evidence. Avoid declaring a root cause from one failed test.
7. Recommend the next read-only test when confidence is low. Recommend a state-changing remediation only after asking for owner approval.

## Autonomous Follow-Up Tests

Run safe follow-ups without asking when they help isolate the fault:

- Repeat the bundled diagnostic script to check whether packet loss, DNS timing, or gateway reachability is transient.
- Use bounded `ping`, `dig`, `getent`, `ip route`, `resolvectl status`, or `nmcli device show` checks if installed.
- Compare DNS resolution against external IP reachability to distinguish DNS from WAN failure.
- Compare gateway reachability against external latency to distinguish LAN/gateway issues from ISP or upstream issues.
- Re-query the configured read-only UniFi helper for device and client-summary status changes.

Keep every follow-up bounded with timeouts where possible, avoid sudo, and redact sensitive identifiers, local paths, private topology, and helper locations from any quoted output.

## Local Helper Discovery

Use `scripts/discover-unifi-config.sh` to find a compatible read-only UniFi helper without emitting full local paths by default. Treat its output as local setup evidence, not network-health evidence.

After explicit owner approval, use `scripts/discover-unifi-config.sh --write` to remember the selected helper path in local configuration outside the repository. Never commit that generated configuration or copy it into public artifacts.

Use `--show-paths` only when the owner explicitly asks to inspect local paths. Do not include full local paths in normal reports.

## State-Changing Actions Requiring Approval

Ask before actions such as rebooting devices, reconnecting clients, changing channels, changing transmit power, changing DNS or DHCP settings, modifying firewall rules, blocking clients, upgrading firmware, restarting services, reprovisioning devices, or editing credentials. Do not create remediation scripts for these actions.

## Output Format

Use this structure:

```markdown
## Current Assessment
One or two sentences describing the most likely affected layer and impact.

## Evidence
- Observations:
- Inferences:
- Hypotheses considered but weakened:

## Ranked Hypotheses
1. Hypothesis - evidence for, evidence against, next test.
2. Hypothesis - evidence for, evidence against, next test.

## Confidence
Low, medium, or high, with a short reason.

## Unresolved Questions
- Unknowns that materially affect the diagnosis.

## Recommended Next Action
The next safest read-only test, or the exact state-changing action that requires owner approval.
```
