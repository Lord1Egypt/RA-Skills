## Description: <br>
Provides primary care clinicians with common-disease differential diagnoses, recommended exams, treatment suggestions, referral assessment, and a natural-language summary from patient symptoms and findings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Community and primary-care physicians use this skill to turn patient case text into draft differential diagnoses, basic exam recommendations, treatment suggestions, and referral guidance for clinician review. <br>

### Deployment Geography for Use: <br>
Global; clinical use should be reviewed against local medical, privacy, and drug formulary requirements. <br>

## Known Risks and Mitigations: <br>
Risk: Patient information is sent to a remote model, while the release promises de-identification that the security evidence says is not implemented. <br>
Mitigation: Use only de-identified cases unless the endpoint, app key handling, data retention terms, and clinical compliance posture are approved; implement actual redaction before model calls. <br>
Risk: Generated medical advice may be incomplete, incorrect, or unsuitable for a specific patient or jurisdiction. <br>
Mitigation: Treat outputs as clinician decision support only; require licensed clinician review and local clinical policy validation before use. <br>
Risk: The skill requires an app key and network access to a remote medical model endpoint. <br>
Mitigation: Handle the app key through approved secret management, restrict endpoint access, and avoid logging credentials or patient case content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-common-disease-advice) <br>
- [Remote medical model API endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, text, guidance] <br>
**Output Format:** [JSON followed by a natural-language summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write output to a file when an output path is provided; otherwise prints to stdout.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
