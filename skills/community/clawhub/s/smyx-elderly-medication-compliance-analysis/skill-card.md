## Description: <br>
Analyzes medication-area video or image inputs to confirm whether an older adult completed pick-up, to-mouth, and swallow steps and returns a structured compliance report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Caregiving teams, family caregivers, and developers of elder-care workflows use this skill to analyze fixed-camera medication-area footage and produce compliance status, missing-step details, reminders, and report links. It is intended as an assistive compliance check and not as medication or clinical guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive medication-area and health-related household video may be sent to the Life Emergence cloud service. <br>
Mitigation: Use only with informed consent from the monitored person or family, restrict video URL sources, and confirm retention, access, and deletion controls before real-world use. <br>
Risk: The skill may create or reuse identities and store authentication tokens while querying analysis reports. <br>
Mitigation: Review identity and token handling before deployment, isolate credentials per environment, and avoid shared workspaces for real household footage or report history. <br>
Risk: Compliance classifications may be incomplete or uncertain because they depend on camera placement, file quality, and cloud analysis results. <br>
Mitigation: Treat outputs as assistive checks, verify missed-dose alerts with a caregiver, and avoid using the skill to change medication dosage or treatment plans. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-elderly-medication-compliance-analysis) <br>
- [API Interface Documentation](references/api_doc.md) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown containing structured JSON-style analysis results, report-list tables, shell command examples, and report links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include medication-action step detections, compliance states, missing-step details, confidence, timestamps, alert text, and exported report links when available.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
