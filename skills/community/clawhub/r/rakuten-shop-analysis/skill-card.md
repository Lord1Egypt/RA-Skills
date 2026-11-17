## Description:

Analyze a Rakuten shop from a shop URL or shop code via a hosted backend and generate a structured report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abca12a](https://clawhub.ai/user/abca12a)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze Rakuten shop URLs or shop codes for competitor research, shop structure review, popular-item sampling, and report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shop links or shop codes, plus the fact that they are being analyzed, are sent to the hosted backend.

Mitigation: Use the skill only when that data sharing is acceptable, and do not provide credentials or private data as shop input.

Risk: A run may be incomplete if the hosted job times out, is interrupted, or is rate-limited.

Mitigation: Wait for the skill to return final results before reporting; if it does not complete, tell the user the invocation did not finish and ask them to retry later.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/abca12a/skills/rakuten-shop-analysis)
- [Hosted analysis backend](https://rakuten.845817074.xyz)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Structured JSON payload that an agent can summarize as a Markdown report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes shop input, shop code, catalog size, degraded reason codes, available buckets, summary data, and bucket data when returned by the hosted backend.]

## Skill Version(s):

0.1.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
