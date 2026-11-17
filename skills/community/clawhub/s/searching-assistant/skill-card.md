## Description:

Searching Assistant breaks a search task into independent, complementary subtasks and assigns them to suitable search agents, always including General_Search_Agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[urrrich0](https://clawhub.ai/user/urrrich0)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to coordinate broad search tasks by decomposing a request into a small set of targeted subtasks for specialized search agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may broaden a search request into multiple parallel subtasks, which can be more expansive than a user intended.

Mitigation: Use it when multi-agent search coverage is desired, review proposed subtasks before acting on results, and keep assignments to the smallest useful set.

## Reference(s):

- [Searching Assistant on ClawHub](https://clawhub.ai/urrrich0/skills/searching-assistant)

## Skill Output:

**Output Type(s):** [guidance, text]

**Output Format:** [Markdown or plain text task assignments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose up to 8 subtasks for a search session.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
