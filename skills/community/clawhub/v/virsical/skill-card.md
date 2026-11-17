## Description:

Virsical 威思客智慧空间管理平台集成技能，用于查询或预订会议、创建工单报修、查询访客记录，并支持中英双语交互。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wafer](https://clawhub.ai/user/wafer)

### License/Terms of Use:

MIT-0

## Use Case:

Employees use this skill to work with Virsical workplace services from an agent: query and book meeting rooms, view their meetings, query visitor records, and create facility repair work orders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Virsical authorization codes may appear in chat transcripts during login.

Mitigation: Treat pasted authorization codes as sensitive credentials, avoid sharing transcripts that contain them, and prefer a safer OAuth or device-code flow when available.

Risk: Local token files are created under the skill directory.

Mitigation: Restrict local filesystem access, avoid committing runtime token data, and use the skill logout flow to clear stored tokens when access is no longer needed.

Risk: The release evidence reports a recoverable embedded OAuth client credential.

Mitigation: Publisher review should remove and rotate the embedded client secret before broad deployment.

Risk: The skill can create live meeting bookings and facility work orders.

Mitigation: Require explicit user confirmation before executing bookings or work-order creation, including the room, time, project, type, priority, and description.

## Reference(s):

- [Virsical API Reference](references/api_reference.md)
- [Virsical Authentication Flow](references/auth_flow.md)
- [Virsical Command Reference](references/commands.md)
- [Virsical Error Codes](references/error_codes.md)
- [Virsical User Guide](https://www.virsical.com/guide.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python command snippets and structured API result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Chinese/English responses; business results should be summarized rather than exposing raw API JSON.]

## Skill Version(s):

1.0.5 (source: evidence.json release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
