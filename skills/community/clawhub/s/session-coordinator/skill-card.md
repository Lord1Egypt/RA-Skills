## Description:

Async Process Pattern for OpenClaw agents that keeps the main process responsive by delegating long, uncertain, remote, or state-modifying work to subagents while the main process handles dialog and dispatch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guytogay](https://clawhub.ai/user/guytogay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep OpenClaw sessions responsive while coordinating slow, remote, uncertain, or state-changing tasks through background subagents. It is intended for workflows that need clear separation between user dialog, task dispatch, execution, and result reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to silently delegate work to subagents, which can reduce user visibility into how tasks are executed.

Mitigation: Require disclosure or confirmation before delegation for high-impact, remote, or state-modifying actions.

Risk: The skill directs agents to write significant outcomes and routine work into persistent memory files.

Mitigation: Review memory writes and use the skill only in environments where persistent logging of task outcomes is acceptable.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline command and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces coordination instructions, spawn examples, timeout guidance, label conventions, lifecycle rules, and memory logging guidance.]

## Skill Version(s):

3.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
