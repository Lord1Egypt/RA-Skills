## Description:

辅助用户完成A3改善报告；通过强制交互收集信息、逐步追问验证、生成可编辑的HTML格式报告，适用于生产现场改善、质量问题分析等场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Manufacturing, quality, and operations teams use this skill to collect structured information for A3 improvement reports, validate STAR, SMART, 5Why, action-plan, and verification inputs, and generate an editable A3 HTML report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML can preserve attacker-supplied markup or scripts when report inputs come from untrusted sources.

Mitigation: Escape user-controlled fields before rendering, and do not open or share reports created from third-party JSON or input until escaping is fixed.

Risk: A3 reports may contain sensitive business, production, quality, or personnel information.

Mitigation: Store generated report files in approved locations and apply the same access controls used for internal operational documents.

## Reference(s):

- [A3 standard reference](references/a3-standard.md)
- [Server-resolved GitHub provenance](https://github.com/duding-engicool/skill-a3-report-generator)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-a3-report-generator)
- [Publisher profile](https://clawhub.ai/user/duding-engicool)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Interactive guidance plus shell command examples and editable HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports are editable in a browser and intended for A3 landscape printing.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
