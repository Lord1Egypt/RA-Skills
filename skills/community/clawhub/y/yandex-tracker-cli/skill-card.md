## Description:

Yandex Tracker CLI lets agents and developers manage Yandex Tracker queues, issues, comments, worklogs, attachments, and YQL searches from a bash command-line client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bkamuz](https://clawhub.ai/user/bkamuz)

### License/Terms of Use:

MIT

## Use Case:

Developers, engineers, and agent operators use this skill to inspect and manage Yandex Tracker work items, comments, worklogs, projects, sprints, checklists, and attachments through a CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI can delete or modify Yandex Tracker issues, comments, and checklist data without built-in confirmation.

Mitigation: Use the least-privileged OAuth token available and manually confirm issue, comment, checklist, and transition IDs before running destructive commands.

Risk: The security evidence reports that attachment path protections can be bypassed with symlinks.

Mitigation: Use a dedicated attachment directory without symlinks or sensitive files, and avoid downloading to or uploading from sensitive paths.

Risk: Credentials may be stored in the optional ~/.yandex-tracker-env file.

Mitigation: Prefer environment variables where practical, keep any ~/.yandex-tracker-env file private, and restrict file permissions to the owning user.

## Reference(s):

- [Yandex Tracker](https://tracker.yandex.ru/)
- [Yandex Tracker API v2](https://api.tracker.yandex.net/v2)
- [Yandex Tracker API v3](https://api.tracker.yandex.net/v3)
- [ClawHub skill page](https://clawhub.ai/bkamuz/skills/yandex-tracker-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands, JSON examples, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TOKEN and ORG_ID credentials plus curl and jq; API responses are generally JSON or tabular text.]

## Skill Version(s):

1.2.8 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
