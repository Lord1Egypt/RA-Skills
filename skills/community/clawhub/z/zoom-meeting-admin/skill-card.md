## Description:

Helps agents manage Zoom meetings and look up account users and cloud recordings through seven approved Server-to-Server OAuth actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mebusw](https://clawhub.ai/user/mebusw)

### License/Terms of Use:

MIT-0

## Use Case:

Zoom account administrators and their agents use this skill to schedule, find, and cancel meetings, retrieve cloud recording information, and look up account users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account-level credentials and cached access tokens could expose meeting and recording data.

Mitigation: Use a dedicated Zoom app, keep .env and token files private and out of repositories and sync tools, and avoid shared machines.

Risk: Unnecessary Zoom permissions could enable deletion or access to sensitive recordings.

Mitigation: Grant only the required OAuth scopes; leave deletion and recording access disabled unless needed.

Risk: Meeting deletion is irreversible and meeting host links are sensitive.

Mitigation: Require explicit confirmation before creating or deleting meetings, use --yes only after confirming deletion, and share attendee links rather than host links.

## Reference(s):

- [Source repository](https://github.com/mebusw/zoom-meeting-admin)
- [ClawHub skill release](https://clawhub.ai/mebusw/skills/zoom-meeting-admin)
- [Zoom App Marketplace](https://marketplace.zoom.us/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with meeting details and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include meeting IDs, attendee links, user details, and recording information; never disclose credentials or host links.]

## Skill Version(s):

1.0.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
