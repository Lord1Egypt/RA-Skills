## Description: <br>
人群宇宙投放追踪周报自动生成工具，面向小红书投放分析场景，自动拉取 RedBI 数据，对比人群宇宙与整体种草效果，分层客户优先级，并生成 HTML 周报和 Redoc 在线文档。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[peike-boop](https://clawhub.ai/user/peike-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business operations and advertising analysis teams use this skill to produce weekly audience-universe campaign tracking reports for a selected industry, week, and RedBI dashboard. It helps compare audience-universe spend and efficiency against overall seeding performance, prioritize customers, and publish stakeholder-ready HTML and Redoc reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses SSO credentials to access RedBI data. <br>
Mitigation: Run it only in an authorized internal environment and confirm that local SSO cookie use is acceptable before execution. <br>
Risk: Generated reports may publish sensitive campaign, customer, and performance data. <br>
Mitigation: Confirm the dashboard scope, report recipients, Redoc visibility, and preview-server lifetime before sharing any output. <br>
Risk: Incorrect dashboard or report scope could expose or summarize the wrong business data. <br>
Mitigation: Validate the industry, week, RedBI dashboard link, and audience-package scope with the requester before data retrieval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/peike-boop/xhs-universe-weekly) <br>
- [Publisher profile](https://clawhub.ai/user/peike-boop) <br>
- [Dashboard reference](artifact/references/dashboard.md) <br>
- [HTML generation rules](artifact/references/html-rules.md) <br>
- [RedBI dashboard](https://redbi.devops.xiaohongshu.com/dashboard/list?dashboardId=45500&pageId=page_pWvbwhxFPz&projectId=4) <br>
- [Reference Redoc report](https://docs.xiaohongshu.com/doc/49ba86d5dcd0e5fe8d0f96c99f152d78) <br>
- [Skill usage guide](https://docs.xiaohongshu.com/doc/86833739ca1981f4212f3c1adcc87d33) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [HTML report, Redoc Markdown document, local preview URL, published document URL, CSV-derived tables, and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated reports may include embedded base64 cover images, customer segmentation tables, KPI cards, trend tables, and action recommendations.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
