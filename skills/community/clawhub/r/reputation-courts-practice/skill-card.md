## Description:

Searches Russian court practice through reputation.ru to find cases, retrieve full document text, or produce synthesized Markdown analysis across arbitration, general jurisdiction, and Supreme Court sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reputationru](https://clawhub.ai/user/reputationru)

### License/Terms of Use:

MIT-0

## Use Case:

External users and legal practitioners use this skill to search Russian court practice, inspect cited case documents, and request synthesized analysis reports for Russian-language legal questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials may be sent to an unintended endpoint if the base URL is changed.

Mitigation: Do not set REPUTATION_BASE_URL unless it is exactly the intended HTTPS reputation.ru service endpoint.

Risk: Persistent MCP authorization configuration can store access credentials locally.

Mitigation: Prefer OAuth where supported, avoid pasting OAuth tokens or callback URLs, and review MCP configuration edits before applying them.

Risk: Search, analysis, and document retrieval use a paid third-party service.

Mitigation: Warn users that calls are billed per the reputation.ru tariff and avoid repeated near-duplicate searches.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/reputationru/skills/reputation-courts-practice)
- [Publisher profile](https://clawhub.ai/user/reputationru)
- [reputation.ru API key page](https://reputation.ru/account/api)
- [reputation.ru API service](https://api.reputation.ru)
- [reputation.ru MCP endpoint](https://api.reputation.ru/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON, shell commands, and optional plain text case documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include case links, case identifiers, setup guidance, and billed API request warnings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
