## Description:

Screens startups listed for sale using Crawlora's TrustMRR marketplace, company records, and daily metric history to support acquisition research and diligence questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Prospective buyers and research analysts use this skill to shortlist startups for sale, compare asking prices and dated revenue history, and identify questions for further acquisition diligence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research requests send the Crawlora API key, search parameters, and selected public website URLs to Crawlora.

Mitigation: Use only if this disclosure is acceptable; keep the key in the environment and limit requests to acquisition research.

Risk: Marketplace asking prices, scores, and revenue claims may be mistaken for audited financials or investment conclusions.

Mitigation: Verify financial claims independently and treat marketplace scores and seller asking prices as diligence inputs, not conclusions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/crawlora-org/skills/startup-acquisition-research)
- [Crawlora API endpoint reference](reference/endpoints.md)
- [TrustMRR FAQ](https://trustmrr.com/faq)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Markdown candidate table with source links and diligence questions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dated metrics, explicitly defined calculations, history coverage, and discrepancies.]

## Skill Version(s):

1.0.13 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
