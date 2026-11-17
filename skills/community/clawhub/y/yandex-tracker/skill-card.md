## Description:

Manages Yandex Tracker issues, queues, comments, attachments, links, worklogs, searches, and bulk changes through the Python yandex_tracker_client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kandler3](https://clawhub.ai/user/kandler3)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and project teams use this skill to read, create, update, transition, organize, and report on Yandex Tracker data through an agent runtime.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a Yandex Tracker token to read or mutate issue data.

Mitigation: Install only where agent access to the Tracker organization is acceptable, use a least-privilege token, and keep credentials in runtime secrets or environment variables.

Risk: Bulk updates, transitions, moves, comments, attachments, links, and worklog edits can affect multiple Tracker records.

Mitigation: Require clear user authorization, confirm exact issue sets before broad changes, and verify results after mutations or asynchronous bulk operations.

Risk: The skill depends on the external Python yandex_tracker_client package.

Mitigation: Pin or review the dependency before installation where supply-chain controls are required.

## Reference(s):

- [Yandex Tracker](https://tracker.yandex.ru)
- [yandex_tracker_client on PyPI](https://pypi.org/project/yandex-tracker-client/)
- [Yandex OAuth](https://oauth.yandex.ru)
- [Setup and Authentication](references/setup-and-auth.md)
- [Search and Reporting](references/search-and-reporting.md)
- [Issue Lifecycle](references/issue-lifecycle.md)
- [Collaboration Resources](references/collaboration.md)
- [Worklogs and Planning](references/worklogs-and-planning.md)
- [Bulk Operations](references/bulk-operations.md)
- [Object Reference and Errors](references/object-reference.md)
- [OpenClaw Compatibility](references/openclaw.md)
- [ClawHub Skill Page](https://clawhub.ai/kandler3/skills/yandex-tracker)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, concise text reports, and Python or shell snippets as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include confirmed issue keys, structured summaries, API call results, and setup guidance while avoiding secrets in output.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
