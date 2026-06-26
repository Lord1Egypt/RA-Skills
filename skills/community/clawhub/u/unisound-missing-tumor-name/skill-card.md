## Description: <br>
门诊病历内涵质控：未记录肿瘤名称。给定门诊病历文本，调用内部医疗大模型，输出无缺陷或有缺陷及原因。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical quality-control teams and authorized operators use this skill to check de-identified outpatient EMR text for missing tumor names in the history fields. It returns a concise defect result for review by qualified medical staff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical record content may be sent to the configured remote LLM endpoint. <br>
Mitigation: Use only de-identified records, confirm authorization and provider retention terms, and route requests only to approved endpoints. <br>
Risk: Authentication keys are required for the remote model call. <br>
Mitigation: Keep appkeys out of repositories and pass them through approved secret-handling workflows. <br>
Risk: Optional prepared-text debug output can persist sensitive medical content locally. <br>
Mitigation: Avoid --save-prepared for real patient data and delete any temporary prepared files created during testing. <br>
Risk: The result is an auxiliary quality-control signal, not a medical diagnosis. <br>
Mitigation: Require review by qualified medical staff before acting on any defect result. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-missing-tumor-name) <br>
- [HiVoice MaaS chat completions endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [UTF-8 text result: 无缺陷, or 有缺陷 followed by a reason] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May also write the result to a local output file when run through the bundled scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
