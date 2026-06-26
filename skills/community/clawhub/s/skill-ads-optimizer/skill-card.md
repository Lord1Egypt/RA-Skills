## Description: <br>
Amazon Ads API v3 skill for OpenClaw agents. List profiles, manage Sponsored Products campaigns, view budgets and performance. Works with any advertiser account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zero2Ai-hub](https://clawhub.ai/user/Zero2Ai-hub) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Advertisers, ecommerce operators, and agents use this skill to connect to Amazon Ads, list advertiser profiles, inspect Sponsored Products campaigns, and summarize active campaign budgets and performance data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads Amazon Ads credentials from amazon-ads-api.json or AMAZON_ADS_PATH. <br>
Mitigation: Keep the credentials file out of source control, restrict filesystem permissions, and use the least-privileged Amazon Ads access available. <br>
Risk: The script can write campaign output to a user-provided --out path. <br>
Mitigation: Review the output path before execution and avoid writing campaign data into shared or public locations. <br>
Risk: The release should be treated as a reporting tool rather than a true bid or keyword optimizer. <br>
Mitigation: Review campaign data and optimization decisions before taking account-changing actions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Zero2Ai-hub/skill-ads-optimizer) <br>
- [Related Amazon SP-API skill](https://github.com/Zero2Ai-hub/skill-amazon-spapi) <br>
- [Amazon OAuth token endpoint](https://api.amazon.com/auth/o2/token) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples; script output is text summaries or JSON files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and an Amazon Ads credentials file referenced by AMAZON_ADS_PATH or ./amazon-ads-api.json.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
