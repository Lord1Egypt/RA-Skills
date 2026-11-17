## Description:

Coordinates implementation plans with independent tasks in the current session by dispatching fresh subagents and two-stage reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to execute implementation plans made of mostly independent tasks while keeping subagent work scoped, reviewed for spec compliance, and reviewed for code quality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable remote install commands can change behavior between installs.

Mitigation: Review and pin the installer source before installation.

Risk: Persistent global installation makes the workflow available outside a single project.

Mitigation: Prefer project-scoped installation unless global availability is intentional.

Risk: The workflow delegates code reading, edits, tests, and commits to subagents.

Mitigation: Use it only in repositories where that level of subagent access is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wpank/skills/subagent-development)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with prompt templates and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses staged implementer, spec-reviewer, and code-quality-reviewer prompts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
