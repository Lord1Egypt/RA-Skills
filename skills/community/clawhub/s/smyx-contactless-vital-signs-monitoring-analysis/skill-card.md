## Description: <br>
Analyzes camera video or image input through a cloud service to estimate heart rate, respiration, blood oxygen, and heart rate variability without wearable devices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit face video or image inputs for non-contact vital-sign analysis and to retrieve historical monitoring reports from the vendor cloud account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Face video and health-related results are processed by the vendor cloud service. <br>
Mitigation: Use only with appropriate consent and avoid sensitive videos unless the publisher provides clear privacy, retention, and account-control documentation. <br>
Risk: The skill silently creates or reuses an internal identity and stores tokens for report access. <br>
Mitigation: Run in a controlled environment, restrict access to local token storage, and review account lifecycle and credential-rotation controls before deployment. <br>
Risk: Vital-sign estimates may be mistaken for clinical measurements or diagnosis. <br>
Mitigation: Present results as health reference information only and direct users to professional medical care for abnormal or concerning findings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-contactless-vital-signs-monitoring-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API interface documentation](references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON analysis report with status text, health metrics, recommendations, and report links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save the returned report content to a user-specified output file.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata; artifact frontmatter reports 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
