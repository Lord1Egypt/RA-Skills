## Description:

Amazon Ads API v3 skill for OpenClaw agents. List profiles, manage Sponsored Products campaigns, view budgets and performance. Works with any advertiser account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to let OpenClaw agents retrieve Amazon Ads profiles, inspect Sponsored Products campaigns, summarize active and paused campaign budgets, and optionally export campaign data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads an Amazon Ads credential file and uses it to request account and campaign data.

Mitigation: Use credentials scoped only to the intended advertiser accounts and permissions, store the credential file carefully, and avoid sharing it with unrelated agents or users.

Risk: Campaign exports created with --out can contain sensitive advertiser account and campaign information.

Mitigation: Treat exported files as sensitive business data and store, review, and delete them according to the advertiser's data-handling requirements.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zero2ai-hub/skills/skill-ads-optimizer)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and JSON credential examples; runtime output is text summaries or JSON exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and an Amazon Ads credential file configured through AMAZON_ADS_PATH or the default amazon-ads-api.json path.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
