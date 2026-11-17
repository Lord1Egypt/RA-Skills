## Description:

TikTok Ads data analysis and reporting via tiktok-ads-cli for checking ad performance, pulling campaign, ad group, and ad stats, managing audiences, inspecting creatives, checking pixel tracking, and creating async reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bin-huang](https://clawhub.ai/user/bin-huang)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, advertisers, and developers use this skill to query TikTok Ads accounts, campaigns, ad groups, ads, reports, creatives, audiences, and pixel tracking through a CLI-backed workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unpinned global third-party CLI.

Mitigation: Prefer a pinned, verified, project-local CLI installation before using the skill in a production or commercial workflow.

Risk: The skill requires TikTok OAuth credentials and may expose account or advertising data if tokens are mishandled.

Mitigation: Use least-privilege, short-lived TikTok tokens; store credentials privately; and do not paste tokens into chat, logs, or shared files.

Risk: Audience-related commands may involve sensitive advertising audience data, and the available evidence does not fully prove they are read-only.

Mitigation: Confirm command permissions and account access scope before granting credentials for audience workflows.

## Reference(s):

- [tiktok-ads-cli documentation](https://github.com/Bin-Huang/tiktok-ads-cli)
- [TikTok Marketing API portal](https://business-api.tiktok.com/portal/docs)
- [TikTok Reporting API](https://business-api.tiktok.com/portal/docs?id=1738864915188737)
- [TikTok Audience Management](https://business-api.tiktok.com/portal/docs?id=1739940570793985)
- [TikTok Pixel API](https://business-api.tiktok.com/portal/docs?id=1739585700402178)
- [ClawHub skill page](https://clawhub.ai/bin-huang/skills/tiktok-ads-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include TikTok Ads CLI commands, credential setup guidance, report query parameters, pagination guidance, and summaries of JSON API responses.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
