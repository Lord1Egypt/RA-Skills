## Description:

Helps users manage Todoist tasks, projects, sections, labels, and comments through a connected Maton account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and teams use this skill to find, organize, create, update, or complete items in their connected Todoist account. It also provides guidance for user-approved scheduled or event-driven Todoist actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting an account or changing Todoist data grants access or alters user content.

Mitigation: Review the requested access and confirm each new connection and write, including the target and intended effect, before proceeding.

Risk: Hosted functions and triggers can repeatedly perform actions without a fresh user request.

Mitigation: Review and approve each function, trigger, schedule, and destination separately; disable automations no longer needed.

Risk: Destinations outside Maton-controlled hosts may expose account or event data.

Mitigation: Keep destinations on Maton-controlled hosts unless the user explicitly names and approves another host and the data sent to it.

## Reference(s):

- [Todoist skill on ClawHub](https://clawhub.ai/byungkyu/skills/todoist-api)
- [Todoist API v1 documentation](https://developer.todoist.com/api/v1)
- [Todoist OAuth documentation](https://developer.todoist.com/guides/#oauth)
- [Maton homepage](https://maton.ai)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Guidance]

**Output Format:** [Markdown with command and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Todoist API responses containing account data.]

## Skill Version(s):

1.2.7 (source: ClawHub server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
