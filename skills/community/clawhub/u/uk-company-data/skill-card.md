## Description:

Search the UK Companies House register by name, then pull a company's full register entry, its officers, and its filing history as structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and compliance teams use this skill to search UK company records, inspect company status and filings, and retrieve officer information for KYB, due-diligence, and B2B data workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Scavio API key and makes network requests to third-party API endpoints.

Mitigation: Use a virtual environment or project lockfile where possible and provide SCAVIO_API_KEY only to the process that needs it.

Risk: Officer records can include public personal details such as correspondence address and partial date of birth.

Mitigation: Use officer data only for the requested company check and avoid compiling profiles of private individuals beyond the user's task.

Risk: Broad searches are capped and may not provide exhaustive results.

Mitigation: Narrow search terms when result windows are too broad and avoid presenting broad searches as complete registers.

## Reference(s):

- [Scavio Companies House Search Documentation](https://scavio.dev/docs/companies-house-search)
- [Scavio Rate Limits](https://scavio.dev/docs/rate-limits)
- [ClawHub Skill Page](https://clawhub.ai/scavio-ai/skills/uk-company-data)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API request and response examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCAVIO_API_KEY; API calls return structured JSON from Scavio's Companies House endpoints.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
