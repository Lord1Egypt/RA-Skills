## Description:

Gets and displays the current time when a user asks time-related questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlikemario](https://clawhub.ai/user/zlikemario)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to answer time-related prompts by returning the current time as a single formatted string.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The broad trigger word "now" may activate the skill during unrelated prompts.

Mitigation: Confirm the user is asking for the current time or narrow routing to time-specific phrases before relying on the output.

Risk: The displayed time uses Chinese locale formatting rather than adapting to the user's locale.

Mitigation: Verify locale and timezone expectations before using the output in user-facing or workflow-critical contexts.

## Reference(s):

- [Utf8 Time ClawHub skill page](https://clawhub.ai/zlikemario/skills/utf8-time)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text timestamp string]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses locale-specific date and time formatting with 24-hour time.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
