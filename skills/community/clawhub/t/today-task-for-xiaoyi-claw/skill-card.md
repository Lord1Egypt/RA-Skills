## Description:

Pushes completed Xiaoyi Claw or OpenClaw task results to Huawei's negative-screen task notification service using a standard JSON payload.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ganhaiyang3](https://clawhub.ai/user/ganhaiyang3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw or Xiaoyi Claw users use this skill to package completed task results as JSON, preserve Markdown content, and push status updates to Huawei negative-screen notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task names, content, results, timestamps, UID, and authenticated requests may be sent to a fixed Huawei endpoint.

Mitigation: Avoid sensitive task content and install only when that destination and data flow are acceptable.

Risk: Personal API credentials may appear in output or logs.

Mitigation: Restrict access to the credential file, generated logs, and push records; rotate credentials if this version has already run.

Risk: Some documented privacy controls do not match the code behavior.

Mitigation: Review the current security statement and assume fixed-endpoint transmission and local credential-file access when assessing use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ganhaiyang3/skills/today-task-for-xiaoyi-claw)
- [Artifact README](artifact/README.md)
- [Artifact security statement](artifact/SECURITY.md)
- [Huawei negative-screen REST endpoint](https://celia-claw-drcn.ai.dbankcloud.cn/celia-claw/v1/rest-api/skill/execute)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Shell commands, Guidance]

**Output Format:** [JSON status objects and Markdown task content, with CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write logs and optional push records locally; normal execution sends task data to a fixed Huawei endpoint.]

## Skill Version(s):

1.0.26 (source: server release evidence and artifact/version.json, released 2026-04-13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
