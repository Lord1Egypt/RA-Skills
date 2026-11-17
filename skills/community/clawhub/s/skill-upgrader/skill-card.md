## Description:

Skill Upgrader helps agents analyze, diagnose, and improve existing OpenClaw skills through structured audits, upgrade phases, quality gates, and validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pmuhammadagus-byte](https://clawhub.ai/user/pmuhammadagus-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, skill authors, and OpenClaw users use this skill to audit an existing skill, identify gaps, and produce an upgraded version with clearer structure, stronger reasoning, quality gates, and validation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to modify skill files, so upgrades may introduce incorrect or misleading guidance.

Mitigation: Review the proposed diff before accepting changes and scan the upgraded skill before deployment.

Risk: Applying the skill across multiple targets at once can make review and rollback harder.

Mitigation: Keep the one-skill-per-run boundary from the artifact guardrails and validate each result before continuing.

Risk: Operational guardrails are partly written in Indonesian, which can be missed by reviewers who do not read the language.

Mitigation: Translate and confirm the guardrails before relying on the skill in production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pmuhammadagus-byte/skills/skill-upgrader)
- [The Anatomy of a Legendary Skill](references/skill-anatomy.md)
- [The 7 Enhancement Layers](references/enhancement-layers.md)
- [Skill Evolution: From Basic to Legendary](references/skill-evolution.md)
- [Absolute Quality Standards](references/quality-standards.md)
- [Skill Upgrade Template](templates/skill-upgrade-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, structured audits, checklists, templates, and proposed skill-file changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed diffs or validation commands when the agent is modifying skill files.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
