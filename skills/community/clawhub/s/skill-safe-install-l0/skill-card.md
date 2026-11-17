## Description:

Skill Safe Install provides a strict secure installation workflow for OpenClaw skills, including duplicate checks, candidate search, security review, isolated test installation, formal installation, and explicit authorization before whitelist changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[halfmoon82](https://clawhub.ai/user/halfmoon82)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to guide skill installation through duplicate checking, candidate search, inspection, isolated test install, formal install, and explicit approval before allowlist changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can proceed to permanent skill installation and persistent OpenClaw configuration changes.

Mitigation: Use explicit package names, verify publisher and digest, perform a real isolated test install first, and require a separate confirmation before formal install or allowlist modification.

Risk: Hard-coded trusted skill IDs can cause review to be skipped for matching skills.

Mitigation: Confirm that any review exemption still matches a verified publisher and release digest before installing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/halfmoon82/skills/skill-safe-install-l0)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include step-by-step install review status and requests for explicit confirmation before persistent configuration changes.]

## Skill Version(s):

2.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
