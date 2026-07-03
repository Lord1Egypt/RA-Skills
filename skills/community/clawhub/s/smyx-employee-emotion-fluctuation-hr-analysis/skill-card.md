## Description: <br>
This skill analyzes office camera video files or URLs through a cloud service to produce employee emotion-fluctuation HR reports, alerts, report links, and history based on facial-expression, posture, behavior, and baseline comparisons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HR leaders and authorized workplace wellbeing teams use this skill to analyze fixed-office camera video or historical report records for anonymized employee emotion-fluctuation alerts and care suggestions. It is intended for consented HR care workflows, not diagnosis, performance evaluation, promotion, or termination decisions. <br>

### Deployment Geography for Use: <br>
Global, subject to local employee monitoring, biometric/privacy, labor, consent, and workplace surveillance requirements. <br>

## Known Risks and Mitigations: <br>
Risk: Workplace emotion monitoring can create privacy, labor, and consent risks if deployed without formal approval. <br>
Mitigation: Install only after confirming the tool is approved for employee monitoring in the relevant jurisdiction and organization, with explicit employee notice/consent, opt-out handling, and a documented retention policy. <br>
Risk: The security evidence says the skill silently creates or reuses persistent identities and stores tokens while claiming anonymous handling. <br>
Mitigation: Require role-based access controls, audit logging, token storage review, token rotation or deletion procedures, and a documented way to disable identity persistence before production use. <br>
Risk: Video, URL, identity, token, and report data may be sent to lifeemergence.com services and stored locally. <br>
Mitigation: Use only after documenting exactly what data is sent and stored, confirming organizational approval for cloud processing, and providing a way to disable cloud upload where required. <br>
Risk: Emotion-fluctuation outputs may be misused as medical diagnoses or employment-decision evidence. <br>
Mitigation: Restrict use to voluntary support and HR care workflows; prohibit mental-health diagnosis, performance review, promotion, or termination use; and route serious concerns to EAP or qualified professionals. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-employee-emotion-fluctuation-hr-analysis) <br>
- [Publisher Profile](https://clawhub.ai/user/smyx-sunjinhui) <br>
- [Employee Emotion Fluctuation HR Report API Documentation](references/api_doc.md) <br>
- [SMYX Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown and JSON text with optional report export links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save report output to a local file when --output is used; history listings are returned from the cloud API.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter declares 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
