## Description:

Security audit tool for OpenClaw skills that scans skill directories for patterns associated with credential harvesting, code injection, network exfiltration, obfuscation, environment access, and subprocess abuse.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suryast](https://clawhub.ai/user/suryast)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to run advisory security checks before installing or reviewing OpenClaw skills. It helps surface risky patterns and manual review needs in skill source files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner is advisory and its install-check controls can be bypassed.

Mitigation: Use results as review input rather than as a reliable enforcement gate, and perform manual review before installing or approving skills.

Risk: The skill can make persistent blocklist changes when critical findings are detected.

Mitigation: Review blocklist changes before relying on them and keep approvals tied to current skill content.

Risk: Allowlist entries alone do not prove a skill is safe.

Mitigation: Confirm trusted approvals against the reviewed skill version and prefer hash-bound approvals for production workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/suryast/skills/skill-security)
- [Publisher Profile](https://clawhub.ai/user/suryast)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text terminal output with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update blocklist.txt when critical findings are found.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
