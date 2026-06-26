## Description: <br>
门诊病历内涵质控：体格检查缺少与诊断相关的体征。给定门诊病历文本，调用内部医疗大模型，输出无缺陷或有缺陷及原因。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical quality-control staff and developers use this skill to review de-identified outpatient EMR text for whether the physical examination includes signs relevant to the diagnosis. It returns either “无缺陷” or “有缺陷” with a reason. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive medical-record content is sent to an external HiVoice MaaS model endpoint. <br>
Mitigation: Use only de-identified records and only after the endpoint and appkey handling are approved for the organization. <br>
Risk: The skill can save extracted records or results as plaintext files. <br>
Mitigation: Use controlled output directories with retention, access-control, and deletion procedures; avoid --save-prepared unless storage is deliberate. <br>
Risk: The output is medical quality-control assistance and may be incomplete or incorrect. <br>
Mitigation: Require review by qualified clinical staff before using results for care, audit, or operational decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-pe-missing-negative) <br>
- [HiVoice MaaS OpenAI-compatible endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, shell commands, guidance] <br>
**Output Format:** [UTF-8 text containing a no-defect or defect-present result, optionally written to a text file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May process txt, json, csv, xls, xlsx, doc, docx, and pdf inputs through the multi-format entry point.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
