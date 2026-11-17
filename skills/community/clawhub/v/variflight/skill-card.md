## Description:

Query Variflight flight, rail, weather, price, transfer, and comfort data through the Variflight HTTP API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lyz1990](https://clawhub.ai/user/lyz1990)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to retrieve flight information, train tickets, airport weather, flight prices, route transfers, and travel comfort metrics from Variflight-backed tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports passing the Variflight API key on the command line or storing it in project-local configuration, which can expose the key through shell history, logs, or committed files.

Mitigation: Prefer a trusted secret manager or protected environment variable, avoid command-line API keys and project-level credential files, keep local credential files outside repositories with restrictive permissions such as 600, and rotate any key that may have been exposed.

## Reference(s):

- [Variflight AI](https://ai.variflight.com)
- [Variflight API Endpoint](https://ai.variflight.com/api/v1/mcp/data)
- [ClawHub Skill Page](https://clawhub.ai/lyz1990/skills/variflight)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Variflight API key supplied through a protected environment or local credential file.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
