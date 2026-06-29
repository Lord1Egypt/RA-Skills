## Description: <br>
Identifies strangers in surveillance-area images or video streams through facial comparison, then returns structured recognition results, warnings, and report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security operators, facility managers, and developers use this skill to analyze uploaded or URL-based surveillance media for unfamiliar faces, compare faces against a known-person base, enroll known persons when authorized, and query historical recognition reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Surveillance images or videos and account-linked metadata are sent to the provider's cloud service. <br>
Mitigation: Use only with explicit authorization for the monitored area and the people affected; avoid submitting sensitive media unless the operator accepts the provider-cloud exposure. <br>
Risk: Face enrollment and history retrieval can affect or expose account-linked biometric records. <br>
Mitigation: Require operator approval before enrollment or history lookup, and confirm the intended account context before running those actions. <br>
Risk: Local workspace data can include a SQLite token store or default account context. <br>
Mitigation: Protect the workspace, avoid shared environments, and clear local data after use when the environment is not trusted. <br>
Risk: The security verdict is suspicious due to biometric media handling, cloud history, enrollment, and local persistence concerns. <br>
Mitigation: Review the skill and scan results before deployment, especially for privacy, consent, account ownership, and retention requirements. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-stranger-recognition-analysis) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>
- [API Interface Documentation](references/api_doc.md) <br>
- [Shared Analysis API Notes](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, files, shell commands] <br>
**Output Format:** [Markdown reports and JSON-formatted structured results, with optional saved text output files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include recognition summaries, enrollment results, warning text, report links, and cloud history query results.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter says 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
