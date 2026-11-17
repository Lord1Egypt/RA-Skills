## Description:

门诊病历内涵质控：主诉和诊断部位不一致。给定门诊病历文本，调用内部医疗大模型，输出无缺陷或有缺陷及原因。

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Clinical quality-control teams and developers use this skill to check outpatient EMR text for inconsistencies between the chief complaint body location and the diagnosis. It returns a concise no-defect or defect finding with a reason and should be used as assistive QC requiring clinician review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes sensitive medical-record text.

Mitigation: Use only de-identified records and confirm that inputs follow the minimum-necessary principle before sending them to any model endpoint.

Risk: The skill sends record-derived prompts and an app key to an external HTTPS LLM endpoint.

Mitigation: Restrict the base URL to an approved HiVoice MaaS host, keep the app key out of repositories and logs, and review endpoint use before regulated deployment.

Risk: Prepared text or QC outputs can be written to local files, including when --save-prepared is used.

Mitigation: Avoid --save-prepared unless plaintext local storage is approved, and write outputs only to approved protected locations.

Risk: The result is assistant-generated clinical quality-control guidance and may be incomplete or incorrect.

Mitigation: Require clinician review before using findings in clinical, compliance, or operational decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-chief-complaint-diagnosis-inconsistent)
- [HiVoice MaaS chat completions endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [UTF-8 text and command-line output; the result is either 无缺陷 or 有缺陷 with a reason.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires de-identified outpatient record text and a HiVoice MaaS app key; run.py can preprocess pdf, doc, docx, xls, xlsx, csv, txt, and json inputs.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
