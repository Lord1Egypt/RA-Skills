## Description:

Guides agents through using fetcher.sh's paid, read-only TikTok data API for keyword search, profile and post lookup, followers, hashtags, sounds, locations, and comments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fetcher-sh](https://clawhub.ai/user/fetcher-sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent builders use this skill to select TikTok data endpoints, form authenticated GET requests, and collect JSON data for trend tracking, hashtag monitoring, profile analysis, and data pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests send TikTok search terms, profile or post IDs, and API or payment credentials to fetcher.sh.

Mitigation: Confirm the data-sharing posture before installation and keep Bearer keys or x402 payment credentials scoped and protected.

Risk: Each paid API call can consume prepaid credits or trigger x402 payment.

Mitigation: Use budget controls, monitor balances, and test with low-volume calls before running automated collection.

Risk: Collected TikTok followers, comments, and monitoring data may carry terms, privacy, or compliance obligations.

Mitigation: Review TikTok terms and applicable privacy requirements before collecting or storing social-media data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fetcher-sh/skills/tiktok-api)
- [Server-Resolved GitHub Provenance](https://github.com/fetcher-sh/fetcher-skills/tree/main/skills/tiktok-api)
- [TikTok API Endpoint Reference](references/endpoints.md)
- [TikTok Scenario Cookbook](references/scenarios.md)
- [TikTok API FAQ](references/faq.md)
- [TikTok Data Access Comparison](references/comparison.md)
- [OpenAPI 3.1 Contract](https://tiktok.fetcher.sh/openapi.json)
- [Condensed Agent Catalog](https://tiktok.fetcher.sh/llms.txt)
- [Full Agent Setup](https://tiktok.fetcher.sh/skill.md)
- [Service Site](https://tiktok.fetcher.sh)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline bash, JSON, and endpoint examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces read-only API usage guidance; API responses are JSON from fetcher.sh.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
