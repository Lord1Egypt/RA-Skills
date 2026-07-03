## Description: <br>
Performs video analysis of children's autism spectrum disorder behavioral characteristics, identifies core symptom features, and provides structured analysis reports and intervention recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, caregivers, educators, and professionals use this skill to submit child behavior videos for preliminary ASD behavior screening, structured report generation, and report-history lookup. The generated output is for screening support and does not replace professional medical diagnosis or clinical evaluation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive child video data and report history may be sent to or fetched from a remote service. <br>
Mitigation: Confirm the backend operator, uploaded data categories, retention terms, and access controls before using the skill with real child media. <br>
Risk: The skill uses account-linked identifiers and can silently initialize or reuse an identity for analysis and history access. <br>
Mitigation: Verify identity handling, account creation behavior, and report-history authorization boundaries before deployment. <br>
Risk: ASD analysis output could be mistaken for a clinical diagnosis. <br>
Mitigation: Present results only as preliminary screening support and require professional medical or clinical evaluation for diagnostic decisions. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-autism-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API interface documentation](references/api_doc.md) <br>
- [Analysis API reference](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, json, files, api calls] <br>
**Output Format:** [Markdown and JSON text, with optional saved report output files and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports local video files or video URLs, analysis modes, report-history queries, and optional output-file paths.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata; artifact frontmatter lists 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
