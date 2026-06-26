## Description: <br>
Converts Sensors Analytics manuals into standardized Feishu user-guide documents for supported analytics, metadata, audience, LTV, funnel, retention, distribution, and overview modules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bianca1227](https://clawhub.ai/user/bianca1227) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Documentation teams, product operations staff, and analytics administrators use this skill to turn official Sensors Analytics manual pages into Feishu-ready user guides. The skill asks the user to confirm the document framework, fetches official manual content, and creates a structured Feishu document. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches external Sensors Analytics manual pages before generating a document. <br>
Mitigation: Use official manual.sensorsdata.cn links and review fetched content before relying on or sharing the generated Feishu document. <br>
Risk: Generated Feishu documents may contain incorrect, outdated, or overly broad guidance if the source manual content or chosen framework is wrong. <br>
Mitigation: Review the generated document before sharing and confirm that the document framework, module coverage, and screenshots or placeholders match the intended audience. <br>
Risk: Created Feishu documents may be visible to unintended users if workspace permissions are too broad. <br>
Mitigation: Check Feishu permissions on every created document before distribution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bianca1227/sensors-analytics-doc-gen) <br>
- [Sensors Analytics Event Analysis Manual](https://manual.sensorsdata.cn/sa/docs/guide_analytics_event) <br>
- [Sensors Analytics Retention Analysis Manual](https://manual.sensorsdata.cn/sa/docs/guide_analytics_retention) <br>
- [Sensors Analytics Funnel Analysis Manual](https://manual.sensorsdata.cn/sa/docs/guide_analytics_funnel) <br>
- [Sensors Analytics Metadata Manual](https://manual.sensorsdata.cn/sa/docs/guide_metadata_meta/v0205) <br>
- [Sensors Analytics User Group Manual](https://manual.sensorsdata.cn/sa/docs/User_Group_Create/v0205) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown content for Feishu documents plus a concise text summary with document link, document ID, specification notes, and document structure overview.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates Feishu documents from user-provided official Sensors Analytics manual links after the user confirms the document framework.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
