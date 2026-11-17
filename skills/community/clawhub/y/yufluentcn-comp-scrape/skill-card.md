## Description:

Provides batch competitor comparison analysis from user-uploaded CSV exports or authorized API snapshots through the Yufluent cloud harness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metahuan](https://clawhub.ai/user/metahuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and ecommerce operators use this skill to submit their own CSV exports or authorized API snapshots for batch competitor benchmarking across Amazon, Shopify, or TikTok.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload sensitive business data and an API token to a configurable Yufluent endpoint.

Mitigation: Use only data intended for Yufluent, keep TOKENAPI_KEY private, set TOKENAPI_BASE_URL only to a trusted HTTPS service unless deliberately using localhost for development, and verify every CLI file path before execution.

Risk: Competitor comparison output may affect product, pricing, or listing decisions.

Mitigation: Review the source data and generated report before relying on conclusions for commercial decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/metahuan/skills/yufluentcn-comp-scrape)
- [Yufluent homepage](https://claw.changzhiai.com)
- [OpenClaw integration](https://claw.changzhiai.com/app/openclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain text competitor analysis report, with optional JSON from the API client.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TOKENAPI_KEY and accepts competitor data as inline text or a local file path.]

## Skill Version(s):

1.1.2 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
