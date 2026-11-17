## Description:

Create, edit, and report on X (Twitter) ads from an AI agent through the AdKit MCP connector, including campaigns, ad groups, promoted posts, account defaults, and results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeannen](https://clawhub.ai/user/jeannen)

### License/Terms of Use:

MIT-0

## Use Case:

External advertisers and campaign managers use the skill to manage X ad campaigns, ad groups, promoted posts, account defaults, and reporting through AdKit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment rates the skill suspicious because account defaults may change without the user approval its workflow promises.

Mitigation: Review the approval behavior before use and confirm with the user that each intended account-default change is approved, since those changes take effect immediately.

## Reference(s):

- [AdKit X Ads setup and feature guide](https://adkit.so/features/ads-mcp/x)
- [X Ads API documentation](https://docs.x.com/x-ads-api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Configuration instructions, API calls]

**Output Format:** [Markdown guidance with shell command snippets and structured AdKit API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include campaign, ad group, promoted post, and reporting details; account-default updates may take effect immediately.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
