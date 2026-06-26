## Description: <br>
Analyzes aquarium camera video to estimate fish gill movement respiratory rate, classify respiratory status, and return hypoxia or abnormal respiration alerts with recommended checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Aquarium owners, aquaculture operators, public aquarium staff, laboratory teams, and developers use this skill to analyze close-range aquarium video for fish respiratory rate trends and abnormal breathing alerts. It is intended to support monitoring workflows and recommended checks, not veterinary diagnosis or automated device control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Aquarium videos or URLs are sent to the publisher's remote service for analysis. <br>
Mitigation: Use only with consent from the aquarium owner or facility, avoid sensitive video content, and confirm that retention and sharing practices meet local policy. <br>
Risk: The skill requires an open-id, username, or phone number for cloud history and may store account tokens or profile data. <br>
Mitigation: Use a dedicated account identifier where possible, review credential handling before deployment, and remove or disable unnecessary token/profile storage. <br>
Risk: Respiratory alerts may be unreliable when the video does not clearly show gill motion or has low signal stability. <br>
Mitigation: Require close-range side-view video at the documented frame rate and treat low-stability results as a prompt to recapture video rather than as a health alert. <br>
Risk: Abnormal breathing output could be mistaken for veterinary diagnosis or permission to automate aquarium equipment. <br>
Mitigation: Present outputs as visual monitoring guidance only, avoid drug names or dosages, and require human confirmation for aeration, heating, water changes, or other device actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/smyx-sunjinhui/smyx-fish-respiratory-rate-monitor-analysis) <br>
- [API 接口文档](references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON analysis report with respiratory metrics, alert level, recommendations, and optional history table] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an open-id and sends aquarium video files or URLs to the publisher's remote analysis service.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
