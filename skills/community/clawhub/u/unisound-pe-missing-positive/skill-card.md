## Description: <br>
门诊病历内涵质控：体格检查中遗漏主要阳性体征。给定门诊病历文本，调用内部医疗大模型，输出无缺陷或有缺陷及原因。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Healthcare quality-control teams and clinical workflow developers use this skill to review de-identified outpatient medical records for missing key positive physical examination findings related to the diagnosis. It returns a concise no-defect or defect result with a reason for clinician review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends de-identified medical-record fields to the configured HiVoice MaaS endpoint. <br>
Mitigation: Use it only where that processing is authorized, and de-identify records before submission. <br>
Risk: The required app key could expose access if committed or shared. <br>
Mitigation: Keep the app key out of repositories and provide it only through an approved secure workflow. <br>
Risk: Changing --base to an untrusted URL can send records to an unintended service. <br>
Mitigation: Use only approved model API base URLs. <br>
Risk: --save-prepared can persist preprocessed record text locally. <br>
Mitigation: Do not use --save-prepared with sensitive records unless local storage is approved. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/unisound-llm/unisound-pe-missing-positive) <br>
- [HiVoice MaaS API endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [UTF-8 text: either 无缺陷 or 有缺陷 followed by a reason] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes the quality-control result to a local text file and prints the same result to the console.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
