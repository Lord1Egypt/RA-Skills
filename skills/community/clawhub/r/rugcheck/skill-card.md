## Description:

Analyze Solana tokens for rug pull risks using the RugCheck API, including risk score, liquidity, holder distribution, metadata mutability, insider patterns, and token discovery signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psychotechv4](https://clawhub.ai/user/psychotechv4)

### License/Terms of Use:


## Use Case:

Developers, analysts, and agent users use this skill to inspect Solana token risk signals and summarize RugCheck findings before making token safety assessments. It supports single-token checks by mint address and discovery of trending, new, recent, or verified Solana tokens.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Token mint addresses and discovery requests are sent to RugCheck's external API.

Mitigation: Avoid querying sensitive watchlists or unpublished token research when strict privacy is required.

Risk: Risk scores and token signals may be incomplete, stale, or misleading if treated as a sole decision source.

Mitigation: Present RugCheck results as risk indicators and encourage corroboration with liquidity, holder, market, and authority data before acting.

Risk: Repeated discovery or token queries may encounter RugCheck rate limits.

Mitigation: Respect 429 responses and add short delays between bulk-like query sequences.

## Reference(s):

- [RugCheck API](https://api.rugcheck.xyz)
- [RugCheck token pages](https://rugcheck.xyz/tokens/<mint>)
- [ClawHub RugCheck skill page](https://clawhub.ai/psychotechv4/skills/rugcheck)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Markdown, Guidance]

**Output Format:** [JSON responses and Markdown summaries with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses read-only RugCheck endpoints for normal operation; bulk endpoints require wallet JWT authentication and are not available for most agents.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
