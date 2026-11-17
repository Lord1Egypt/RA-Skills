## Description:

Automatically preserves reusable task experience as a skill by evaluating completed work, checking for similar existing skills, and creating, updating, or publishing a skill when the criteria are met.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binyuli](https://clawhub.ai/user/binyuli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill after non-trivial tasks to decide whether reusable workflows, corrections, or error recoveries should be captured as durable skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or update persistent skills automatically.

Mitigation: Require manual confirmation before creating or updating any skill, and review generated content for secrets or private details before use.

Risk: The skill includes a publish command without clear approval gates in the artifact.

Mitigation: Require explicit user approval before publishing and review the target skill path and metadata first.

Risk: Duplicate checks may inspect broad skill directories and compare content beyond explicit metadata.

Mitigation: Limit duplicate checks to explicit skill metadata when possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/binyuli/skills/skill-autosave)
- [Publisher profile](https://clawhub.ai/user/binyuli)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with bash command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes evaluation criteria, duplicate-check guidance, SKILL.md quality standards, and publish commands.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
