## Description: <br>
诊断依据充分性审核。输入结构化病案 record 与待审核诊断列表，输出诊断依据充分性审核结果。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Medical coding, reimbursement audit, and hospital record review workflows use this skill to check whether candidate diagnoses are sufficiently supported by structured case records and ICD/DRG guideline evidence. The output is an audit aid and does not provide medical diagnosis or treatment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive medical record text can be sent to configurable remote services. <br>
Mitigation: Run only in an approved medical-record processing environment, de-identify records before use, restrict the LLM base URL and guideline API endpoint, and enable LLM calls only for contractually approved endpoints. <br>
Risk: Prepared case text or JSON review output can be written locally when optional output flags are used. <br>
Mitigation: Avoid --save-prepared and output file options on shared, synced, or backed-up storage, and apply local retention controls when file output is required. <br>
Risk: The skill's review is an audit aid and may be incomplete when guidelines or record evidence are missing. <br>
Mitigation: Route 待人工复核, missing-guideline cases, and high-impact decisions to qualified human review before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-diagnosis-sufficiency-review) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/unisound-llm) <br>
- [Configured medical LLM endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [json, text, guidance] <br>
**Output Format:** [JSON object with final_decision and reasoning fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The final decision is one of 依据充分, 依据不充分, or 待人工复核; optional file outputs are created only when the caller supplies output paths or save-prepared options.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact _meta.json reports package metadata 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
