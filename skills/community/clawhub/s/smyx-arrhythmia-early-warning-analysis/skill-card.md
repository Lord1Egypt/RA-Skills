## Description: <br>
Based on facial video, this skill identifies abnormal rhythms such as premature beats, atrial fibrillation, tachycardia, and bradycardia to assist early heart-health risk screening. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to submit facial video for non-invasive arrhythmia early-warning analysis and to retrieve structured risk reports. The results are screening guidance only and do not replace ECG testing or diagnosis by a cardiology professional. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Facial video and health-risk report data are processed by the vendor's cloud service. <br>
Mitigation: Use only when the publisher's privacy, retention, deletion, and account-scoping terms are acceptable for the data being submitted. <br>
Risk: The skill silently creates or reuses an internal identity and stores tokens locally. <br>
Mitigation: Review installation and runtime handling before deployment, especially for sensitive medical or account-scoped use cases. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-arrhythmia-early-warning-analysis) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>
- [API Documentation](references/api_doc.md) <br>
- [SMYX Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-style structured analysis reports with report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include historical report tables and health-risk screening guidance from the vendor cloud service.] <br>

## Skill Version(s): <br>
1.0.9 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
