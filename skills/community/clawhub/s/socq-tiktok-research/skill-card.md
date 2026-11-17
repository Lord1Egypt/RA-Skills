## Description:

Helps agents discover, collect, and analyze public TikTok data with SocQ, including endpoint selection, credit estimates, and paginated results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[socq](https://clawhub.ai/user/socq)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and developers use this skill to select SocQ TikTok endpoints, estimate credits, collect public posts and account data, and report findings with coverage and collection-time caveats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research queries and collected public TikTok data pass through SocQ; profiles, comments, relationships, and transcripts can raise privacy and retention concerns.

Mitigation: Use only approved public-data research and apply appropriate privacy and retention rules.

Risk: Broad collection can incur unexpected credits or hit API-key limits.

Mitigation: Check endpoint costs, set rate or credit limits, and confirm scope before large runs.

Risk: Installing an unpinned CLI can introduce unexpected changes.

Mitigation: Pin the @socq/cli version in the execution environment.

## Reference(s):

- [SocQ TikTok API documentation](https://docs.socq.ai/api-manual/tiktok)
- [SocQ MCP and CLI documentation](https://docs.socq.ai/integrations/overview)
- [SocQ CLI homepage](https://github.com/SocQAPI/socq-devtools)
- [TikTok endpoint selection and costs](artifact/references/platform.md)
- [SocQ billing guidance](artifact/references/billing.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands]

**Output Format:** [Markdown with optional commands and result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes endpoint, credit usage, task status, result counts, collection time, and coverage caveats when available.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
