## Description: <br>
Detects baby cries via audio AI, analyzes likely causes, and identifies needs such as hunger, tiredness, pain, discomfort, or irritability to assist caregivers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and caregiving support agents use this skill to submit a baby cry audio/video file or URL for cloud analysis and receive a structured report with likely cry causes, care suggestions, and report links. It can also retrieve prior analysis reports associated with the managed workspace identity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Baby audio/video or submitted URLs are sent to Life Emergence cloud services for analysis. <br>
Mitigation: Use only media you are authorized to share and avoid private household recordings unless retention, access, and deletion practices are acceptable. <br>
Risk: Reports are tied to an automatically managed identity and prior cloud history can be retrieved. <br>
Mitigation: Review workspace identity handling before installation and avoid shared workspaces for sensitive family media. <br>
Risk: Tokens and history may be stored in the workspace data area. <br>
Mitigation: Restrict workspace access and remove stored credentials or history when the skill is no longer needed. <br>
Risk: Cry analysis is advisory and may be incomplete or incorrect. <br>
Mitigation: Treat results as caregiver support only and seek professional medical care when a baby remains distressed or appears unwell. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-infant-cry-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API interface documentation](references/api_doc.md) <br>
- [Analysis API error codes](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON text, with optional saved output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Analysis output may include structured results, care suggestions, historical report records, and report export links.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
