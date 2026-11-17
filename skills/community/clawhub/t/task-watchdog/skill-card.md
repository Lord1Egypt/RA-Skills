## Description:

挂机任务的守护者。定时检查屏幕进度条，自动关闭干扰性系统或广告弹窗，遇致命错误时发送报警。

This skill is ready for commercial/non-commercial use.

## Publisher:

[anotherj1](https://clawhub.ai/user/anotherj1)

### License/Terms of Use:


## Use Case:

External users can use this agent skill to monitor long-running desktop tasks while away, periodically check visible progress, close disruptive popups, and notify the user when a fatal interruption appears to require human intervention.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may dismiss important system, security, update, permission, crash, storage, or memory warnings while trying to close disruptive popups.

Mitigation: Use the skill only in non-sensitive or isolated desktop sessions, and keep antivirus, update, permission, crash, storage, and memory warnings outside the set of popups the agent may close.

Risk: Unattended screen watching and clicking grants the agent broad control over the active desktop session.

Mitigation: Run it only when that level of desktop control is acceptable, and limit use to the specific long-running task window the user wants monitored.

Risk: Webhook alerts with screenshots may expose sensitive screen contents to the configured endpoint.

Mitigation: Enable webhook screenshots only when the endpoint is controlled by the user and the monitored session does not display sensitive information.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, text]

**Output Format:** [Markdown instructions for agent behavior]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve screen observation, mouse clicks, screenshots, and webhook notifications when configured by the user.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
