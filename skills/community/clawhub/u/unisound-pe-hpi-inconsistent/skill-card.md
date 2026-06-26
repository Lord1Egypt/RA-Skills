## Description: <br>
门诊病历内涵质控：体格检查结果与现病史不符。给定门诊病历文本，调用内部医疗大模型，输出无缺陷或有缺陷及原因。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical quality-control teams and medical-record workflow developers use this skill to check whether outpatient physical examination findings are inconsistent with the history of present illness. It is an auxiliary review tool and requires physician oversight for final judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical records may contain protected health information or other identifying details. <br>
Mitigation: Use only approved, de-identified records and do not pass real PHI unless organizational approval and safeguards are in place. <br>
Risk: The skill sends record content to the configured HiVoice MaaS or replacement LLM endpoint. <br>
Mitigation: Deploy only with a trusted endpoint approved for de-identified medical-record processing and protect the app key. <br>
Risk: Prepared text can be saved when --save-prepared is used. <br>
Mitigation: Avoid --save-prepared unless the output directory is access-controlled. <br>
Risk: The quality-control output is auxiliary and may be incorrect or incomplete. <br>
Mitigation: Require review by licensed physicians or qualified clinical reviewers before acting on results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-pe-hpi-inconsistent) <br>
- [HiVoice MaaS OpenAI-compatible endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [UTF-8 text containing a no-defect or defect result with an explanation when a defect is found] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a result file and prints the same quality-control result to the console.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
