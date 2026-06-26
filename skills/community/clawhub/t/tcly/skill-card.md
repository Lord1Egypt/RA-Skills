## Description: <br>
Travel In China is a bilingual assistant that collects inbound China travel requirements and submits structured lead details to a configured Feishu Bitable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lijingxu007](https://clawhub.ai/user/lijingxu007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel service teams and agents use this skill to collect overseas travelers' China trip requirements, confirm key details in Chinese or English, and send the structured intake record to Feishu Bitable for follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill submits travelers' contact and trip details to the configured Feishu Bitable. <br>
Mitigation: Use a dedicated Feishu app and table with minimal permissions, protect the App Secret, and obtain explicit consent before submission. <br>
Risk: The listing and skill text advertise itinerary search, update, and delete behavior that is not supported by the artifact-backed tool implementation. <br>
Mitigation: Treat those features as unavailable unless the publisher adds matching tools, documentation, and safeguards. <br>


## Reference(s): <br>
- [Travel In China ClawHub listing](https://clawhub.ai/lijingxu007/tcly) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Guidance] <br>
**Output Format:** [Markdown or plain text conversation responses with structured Feishu Bitable submissions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FEISHU_APP_ID, FEISHU_APP_SECRET, FEISHU_BASE_TOKEN, and FEISHU_TABLE_ID environment variables.] <br>

## Skill Version(s): <br>
2.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
