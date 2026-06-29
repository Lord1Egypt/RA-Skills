## Description: <br>
Analyzes infant diaper or stool images and videos to classify stool color, flag clay-pale or bloody findings, and return structured risk guidance and report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External caregivers, pediatric-adjacent staff, and developers use this skill to submit infant diaper or stool media for visual color screening and to retrieve cloud-stored screening report history. It provides directional risk prompts only and is not a medical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive infant health images are uploaded to remote services for analysis. <br>
Mitigation: Use only with explicit guardian consent and only when the publisher and backend service are trusted for handling minor health data. <br>
Risk: The skill can silently create or reuse a cloud-linked identity and store local account tokens. <br>
Mitigation: Review local identity and token storage before deployment, restrict workspace access, and require clear account-control procedures for users. <br>
Risk: Cloud history retrieval can expose prior screening reports. <br>
Mitigation: Limit use to environments where report access is authorized and where retention, deletion, and access-control expectations are documented. <br>
Risk: Visual stool-color screening can be misleading under poor lighting or with filtered images. <br>
Mitigation: Require clear natural or cool-white lighting, avoid filters, and treat abnormal or inconclusive results as prompts for professional pediatric review rather than diagnosis. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-infant-stool-color-abnormality-analysis) <br>
- [Infant Stool Color API Documentation](references/api_doc.md) <br>
- [SMYX Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance, Shell commands] <br>
**Output Format:** [Markdown text with structured JSON report content and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save analysis output to a user-specified file and may render history results as a Markdown table.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
