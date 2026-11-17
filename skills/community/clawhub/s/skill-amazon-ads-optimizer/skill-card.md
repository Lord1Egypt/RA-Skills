## Description:

Amazon Ads API v3 skill for OpenClaw agents. List profiles, manage Sponsored Products campaigns, view budgets and performance. Works with any advertiser account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub)

### License/Terms of Use:


## Use Case:

External advertisers, agencies, and e-commerce operators use this skill through OpenClaw agents to list Amazon Ads profiles, inspect Sponsored Products campaigns, review budgets, and export campaign data for analysis.

### Deployment Geography for Use:

North America, Europe, Middle East, and Far East

## Known Risks and Mitigations:

Risk: Durable Amazon Ads credentials may be stored in a local plaintext credentials file.

Mitigation: Use a dedicated least-privilege Amazon Ads app and token, keep the credentials file outside repositories and shared workspaces, restrict file permissions, add the path to .gitignore, and rotate the token if exposure is possible.

Risk: Campaign exports can contain sensitive business data.

Mitigation: Store exported campaign files only in approved locations and limit access to users who are allowed to view advertising performance data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zero2ai-hub/skills/skill-amazon-ads-optimizer)
- [Publisher profile](https://clawhub.ai/user/zero2ai-hub)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent guidance may lead to live Amazon Ads API calls and optional campaign JSON exports.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
