## Description:

Harden an OpenClaw Linux server with SSH key-only authentication, UFW firewall rules, fail2ban brute-force protection, and credential permissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ppiankov](https://clawhub.ai/user/ppiankov)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill when setting up a new OpenClaw Linux server, auditing server security, or recovering after a security incident.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Disabling password authentication and enabling UFW can lock out administrators if key-based SSH access or required ports are not confirmed first.

Mitigation: Run the commands only from a confirmed key-based SSH session and verify all required network ports are allowed before enabling UFW.

Risk: The skill creates a persistent OpenClaw gateway service running as root without clear hardening or scope.

Mitigation: Install the service only when intentionally required, verify the executable path and ownership, and run it under a dedicated least-privileged account with systemd hardening.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ppiankov/skills/server-host-hardening)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes host-level commands that should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
