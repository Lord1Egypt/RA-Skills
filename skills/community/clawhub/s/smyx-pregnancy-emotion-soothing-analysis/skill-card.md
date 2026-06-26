## Description: <br>
Analyzes authorized fixed-camera video and optional audio from pregnancy care settings to detect observable emotional fluctuation signals, return a structured report, and suggest escalating soothing actions without making a medical diagnosis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and care-support developers use this skill to analyze consented pregnancy-related video or optional audio for observable emotion-related behaviors, retrieve cloud history, and produce reports or suggested soothing actions for review by caregivers or authorized contacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes highly sensitive pregnancy-related video, optional audio, identity values, and cloud history. <br>
Mitigation: Use only with explicit consent from the pregnant person and any bystanders, minimize identifiers used as open-id values, and verify the receiving API services before sending media or personal data. <br>
Risk: Notification workflows may send spouse or emergency-contact alerts to unintended recipients. <br>
Mitigation: Confirm authorized recipients and notification tokens before deployment, and review alert behavior during installation and testing. <br>
Risk: Emotion analysis outputs could be mistaken for clinical judgment. <br>
Mitigation: Present outputs as observable behavior signals and soothing suggestions only, and direct repeated or urgent concerns to prenatal care or mental-health professionals. <br>


## Reference(s): <br>
- [Pregnancy Emotion Soothing API Documentation](references/api_doc.md) <br>
- [Common Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/smyx-pregnancy-emotion-soothing-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tables and structured JSON analysis reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include event identifiers, scene labels, video and optional audio signal summaries, soothing-action recommendations, daily summaries, and report links.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
