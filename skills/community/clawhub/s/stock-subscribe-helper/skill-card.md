## Description: <br>
Tracks A-share IPO and convertible-bond subscription opportunities from Eastmoney and Jisilu data sources, filters them by user preferences, and sends Feishu reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mc82465](https://clawhub.ai/user/mc82465) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users who monitor China A-share IPO and convertible-bond subscriptions use this skill to fetch current subscription data, filter it by product and market board, and receive operational reminders in Feishu. It is a reminder and workflow automation aid, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends automated Feishu notifications and requires Feishu credentials. <br>
Mitigation: Use a dedicated low-privilege Feishu bot or webhook, store credentials outside source control, and rotate them if exposed. <br>
Risk: Security evidence says the requested Feishu table access may be broader than the code appears to require. <br>
Mitigation: Review whether table read/write tokens are needed for the deployment and avoid granting unused permissions. <br>
Risk: Security evidence flags unsupported safety or certification claims in the artifact. <br>
Mitigation: Treat those claims as unverified and rely on independent review, ClawHub scan results, and deployment-specific testing. <br>
Risk: Market subscription data can be incomplete, delayed, or unsuitable for a user's investment decision. <br>
Mitigation: Verify reminders against official trading, broker, or exchange sources before taking financial action. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mc82465/stock-subscribe-helper) <br>
- [Eastmoney IPO Data API Endpoint](https://datacenter-web.eastmoney.com/api/data/v1/get) <br>
- [Jisilu Convertible Bond Pre-list Endpoint](https://www.jisilu.cn/data/cbnew/pre_list/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Plain text Feishu notifications, console logs, and environment-variable configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu webhook and optional Feishu table credentials supplied through environment variables.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
