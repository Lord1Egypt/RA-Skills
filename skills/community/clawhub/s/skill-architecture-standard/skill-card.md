## Description:

Use this skill as a reference when creating, reviewing, or upgrading OpenClaw skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pmuhammadagus-byte](https://clawhub.ai/user/pmuhammadagus-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this reference to structure, review, and upgrade OpenClaw skills with guidance for triggers, context handling, decision policy, verification, recovery, security, evaluation, and exit conditions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill influences how agents create or review OpenClaw skills, so its recommendations could be over-applied as mandatory enforcement.

Mitigation: Treat the standard as design guidance and keep normal human review for skill acceptance, especially when changing behavior, permissions, or enforcement rules.

Risk: Applying its tool, memory, and security sections without context could lead an agent toward inappropriate installs, configuration edits, deletions, credential handling, or external calls.

Mitigation: Require normal user approval for high-risk actions and validate the user's environment, tools, and permissions before applying operational guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pmuhammadagus-byte/skills/skill-architecture-standard)
- [Artifact SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration instructions]

**Output Format:** [Markdown guidance and checklist-style recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only reference; no executable code or hidden data access is identified in the release evidence.]

## Skill Version(s):

1.1.2 (source: frontmatter metadata.openclaw.version and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
