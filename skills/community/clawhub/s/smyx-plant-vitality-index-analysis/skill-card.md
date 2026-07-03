## Description: <br>
Analyzes plant images or video plus optional growth and environment data to produce a 0-100 plant vitality score, grade, trend, alert hint, and report link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit plant media or URLs to a remote analysis service and receive a vitality score, trend, structured report, and historical report list for plant monitoring workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plant images, videos, or URLs are sent to a remote service for analysis. <br>
Mitigation: Review data-sharing expectations before installation and avoid submitting sensitive media unless remote processing is acceptable. <br>
Risk: The skill may silently create or reuse a user identity and persist authentication tokens for cloud report and history access. <br>
Mitigation: Install only in environments where local token persistence and cloud history access under that identity are approved; review identity storage and access controls before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-plant-vitality-index-analysis) <br>
- [Plant vitality API documentation](references/api_doc.md) <br>
- [Shared analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown text with structured JSON content and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include remote report links; local file inputs are limited to supported media formats and size constraints.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
