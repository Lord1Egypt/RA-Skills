## Description:

Semrush SEO integration with API key authentication. Analyze backlinks, keyword rankings, competitor domains, traffic metrics, and SEO data across organic and paid search channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

SEO, content, and growth teams use this skill to ask an agent for Semrush-backed keyword, backlink, competitor, traffic, and search performance analysis. It helps agents install and use the ClawLink Semrush integration, verify connections, run read-only Semrush API calls, and interpret CSV-like responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a third-party ClawLink plugin and external service that handle the user's Semrush API key.

Mitigation: Use a dedicated and revocable Semrush API key, review the ClawLink plugin version and permissions before enabling it, and revoke the key if the integration is no longer needed.

Risk: Semrush API units are consumed per request, so broad or repeated analysis can exhaust account quota.

Mitigation: Check the account API unit balance before large batches and limit batch size or pagination to the minimum needed for the task.

Risk: Semrush responses are CSV-like text and traffic metrics are modeled estimates, which can lead to parsing mistakes or overconfident conclusions.

Mitigation: Parse responses with delimiter-aware handling, cast numeric columns before aggregation, and label Semrush traffic values as estimates rather than first-party analytics.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hith3sh/skills/semrush-seo)
- [Publisher profile](https://clawhub.ai/user/hith3sh)
- [Semrush API Documentation](https://developers.semrush.com/api/)
- [Semrush Domain Analytics](https://www.semrush.com/domain-analytics/)
- [Semrush Keyword Research](https://www.semrush.com/keyword-research/)
- [Semrush Backlink Analytics](https://www.semrush.com/backlinks/)
- [ClawLink OpenClaw documentation](https://docs.claw-link.dev/openclaw)
- [ClawLink verification](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and CSV-like Semrush response handling notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces read-only Semrush analysis guidance and tool-call instructions; API unit consumption should be checked before large batches.]

## Skill Version(s):

1.0.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
