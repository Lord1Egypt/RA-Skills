## Description:

Scans M&A, insider, analyst, social, and regulatory rumor signals through AISA for early market-signal analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request early market-signal scans for takeover chatter, insider activity, analyst changes, social/news whispers, and regulatory activity. Its outputs are informational and should be independently verified before any financial decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runtime can send the AISA API key to an arbitrary endpoint if AISA_BASE_URL is set unexpectedly.

Mitigation: Use a scoped and revocable AISA credential, run only in a trusted environment, avoid setting AISA_BASE_URL unless the endpoint is intentionally trusted, and rotate the key after unexpected endpoint use.

Risk: The skill analyzes rumors and early signals that may be unconfirmed or misleading.

Mitigation: Treat results as informational, verify claims against primary market and regulatory sources, and do not rely on the output as financial advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aisadocs/skills/stock-rumors-aisa)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown report with an optional compact JSON summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY; reports unconfirmed market signals and rumor evidence quality.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
