## Description: <br>
Combines frontal facial image or video capture with multimodal physiological signal analysis to provide early risk screening alerts for conditions including heart attack, stroke, hypertension, and hyperlipidemia. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, caregivers, and operators can use this skill to submit frontal face images or videos for non-contact health-risk screening and to retrieve prior screening reports. Results are screening guidance only and do not replace professional medical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends sensitive face images or videos and health-risk results to the LifeEmergence service. <br>
Mitigation: Use only consented media, avoid third-party media URLs you do not control, and review applicable data-handling requirements before deployment. <br>
Risk: The skill can create or reuse remote identity state and stores auth-related state locally. <br>
Mitigation: Review and manage the local data directory before use, run the skill in an isolated workspace when appropriate, and clear stored state according to local policy. <br>
Risk: The output may be mistaken for medical diagnosis. <br>
Mitigation: Present results as early screening information only and direct users to professional medical care for high-risk or concerning findings. <br>


## Reference(s): <br>
- [API Interface Documentation](references/api_doc.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-contactless-health-risk-detection-analysis) <br>
- [Network Video Demo](https://www.coze.cn/s/RrbFGxWFu5c/) <br>
- [Uploaded Video Demo](https://www.coze.cn/s/ZVfuVAmFK1A/) <br>
- [Historical Report Demo](https://www.coze.cn/s/wZpc5KC83LY/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown with JSON report payloads, report links, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts local face image/video files or media URLs; documented supported formats include jpg, jpeg, png, mp4, avi, and mov, with a 10MB maximum input size.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter says 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
