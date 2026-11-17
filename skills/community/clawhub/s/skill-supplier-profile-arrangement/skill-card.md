## Description:

供应商信息结构化整理与 Markdown 档案生成；根据用户提供的 WORD、PDF 或 Excel 资料提取供应商关键信息，按模板汇总生成质量管理档案，并可辅助生成 SVG 组织架构图。

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and quality or supplier-management teams use this skill to turn user-provided supplier documents into structured supplier profiles for quality management records. It helps identify missing required fields, normalize contact and certification details, and produce Markdown output with optional guidance for Word or SVG conversion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supplier documents can contain business-sensitive contacts, certifications, cooperation records, and company identifiers.

Mitigation: Process only user-provided files in an approved workspace, avoid adding internet-sourced supplier data, and review generated profiles before sharing.

Risk: Optional Word or SVG generation may require scripts or dependencies that are referenced by the skill but not included in the artifact.

Mitigation: Use Markdown output as the fallback and run any separately provided conversion tooling only after user approval and environment review.

## Reference(s):

- [Server-resolved source repository](https://github.com/duding-engicool/skill-supplier-profile-arrangement)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-supplier-profile-arrangement)
- [Publisher profile](https://clawhub.ai/user/duding-engicool)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown supplier profile with optional SVG or Word conversion guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May mark incomplete fields with [需补充]; optional conversion outputs depend on separately available local tooling.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
