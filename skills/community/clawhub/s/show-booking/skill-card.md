## Description:

Book real estate showing tours from emailed or pasted listing details, including extracting listing data, preparing outbound call jobs, coordinating a calling sub-agent, creating calendar invites, and returning confirmations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielfoch](https://clawhub.ai/user/danielfoch)

### License/Terms of Use:


## Use Case:

Real estate agents, brokerages, and their assistants use this skill to turn emailed or pasted showing requests into structured booking plans, outbound call jobs, calendar invite files, and concise confirmation summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles real client and listing data.

Mitigation: Review before installation, store generated JSON and audit logs in a controlled location, and avoid sharing client data beyond the booking workflow.

Risk: Live outbound calls may create legal, consent, or caller-identification obligations.

Mitigation: Run live calls only after explicit approval, identify the caller as an AI assistant acting for the brokerage or realtor, and follow applicable telemarketing and consent requirements.

Risk: Generated calendar invites may include untrusted listing or notes content.

Mitigation: Review .ics files before importing or forwarding them until calendar content escaping is confirmed.

## Reference(s):

- [Email Intake Template](artifact/references/email-intake-template.md)
- [Integration Notes](artifact/references/integration-notes.md)
- [Show Booking on ClawHub](https://clawhub.ai/danielfoch/skills/show-booking)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with shell commands, JSON workflow artifacts, and .ics calendar files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces blocked-listing status, call queue details, confirmation summaries, and one .ics file per confirmed showing.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
