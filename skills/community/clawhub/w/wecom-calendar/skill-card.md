## Description:

Manage WeCom calendars and schedules by creating, querying, updating, and canceling events with support for repeats, reminders, attendees, and timezone settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davinwang](https://clawhub.ai/user/davinwang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage WeCom calendars and schedules from an agent workflow, including event creation, lookup, updates, cancellation, attendees, reminders, recurrence, and timezone-aware scheduling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform live WeCom calendar updates and cancellations.

Mitigation: Use it only where calendar changes are intended and verify schedule_id and cal_id values before update or cancel commands.

Risk: The skill requires WeCom application credentials loaded from environment variables.

Mitigation: Keep the .env file private and grant the WeCom app only the permissions needed for the intended calendar workflow.

Risk: Dependency versions are declared without a lockfile in the artifact evidence.

Mitigation: Pin dependencies with a lockfile before production deployment.

Risk: Some documented calendar and cancellation operations are marked as untested in the artifact documentation.

Mitigation: Test those operations in a non-critical calendar before relying on them for production workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/davinwang/skills/wecom-calendar)
- [WeCom Schedule API Documentation](https://developer.work.weixin.qq.com/document/path/93703)
- [WeCom Calendar API Documentation](https://developer.work.weixin.qq.com/document/path/93707)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WeCom application credentials in environment variables and performs live WeCom calendar API operations.]

## Skill Version(s):

1.1.0 (source: server release evidence, changelog source: user)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
