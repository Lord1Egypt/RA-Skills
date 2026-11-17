## Description:

Guides agents through exploration, questioning, design proposals, and specification documentation before creative implementation work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to turn creative feature, component, functionality, or behavior-change requests into reviewed design proposals and written specifications before implementation begins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enforces a design-first workflow that can slow direct implementation.

Mitigation: Use it only for projects where mandatory upfront design review is desired.

Risk: The skill directs the agent to write specification files and commit them to the repository.

Mitigation: Require explicit approval before file writes and git commits when operating in protected or shared repositories.

Risk: The skill steers the agent to a specific follow-up planning skill before implementation.

Mitigation: Review downstream skill invocation policies and require approval before invoking additional skills.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/axelhu/skills/superpowers-brainstorming)
- [Publisher profile: axelhu](https://clawhub.ai/user/axelhu)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown design proposals and specification text with occasional shell command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to write and commit a specification file before handing off to a planning skill.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
