## Description: <br>
Analyzes office workstation video to detect prolonged sitting, neck-forward posture, back curvature, shoulder asymmetry, and close screen distance, then returns posture and activity warnings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Workplace health, facilities, HR, or health SaaS teams can use this skill to analyze office workstation video and produce posture or prolonged-sitting alerts for employee wellness workflows. It is intended to provide visual monitoring results and directional wellness reminders, not medical diagnosis or treatment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workplace video and posture reports may contain sensitive employee data and are sent to a cloud service for processing. <br>
Mitigation: Use only approved camera or URL sources, provide employee notice and consent, and confirm the cloud processing arrangement meets applicable privacy requirements before deployment. <br>
Risk: The skill can automatically associate identity state and store returned service tokens or profile records locally. <br>
Mitigation: Install only in managed environments where local token storage is acceptable, access is restricted, and token/profile data can be rotated or deleted under organizational policy. <br>
Risk: Historical report queries can return report links that may expose prior workplace health analyses. <br>
Mitigation: Limit who can request history, define report retention and deletion controls, and restrict access to exported report links. <br>
Risk: Posture and sitting warnings may be mistaken for medical advice. <br>
Mitigation: Present outputs as visual wellness reminders only and direct users with pain or medical concerns to qualified health professionals. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-office-worker-posture-warning-analysis) <br>
- [Office posture warning API documentation](references/api_doc.md) <br>
- [Analysis API error reference](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown text containing structured JSON-style analysis fields, warning messages, and report links when historical reports are requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include posture metrics, warning categories, sitting-duration statistics, summary text, and export links for generated reports.] <br>

## Skill Version(s): <br>
1.0.2 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
