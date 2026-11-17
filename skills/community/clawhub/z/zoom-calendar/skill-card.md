## Description:

Create Zoom meetings and add them to Google Calendar events with proper conferenceData, including the icon, video entry point, and notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaharsha](https://clawhub.ai/user/shaharsha)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and calendar automation users use this skill to create Zoom meetings and attach them to Google Calendar events. It is intended for workflows that explicitly request Zoom meeting creation or adding Zoom conference data to an existing event.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Zoom and Google Calendar credentials and access tokens.

Mitigation: Use only trusted machines and accounts, keep credential scopes as narrow as possible, and review credential paths before execution.

Risk: The script prints live meeting join details and passcodes.

Mitigation: Run it only in terminals and logs appropriate for sensitive meeting information.

Risk: The workflow assumes the Asia/Jerusalem timezone for created Zoom meetings.

Mitigation: Confirm the intended timezone before using it for events outside that timezone.

Risk: The security summary reports brittle shell handling around credentials and request bodies.

Mitigation: Review before installing and prefer fixes that JSON-encode request bodies and clean up temporary token files with an exit trap.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shaharsha/skills/zoom-calendar)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and credential setup notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The shell workflow creates a Zoom meeting, patches the Google Calendar event, and prints the join URL, meeting ID, and passcode.]

## Skill Version(s):

1.1.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
