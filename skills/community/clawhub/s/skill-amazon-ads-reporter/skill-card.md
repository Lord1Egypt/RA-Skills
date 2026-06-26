## Description: <br>
Fetches Amazon Ads Sponsored Products keyword reporting and live bid data using Amazon Ads credentials supplied by the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Advertisers, operators, and developers who manage Amazon Sponsored Products campaigns use this skill to inspect keyword bids and generate keyword-level performance analysis from their own Amazon Ads profile. <br>

### Deployment Geography for Use: <br>
Europe, Middle East, and Africa (EMEA); the included scripts use Amazon Ads EU endpoints. <br>

## Known Risks and Mitigations: <br>
Risk: The scripts read an Amazon Ads OAuth credential file and exchange the refresh token for access tokens. <br>
Mitigation: Use credentials scoped only to the intended advertising profile, store the credential file securely, and rotate or revoke tokens when access is no longer needed. <br>
Risk: The current implementation is EU-focused and uses Amazon Ads EU endpoints. <br>
Mitigation: Confirm the advertising profile region and endpoint before running the scripts against non-EU accounts. <br>
Risk: The documentation references campaign-level commands whose scripts are not included in this artifact. <br>
Mitigation: Use only the included keyword-report.js and get-bids.js commands unless the missing scripts are supplied and reviewed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zero2ai-hub/skill-amazon-ads-reporter) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands, JSON credential examples, console tables, and JSON report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the configured Amazon Ads profile and credential file; included scripts may write temporary report state and print keyword or bid tables.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
