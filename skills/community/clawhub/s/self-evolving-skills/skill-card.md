## Description:

Agent self-evolution mechanism that helps agents turn successful complex tasks into reusable skills for continuous learning and procedural knowledge accumulation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tunsuy](https://clawhub.ai/user/tunsuy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to decide when an agent should preserve a completed workflow as a reusable skill, create the supporting skill files, and validate the resulting skill structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to create or modify reusable skills, which may persist incorrect, misleading, or unsafe procedures.

Mitigation: Require the agent to show the target path and exact diff before creating or updating skill files, and require explicit approval before changing existing skills or scripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tunsuy/skills/self-evolving-skills)
- [Skill deposition decision flow](references/decision-flow.md)
- [SKILL.md format reference](references/skill-format.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional skill files, templates, scripts, and validation command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce persistent skill instructions and supporting files when the user approves skill creation or updates.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
