## Description: <br>
Integrate with Odoo 17 via XML-RPC API for project, task, calendar, time off, helpdesk, knowledge, document, and timesheet operations with read, create, and update support only. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DVNghiem](https://clawhub.ai/user/DVNghiem) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and developers use this skill to turn assistant requests into Odoo 17 XML-RPC script actions for projects, tasks, calendars, helpdesk, knowledge, documents, time off, and timesheets. It is suited for Odoo workflows where an assistant may read records, create new records, update existing records, post notes, and schedule activities through a configured Odoo account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change real Odoo business records immediately through the configured account. <br>
Mitigation: Install only when the assistant is allowed to act through Odoo, use a dedicated least-privilege API key, and add confirmation for write, note, notify, HR, document, and timesheet actions when appropriate. <br>
Risk: Generic model access through custom_app.py and low-level access through odoo_core.py can broaden the reachable Odoo surface. <br>
Mitigation: Remove or restrict generic custom_app.py and odoo_core.py access if those capabilities are not needed for the deployment. <br>
Risk: The skill may handle sensitive business, HR, document, helpdesk, and timesheet data. <br>
Mitigation: Scope the Odoo account permissions to the minimum required modules and avoid admin credentials. <br>


## Reference(s): <br>
- [Odoo Models Reference](references/odoo-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; executed scripts return JSON on stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Logs are written to stderr, and Odoo credentials are supplied through environment variables.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
