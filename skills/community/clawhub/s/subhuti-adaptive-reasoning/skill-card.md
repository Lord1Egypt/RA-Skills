## Description:

Automatically assess task complexity and adjust reasoning level.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dorjenorbulim](https://clawhub.ai/user/dorjenorbulim)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill as a pre-processing step to decide when a request would benefit from deeper reasoning before answering complex questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can silently change reasoning behavior across a session and affect every user message.

Mitigation: Install only when session-wide reasoning automation is desired, review its behavior before deployment, and prefer explicit opt-in controls for reasoning changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dorjenorbulim/skills/subhuti-adaptive-reasoning)
- [Publisher profile](https://clawhub.ai/user/dorjenorbulim)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown text with optional reasoning status indicators]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append visible reasoning markers to responses when the skill classifies a request as complex.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
