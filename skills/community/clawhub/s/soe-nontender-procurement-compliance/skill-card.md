## Description:

国企非招标采购领域的合规辅助AI，基于用户上传的企业采购制度与招投标法规体系，辅助判定非招标采购方式的适用条件、识别依法必须招标边界与方式选择风险。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

SOE procurement staff, legal and compliance personnel, discipline inspection personnel, and procurement managers use this skill to assess whether a non-tender procurement method is appropriate, identify mandatory-tender boundaries, scan method-selection risks, and draft an internal reference analysis.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Users may submit company names, supplier names, amounts, personal data, trade secrets, or state-secret material while seeking procurement compliance analysis.

Mitigation: Redact sensitive identifiers and confidential details before sharing inputs with the skill, and use it only for Chinese SOE non-tender procurement compliance support.

Risk: Outputs may be mistaken for final procurement decisions or formal legal opinions.

Mitigation: Treat outputs as advisory internal references and require review by the enterprise procurement decision maker, legal or compliance staff, and applicable approval bodies.

Risk: The maintainer attribution or WeChat feedback channel may appear in ordinary outputs and be confused with compliance analysis.

Mitigation: Separate support or promotion text from the substantive compliance analysis when reviewing or sharing outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chesaram/skills/soe-nontender-procurement-compliance)
- [四种非招标采购方式对照表](references/四种采购方式对照表.md)
- [非招标采购法规索引](references/法规索引.md)
- [直接采购七类情形详解](references/直接采购七类情形详解.md)
- [非招标采购负面案例库](references/负面案例库.md)
- [场景路由映射表](references/场景路由映射表.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown with tables, structured findings, citations to provided sources, risk levels, and decision-record templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory compliance references and do not replace the enterprise procurement decision maker or legal counsel.]

## Skill Version(s):

1.0.0 (source: frontmatter, manifest, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
