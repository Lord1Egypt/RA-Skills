## Description:

Automates online law course video watching on 律师云学院 (lawschool.lawyerpass.com), including course enrollment, video completion checks, next-course switching, and progress notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vanishedzhou](https://clawhub.ai/user/vanishedzhou)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to automate progress through online law-course videos on 律师云学院 while maintaining a state file and sending course progress notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enroll in courses, play videos, and send progress notifications through a logged-in Chrome session.

Mitigation: Use it only when automated course playback is allowed for the account, and review the selected courses and notification destination before starting.

Risk: The skill creates a recurring video-check-loop job that may continue using the browser session after setup.

Mitigation: Inspect the recurring job and video_state.json during use, and remove them after the requested courses finish.

## Reference(s):

- [Full Workflow](references/workflow.md)
- [Video State Schema](references/state-schema.md)
- [Known Issues and Gotchas](references/known-issues.md)
- [ClawHub Skill Page](https://clawhub.ai/vanishedzhou/skills/sh-lawschool-video-autopilot)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline JavaScript, JSON, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces browser automation steps, recurring job configuration, state-file guidance, and notification text for an agent.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
