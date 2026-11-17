## Description:

Helps administer Zoom users, meetings, webinars, recordings, and account settings through a user-authorized Maton connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Zoom workspace administrators use this skill to inspect account resources and, with explicit approval, manage users, meetings, webinars, recordings, and settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Admin access can expose or change other users' Zoom resources.

Mitigation: Authorize only the intended account with the minimum scopes, favor read-only requests, and confirm each write and new connection.

Risk: Bulk retrieval of other users' recordings may expose sensitive content.

Mitigation: Avoid bulk access and retrieve only the recordings needed for the approved task.

Risk: Triggers or destinations can send data automatically beyond the immediate task.

Mitigation: Confirm the data, recipient, and retention period before creating any trigger or destination.

## Reference(s):

- [Zoom API documentation](https://developers.zoom.us/docs/api/)
- [Maton documentation](https://docs.maton.ai)
- [Maton](https://maton.ai)
- [Zoom Admin skill release](https://clawhub.ai/byungkyu/skills/zoom-admin-api)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown with command and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations and examples depend on the authorized Zoom account and its available scopes.]

## Skill Version(s):

1.2.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
