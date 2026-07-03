## Description: <br>
Analyzes home or office fixed-camera videos to detect hand-rubbing, nail-biting, and pacing, then returns behavior statistics, an anxiety-behavior index, and self-care guidance without making a medical diagnosis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, counselors, caregivers, and developers use this skill to analyze consented fixed-camera videos for objective anxiety-related behavior counts, trend indicators, and supportive self-awareness reminders. It is positioned as behavior analysis support, not a medical diagnosis or treatment tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive home, office, school, or counseling-room behavioral videos may be sent to a cloud service and linked to an automatically managed identity. <br>
Mitigation: Use only with informed subject consent, clear retention and deletion practices, access controls, and data minimization such as masked or metric-only workflows where available. <br>
Risk: Reusable local account tokens or history can connect future analyses to the same user identity. <br>
Mitigation: Deploy only where persistent local identity storage is acceptable, restrict local file access, and provide an operational process to clear stored tokens or history. <br>
Risk: Third-party, workplace, classroom, counseling, or minor-subject footage can create heightened consent and privacy exposure. <br>
Mitigation: Require explicit authorization from the subject or guardian and verify organizational privacy, retention, access, and deletion controls before use. <br>
Risk: Behavior indices and alerts may be mistaken for a clinical anxiety diagnosis. <br>
Mitigation: Present outputs as visual behavior statistics and self-awareness guidance only, and route urgent or high-concern cases to qualified medical or mental-health professionals. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-anxiety-behavior-recognition-analysis) <br>
- [API Interface Documentation](references/api_doc.md) <br>
- [Shared Analysis API Reference](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill usage demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or JSON analysis reports, with optional saved text output and report links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May query cloud-hosted historical reports and return behavior metrics, trend comparisons, self-care suggestions, and links.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
