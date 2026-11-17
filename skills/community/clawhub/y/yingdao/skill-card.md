## Description:

影刀 wraps the Yingdao RPA API for authentication, task discovery, task execution, execution log retrieval, and result queries using environment-provided API credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yflmq001](https://clawhub.ai/user/yflmq001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation operators use this skill to connect agents to Yingdao RPA workspaces, inspect schedules and execution logs, start scheduled automation tasks, and read task results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can start real Yingdao RPA automation jobs.

Mitigation: Require explicit human approval before invoking task starts against production schedules and use a dedicated least-privileged Yingdao credential.

Risk: The skill uses sensitive API secrets supplied through environment variables.

Mitigation: Store credentials in a protected environment or secrets manager, avoid logging URLs or request parameters that may expose credentials, and rotate keys if exposure is suspected.

Risk: The dependency requirement allows unpinned newer versions of requests.

Mitigation: Use a pinned lockfile or vetted dependency installation process for production deployments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yflmq001/skills/yingdao)
- [ClawHub Skill Homepage](https://clawhub.ai/yflmq001/yingdao)
- [Publisher Profile](https://clawhub.ai/user/yflmq001)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell snippets; runtime calls return Python dictionaries and lists from Yingdao API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires YINGDAO_ACCESS_KEY_ID and YINGDAO_ACCESS_KEY_SECRET; external requests target Yingdao and WinRobot360 API endpoints.]

## Skill Version(s):

2.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
