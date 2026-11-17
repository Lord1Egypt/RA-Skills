## Description:

This skill analyzes living-room camera video to estimate when an older adult is seated on a sofa and watching TV, then produces sedentary-duration reports and movement reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

External users, caregivers, and developers can use this skill to analyze fixed-camera home or elder-care video for seated TV-watching duration, activity reminders, and historical behavior reports. The skill is intended to provide visual behavior statistics and friendly prompts, not medical diagnosis or treatment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles private living-room video or video URLs through a cloud analysis workflow.

Mitigation: Confirm informed consent from the recorded person or guardian and verify that cloud processing is acceptable before installing or running the skill.

Risk: The security evidence says the skill may create or reuse local and remote identity records and store access tokens in a workspace SQLite database.

Mitigation: Review workspace access controls, token retention, and cleanup practices before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-elderly-tv-sedentary-reminder-analysis)
- [API documentation](references/api_doc.md)
- [Skill usage demo](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON-style structured analysis reports with optional report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call cloud video-analysis APIs and can write requested output files.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter says 1.0.14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
