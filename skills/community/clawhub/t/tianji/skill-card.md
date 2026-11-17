## Description:

Query website analytics, monitor uptime, survey results, telemetry data, feed events, application stats, and more from the Tianji platform via its read-only OpenAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moonrailgun](https://clawhub.ai/user/moonrailgun)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and analytics teams use this skill to query Tianji workspace data such as website traffic, uptime monitor status, survey feedback, telemetry, feed events, billing usage, and audit activity through read-only API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose broad read-only Tianji workspace data, including audit logs, member information, billing details, worker code, survey responses, and AI gateway records.

Mitigation: Install it only for authorized Tianji workspaces, use a trusted HTTPS base URL, and provide the narrowest read-only API key that supports the intended task.

Risk: Some API responses may include secrets or personal information, including API keys, tokens, passwords, credentials, member emails, or raw survey details.

Mitigation: Redact or omit sensitive fields before presenting results, and avoid querying high-sensitivity domains unless the user has explicitly authorized that access.

## Reference(s):

- [Tianji API Endpoints](references/api-endpoints.md)
- [Tianji OpenAPI Read-Only Specification](references/openapi-readonly.json)
- [ClawHub Skill Page](https://clawhub.ai/moonrailgun/skills/tianji)
- [Tianji Repository](https://github.com/msgbyte/tianji)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries with optional shell command examples and JSON-derived results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [API responses should be summarized with sensitive fields redacted or omitted.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
