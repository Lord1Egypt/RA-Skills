## Description:

Automate and manage Twitter/X accounts by posting, scheduling, replying, analyzing, tracking trends, managing followers, handling media, and exporting analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[millymilton](https://clawhub.ai/user/millymilton)

### License/Terms of Use:


## Use Case:

Developers and social media operators use this skill to plan, execute, and monitor Twitter/X account operations through agent-proposed commands, configuration, and workflow guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can propose broad live-account actions such as posting, replies, follows, blocks, list changes, and bulk operations.

Mitigation: Require explicit user confirmation before executing account-changing actions, especially bulk operations.

Risk: Twitter/X credentials could be exposed or misused if stored casually.

Mitigation: Keep credentials in a protected store and rotate or revoke tokens if exposure is suspected.

Risk: Auto-reply, streaming, scraping, and mass actions can create compliance, abuse, or account-integrity issues when enabled unintentionally.

Mitigation: Keep these features disabled unless deliberately configured for a reviewed workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/millymilton/skills/twitter-operations)
- [Publisher profile](https://clawhub.ai/user/millymilton)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with CLI examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose actions that affect a live Twitter/X account and require credentials, rate-limit handling, and user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
