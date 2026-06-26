## Description: <br>
Uses visual AI on frontal face images or videos to identify happiness, sadness, depression, calmness, anger, surprise, and fear, returning emotion intensity scores, dominant emotion, and abnormal-emotion markers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to submit frontal face images, videos, or media URLs to a cloud service and receive structured visual emotion-recognition reports. It can also retrieve prior analysis reports associated with an open-id, username, or phone number. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Face images, videos, media URLs, and emotion reports may be sent to a cloud service and associated with an open-id, username, or phone number. <br>
Mitigation: Use only consented media and identifiers you are comfortable sharing; review the publisher's retention, deletion, and account-control terms before use. <br>
Risk: The skill can retrieve report history and store account tokens locally. <br>
Mitigation: Run it in an isolated workspace, protect local config/data files, and remove local account or token data when the workflow is finished. <br>
Risk: Emotion and mental-health-related outputs may be mistaken for professional assessment. <br>
Mitigation: Treat reports as informational signals only and require qualified human review for health, counseling, employment, or other consequential decisions. <br>


## Reference(s): <br>
- [Root API documentation](references/api_doc.md) <br>
- [Shared analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files] <br>
**Output Format:** [Markdown-style reports or structured JSON, with optional saved output files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include report-history tables and cloud report image/export URLs when returned by the service.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata; artifact SKILL.md frontmatter is 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
