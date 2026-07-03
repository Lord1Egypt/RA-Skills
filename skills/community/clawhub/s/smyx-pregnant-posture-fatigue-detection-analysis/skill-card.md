## Description: <br>
Uses fixed home-camera images or video to detect prolonged standing, bending, and related posture for pregnancy fatigue reminders, producing health-reference reports rather than medical diagnosis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze pregnancy activity-area camera footage, generate posture and fatigue-risk reports, and retrieve historical report lists. It is intended for wellness reminders in homes, prenatal schools, community health centers, smart-home systems, or pregnancy-management apps, not clinical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes sensitive pregnancy-related home-camera footage and cloud report history through external services. <br>
Mitigation: Use it only with informed consent from the pregnant person and any bystanders, minimize private household footage, and prefer privacy-preserving silhouette or ROI modes when available. <br>
Risk: The skill may create or reuse a local identity and store service tokens in the workspace data directory. <br>
Mitigation: Run it only in a trusted workspace, restrict filesystem access, and rotate or delete local tokens when access is no longer needed. <br>
Risk: Fatigue reminders or posture results could be mistaken for medical advice. <br>
Mitigation: Present outputs as wellness reminders based on visual posture statistics and direct users to qualified medical care for symptoms, diagnosis, or treatment decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-pregnant-posture-fatigue-detection-analysis) <br>
- [Pregnant Posture Fatigue API Documentation](references/api_doc.md) <br>
- [Shared Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON/text report with optional shell commands and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include posture statistics, alert type, reminder text, recommended action, cloud report links, and an optional saved output file.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter says 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
