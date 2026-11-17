## Description:

TalonForge Safety Rails (EN/AR) helps an agent configure trust levels, non-negotiable safety rules, prompt injection defenses, and approval workflows for safer autonomous AI interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[casperzinou](https://clawhub.ai/user/casperzinou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to have an agent collect risk tolerance, hard rules, and a verified messaging channel, then draft markdown safety rules for OpenClaw-style autonomous workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends installing additional unpinned remote components at install time.

Mitigation: Verify the publishers and package contents before running the commands, and prefer pinned, reviewed versions of ai-sentinel, skill-guard, and the ClawHub installer where possible.

Risk: Generated safety rules may not fully match the user's operational risk tolerance or approval requirements.

Mitigation: Review the generated trust level, hard rules, verified channel, and approval workflow before relying on the configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/casperzinou/skills/talonforge-safety)
- [Publisher profile](https://clawhub.ai/user/casperzinou)
- [TalonForge homepage](https://talonforge.xyz)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown safety configuration with setup questions and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a trust ladder, approval workflow, prompt-injection defenses, and install commands for related components.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
