## Description: <br>
Analyzes child surveillance images or video to identify negative emotions such as crying, anger, fear, and distress, then returns structured reports, soothing suggestions, and caregiver notification guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and caregivers use this skill through an agent to analyze child monitoring media and review current or historical emotion-recognition reports. Results are informational and should not replace adult supervision or emergency response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload child surveillance images or videos to external services for analysis. <br>
Mitigation: Install and run it only with appropriate consent, a trusted publisher and backend service, and a data-handling review suitable for children's media. <br>
Risk: The skill can silently create or reuse an internal identity, read a workspace identity file, and store tokens locally. <br>
Mitigation: Run it in a controlled workspace, review identity and token storage before use, and remove local identity or token files when they are no longer needed. <br>
Risk: Historical report retrieval can expose account-linked child emotion analysis history. <br>
Mitigation: Limit report-list access to authorized users and review generated reports before sharing them outside the intended caregiver workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-child-emotion-recognition-analysis) <br>
- [API 接口文档](references/api_doc.md) <br>
- [SMYX analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [Network video analysis demo](https://www.coze.cn/s/1C7uyv2vnck/) <br>
- [Uploaded video analysis demo](https://www.coze.cn/s/BXP4CW3eI3o/) <br>
- [Historical report demo](https://www.coze.cn/s/Tjtdye1Hwo8/) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown text with JSON-formatted analysis results, report links, and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save requested output to a local file and can retrieve cloud-stored historical reports.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata; artifact frontmatter says 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
