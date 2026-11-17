## Description:

Amazon Ads API v3 skill for OpenClaw agents to list advertiser profiles, retrieve Sponsored Products campaigns, view budgets, and summarize campaign performance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub)

### License/Terms of Use:


## Use Case:

Developers and advertisers use this skill to connect an OpenClaw agent to an Amazon Ads account, inspect advertiser profiles, retrieve Sponsored Products campaign data, and generate campaign budget summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an Amazon Ads refresh token and advertiser profile data.

Mitigation: Store amazon-ads-api.json outside version control with restricted permissions and grant the minimum Amazon Ads permissions needed.

Risk: Campaign exports written with --out can contain sensitive business data.

Mitigation: Write exports only to approved locations, restrict file access, and handle exported JSON according to business data policies.

Risk: Some documentation describes broader campaign, keyword, bid, or optimization management than this version implements.

Mitigation: Use this version for profile listing, campaign retrieval, and summaries unless the artifact is updated and rescanned.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zero2ai-hub/skills/skill-amazon-ads)
- [Related Amazon SP-API Skill](https://github.com/Zero2Ai-hub/skill-amazon-spapi)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [Markdown guidance with CLI commands; script output as JSON or plain-text campaign summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and Amazon Ads credentials; optional --out exports campaign data to JSON.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
