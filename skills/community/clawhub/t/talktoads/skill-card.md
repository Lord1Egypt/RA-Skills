## Description:

Lets an AI agent review Meta ad performance, audit accounts, boost Instagram posts, and create or manage campaigns that remain paused until the user approves launch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theindianappguy](https://clawhub.ai/user/theindianappguy)

### License/Terms of Use:

MIT-0

## Use Case:

External users who manage Facebook and Instagram ad accounts can review performance, audit spend, and prepare or manage campaigns through their AI agent. The skill requires explicit user direction before campaigns go live or budgets are raised.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags automatic saving of brand preferences without a privacy notice; the review is incomplete because a referenced path could not be resolved.

Mitigation: Review what preferences are stored and what controls are available before connecting the ad account.

Risk: Campaign activation and budget changes can affect advertising spend.

Mitigation: Keep campaigns paused until the user explicitly approves launch, and do not raise budgets without the user's request.

## Reference(s):

- [TalkToAds homepage](https://talktoads.com/?ref=openclaw)
- [TalkToAds MCP server](https://talktoads.com/mcp)
- [ClawHub release page](https://clawhub.ai/theindianappguy/skills/talktoads)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Configuration]

**Output Format:** [Markdown performance summaries and reports, plus structured Meta campaign configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Campaigns created by the skill start paused; activation requires an explicit user request.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
