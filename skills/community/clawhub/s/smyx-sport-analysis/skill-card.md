## Description: <br>
Analyzes outdoor sports event videos to identify participant injury, physical discomfort, posture, environmental, and emergency risks, then returns structured safety reports and warnings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Event operators, safety staff, and agents use this skill to analyze participant video files or public video URLs for outdoor sports safety risks and to retrieve prior risk-analysis reports. The generated output supports situational review and response planning, but it is not a substitute for professional medical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Participant videos or URLs may be sent to the Life Emergence backend. <br>
Mitigation: Review the backend operator, privacy terms, and retention/deletion policy before using real participant media. <br>
Risk: Identity values such as open-id, username, or phone may be used for account and report access, and tokens or profile data may be stored locally. <br>
Mitigation: Use only approved identifiers and credentials, limit access to the workspace, and avoid sharing sensitive account data unless required. <br>
Risk: The security summary flags under-disclosed health-inference and surveillance behavior. <br>
Mitigation: Confirm the intended health and device-management features before deployment and require human review for safety or medical decisions. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/smyx-sunjinhui/smyx-sport-analysis) <br>
- [API reference](references/api_doc.md) <br>
- [Shared analysis API reference](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON results, shell command invocations, configuration values, and saved text or JSON files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send local video files or public video URLs to a backend API and may save analysis output when requested.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
