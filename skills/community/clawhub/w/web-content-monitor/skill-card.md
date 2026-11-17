## Description:

网页内容监控助手。监控指定网页的内容变化，检测关键词出现或消失，支持变化时自动告警。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuyongliang-eccom](https://clawhub.ai/user/xuyongliang-eccom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and analysts use this skill to monitor public web pages for content changes and keyword appearances or disappearances, such as competitor updates, policy pages, news updates, and website change alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary URLs supplied for monitoring.

Mitigation: Use only approved, non-sensitive public URLs or add URL allowlisting and validation before use.

Risk: Fetched page contents are saved locally under the user's home directory.

Mitigation: Avoid monitoring sensitive pages unless restrictive file permissions, retention limits, and cleanup procedures are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuyongliang-eccom/skills/web-content-monitor)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and plain-text monitor results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The monitor command reports the target URL, whether content changed, and any newly appeared or disappeared keywords.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
