## Description:

Inspect Reddit Ads campaigns, ad groups, creatives, and reporting data via the Reddit Ads API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect Reddit Ads campaign performance, audit ad group and creative settings, verify account connection state, and safely prepare or execute Reddit Ads API actions through ClawLink.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawLink OAuth access and proxied Reddit Ads API requests create account-control trust risk.

Mitigation: Use the minimum available Reddit Ads permissions, review write previews carefully, and revoke the ClawLink Reddit Ads connection when it is no longer needed.

Risk: Confirmed write operations can affect live advertising campaigns and spend.

Mitigation: Preview and confirm the target resource and intended effect before create, update, delete, launch, pause, or edit actions.

Risk: Tool availability depends on the connected Reddit Ads account, API scopes, and account eligibility.

Mitigation: List connected integrations and the live Reddit Ads tool catalog before use, and verify account eligibility when tools or ad accounts are missing.

## Reference(s):

- [Reddit Ads API documentation](https://ads-api.reddit.com/docs/)
- [ClawLink OpenClaw documentation](https://docs.claw-link.dev/openclaw)
- [ClawLink Reddit Ads connection](https://claw-link.dev/dashboard?add=reddit-ads)
- [ClawHub skill page](https://clawhub.ai/hith3sh/skills/reddit-ads-campaigns)
- [Publisher profile](https://clawhub.ai/user/hith3sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call ClawLink tools for Reddit Ads discovery, read operations, previews, and confirmed write operations.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
