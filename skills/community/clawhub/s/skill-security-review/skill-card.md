## Description:

Review the security of an OpenClaw skill or agent before installation, import, activation, or trust.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kickook](https://clawhub.ai/user/kickook)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to audit OpenClaw skills, agents, repositories, archives, or pasted skill files before installation or trust decisions. It guides review of data exposure, local command execution, persistence, network access, privilege escalation, destructive behavior, and supply-chain risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is an advisory checklist and does not replace sandboxing, malware scanning, or manual review for opaque binaries and remote content.

Mitigation: Use the checklist before installation, and isolate or reject artifacts whose behavior cannot be inspected.

Risk: The default workflow can slow skill installation because it asks for an audit and confirmation first.

Mitigation: Plan the review as an explicit approval step before enabling or importing new skills.

Risk: The artifact contains user-specific wording that may not be suitable for broad reuse.

Mitigation: Replace user-specific wording with neutral organizational language before redistribution.

## Reference(s):

- [Security Review Checklist](references/checklist.md)
- [ClawHub skill page](https://clawhub.ai/kickook/skills/skill-security-review)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown security audit summary with findings and an install decision]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces advisory review output; no executable code is bundled in the release artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
