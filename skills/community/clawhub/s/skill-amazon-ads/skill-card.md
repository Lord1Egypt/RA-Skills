## Description: <br>
Amazon Ads API v3 skill for OpenClaw agents to list advertiser profiles, inspect Sponsored Products campaigns, and summarize budgets and performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zero2Ai-hub](https://clawhub.ai/user/Zero2Ai-hub) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External advertisers, agencies, and developers use this skill to connect an OpenClaw agent to Amazon Ads, list advertiser profiles, retrieve Sponsored Products campaign data, summarize campaign state and budgets, and optionally save campaign JSON for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local Amazon Ads credentials can expose advertiser profile data if committed, shared, or stored with broad permissions. <br>
Mitigation: Keep amazon-ads-api.json outside source control with restrictive permissions, use dedicated or least-privilege credentials where possible, and rotate the refresh token if it is exposed. <br>
Risk: The optional output path can write campaign data to a local file that may be misplaced or exposed. <br>
Mitigation: Choose an explicit output path, review file permissions, and avoid writing reports into shared or public directories. <br>
Risk: The release text describes broader campaign management, while the reviewed security evidence characterizes this version as a read/reporting helper. <br>
Mitigation: Treat this version as a reporting helper unless future release evidence validates broader campaign modification behavior. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Zero2Ai-hub/skill-amazon-ads) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with Node.js shell commands and JSON credential/output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and a local amazon-ads-api.json credentials file referenced by AMAZON_ADS_PATH or the working directory; campaign JSON can be written with --out.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
