## Description: <br>
Guides agents in using tiktok-ads-cli to query TikTok Ads account, campaign, creative, audience, pixel, and reporting data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bin-huang](https://clawhub.ai/user/bin-huang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, analysts, and advertising operators use this skill to retrieve TikTok Ads account details, campaign hierarchy data, performance reports, creatives, audiences, and pixel status through a CLI workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a TikTok OAuth access token, which could expose account data if handled carelessly. <br>
Mitigation: Use a least-privileged token and avoid sharing secrets in chat, command history, logs, or generated output. <br>
Risk: Installing or invoking an unpinned global npm package can introduce supply-chain or version drift risk. <br>
Mitigation: Verify the npm package before installation and prefer a pinned version. <br>
Risk: Incorrect advertiser IDs, filters, or report date ranges can produce misleading analysis. <br>
Mitigation: Confirm advertiser IDs, filters, and date ranges before running report commands or presenting results. <br>
Risk: Commands outside the documented read, report, and list workflows may have unclear effects. <br>
Mitigation: Require explicit user confirmation before running any command outside the documented workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Release](https://clawhub.ai/bin-huang/tiktok-ads-cli) <br>
- [TikTok Marketing API Portal](https://business-api.tiktok.com/portal/docs) <br>
- [TikTok Reporting API](https://business-api.tiktok.com/portal/docs?id=1738864915188737) <br>
- [TikTok Audience Management](https://business-api.tiktok.com/portal/docs?id=1739940570793985) <br>
- [TikTok Pixel API](https://business-api.tiktok.com/portal/docs?id=1739585700402178) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI responses described by the skill are JSON, with pretty-printed and compact output modes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
