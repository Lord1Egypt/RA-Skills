## Description: <br>
根据手术相关病历素材生成规范的手术记录。输入术前小结、术中记录、术后记录等，调用内部医疗大模型，输出结构化手术记录（含手术日期、时间、地点、医生、手术名称、指征、诊断、经过、异常情况、术后情况、签名等 14 个字段）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical documentation teams and developers use this skill to turn de-identified surgical source materials into a standardized 14-field surgical record draft for physician review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles highly sensitive medical text and may send it to the configured LLM endpoint. <br>
Mitigation: Use only de-identified records and verify that the configured endpoint is approved for medical data before use. <br>
Risk: The required app key can grant access to the medical model endpoint. <br>
Mitigation: Protect the app key as a secret, limit access to authorized operators, and rotate it if exposure is suspected. <br>
Risk: Prepared text and generated output can be written to local paths when save options are used. <br>
Mitigation: Avoid save options unless local retention of patient-derived text is permitted and the destination is appropriately protected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-operation-record) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files] <br>
**Output Format:** [UTF-8 text surgical record with 14 ordered fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prints to stdout by default and can write the generated record to a requested output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
