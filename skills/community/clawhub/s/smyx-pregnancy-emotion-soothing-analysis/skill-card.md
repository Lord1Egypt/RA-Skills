## Description: <br>
This skill analyzes authorized pregnancy-related home or waiting-room audio/video for emotional fluctuation signals, returns structured reports, and recommends or triggers staged soothing actions without making medical diagnoses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, care teams, and authorized operators use this skill to analyze pregnancy-related audio/video for visible or audible distress signals, review structured emotion-soothing reports, and retrieve prior cloud reports. It is intended for supportive intervention workflows, not clinical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send highly sensitive pregnancy-related audio, video, or URLs to a cloud service. <br>
Mitigation: Use it only with informed consent from the pregnant person and bystanders, and confirm that the cloud service and retention practices are acceptable before deployment. <br>
Risk: The skill can create or reuse a local identity and may store account-related data locally. <br>
Mitigation: Treat the local data directory as sensitive, restrict filesystem access, and review local token or identity storage before production use. <br>
Risk: The skill can trigger spouse or emergency-contact alerts based on emotion-analysis results. <br>
Mitigation: Preconfigure approved recipients and escalation thresholds, and test the alert path before enabling automated notifications. <br>
Risk: Shared waiting-room deployment could capture bystanders or users who did not opt in. <br>
Mitigation: Provide clear notice, obtain required authorization, and offer an opt-out mechanism before using the skill in shared clinical spaces. <br>
Risk: Emotion-analysis output could be misread as a medical diagnosis. <br>
Mitigation: Present results as behavioral observations and supportive guidance only, and route repeated or severe distress to qualified prenatal mental-health resources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-pregnancy-emotion-soothing-analysis) <br>
- [Pregnancy Emotion Soothing API documentation](artifact/references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown or JSON text containing structured analysis results, recommendations, history lists, and report links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cloud report export URLs and history records returned by the configured service.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; skill frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
