## Description:

根据项目属性自动匹配最合适的Solution标签，支持字段校验、优先级匹配和特殊规则验证。

This skill is ready for commercial/non-commercial use.

## Publisher:

[luorixin](https://clawhub.ai/user/luorixin)

### License/Terms of Use:

MIT-0

## Use Case:

Consultants and project teams use this skill to classify project records into the most appropriate Solution label from a predefined competency-to-solution mapping. It accepts CSV or JSON project data and returns matched labels with confidence, validation status, and processing notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may provide sensitive project metadata such as project names, descriptions, company type, and partner names.

Mitigation: Confirm the workflow is appropriate for the team and avoid submitting confidential records unless the deployment environment is approved for that data.

Risk: Malformed frontmatter may affect reliable installation or metadata parsing.

Mitigation: Correct the skill frontmatter before publishing or installing in environments that depend on strict metadata parsing.

Risk: Automated classification can assign an incorrect Solution when inputs are incomplete or ambiguous.

Mitigation: Review low-confidence, validation-failed, or manually flagged records before relying on the classification.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/luorixin/skills/solution-tag)
- [Competency的Solution清单.csv](artifact/assets/Competency的Solution清单.csv)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown table or structured text with matched Solution labels, confidence, validation status, and processing notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs add Matched_Solution, Match_Confidence, Validation_Status, and Processing_Notes fields to each project record.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
