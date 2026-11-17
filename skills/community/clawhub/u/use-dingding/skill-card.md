## Description:

Interact with DingTalk enterprise workspace using the dws CLI. Required: dws CLI, DWS_CLIENT_ID, DWS_CLIENT_SECRET. Use for: contacts, chat, calendar, todo, approvals, attendance, reports, AITable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucezhu888](https://clawhub.ai/user/brucezhu888)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and workplace automation agents use this skill to operate DingTalk workspace workflows through the dws CLI, including contacts, chat, calendar scheduling, todos, approvals, attendance, reports, and AITable records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents remote installer commands for the dws CLI.

Mitigation: Install only from verified releases or a reviewed source build, and avoid pipe-to-shell installer commands.

Risk: The skill can trigger business mutations such as approvals, messages, calendar changes, todos, deletions, and AITable writes.

Mitigation: Keep dry-run as the default, require explicit human review before execution, and block unattended approvals, bulk messaging, deletions, or employee-data queries.

Risk: The skill requires DingTalk OAuth credentials and may access sensitive workspace data.

Mitigation: Use least-privilege DingTalk app permissions, prefer interactive login with encrypted token storage, avoid credential exposure in logs or process listings, and test in a sandbox tenant first.

## Reference(s):

- [Global Reference](references/global-reference.md)
- [Intent Guide](references/intent-guide.md)
- [Error Codes Reference](references/error-codes.md)
- [Contact Product Reference](references/products/contact.md)
- [Chat Product Reference](references/products/chat.md)
- [Calendar Product Reference](references/products/calendar.md)
- [Todo Product Reference](references/products/todo.md)
- [Approval Product Reference](references/products/oa.md)
- [Attendance Product Reference](references/products/attendance.md)
- [Report Product Reference](references/products/report.md)
- [AITable Product Reference](references/products/aitable.md)
- [DingTalk Workspace CLI Repository](https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli)
- [DingTalk Workspace CLI Releases](https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli/releases)
- [DingTalk Open Platform App Console](https://open-dev.dingtalk.com/fe/app)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce dws CLI JSON, table, or raw output when commands are executed.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
