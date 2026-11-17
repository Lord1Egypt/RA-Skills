## Description:

Synchronize TickTick (Dida) and Google Tasks bidirectionally, including list/project mapping, task content sync, completion sync, and smart-list export (Today, Next 7 Days, All).

This skill is ready for commercial/non-commercial use.

## Publisher:

[jp1222](https://clawhub.ai/user/jp1222)

### License/Terms of Use:

MIT

## Use Case:

Developers and task-system operators use this skill to configure, run, schedule, and troubleshoot bidirectional synchronization between TickTick and Google Tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically delete real Google Tasks and TickTick data with insufficient safeguards.

Mitigation: Use dedicated test accounts or empty test lists first, avoid cron on important task data until safeguards are added, and add dry-run or confirmation controls before delete propagation.

Risk: OAuth token files can grant access to task data.

Mitigation: Restrict token file permissions and keep configured token paths private.

Risk: A configurable TickTick API endpoint can route requests away from the official service.

Mitigation: Pin the TickTick API base URL to https://api.ticktick.com/open/v1.

## Reference(s):

- [ClawHub Task Sync Skill](https://clawhub.ai/jp1222/skills/task-sync)
- [Google Tasks REST API](https://developers.google.com/workspace/tasks/reference/rest)
- [TickTick Open API](https://developer.ticktick.com/)
- [TickTick Open API Base Endpoint](https://api.ticktick.com/open/v1)
- [OpenClaw](https://openclaw.ai/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration examples, and Python automation files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces task synchronization guidance and executable setup/sync scripts for OAuth-backed Google Tasks and TickTick workflows.]

## Skill Version(s):

2.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
