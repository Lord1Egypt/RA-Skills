## Description: <br>
Analyzes elderly frontal face images or short videos with facial-landmark detection to estimate facial asymmetry, mouth-corner deviation, risk level, and related report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External caregivers, families, nursing-home staff, and health-monitoring developers use this skill to submit elderly frontal face images or short videos for auxiliary facial asymmetry screening and history-report lookup. The output is a screening aid and does not replace professional medical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive elderly face images, videos, and health-analysis metadata are processed by the publisher's cloud service. <br>
Mitigation: Use only with informed consent, avoid unnecessary patient or resident identifiers in inputs, and review the publisher's privacy and retention controls before real-world use. <br>
Risk: Report history is tied to a locally persisted account identity that may be silently created or reused. <br>
Mitigation: Review local identity storage and account controls before deployment, and clear or segregate workspace data when switching users or care contexts. <br>
Risk: The skill provides auxiliary screening signals for possible facial asymmetry and related risk levels, not a medical diagnosis. <br>
Mitigation: Treat outputs as screening support only and route concerning symptoms or high-risk outputs to qualified medical review. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-elderly-facial-asymmetry-analysis) <br>
- [API Interface Documentation](references/api_doc.md) <br>
- [Skill Usage Demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files] <br>
**Output Format:** [Markdown text with JSON-formatted structured analysis content and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include asymmetry metrics, risk level, medical follow-up hint, history records, report export links, and an optional saved output file.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
