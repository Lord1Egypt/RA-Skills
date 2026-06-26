## Description: <br>
门诊病历内涵质控：主诉和诊断部位不一致。给定门诊病历文本，调用内部医疗大模型，输出无缺陷或有缺陷及原因。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical quality-control teams and healthcare developers use this skill to check de-identified outpatient EMR text for inconsistency between the chief complaint body site and the preliminary diagnosis body site. It supports text and common document formats, then writes a concise defect/no-defect result for clinician review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: De-identified medical-record text is sent to the configured HiVoice MaaS or other --base endpoint. <br>
Mitigation: Use only in workflows that permit this transfer, de-identify records before use, and keep clinician review in the loop. <br>
Risk: The skill can write local result files and, with --save-prepared, local debug copies of prepared record text. <br>
Mitigation: Control output locations, avoid --save-prepared unless needed, and handle generated files as sensitive workflow artifacts. <br>
Risk: The app key authorizes access to the configured medical LLM service. <br>
Mitigation: Keep the app key out of source control and restrict access to operators who need it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-chief-complaint-diagnosis-inconsistent) <br>
- [HiVoice MaaS API endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [UTF-8 text containing 无缺陷 or 有缺陷 with a reason] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes the result to a local output file and prints it to the console.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
