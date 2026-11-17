## Description:

Helps agents look up company CIKs and retrieve SEC EDGAR filer profiles, filings, XBRL financial facts, and full-text filing search results through Scavio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, analysts, and developers use the skill to resolve tickers to CIKs, review company filings and reported financial concepts, and search filing documents for public-company research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries are sent through Scavio, including any sensitive search terms.

Mitigation: Use only when comfortable with Scavio as an intermediary; avoid sending confidential search terms.

Risk: An exposed API key or unnecessary requests can consume paid credits.

Mitigation: Keep SCAVIO_API_KEY out of source control and monitor credit usage.

Risk: Incomplete filing history or search coverage may be mistaken for a complete record.

Mitigation: Check history truncation and search date coverage before drawing conclusions.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/scavio-ai/skills/sec-edgar-api)
- [Scavio SEC EDGAR API documentation](https://scavio.dev/docs/sec-edgar-lookup?utm_source=agent-skills&utm_medium=skill&utm_campaign=sec-edgar-api)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=sec-edgar-api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown prose with structured filing data, document links, and optional code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Filing-backed figures should identify their source; API responses are structured JSON.]

## Skill Version(s):

1.0.4 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
