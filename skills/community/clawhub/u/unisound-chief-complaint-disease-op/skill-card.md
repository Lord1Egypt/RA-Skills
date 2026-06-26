## Description: <br>
门诊病历内涵质控：主诉不应使用疾病和操作。给定门诊病历文本，调用内部医疗大模型，输出无缺陷或有缺陷及原因。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical quality-control staff and developers use this skill to check outpatient medical records for the rule that chief complaints should not be expressed as diseases or operations when a symptom-based complaint is required. It returns a concise no-defect or defect finding with the reason for review by qualified medical personnel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical records may contain sensitive patient information and are sent to the configured HiVoice MaaS endpoint for analysis. <br>
Mitigation: Use the skill only when authorized, de-identify records before use, and confirm the endpoint is approved for the data being processed. <br>
Risk: The app key grants access to the model endpoint. <br>
Mitigation: Protect the app key, do not commit it to source control, and avoid sharing it in logs or command histories. <br>
Risk: Prepared or output text can persist medical-record content when saved locally. <br>
Mitigation: Do not use --save-prepared or local output paths for real patient data unless storage is approved and protected. <br>
Risk: Overriding --base can send medical text to an unintended service. <br>
Mitigation: Keep the default endpoint or use only trusted, approved replacement endpoints. <br>
Risk: The result is an automated quality-control aid, not a medical diagnosis or treatment recommendation. <br>
Mitigation: Require review by qualified medical personnel before acting on findings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-chief-complaint-disease-op) <br>
- [HiVoice MaaS chat completions endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Analysis, Files, Shell commands, Guidance] <br>
**Output Format:** [UTF-8 plain text with a no-defect result or defect result and reason] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write the quality-control result to a text output path; optional preprocessing supports txt, pdf, doc, docx, xls, xlsx, csv, and json inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
