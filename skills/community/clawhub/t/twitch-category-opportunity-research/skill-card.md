## Description:

Compares Twitch categories using Crawlora live snapshots and channel content to help creators shortlist categories and plan content while preserving sampling and audience limitations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and content planners use this skill to compare specified Twitch categories, assess observed live-stream concentration, and develop testable content ideas without treating snapshots as audience or revenue forecasts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Crawlora API key and sends Twitch research queries to Crawlora.

Mitigation: Use a key only if comfortable with this disclosure, and scope requests to intended categories and channels.

Risk: Public, sampled live snapshots could be mistaken for complete competition data or audience and revenue forecasts.

Mitigation: Preserve sample limits and observation times; label conclusions as source-bounded hypotheses rather than predictions.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/twitch-category-opportunity-research)
- [Twitch endpoint reference](reference/endpoints.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown brief with a snapshot ledger, concentration table, content examples, and testable hypotheses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retains source dates, collection times, sample sizes, and uncertainty; does not predict audience or revenue.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
