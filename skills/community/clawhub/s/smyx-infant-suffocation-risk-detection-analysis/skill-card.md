## Description: <br>
Analyzes crib camera videos or URLs to detect infant sleep posture, face occlusion, risk level, and alert or report information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External caregivers, childcare staff, and developers can submit crib camera video files or URLs to obtain structured visual assessments of infant posture, mouth/nose occlusion, risk level, and related report links. The skill is an auxiliary monitoring aid and does not provide medical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Infant sleep videos or video URLs may be sent to remote services for analysis. <br>
Mitigation: Use only footage you are authorized to share, and review the provider's privacy, retention, and deletion practices before using real child or home-monitor footage. <br>
Risk: The skill may silently create or reuse account identity and store tokens locally. <br>
Mitigation: Run the skill in an isolated environment, review token storage and rotation practices, and clear local state when the skill is no longer needed. <br>
Risk: Visual risk results can influence infant safety decisions. <br>
Mitigation: Treat results as an auxiliary monitoring signal, verify alerts with responsible adult supervision, and do not use the skill as a medical diagnosis tool. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-infant-suffocation-risk-detection-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API interface documentation](artifact/references/api_doc.md) <br>
- [Analysis API documentation](artifact/skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with JSON-backed structured fields and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote video analysis; supports history and report retrieval.] <br>

## Skill Version(s): <br>
1.0.2 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
