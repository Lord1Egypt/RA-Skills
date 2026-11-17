## Description:

在 Windows 上抓取 VisPatrol 设备实时抓拍；仅允许在用户明确批准后读取本机 %TEMP%/vpup.json 以执行只读抓拍查询。

This skill is ready for commercial/non-commercial use.

## Publisher:

[baymax1957](https://clawhub.ai/user/baymax1957)

### License/Terms of Use:

MIT-0

## Use Case:

Operators and support teams use this skill on trusted Windows hosts to retrieve real-time VisPatrol snapshots for a named device, or all configured devices after separate confirmation, and return a concise capture report with image attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access local VisPatrol session material and use it to query camera inventory and snapshots.

Mitigation: Deploy only on trusted Windows hosts, require explicit approval before each run, and prefer named-device queries.

Risk: All-device capture can retrieve and forward more camera images than the user intended.

Mitigation: Require a separate confirmation before any all-device capture and ask for a specific device when scope is ambiguous.

Risk: Captured images are written to disk and may persist after the query.

Mitigation: Use approved snapshot directories, define retention expectations, and remove generated images when they are no longer needed.

Risk: Authenticated service behavior may exceed the skill's read-only framing if endpoints or permissions are not reviewed.

Mitigation: Review the code and service permissions before production use, enforce read-only snapshot endpoints, and redact secrets from logs and outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baymax1957/skills/vispatrol-picture)
- [Security Boundary](artifact/SECURITY.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown report with JSON-derived snapshot details and image file attachments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires approval before reading %TEMP%/vpup.json; all-device capture requires a separate confirmation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
