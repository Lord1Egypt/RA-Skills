## Description: <br>
Analyzes facial micro-expression videos through a remote API and returns structured emotional-state reports, report links, and history listings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to submit face videos or public video URLs for micro-expression and emotional-state analysis, then receive structured reports or report-history listings. Results are positioned as reference material and not as a replacement for professional psychological assessment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends face videos, video URLs, identifiers, and report-history requests to a remote LifeEmergence/Open API service. <br>
Mitigation: Use it only with videos you are authorized to submit, avoid sensitive or third-party faces without consent, and verify the remote service's data-handling terms before deployment. <br>
Risk: Account creation, account tokens, and report access may be handled beyond a simple one-off analysis request. <br>
Mitigation: Use a dedicated non-personal open-id, isolate the runtime workspace, restrict token/config file access, and clear stored credentials or local account state after use. <br>
Risk: History lookup and report export links can expose prior analysis reports associated with an identifier. <br>
Mitigation: Confirm the open-id belongs to the requesting user before listing history, and avoid sharing report links outside the intended audience. <br>
Risk: The security guidance calls out dependency review, including the yaml dependency. <br>
Mitigation: Review and pin dependencies from trusted package sources before installing the skill in a sensitive environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/smyx-emotion-analysis) <br>
- [API interface documentation](references/api_doc.md) <br>
- [Analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, files, guidance] <br>
**Output Format:** [Structured report text, JSON payloads, Markdown tables for history listings, and optional saved output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts local video files or video URLs, requires an open-id, supports analysis modes such as comprehensive, basic, micro, trust, and other, and limits local video inputs to supported formats and size checks.] <br>

## Skill Version(s): <br>
1.0.8 (source: ClawHub release metadata; artifact SKILL.md frontmatter says 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
