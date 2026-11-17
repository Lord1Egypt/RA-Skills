## Description:

Helps eligible Tsinghua University users access campus coursework, schedules, grades, library services, email, notices, literature search, and campus AI services through an agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomuiv](https://clawhub.ai/user/tomuiv)

### License/Terms of Use:

MIT-0

## Use Case:

Tsinghua students and other authorized users use this skill to look up coursework and campus information, manage library bookings and email, search literature, and access campus AI models. Campus login and additional credentials are required for some services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email may be sent or marked as read immediately, without the confirmation described in the skill documentation.

Mitigation: Review recipient, subject, and body before sending; explicitly confirm mail actions and avoid marking messages read without consent.

Risk: Campus login, mailbox and API credentials, browser sessions, and booking authority grant access to sensitive accounts and actions.

Mitigation: Install only when this access is appropriate; restrict access to the local credential vault, master key, and sessions, and do not sync them to shared storage.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/tomuiv/skills/tsinghua-campus)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files]

**Output Format:** [Conversational responses and structured service results; downloaded files when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on campus access and configured credentials.]

## Skill Version(s):

1.0.9 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
