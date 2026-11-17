## Description:

Checks phone numbers, WhatsApp status, email addresses, and website domains through the UpKuaJing Open Platform API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External users, sales teams, recruiters, and export businesses use this skill to validate contact records before outreach, CRM cleansing, candidate screening, supplier checks, and buyer verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid validation calls and account top-ups can incur charges.

Mitigation: Inform users about paid operations and wait for explicit confirmation before running fee-incurring calls or creating top-up orders.

Risk: Phone numbers, email addresses, domains, and optional error reports may contain personal or customer data sent to UpKuaJing.

Mitigation: Submit only data needed for the validation task and avoid including unnecessary personal or customer data in error reports.

Risk: The UpKuaJing API key is a secret that may be stored in ~/.upkuajing/.env.

Mitigation: Protect the API key as a secret, restrict access to the env file, and avoid sharing it in prompts, logs, or reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/upkuajing-contact-info-validity-check)
- [UpKuaJing publisher profile](https://clawhub.ai/user/upkuajing)
- [UpKuaJing homepage](https://www.upkuajing.com)
- [UpKuaJing Open Platform](https://developer.upkuajing.com/)
- [Detailed price description](https://www.upkuajing.com/web/openapi/price.html)
- [Phone validity API reference](references/phone-api.md)
- [Email validity API reference](references/email-api.md)
- [Domain validity API reference](references/domain-api.md)
- [Skill error report API reference](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON validation-result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Validation results include totals, result lists, fee information, and request IDs when returned by the API.]

## Skill Version(s):

1.0.4 (source: server release metadata and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
