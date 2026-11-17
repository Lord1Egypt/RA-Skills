## Description:

Helps agents collect and analyze public YouTube content, channels, comments, and transcripts through SocQ.

This skill is ready for commercial/non-commercial use.

## Publisher:

[socq](https://clawhub.ai/user/socq)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, analysts, and developers use this skill to discover and compare public YouTube content, collect channel and audience data, and summarize findings with coverage and credit-usage details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exposing a SocQ API key while accessing the external service.

Mitigation: Keep SOCQ_API_KEY in the environment; do not paste it into prompts, URLs, or shell history.

Risk: Unexpected credit charges from large or repeated remote tasks.

Mitigation: Check estimated credits and account spending limits; get confirmation before large or multi-endpoint runs and inspect failed tasks before retrying.

Risk: Fetching an unpinned CLI package at runtime.

Mitigation: Prefer a pinned or managed @socq/cli installation over runtime npx fetching.

## Reference(s):

- [SocQ YouTube API documentation](https://docs.socq.ai/api-manual/youtube)
- [SocQ MCP and CLI integration guide](https://docs.socq.ai/integrations/overview)
- [SocQ agent skill guide](https://docs.socq.ai/integrations/skill)
- [SocQ devtools homepage (skill metadata)](https://github.com/SocQAPI/socq-devtools)
- [YouTube endpoint selection reference](references/platform.md)
- [Billing and cost control reference](references/billing.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include endpoint selection, credit estimates, task status, result counts, coverage limitations, and raw export locations.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
