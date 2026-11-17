## Description:

Checks the Google ranking position of a keyword for a target domain using the ValueSERP API, defaulting to Google Colombia in Spanish unless another country or language is requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jorgejaramillo](https://clawhub.ai/user/jorgejaramillo)

### License/Terms of Use:

MIT-0

## Use Case:

SEO practitioners, marketers, and agents use this skill to check where a domain ranks for a specific keyword in Google results and present the result clearly to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a ValueSERP API key and sends search queries to the ValueSERP service.

Mitigation: Use a key scoped to ValueSERP, store it in VALUESERP_API_KEY, and rotate it if exposure is suspected.

Risk: Large page counts can consume API quota or create unexpected costs.

Mitigation: Use modest page counts unless deeper ranking checks are required.

Risk: Default Google Colombia and Spanish settings may not match the intended search market.

Mitigation: Set the country and language options explicitly when another market is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jorgejaramillo/skills/valueserp-rank-checker)
- [ValueSERP Search API documentation](https://www.valueserp.com/docs/search-api/overview)
- [ValueSERP API key portal](https://app.valueserp.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown response backed by JSON results from a command-line API query]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VALUESERP_API_KEY and supports country, language, and page-count options.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
