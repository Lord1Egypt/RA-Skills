## Description:

Assists agents with Feishu calendar coordination, including availability checks, meeting creation, event updates or deletion, invitation responses, calendar lookup, and meeting-context preparation from Feishu documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and agents use this skill to coordinate Feishu meetings, find shared availability, manage calendar events, and prepare concise background material before meetings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback script stores Feishu access tokens insecurely.

Mitigation: Prefer the OAuth-backed plugin path; if the script is used, replace the token cache with restricted, user-scoped secure storage before deployment.

Risk: The skill can create, update, notify attendees about, subscribe to, or delete calendar data.

Mitigation: Require explicit user confirmation before calendar-changing actions and restrict Feishu app scopes to the minimum needed.

Risk: The fallback script uses an application token with limitations compared with user OAuth.

Mitigation: Use the plugin tool path with user OAuth for personal calendars and free/busy operations; clearly disclose script-mode limitations when fallback is necessary.

## Reference(s):

- [Feishu Calendar API reference](references/feishu-calendar-api.md)
- [Feishu Open API base endpoint](https://open.feishu.cn/open-apis)
- [ClawHub skill page](https://clawhub.ai/tujinsama/skills/schedule-sync-claw)
- [Publisher profile](https://clawhub.ai/user/tujinsama)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown with structured summaries and inline command or API guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or perform calendar mutations only after user confirmation and appropriate Feishu authorization.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
