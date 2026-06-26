## Description: <br>
基于“多模型并行推理、主动抗辩”的低幻觉（国家发明专利）独有模式，快速为用户提供精准的、个性化的疾病诊断、智能荐药、推拿按摩、针灸等服务，并推荐对应的检测机构、治疗机构。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lantian888](https://clawhub.ai/user/lantian888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users describe symptoms to receive a guided medical intake, follow-up questions, and a structured diagnostic report with medication, daily-care, and high-risk warning guidance. The skill is for general information and should not be treated as a licensed medical diagnosis or medication plan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides diagnosis and medication guidance for medical symptoms. <br>
Mitigation: Use it only for general information and route urgent, severe, persistent, pregnancy-related, pediatric, medication-interaction, or cancer-related concerns to licensed medical care. <br>
Risk: Sensitive health conversations may be sent to external services. <br>
Mitigation: Confirm who operates the external endpoints, what data is transmitted or retained, and whether users have appropriate notice and consent before deployment. <br>
Risk: The release uses external API credentials and a remote token endpoint. <br>
Mitigation: Review API-key handling, rotate credentials as needed, and restrict access to approved operators and environments. <br>
Risk: Cancer-related outputs may add an appointment or screening link without enough disclosure. <br>
Mitigation: Disclose whether the link is commercial or affiliated and provide users with independent clinical-care options. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lantian888/yixiaozhi) <br>
- [Publisher profile](https://clawhub.ai/user/lantian888) <br>
- [LLM API endpoint](https://ydai.jinbaisen.com/api/v1) <br>
- [Remote token endpoint](https://jiyinjia.jinbaisen.com/!token?key=skill_yxz) <br>
- [Cancer-screening appointment link](https://bmsapp.geneplus.org.cn/business/addOrder) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, API Calls] <br>
**Output Format:** [Markdown diagnostic intake questions and structured diagnostic reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include HTML-styled headings, medication guidance, high-risk warnings, and cancer-screening appointment links.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
