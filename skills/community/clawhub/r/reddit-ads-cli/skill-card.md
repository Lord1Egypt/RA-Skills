## Description:

Reddit Ads data analysis and reporting via reddit-ads-cli for checking ad performance, listing campaign entities, exploring targeting, tracking conversion pixels, and generating reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bin-huang](https://clawhub.ai/user/bin-huang)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operators, analysts, and developers use this skill to query Reddit Ads accounts, campaign hierarchy, creatives, audiences, pixels, targeting options, and performance reports through a read-only CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to install an unpinned third-party npm package that will handle Reddit Ads OAuth credentials.

Mitigation: Use a pinned, locally isolated install after verifying the package source and publisher.

Risk: The skill may handle sensitive ad-account data and Reddit Ads OAuth tokens during reporting workflows.

Mitigation: Use least-privilege or short-lived tokens and avoid exposing unrelated environment secrets.

## Reference(s):

- [Reddit Ads CLI Documentation](https://github.com/Bin-Huang/reddit-ads-cli)
- [Reddit Ads API v3 Docs](https://ads-api.reddit.com/docs/v3)
- [Reddit OAuth2 Authentication](https://github.com/reddit-archive/reddit/wiki/OAuth2)
- [ClawHub Skill Page](https://clawhub.ai/bin-huang/skills/reddit-ads-cli)
- [Publisher Profile](https://clawhub.ai/user/bin-huang)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON examples, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides use of a third-party CLI that returns Reddit Ads API data as JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
