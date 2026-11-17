## Description:

Look up U.S. sales tax rates with the ZipTax API for addresses, ZIP codes, coordinates, jurisdiction breakdowns, freight or service taxability, use tax versus sales tax, account metrics, and product taxability codes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericlakich](https://clawhub.ai/user/ericlakich)

### License/Terms of Use:


## Use Case:

External users, developers, and agents use this skill to retrieve and interpret U.S. sales tax rates and taxability details for addresses, postal codes, or coordinates. It can also guide ZipTax API integration and account usage checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled lookup script has unsafe address handling that can run injected local commands when addresses are user-controlled.

Mitigation: Review or patch scripts/lookup.sh before use with user-supplied addresses; prefer direct API calls with safe parameter encoding.

Risk: The metrics path places the API key in the request URL.

Mitigation: Use header-based authentication and avoid putting API keys in query strings.

Risk: Precise addresses or coordinates are sent to ZipTax during live lookups.

Mitigation: Inform users before sending location data and avoid submitting sensitive addresses unless the lookup requires that precision.

## Reference(s):

- [ZipTax API Reference](artifact/references/api-reference.md)
- [ZipTax Platform](https://platform.zip.tax)
- [ZipTax API Base URL](https://api.zip-tax.com)
- [ZipTax OpenAPI Specification](https://raw.githubusercontent.com/ZipTax/ziptax-reference/main/openapi/openapi.json)
- [ZipTax Python SDK](https://github.com/ZipTax/ziptax-python)
- [ZipTax Go SDK](https://github.com/ZipTax/ziptax-go)
- [ZipTax Node.js SDK](https://github.com/ZipTax/ziptax-node)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, API examples, and JSON response interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ZipTax API requests that return JSON; live use requires ZIPTAX_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
