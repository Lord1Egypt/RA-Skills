## Description:

Summarizes sampled Reddit discussion about a publicly traded company or ticker and, when useful, compares it with same-window Yahoo Finance price context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Investors and researchers can review a bounded sample of public Reddit discussion about a verified security, identify contrasting themes, and optionally compare it with dated price context. The brief is not investment advice or a trading signal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Crawlora API receives the API key and finance and Reddit lookup terms.

Mitigation: Use a dedicated API key and exclude private information from search terms.

Risk: Sampled Reddit posts may not represent broader investor sentiment or predict price movement.

Mitigation: Report sample sizes and coverage limits, separate discussion from observed prices, and do not treat the brief as investment advice.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/crawlora-org/skills/reddit-stock-sentiment-research)
- [Endpoint reference](artifact/reference/endpoints.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown research brief with a theme table and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes security identity, sample scope and counts, dated price context when useful, coverage limits, and unanswered questions.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
