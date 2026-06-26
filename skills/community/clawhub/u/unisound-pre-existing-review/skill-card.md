## Description: <br>
理赔既往症审核。由调用方传入完整题干（病历/材料 + 关系类型与报销结论格式），经内部医疗大模型判断其他诊断与主诊断关系及是否报销；仅含 scripts/run.py，无 _shared 依赖。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Claims reviewers and insurance workflow developers use this skill to review medical claim text or OCR excerpts for the relationship between other diagnoses and the primary diagnosis, then produce an auxiliary reimbursement judgment in the requested format. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided medical claim text is sent to a configured medical LLM endpoint. <br>
Mitigation: Use only with organizational approval for the endpoint and app key, and redact names, IDs, account numbers, and unnecessary patient details before processing. <br>
Risk: The optional --output flag can write claim review results to disk. <br>
Mitigation: Use --dry-run to inspect parsed input first, and use --output only when stored UTF-8 JSON or NDJSON results are intended and protected. <br>
Risk: The model output is an auxiliary claims review judgment, not a legal or final reimbursement decision. <br>
Mitigation: Route outputs through the applicable policy, claims, and human review process before making final reimbursement decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-pre-existing-review) <br>
- [Publisher profile](https://clawhub.ai/user/unisound-llm) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON object by default, plain text with --text-only, or NDJSON for batch output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include the original question, model name, input metadata, record index, and model answer; --output writes UTF-8 JSON or NDJSON to disk.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
