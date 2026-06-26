## Description: <br>
This skill analyzes consented enterprise office video through an external API to produce anonymized employee emotion-fluctuation alerts, baseline comparisons, and HR care report summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HR senior management and authorized workplace well-being reviewers use this skill to submit office video or query historical reports for anonymized emotion trend alerts, baseline comparisons, and voluntary care recommendations. The output is intended for employee support workflows and not for diagnosis, performance review, promotion, or termination decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles workplace video, employee identifiers, tokens, report retrieval, and backend mutations for a sensitive employee surveillance use case. <br>
Mitigation: Install only after privacy, legal, and security review; confirm the external service contract; require explicit HR authorization and employee consent before every upload or history query. <br>
Risk: The security evidence flags broad and under-controlled handling of workplace identity and report data. <br>
Mitigation: Limit access to authorized HR reviewers, keep audit logs, avoid username or phone identifiers where possible, and secure or eliminate local token storage. <br>
Risk: The security guidance identifies unrelated health, pet, and admin paths that may expand the operational surface beyond the stated HR report purpose. <br>
Mitigation: Remove unrelated paths and verify that only the employee emotion-report endpoints needed for upload, retrieval, and history queries remain enabled. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/smyx-sunjinhui/smyx-employee-emotion-fluctuation-hr-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/smyx-sunjinhui) <br>
- [API interface documentation](references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [JSON or Markdown HR report output, with optional saved text output file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an open-id/API credential and either a local video path, video URL, or list query.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
