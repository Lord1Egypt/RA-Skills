## Description: <br>
Analyzes cat litter box video or image inputs through a remote service to produce structured observations about feces, urine clumps, trends, and non-diagnostic health risk alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External pet owners, smart litter box builders, and developers use this skill to analyze cat litter box media and retrieve cloud-stored historical reports for monitoring urinary or digestive health signals without disease diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends pet-area media and identity-linked metadata to the Life Emergence service. <br>
Mitigation: Use it only when that data sharing is acceptable, and avoid submitting sensitive footage or metadata. <br>
Risk: The skill silently creates or reuses an identity and stores reusable account tokens locally. <br>
Mitigation: Review token retention and cleanup expectations before installing, and remove local token state when access should be revoked. <br>
Risk: Generated health risk alerts are observational and are not disease diagnoses or treatment advice. <br>
Mitigation: Treat outputs as monitoring signals and consult a qualified veterinarian for medical decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-pet-litter-box-waste-analysis) <br>
- [Skill usage demo](https://lifeemergence.com/sample.html) <br>
- [Pet health analysis API reference](references/api_doc.md) <br>
- [SMYX analysis API reference](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown reports and JSON-style structured analysis output, with optional saved result files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts local media file paths or public media URLs; historical report lookup returns cloud report links.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
