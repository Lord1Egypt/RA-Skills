## Description:

Meta-skill for secure network tunnel setup, geo-access diagnostics, and leak-aware task resumption by orchestrating shell-scripting, curl-http, wireguard, tailscale, dns, ipinfo, and moltguard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[h4gen](https://clawhub.ai/user/h4gen)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to diagnose geo/IP access blocks, switch an approved VPN, WireGuard, or Tailscale tunnel path with explicit consent, verify IP, region, and DNS posture, then retry a blocked workflow with auditable results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable install commands can execute newer unreviewed ClawHub code or update unrelated skills.

Mitigation: Review the skill before installation, pin dependency versions where possible, and update only the named dependencies needed for the workflow.

Risk: Tunnel switching modifies network routing and could be used against legal, policy, or service terms expectations.

Mitigation: Require explicit user authorization, legal or terms acknowledgment, and a stated purpose before any tunnel switch; return diagnostics-only output when acknowledgment is missing.

Risk: A connected tunnel can still have region mismatch, DNS leakage, unsupported kill-switch behavior, or missing credential coverage.

Mitigation: Verify pre/post IP, target region, DNS posture, kill-switch support when requested, and credential availability before declaring success or resuming a blocked workflow.

## Reference(s):

- [Stealth Proxy on ClawHub](https://clawhub.ai/h4gen/skills/stealth-proxy)
- [Publisher profile](https://clawhub.ai/user/h4gen)
- [Inspected upstream skills](references/inspected-skills.md)
- [ClawHub homepage](https://clawhub.ai)
- [IPinfo JSON endpoint](https://ipinfo.io/json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured status sections and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Partial, Needs Review, MissingAPIKeys, or MissingCredentials status when verification, authorization, credentials, or tunnel setup are incomplete.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
