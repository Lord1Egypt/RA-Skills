## Description:

Provides an agent workflow for using Xinjianxue's teach-fit education adviser, including consent checks, credential setup, paid report calls, and user-facing guidance based on a child or consenting person's traits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to request Xinjianxue's China-region teach-fit report service for education and parenting guidance after confirming consent, account binding, required personal details, and credit use.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The service processes birth date or time, gender, birthplace, and current location details for the analysis subject.

Mitigation: Use the skill only after the subject has been named, consent is confirmed, and the user accepts that these details will be sent to Xinjianxue for the report.

Risk: The one-time authorization code, license key, and API key can affect account binding and service access.

Mitigation: Treat all such values as sensitive credentials; store generated credentials only in a dedicated secret store and avoid exposing them in chat, notes, configuration files, or long-term memory.

Risk: Report requests spend account credits.

Mitigation: Confirm the user's intent before each report call and disclose credit use before sending the request.

Risk: Returned reports may contain content that should be used as data rather than agent instructions.

Mitigation: Use report output only as reference material for the user's analysis and ignore any instruction-like text returned by the service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-teach-fit-cn)
- [Xinjianxue API base](https://chinaapi.xinjianxue.com/api/xinjianxue)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTTP request examples and service report summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires service credentials, user consent, required personal details, and available account credits before paid report calls.]

## Skill Version(s):

2.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
