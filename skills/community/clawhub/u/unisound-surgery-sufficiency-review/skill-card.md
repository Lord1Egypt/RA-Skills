## Description: <br>
手术/操作依据充分性审核。输入结构化病案 record 与待审核手术/操作列表，输出依据充分性审核结果。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Medical coding, billing, and review teams use this skill to compare structured inpatient records and candidate surgery or procedure codes against sufficiency guidance. It returns whether the supporting record evidence is sufficient, insufficient, or requires human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes medical record text and may send sensitive case content to configurable external services. <br>
Mitigation: Install only in environments approved for PHI handling; use --no-llm or use_llm=false unless the model endpoint is contractually approved, and configure GUIDELINE_API_BASE to a trusted service. <br>
Risk: The CLI can save prepared patient text locally when --save-prepared is used. <br>
Mitigation: Do not use --save-prepared with real patient data unless local retention, access controls, and cleanup are explicitly managed. <br>
Risk: Changing the --base model endpoint can route sensitive content to an unapproved service. <br>
Mitigation: Avoid arbitrary --base values and restrict endpoint configuration to approved services. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-surgery-sufficiency-review) <br>
- [Publisher profile](https://clawhub.ai/user/unisound-llm) <br>
- [Internal medical model API endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON object with final_decision and concise reasoning fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [final_decision is one of 依据充分, 依据不充分, or 待人工复核.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
