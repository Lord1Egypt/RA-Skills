## Description:

Launch Sentiment Sweep guides an agent through a one-time Reddit and X reaction sweep for a product launch, announcement, release, or news moment, reporting volume, representative quotes, themes, and notable accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[veezee-build](https://clawhub.ai/user/veezee-build)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to gather a one-time, fixed-window readout of Reddit and X reactions to a launch or announcement, including volume, representative verbatim quotes, recurring themes, notable accounts, and credits spent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Launch names, topic terms, and selected public URLs are sent to Veezee during sweeps.

Mitigation: Use the skill only for public or approved topics, and avoid confidential or unreleased launch names without explicit approval.

Risk: The artifact describes an `/all` MCP mount with broader platform coverage than the stated Reddit-and-X purpose.

Mitigation: Prefer the separate Reddit and X MCP endpoints when configuring the skill.

Risk: The artifact mentions running the Veezee CLI through unpinned `npx` package execution.

Mitigation: Review or pin the package before using the CLI path, or use the MCP/API setup surfaces instead.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/veezee-build/skills/veezee-launch-sentiment-sweep)
- [Veezee Reddit MCP endpoint](https://mcp.veezee.io/reddit)
- [Veezee X MCP endpoint](https://mcp.veezee.io/x)
- [Veezee API key mint endpoint](https://api.veezee.io/v1/keys/mint)

## Skill Output:

**Output Type(s):** [Markdown, Text, API calls, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown readout with representative quotes, links, counts, themes, notable accounts, and credit usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Quotes are expected to be verbatim from returned Reddit and X results with real links; no sentiment score is produced by Veezee.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
