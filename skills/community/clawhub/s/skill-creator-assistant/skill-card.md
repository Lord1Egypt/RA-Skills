## Description:

Guides non-technical users through targeted questions to create complete OpenClaw skills without coding, including SKILL.md and optional GitHub upload.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zihaowyt5525-max](https://clawhub.ai/user/zihaowyt5525-max)

### License/Terms of Use:

MIT-0

## Use Case:

Non-technical OpenClaw users use this skill to turn an idea into a structured skill definition through a guided questionnaire. It helps produce a ready-to-use SKILL.md, optional README content, and optional GitHub publishing steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SKILL.md or README content could include secrets, proprietary workflow details, or unintended sensitive information.

Mitigation: Review generated files before publishing and remove credentials, private process details, or confidential examples.

Risk: Optional GitHub upload could publish to the wrong account or expose a repository that should remain private.

Mitigation: Confirm the target GitHub account and repository visibility before running upload commands.

Risk: Generated skills that depend on paid APIs, runtime environments, or complex multi-agent behavior may not be fully testable by this assistant.

Mitigation: Manually validate dependencies, credentials, and runtime behavior before using the generated skill in production.

## Reference(s):

- [Artifact SKILL.md](artifact/SKILL.md)
- [Artifact README.md](artifact/README.md)
- [ClawHub skill page](https://clawhub.ai/zihaowyt5525-max/skills/skill-creator-assistant)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Guided conversation with generated Markdown files and optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce SKILL.md, README.md, and optional GitHub publishing instructions; users should review generated content before upload.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
