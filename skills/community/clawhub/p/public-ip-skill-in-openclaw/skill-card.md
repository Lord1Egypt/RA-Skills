## Description:

Queries the current machine's public IP address for cases where an agent needs to identify the server or client as seen on the public internet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trollhe](https://clawhub.ai/user/trollhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to confirm a machine's internet-facing IP address for network diagnostics, allowlist configuration, and firewall troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the skill contacts third-party public IP lookup services, which can observe the caller's public IP address, request timing, and normal HTTP metadata.

Mitigation: Use it only in environments where external IP lookup is allowed, and avoid restricted or privacy-sensitive systems unless that disclosure is approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/trollhe/skills/public-ip-skill-in-openclaw)
- [api.ipify.org endpoint](https://api.ipify.org?format=json)
- [ifconfig.me endpoint](https://ifconfig.me/all.json)
- [ipapi.co endpoint](https://ipapi.co/json/)
- [api.myip.com endpoint](https://api.myip.com)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands]

**Output Format:** [JSON from the lookup script, typically summarized to the user as text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes the selected public_ip value and per-service lookup details when services respond.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
