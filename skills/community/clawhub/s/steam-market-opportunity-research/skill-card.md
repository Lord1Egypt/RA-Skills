## Description:

Evaluates Steam game niches using comparable titles, player activity, pricing, reviews, and release news to develop evidence-backed opportunity hypotheses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Game developers and market researchers use this skill to compare Steam titles, assess player activity and pricing, identify review themes, and draft qualified game opportunity briefs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Steam research queries and the Crawlora API key are sent to Crawlora's service.

Mitigation: Install only if this disclosure is acceptable, keep CRAWLORA_API_KEY private, and review query parameters before running the helper.

Risk: Returned records consume Crawlora API credits.

Mitigation: Limit query size and check expected credit use before broad searches.

## Reference(s):

- [Steam research endpoint reference](reference/endpoints.md)
- [Crawlora](https://crawlora.net)
- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/steam-market-opportunity-research)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands]

**Output Format:** [Markdown with comparison tables and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separates observed metrics and estimates from commercial hypotheses; includes conflicting evidence and validation steps.]

## Skill Version(s):

1.0.11 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
