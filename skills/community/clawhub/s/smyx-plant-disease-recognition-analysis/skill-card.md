## Description: <br>
Identifies plant diseases from image or video input and returns structured diagnostic reports with disease type, likely cause, severity context, prevention suggestions, and report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agricultural support teams use this skill to analyze plant disease symptoms in uploaded images, videos, or media URLs and receive diagnostic reports and prevention guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plant photos, videos, URLs, and identifiers are sent to external lifeemergence.com services. <br>
Mitigation: Use only with clear user consent, approved data-flow review, and retention/deletion terms appropriate for the deployment. <br>
Risk: The skill can create or reuse an internal account identity and store tokens in a local SQLite database. <br>
Mitigation: Run with scoped credentials, protect local storage, and review identity lifecycle and token cleanup before installation. <br>
Risk: Cloud report history is linked to the internal identity and can be queried by the skill. <br>
Mitigation: Limit access to trusted operators and confirm that history retrieval, retention, and deletion behavior match user expectations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-plant-disease-recognition-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API interface documentation](artifact/skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown and JSON diagnostic reports, with optional saved output files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return a diagnosis for a submitted plant image/video or a Markdown table of cloud report history.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
