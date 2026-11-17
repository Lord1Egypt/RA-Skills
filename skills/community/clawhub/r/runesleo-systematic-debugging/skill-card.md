## Description:

Four-phase debugging framework that ensures root cause investigation before attempting fixes. Never jump to solutions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runesleo](https://clawhub.ai/user/runesleo)

### License/Terms of Use:


## Use Case:

Developers and engineering agents use this skill when investigating bugs, test failures, build failures, performance problems, integration issues, or other unexpected technical behavior. It guides the agent to recall relevant context, identify root cause, compare working patterns, test a focused hypothesis, and implement a verified fix.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to check memory files or past conversations before debugging, which can expose unrelated sensitive history.

Mitigation: Restrict context recall to the current project unless the user explicitly approves broader memory, conversation, or shared-workspace access.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown with structured debugging steps and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce context-recall summaries, root-cause hypotheses, diagnostic commands, test plans, and implementation guidance.]

## Skill Version(s):

3.0.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
