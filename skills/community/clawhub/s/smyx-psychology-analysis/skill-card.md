## Description: <br>
Analyzes human mental health and psychological behavior from video inputs, identifies common psychological issue tendencies, and returns structured mental health reports with improvement suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit video files or video URLs for psychological analysis, receive structured reports, and retrieve prior report records. The analysis is positioned as mental-health reference material and not a substitute for professional diagnosis or treatment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive mental-health or biometric media may be sent to lifeemergence cloud services for analysis. <br>
Mitigation: Use only with informed consent, approved data handling terms, and media that is appropriate for third-party cloud processing. <br>
Risk: Reports may be linked to local or service-created identities and retrievable later. <br>
Mitigation: Review retention, deletion, access control, and identity-linking expectations before processing real user media. <br>
Risk: The skill may create local identity records and store service tokens. <br>
Mitigation: Deploy in an environment where local storage is protected and token lifecycle handling is reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-psychology-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API interface documentation](references/api_doc.md) <br>
- [smyx_analysis API interface documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown report text with optional JSON-formatted structured analysis and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write analysis output to a local file and can return historical report records from the cloud API.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release metadata; artifact frontmatter reports 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
