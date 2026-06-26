## Description: <br>
Analyzes submitted videos or video URLs to produce structured mental-health assessment reports, including emotional state, behavior patterns, common psychological concern tendencies, suggestions, and report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to submit supported video files or public video URLs for cloud-based mental-health analysis, then receive structured results, suggestions, and optional historical report listings. Outputs are for mental-health reference only and are not a substitute for professional diagnosis or treatment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mental-health videos, video URLs, report histories, and analysis results are sent to the publisher's cloud service. <br>
Mitigation: Install and use only when users are comfortable sharing this sensitive content with the publisher's service, and avoid submitting unnecessary or non-consensual personal media. <br>
Risk: Reports are linked to an automatically managed identity and local token reuse, which may persist report access across sessions. <br>
Mitigation: Treat the workspace data directory as sensitive and review or clear stored identity and token data when persistent association is not desired. <br>
Risk: Mental-health analysis output may be incomplete, incorrect, or over-relied on for clinical decisions. <br>
Mitigation: Present results as reference information only and direct users with clear distress or health concerns to qualified mental-health professionals. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/smyx-sunjinhui/skills/smyx-psychology-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API documentation](references/api_doc.md) <br>
- [Analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with structured JSON report content and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save report output to a user-specified file; historical report queries return structured records from the publisher's cloud API.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
