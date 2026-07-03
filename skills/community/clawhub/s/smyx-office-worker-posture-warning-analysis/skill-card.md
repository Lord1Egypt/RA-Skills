## Description: <br>
Using a fixed office camera, this skill analyzes worker posture video to detect continuous sitting duration, forward-head angle, and back curvature, then returns prolonged-sitting or posture-abnormality alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, workplace health teams, and developers use this skill to review office workstation videos or URLs for prolonged sitting and posture warning signals. It produces behavior-oriented reminders and historical report listings, not medical diagnosis or rehabilitation plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workplace video or video URLs are sent to the Life Emergence cloud service for analysis. <br>
Mitigation: Use the skill only with employee consent, approved retention practices, and appropriate handling of workplace video. <br>
Risk: The skill can create or reuse a local/cloud identity for report history and stores tokens locally. <br>
Mitigation: Review the workspace data directory for stored tokens when removing the skill and restrict use to approved environments. <br>
Risk: Posture warnings could be mistaken for medical advice. <br>
Mitigation: Present results as visual posture and activity reminders only, and direct users with neck or back discomfort to professional medical care. <br>


## Reference(s): <br>
- [API Interface Documentation](artifact/references/api_doc.md) <br>
- [Analysis API Error Codes](artifact/skills/smyx_analysis/references/api_doc.md) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-office-worker-posture-warning-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with optional JSON detail output, posture metrics, warning messages, history tables, and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are based on uploaded workplace video files or video URLs and may include cloud report links.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
