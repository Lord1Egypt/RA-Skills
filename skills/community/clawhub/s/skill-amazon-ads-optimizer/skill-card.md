## Description: <br>
Amazon Ads API v3 skill for OpenClaw agents to list profiles, manage Sponsored Products campaigns, view budgets, and pull performance data for advertiser accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zero2Ai-hub](https://clawhub.ai/user/Zero2Ai-hub) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External advertisers, e-commerce operators, and agent developers use this skill to let OpenClaw agents retrieve Amazon Ads profiles, campaign status, budgets, and campaign exports for Sponsored Products reporting and optimization workflows. <br>

### Deployment Geography for Use: <br>
North America, Europe and Middle East, and Far East regions supported by the Amazon Ads endpoints listed in the skill. <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive Amazon Ads credentials can expose advertiser account access if the credentials file is committed or shared. <br>
Mitigation: Keep amazon-ads-api.json private, store it outside shared repositories when possible, add it to .gitignore, use restrictive file permissions, and rotate the refresh token if exposed. <br>
Risk: Campaign exports may write advertiser data to an unintended location. <br>
Mitigation: Review any --out path before execution and keep exported campaign data in approved storage locations. <br>
Risk: The skill lets an agent access Amazon Ads profile and campaign data. <br>
Mitigation: Install only when agent access to the intended Amazon Ads account is acceptable, and use credentials scoped to the required Advertising permission and profiles. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Zero2Ai-hub/skill-amazon-ads-optimizer) <br>
- [Zero2AI publisher site](https://zeerotoai.com) <br>
- [Related skill: skill-amazon-spapi](https://github.com/Zero2Ai-hub/skill-amazon-spapi) <br>
- [Related skill: skill-amazon-listing-optimizer](https://github.com/Zero2Ai-hub/skill-amazon-listing-optimizer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; CLI output is text summaries or JSON exports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and Amazon Ads LWA credentials; campaign data can be exported to a user-selected file path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
