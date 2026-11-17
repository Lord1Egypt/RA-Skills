## Description:

Create, edit, and report on TikTok ads from an AI agent through the AdKit MCP connector: campaigns, ad groups, video ads, Spark Ads, media upload, and results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeannen](https://clawhub.ai/user/jeannen)

### License/Terms of Use:

MIT-0

## Use Case:

Advertisers and marketing operators use this skill to create and manage TikTok campaigns, ad groups, video ads, and Spark Ads through AdKit, then review performance results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected local videos are transferred through AdKit to TikTok.

Mitigation: Disclose the transfer and get the user's approval for each selected file before uploading.

Risk: Publishing ad changes can put campaign content live.

Mitigation: Show the saved draft and wait for the user's approval before publishing it.

## Reference(s):

- [AdKit TikTok Ads setup and product documentation](https://adkit.so/features/ads-mcp/tiktok)
- [TikTok Marketing API v1.3 campaign management reference](https://business-api.tiktok.com/portal/docs/campaign-management-api-reference/v1.3)
- [ClawHub skill release](https://clawhub.ai/jeannen/skills/tiktok-ads)

## Skill Output:

**Output Type(s):** [API Calls, Guidance, Reports]

**Output Format:** [AdKit MCP calls with concise text summaries and performance reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ad changes are prepared as drafts for user review and approval before publication.]

## Skill Version(s):

2.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
