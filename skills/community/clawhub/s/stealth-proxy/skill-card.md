## Description: <br>
Stealth Proxy orchestrates VPN, WireGuard, or Tailscale tunnel switching with consent gates, geo/IP verification, DNS safety checks, and bounded retry of blocked workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[h4gen](https://clawhub.ai/user/h4gen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to diagnose geo/IP access blocks, switch an approved local tunnel path with explicit consent, verify the resulting IP, region, and DNS posture, and resume blocked workflows with auditable evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent-controlled tunnel changes can alter local network routing or access context. <br>
Mitigation: Require explicit user authorization, legal or terms acknowledgement, target region, tunnel path, and purpose before switching; use diagnose-only mode when consent is missing. <br>
Risk: VPN, WireGuard, or Tailscale credentials, profiles, or binaries may be unavailable or misconfigured. <br>
Mitigation: Run preflight checks for required binaries and sessions, report MissingCredentials or MissingAPIKeys with blocked stages, and continue only non-blocked diagnostics when setup is incomplete. <br>
Risk: A tunnel may connect while geo, IP, DNS, or endpoint access checks remain misaligned. <br>
Mitigation: Compare pre/post public IP, region, resolver behavior, and HTTP evidence; stop or mark Needs Review when verification fails, kill-switch support is unverified, or bounded retries are exhausted. <br>
Risk: Automatically resumed workflows could perform sensitive actions after access is restored. <br>
Mitigation: Require a separate explicit approval before resuming workflows that can trade, purchase, post, or change accounts. <br>


## Reference(s): <br>
- [Stealth Proxy ClawHub Release](https://clawhub.ai/h4gen/stealth-proxy) <br>
- [Inspected Upstream Skills](references/inspected-skills.md) <br>
- [IPinfo Verification Endpoint](https://ipinfo.io/json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with structured status sections and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes block diagnosis, tunnel status, DNS safety, security status, access retest results, task resumption state, and next actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
