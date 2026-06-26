## Description: <br>
门诊病历内涵质控：主诉和现病史描述不一致。给定门诊病历文本，调用内部医疗大模型，输出无缺陷或有缺陷及原因。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical quality-control teams and agent operators use this skill to review de-identified outpatient medical-record text for inconsistency between the chief complaint and history of present illness. It supports direct UTF-8 text and, through the bundled runner, common document, spreadsheet, CSV, TXT, and JSON inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Outpatient record text is sent to the configured HiVoice MaaS endpoint and may contain sensitive medical information if the operator provides non-de-identified input. <br>
Mitigation: Use only de-identified records and install the skill only where organizational policy permits sending that text to the configured MaaS endpoint. <br>
Risk: The app key used for the MaaS request could be exposed or reused beyond the intended deployment. <br>
Mitigation: Use a dedicated app key, pass it at runtime, and do not store it in the skill package or repository. <br>
Risk: Prepared text and result files can create local copies of medical-record content. <br>
Mitigation: Avoid --save-prepared with real patient data and manage generated output files under the applicable medical-data retention policy. <br>
Risk: Automated quality-control output may be incorrect or incomplete for clinical review purposes. <br>
Mitigation: Treat the result as an auxiliary quality-control signal and require review by licensed medical staff before acting on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-chief-complaint-hpi-inconsistent) <br>
- [HiVoice MaaS chat completions endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, files] <br>
**Output Format:** [UTF-8 text containing either "无缺陷" or "有缺陷" followed by a reason.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes the same quality-control result to a local output file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
