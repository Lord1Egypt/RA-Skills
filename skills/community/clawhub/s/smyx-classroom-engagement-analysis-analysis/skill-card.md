## Description: <br>
Analyzes fixed classroom-camera video to estimate class-level student engagement, emotion distribution, anonymous low-engagement seat positions, alerts, and teacher-facing suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teachers, classroom technology operators, and education developers use this skill to process classroom video or report history and receive aggregate engagement analytics, heatmap links, and real-time instructional suggestions. It is intended for classroom support, not individual student evaluation or diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads sensitive classroom video involving students to an external analysis service with under-disclosed account, token, history, and retention behavior. <br>
Mitigation: Review the external service operator, storage and deletion terms, token handling, report retention, and school plus parent consent before use; avoid history/report features until retention controls are clear. <br>
Risk: Facial-expression engagement analysis in classrooms can be misused for student profiling, performance evaluation, or decisions about minors. <br>
Mitigation: Use outputs only as aggregate classroom support, preserve the anonymous seat-coordinate constraint, and require teacher or qualified staff review before acting on any alert. <br>
Risk: Configuration may confuse open-id user identifiers with API keys or other secrets. <br>
Mitigation: Do not place API keys in the open-id field; store credentials only in approved configuration locations and review configuration files before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/smyx-classroom-engagement-analysis-analysis) <br>
- [Classroom Engagement API Documentation](artifact/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON with shell command examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include engagement scores, emotion distributions, anonymous seat coordinates, report image URLs, and teacher suggestions returned from an external API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
