## Description: <br>
基于普睿科公司蚩尤智核CFC的智能医疗诊断助手，通过2+4+病史收集和三轮问诊生成结构化诊断报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lantian888](https://clawhub.ai/user/lantian888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can describe symptoms and receive guided medical intake questions followed by a structured preliminary diagnostic report. The skill is intended for symptom triage, medication guidance, daily care suggestions, and high-risk alerts, not as a substitute for professional medical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive health details may be processed by configured external services. <br>
Mitigation: Deploy only with explicit user consent, clear disclosure of data recipients and retention practices, and review of the configured model and token endpoints. <br>
Risk: The skill can produce definitive medical diagnoses and medication instructions. <br>
Mitigation: Use the output as preliminary guidance only, require qualified clinical review for care decisions, and preserve escalation paths for severe or worsening symptoms. <br>
Risk: Cancer-related outputs can add an under-disclosed referral link. <br>
Mitigation: Disclose the referral destination and purpose before use, and require user confirmation before navigating to external screening or appointment services. <br>
Risk: Credential and remote token behavior requires careful operational review. <br>
Mitigation: Use managed secrets, avoid embedding API keys in skill files, and verify remote credential retrieval before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lantian888/yixiaozhi-pro) <br>
- [Publisher profile](https://clawhub.ai/user/lantian888) <br>
- [External model API endpoint](https://ydai.jinbaisen.com/api/v1) <br>
- [Remote token endpoint](https://jiyinjia.jinbaisen.com/!token?key=skill_yxz) <br>
- [Cancer screening referral link](https://bmsapp.geneplus.org.cn/business/addOrder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown diagnostic intake questions and structured reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include medication guidance, high-risk alerts, and a cancer-related referral link when cancer keywords appear.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
