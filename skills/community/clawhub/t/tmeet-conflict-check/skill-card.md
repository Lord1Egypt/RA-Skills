## Description:

Checks the current account's visible Tencent Meeting list for hard overlaps, short transition gaps, and three-or-more concurrent meetings, or configures a deterministic weekday office-hours watcher that wakes the Agent only for new conflicts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metaphor279](https://clawhub.ai/user/metaphor279)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external users use this skill to check visible Tencent Meeting schedules for overlapping meetings, short transition gaps, and three-or-more concurrent meetings. Users can also configure a quiet office-hours watcher that reports only newly detected conflicts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads meeting metadata visible to the user's Tencent Meeting account.

Mitigation: Use it only with accounts where reading meeting topic, meeting number, and time is acceptable, and keep user-visible results limited to those fields.

Risk: The watcher stores local state and can run in the background when enabled.

Mitigation: Enable the watcher or Windows Task Scheduler only when background checks are desired, and store state in a private local directory.

Risk: Dependency versions may change if installed without review.

Mitigation: Pin reviewed dependency versions before installation.

## Reference(s):

- [会议冲突监测协议](references/conflict-watcher-protocol.md)
- [Windows x64 执行与验收](references/windows-execution.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional NDJSON event handling details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [User-facing results should show only meeting topic, meeting number, time, conflict type, and overlap or gap duration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
