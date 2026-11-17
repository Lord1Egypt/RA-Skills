## Description:

Run bulk corporate cold-email campaigns through the UpKuaJing Open Platform API and track task, delivery, open, click, and read status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External business users, exporters, sourcing agents, and sales teams use this skill to submit B2B email campaigns, inspect email task records, and review campaign performance signals through an UpKuaJing API account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email sending can incur account fees.

Mitigation: Confirm recipients, content, and current pricing before any send operation.

Risk: API-key handling may expose credentials if keys are passed on the command line or stored loosely.

Mitigation: Use UPKUAJING_API_KEY from a locked-down environment file and avoid command-line API-key arguments.

Risk: Normal API use performs an automatic vendor version check.

Mitigation: Install only in environments where this additional vendor network call is acceptable.

Risk: Error reports can expose sensitive campaign data if submitted with email bodies, recipient lists, or secrets.

Mitigation: Review and redact error-report context and request details before reporting failures.

## Reference(s):

- [UpKuaJing Skill Page](https://clawhub.ai/upkuajing/skills/upkuajing-email-tool)
- [UpKuaJing Publisher Profile](https://clawhub.ai/user/upkuajing)
- [UpKuaJing Homepage](https://www.upkuajing.com)
- [UpKuaJing Open Platform](https://developer.upkuajing.com/)
- [UpKuaJing OpenAPI Pricing](https://www.upkuajing.com/web/openapi/price.html)
- [Email Send API](artifact/references/email-send-api.md)
- [Email Task List API](artifact/references/email-task-list-api.md)
- [Email Task Record List API](artifact/references/email-task-record-list-api.md)
- [Skill Error Report API](artifact/references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and UPKUAJING_API_KEY; email sending may incur account fees.]

## Skill Version(s):

1.0.4 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
