## Description:

A Feishu schedule management skill that creates a personal schedule document, adds and updates schedule entries, tracks status, sends reminders, and supports automatic cleanup of old entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minghu0902](https://clawhub.ai/user/minghu0902)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to manage personal Feishu schedules through natural-language requests, with entries written to a Feishu document and reminders sent through Feishu messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Feishu document read/write and reminder-message access for the schedule workflow.

Mitigation: Install only when those permissions are acceptable for the intended account and workspace.

Risk: The skill stores Feishu document metadata, document token, retention settings, and chat identifier in config.json.

Mitigation: Avoid sharing or committing config.json after configuration, and review stored values before support or migration workflows.

Risk: Old schedule entries are deleted automatically according to the configured retention period.

Mitigation: Check max_retention_days before use and preserve any schedule history that must not be deleted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/minghu0902/skills/schedule-feishu)
- [Publisher profile](https://clawhub.ai/user/minghu0902)
- [Schedule document preview](https://picui.ogmua.cn/s1/2026/03/12/69b2b29e6cc6a.webp)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Markdown, API Calls]

**Output Format:** [Natural-language responses, Feishu document updates, reminder messages, and local JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Feishu document read/write and message permissions; stores document metadata and chat identifier in config.json.]

## Skill Version(s):

1.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
