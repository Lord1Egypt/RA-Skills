## Description:

Query whether a phone number is registered on WhatsApp, using the wa-check-api MCP service when configured or the documented REST API fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuqling](https://clawhub.ai/user/zhuqling)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check whether a supplied phone number is registered on WhatsApp. It is useful for single-number verification workflows where the user has authorization to query the number and can provide the country code when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queried phone numbers are sent to wa-check-api.whatsabot.com or a configured MCP service.

Mitigation: Use the skill only for authorized checks and only in deployments where sending the number to that provider is acceptable.

Risk: API keys are required for REST API use and could be exposed if placed directly in prompts, code, or logs.

Mitigation: Store API keys in a protected secret store and avoid printing or sharing them.

Risk: The capability could be misused for unauthorized or bulk number enumeration.

Mitigation: Avoid checking numbers without authorization and apply retention, redaction, rate-limit, and abuse-control policies.

## Reference(s):

- [WhatsApp Number Checker API](references/api.md)
- [wa-check-api service](https://wa-check-api.whatsabot.com)
- [ClawHub skill page](https://clawhub.ai/zhuqling/skills/wa-number-checker)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown or text responses with optional JSON, code, and cURL examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call an MCP tool or external REST API and returns a registered/not registered interpretation plus concise error guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
