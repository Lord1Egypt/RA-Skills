## Description:

Provides read-only guidance and scripts for querying Umeng U-Push application lists, push message details, delivery diagnostics, statistics, trace data, and attribution reports using a user-supplied Umeng session Cookie.

This skill is ready for commercial/non-commercial use.

## Publisher:

[squall0925](https://clawhub.ai/user/squall0925)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to inspect Umeng U-Push account data, troubleshoot delivery issues, and generate read-only reports without using write or message-sending APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full Umeng session Cookies can grant account access if pasted into chat, saved insecurely, or exposed in logs.

Mitigation: Avoid pasting full session Cookies into chat; if the skill is used, use a disposable or least-privilege Umeng account and rotate Cookies or related secrets after use.

Risk: Automatic Cookie extraction and custom authenticated request commands can broaden access beyond the intended read-only workflow.

Mitigation: Do not run automatic Cookie extraction or custom request commands; limit use to reviewed read-only queries and inspect commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/squall0925/skills/umeng-push-helper)
- [ClawHub publisher profile](https://clawhub.ai/user/squall0925)
- [Umeng U-Push console](https://upush.umeng.com)
- [Umeng developer documentation](https://developer.umeng.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Markdown, JSON, HTML reports]

**Output Format:** [Markdown guidance with command examples, structured API summaries, JSON-derived tables, and optional local HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided Umeng authentication Cookie for live queries; documented behavior is read-only.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
