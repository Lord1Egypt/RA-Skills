## Description:

swagger-skill helps agents query Swagger/OpenAPI specifications, inspect endpoint details, and call matching APIs from natural-language requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minusgod](https://clawhub.ai/user/minusgod)

### License/Terms of Use:

MIT

## Use Case:

Developers and API integrators use this skill to load Swagger/OpenAPI documentation, search for endpoints, inspect request and response schemas, and call APIs with optional token, cookie, or file-upload support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install npm packages into its directory on first import.

Mitigation: Review the code and run it in a controlled environment with expected npm registry access before deployment.

Risk: The skill can send tokens, cookies, API payloads, and uploaded local files to user-supplied API endpoints.

Mitigation: Use trusted HTTPS Swagger URLs and API hosts, scope credentials narrowly, and verify upload destinations before sending credentials or files.

## Reference(s):

- [swagger-skill on ClawHub](https://clawhub.ai/minusgod/skills/swagger-skill)
- [minusgod publisher profile](https://clawhub.ai/user/minusgod)

## Skill Output:

**Output Type(s):** [text, json, api calls, shell commands, configuration, guidance]

**Output Format:** [JSON results and console text, with usage guidance and JavaScript examples in Markdown documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return endpoint summaries, detailed schema information, API responses, upload results, and error messages.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
