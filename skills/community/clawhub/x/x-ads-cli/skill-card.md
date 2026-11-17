## Description:

X Ads CLI helps agents analyze and report on X/Twitter Ads data through the x-ads-cli command-line tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bin-huang](https://clawhub.ai/user/bin-huang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and analysts use this skill to inspect X/Twitter Ads accounts, campaign performance, creatives, targeting, billing, conversion events, and reach estimates through read-only CLI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to install an unpinned global third-party CLI that handles OAuth credentials and sensitive X Ads data.

Mitigation: Prefer a pinned, locally installed, reviewed version of x-ads-cli and verify package source and integrity before use.

Risk: OAuth credentials and ad account data can be exposed through command output, logs, shell history, or shared reports.

Mitigation: Use least-privileged X Ads credentials, avoid printing or sharing secrets, and redact sensitive account, billing, and funding data before sharing outputs.

Risk: Billing and funding-instrument commands can reveal sensitive payment metadata.

Mitigation: Run billing or funding-instrument commands only when the user explicitly intends to inspect that information.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bin-huang/skills/x-ads-cli)
- [x-ads-cli Documentation](https://github.com/Bin-Huang/x-ads-cli)
- [X Ads API Introduction](https://docs.x.com/x-ads-api/introduction)
- [X Ads API Campaign Management](https://docs.x.com/x-ads-api/campaign-management)
- [X Ads API Analytics](https://docs.x.com/x-ads-api/analytics)
- [X Ads API Getting Started](https://docs.x.com/x-ads-api/getting-started)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The referenced CLI returns JSON and may expose sensitive ads, billing, funding, and OAuth-related data.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
