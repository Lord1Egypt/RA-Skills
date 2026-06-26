## Description: <br>
Query the X2C personal dashboard to get real-time KPI data, earnings trends, platform views, recent transactions, and earning projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luoyalab](https://clawhub.ai/user/luoyalab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External X2C users and agents use this skill to query personal dashboard metrics such as revenue, ROI, mining status, platform performance, recent transactions, and earning projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an X2C API key and can access private dashboard data. <br>
Mitigation: Store X2C_API_KEY as a secret and do not commit configuration files containing the key. <br>
Risk: Skill outputs may include earnings, transaction records, project performance, and platform metrics. <br>
Mitigation: Review outputs before sharing them outside the account or workspace. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/luoyalab/x2c-real-dashboard) <br>
- [X2C Open API endpoint](https://eumfmgwxwjyagsvqloac.supabase.co/functions/v1/open-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires X2C_API_KEY and returns private account, earnings, transaction, project, and platform metrics from the X2C dashboard API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
