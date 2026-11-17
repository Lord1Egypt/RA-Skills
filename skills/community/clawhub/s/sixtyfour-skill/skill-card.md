## Description:

Sixtyfour Skill helps agents enrich leads, research companies, find contact details, score prospects, search for people or companies, and run batch enrichment through the Sixtyfour AI API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rxhxm](https://clawhub.ai/user/rxhxm)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and revenue teams use this skill to connect an agent to Sixtyfour AI for people and company enrichment, contact discovery, lead qualification, prospect search, and batch workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send lead, company, and contact data to Sixtyfour AI.

Mitigation: Use it only when that data transfer is approved and lawful for the intended enrichment workflow.

Risk: Email, phone, and bulk enrichment workflows can involve personal contact data.

Mitigation: Avoid personal email or phone lookups without a lawful basis and review bulk CSV uploads before processing.

Risk: The MCP setup example runs an unpinned npm package with an API key.

Mitigation: Pin or separately review the MCP package before running it, and use a narrowly scoped API key with usage limits.

## Reference(s):

- [Sixtyfour API Detailed Reference](references/api-details.md)
- [Sixtyfour API Docs](https://docs.sixtyfour.ai)
- [Sixtyfour OpenAPI Spec](https://api.sixtyfour.ai/openapi.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl commands, JSON payloads, response examples, and MCP configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce API request examples and configuration that send lead, company, and contact data to Sixtyfour AI.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
