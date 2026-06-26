## Description: <br>
AI-powered pet treadmill exercise intensity analysis combined with optional heart-rate band data; it detects stride frequency, limb extension, and respiratory rate from treadmill video to assess exercise load and provide pacing suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, pet treadmill operators, pet training centers, and pet rehabilitation staff use this skill to analyze dog or cat treadmill videos, optionally combine heart-rate band data, classify exercise intensity, and review historical reports. The output is for exercise training support and is not medical diagnosis or treatment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pet or home videos and public video URLs may be uploaded to a backend service. <br>
Mitigation: Use the skill only with a trusted publisher and backend, and confirm retention, deletion, and access-control practices before uploading sensitive media. <br>
Risk: Analysis and history retrieval can be linked to usernames, phone numbers, account tokens, or report history. <br>
Mitigation: Avoid personal phone numbers as identifiers when possible, limit shared identifiers to the minimum needed, and verify how local tokens and backend accounts are managed. <br>
Risk: Report links may expose historical analysis results if backend access controls are weak. <br>
Mitigation: Do not assume report links are private unless the backend proves access control; review generated report links before sharing them. <br>


## Reference(s): <br>
- [Pet Treadmill Intensity & Heart Rate Analysis ClawHub Page](https://clawhub.ai/18072937735/smyx-pet-treadmill-intensity-analysis) <br>
- [API 接口文档](references/api_doc.md) <br>
- [API接口文档](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-like structured analysis reports with optional report-list tables and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May upload local video files or submit public video URLs to a backend API; may save analysis output to a user-specified file.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
