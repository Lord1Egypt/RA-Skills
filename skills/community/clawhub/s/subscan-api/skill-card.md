## Description:

Subscan API Skill helps agents select Subscan endpoints, query blockchain data such as blocks, accounts, transactions, staking, governance, and assets, and format results for users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[carlhong](https://clawhub.ai/user/carlhong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to query Subscan for on-chain data across supported blockchain networks and receive readable summaries instead of raw API responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and reuses a Subscan API key, which could expose credentials if local files or command logs are mishandled.

Mitigation: Use a limited or revocable API key, avoid sharing the full key, rotate any key pasted into logs, and restrict key-file permissions before deployment.

Risk: A misused API call path could send the API key to an unintended URL.

Mitigation: Restrict calls to intended Subscan API hosts and add URL allowlisting before broad use.

Risk: External API requests may fail, time out, or hit rate limits.

Mitigation: Review errors before retrying, use scoped queries, and follow the skill's retry or parameter-correction guidance.

## Reference(s):

- [Subscan API Skill page](https://clawhub.ai/carlhong/skills/subscan-api)
- [Subscan support documentation](https://support.subscan.io)
- [Subscan Pro account](https://pro.subscan.io)
- [API usage reference](artifact/references/api-usage.md)
- [Endpoint details reference](artifact/references/endpoint-details.yaml)
- [Routing reference](artifact/references/routing.yaml)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summaries with tables, bullet lists, error guidance, and optional raw JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local route and swagger references to choose Subscan API endpoints; may require a Subscan API key.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
