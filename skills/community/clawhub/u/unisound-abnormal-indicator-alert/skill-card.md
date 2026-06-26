## Description: <br>
Alerts on abnormal chronic-disease indicators such as glucose, blood pressure, and heart rate using caller-supplied thresholds and remote medical model analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Health application and care-management developers use this skill to flag patient-side chronic-disease measurements against supplied thresholds and generate an explanatory alert. The output is for monitoring and follow-up support, not diagnosis or treatment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive health indicators and related context are sent to a remote medical model service. <br>
Mitigation: Use the skill only when users and administrators accept that data flow, minimize submitted context, and apply appropriate privacy controls. <br>
Risk: The app key is a sensitive credential required for remote model access. <br>
Mitigation: Store and pass the key through a secure secret mechanism and keep it out of command history, process logs, and committed files. <br>
Risk: Untrusted PDF, DOC, XLS, or image inputs may exercise broad document conversion and OCR paths. <br>
Mitigation: Prefer structured JSON or CSV inputs; run document conversion and OCR in a sandbox when handling untrusted files. <br>
Risk: Generated medical explanations could be mistaken for diagnosis or treatment advice. <br>
Mitigation: Present results as threshold-based monitoring alerts and require qualified clinical review for medical decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-abnormal-indicator-alert) <br>
- [Unisound-LLM publisher profile](https://clawhub.ai/user/unisound-llm) <br>
- [Open Wearables](https://openwearables.io/) <br>
- [Hivoice MaaS chat completions endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [json, markdown, text, guidance] <br>
**Output Format:** [UTF-8 JSON containing structured alert fields and Markdown explanatory text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes abnormality status, alert level, rule-based reasons, and model-generated explanatory guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
