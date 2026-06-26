## Description: <br>
Analyzes fixed-camera window or balcony video to identify child climbing, leaning, gripping, or other fall-risk behavior and return warning results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze authorized window or balcony camera video, detect child fall-risk behavior, and generate structured warning reports or historical report lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive child or home video and an open-id, username, or phone number may be sent to external services. <br>
Mitigation: Use only videos the user is authorized to share, obtain appropriate consent for child/home footage, and avoid shared or real phone identifiers unless necessary. <br>
Risk: Account tokens may be created or reused and stored locally in workspace data. <br>
Mitigation: Treat locally stored tokens as sensitive credentials, isolate the workspace, and review backend account and report-history access controls before deployment. <br>
Risk: The package includes mismatched health/face-analysis artifacts that may confuse expected behavior or outputs. <br>
Mitigation: Review the installed artifact and API responses before relying on the skill for child-safety alerts. <br>


## Reference(s): <br>
- [API 接口文档](references/api_doc.md) <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/smyx-child-window-climbing-detection-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/18072937735) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands] <br>
**Output Format:** [Markdown tables or structured JSON/text reports, with optional saved output file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local video path or public video URL and an open-id; historical report queries return report links when available.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; SKILL.md frontmatter reports 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
