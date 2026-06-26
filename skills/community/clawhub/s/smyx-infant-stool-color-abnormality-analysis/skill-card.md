## Description: <br>
Analyzes infant diaper or stool images through a remote visual analysis service to classify stool color, flag clay-pale or bloody findings, and return risk-oriented guidance and history reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and infant-care operators use this skill to submit infant diaper or stool images or image URLs for stool color screening, abnormal-color risk reminders, and cloud history lookup. It is intended as visual screening support, not a medical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends sensitive infant health images or image URLs and user identifiers to a remote service and can retrieve cloud-stored history reports. <br>
Mitigation: Use only with explicit guardian consent, a trusted backend, understood retention and deletion terms, and the minimum necessary identifier. <br>
Risk: The skill may store account tokens or API credentials in local configuration. <br>
Mitigation: Keep credentials out of shared workspaces, restrict file access, and rotate or remove tokens after use. <br>
Risk: Visual screening output could be mistaken for clinical diagnosis. <br>
Mitigation: Treat results as directional screening only and require pediatric or surgical evaluation for warning or urgent findings. <br>


## Reference(s): <br>
- [API interface documentation](references/api_doc.md) <br>
- [ClawHub skill release page](https://clawhub.ai/smyx-sunjinhui/smyx-infant-stool-color-abnormality-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON text with optional saved output files and Markdown tables for history reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include stool color class, risk level, confidence, recommended action, alert text, and cloud report links.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
