## Description: <br>
Conducts video analysis of children/student learning behavior to identify poor study habits and provide structured reports with family education improvement suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users such as parents or education-support agents use this skill to submit child/student study videos or video URLs for learning-behavior analysis. The skill returns structured findings about focus, posture, study habits, risk signals, and family education suggestions, and can list prior cloud-hosted reports for a supplied open-id. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends child/student videos and a user identifier to the publisher's cloud service. <br>
Mitigation: Use only with appropriate consent and after confirming the publisher's privacy, retention, and account-linking practices. <br>
Risk: Phone numbers may be used as open-id values, which can create sensitive account-linking exposure. <br>
Mitigation: Prefer a non-phone identifier when possible and confirm how identifiers are stored, hashed, linked, and retained before use. <br>
Risk: Security evidence reports local token storage, auto-created accounts, and overbroad or inconsistent support code. <br>
Mitigation: Review token storage, report-history access, and unused admin-style API helpers before deployment; restrict API permissions to the learning-analysis workflow. <br>
Risk: The dependency list includes an invalid yaml package name in the security guidance. <br>
Mitigation: Replace the dependency with the intended package, such as PyYAML, and verify installation in a clean environment before release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/smyx-study-analysis) <br>
- [API 接口文档](references/api_doc.md) <br>
- [API接口文档](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown or JSON analysis report; report-history queries are formatted as Markdown tables.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write output to a file when requested; artifact docs state mp4, avi, and mov video inputs up to 10MB.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence and target metadata; artifact frontmatter says 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
