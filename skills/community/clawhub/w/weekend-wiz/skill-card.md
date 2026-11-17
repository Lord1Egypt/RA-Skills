## Description:

Weekend schedule management assistant that creates, updates, and visualizes weekend schedules with markdown schedule files, HTML rendering, screenshots, automated reminders, and cleanup of expired events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaorui03](https://clawhub.ai/user/gaorui03)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use WeekendWiz to maintain weekend schedule files, render a visual HTML schedule, generate screenshots for sharing, and configure reminders for upcoming events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Schedule maintenance can clean up expired events under memory/, which may remove entries the user expected to keep.

Mitigation: Review proposed schedule changes before execution and keep important schedule history outside the managed schedule file.

Risk: Reminder text can include sensitive event details and may be sent through qqbot when reminders are configured.

Mitigation: Use trusted delivery channels and avoid putting sensitive locations, notes, or personal details in reminder messages.

Risk: Rendered schedule HTML loads a Google-hosted font, which may make an external request during viewing or screenshot generation.

Mitigation: Use a local font or remove the external font link when operating in offline or privacy-sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gaorui03/skills/weekend-wiz)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown schedule entries, rendered HTML, PNG screenshots, and reminder setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains schedule files under memory/, updates date labels, and can configure one-time reminders.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
