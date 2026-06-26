## Description: <br>
Checks outpatient medical records for missing blood pressure or blood glucose control information in the past medical history and returns a defect status with a reason when applicable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical quality-control staff and developers use this skill to check whether outpatient records document blood pressure or blood glucose control status when relevant conditions appear in past medical history. The skill is an assistive quality-control tool and its findings should be reviewed by qualified medical personnel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Outpatient record text is sent to a remote LLM endpoint and may contain sensitive medical information. <br>
Mitigation: Use only de-identified input and deploy the skill only where the configured HiVoice MaaS or compatible endpoint is approved for that data. <br>
Risk: The app key is required for model access and could be exposed if placed in source control or logs. <br>
Mitigation: Provide the key at runtime through approved secret-handling practices and keep it out of repositories, command history, and logs. <br>
Risk: Multi-format inputs depend on shared document preprocessing, and prepared text can be saved locally when requested. <br>
Mitigation: Review the shared preprocessing dependency before use and enable --save-prepared only when local storage of record text is approved. <br>
Risk: The quality-control result is assistive and may be incomplete or incorrect for clinical governance decisions. <br>
Mitigation: Require review by qualified medical personnel before acting on a defect result or treating a no-defect result as final. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-pmh-missing-bp-glucose) <br>
- [HiVoice MaaS chat completions endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, shell commands] <br>
**Output Format:** [UTF-8 plain text: either 无缺陷, or 有缺陷 followed by a reason.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes the quality-control result to an output text file and prints the same result to the console.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
