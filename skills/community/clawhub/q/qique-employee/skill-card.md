## Description:

Helps Qique employees query permitted clinic CRM data and carry out supported, employee-confirmed actions through a local connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qique](https://clawhub.ai/user/qique)

### License/Terms of Use:

MIT-0

## Use Case:

Qique employees use this skill to answer authorized questions about clinic operations, customers, appointments, and reports, and to complete the limited actions currently supported by their permissions and employee confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The separately installed runtime and Chrome extension can access sensitive browser and clinic CRM context.

Mitigation: Install only for authorized Qique users, verify official download hashes, inspect extension permissions, and do not share cookies, tokens, or customer records in chat.

Risk: Unsupported or high-impact operations could change or expose business records.

Mitigation: Honor employee and administrator permissions, restrict actions to supported operations, and require the employee to review and confirm the affected objects through the documented flow.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/qique/skills/qique-employee)
- [Local connection and setup guide](references/setup.md)
- [MCP configuration example](examples/mcp.example.json)
- [Official download hash snapshot](distribution/official-downloads.json)

## Skill Output:

**Output Type(s):** [Text, Guidance, Configuration instructions]

**Output Format:** [Text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers and actions depend on the employee's current access and a separately installed local runtime.]

## Skill Version(s):

0.2.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
