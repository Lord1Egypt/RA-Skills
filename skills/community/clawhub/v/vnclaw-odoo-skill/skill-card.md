## Description:

Integrate with Odoo 17 via XML-RPC API for managing projects, tasks, calendar events, time off requests, helpdesk tickets, knowledge articles, documents, and timesheets with read, create, and update operations only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dvnghiem](https://clawhub.ai/user/dvnghiem)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers use this skill to translate natural language Odoo 17 requests into authenticated actions for project work, service tickets, calendars, time off, knowledge, documents, timesheets, and custom Odoo models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make broad, immediate changes across an ERP system.

Mitigation: Install only after review and review write, bulk update, note, notification, timesheet, calendar, and leave actions before execution.

Risk: Weak account scoping or transport safeguards could expose or alter sensitive Odoo data.

Mitigation: Use a least-privileged Odoo account, require HTTPS in ODOO_URL, and avoid admin credentials.

Risk: Custom and generic model access can read or modify many Odoo models.

Mitigation: Be especially careful with custom_app.py and odoo_core.py, and limit their use to reviewed models and fields.

## Reference(s):

- [Odoo 17 Models Reference](artifact/references/odoo-models.md)
- [ClawHub Skill Page](https://clawhub.ai/dvnghiem/skills/vnclaw-odoo-skill)

## Skill Output:

**Output Type(s):** [Text, Shell commands, JSON, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Odoo connection settings from environment variables; scripts emit JSON to stdout and logs to stderr.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
