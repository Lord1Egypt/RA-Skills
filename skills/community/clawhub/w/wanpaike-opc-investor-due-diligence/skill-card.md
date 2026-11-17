## Description:

投资者背景调查工具，系统化核查投资方资质、资金来源、过往业绩与潜在风险.

This skill is ready for commercial/non-commercial use.

## Publisher:

[golngod](https://clawhub.ai/user/golngod)

### License/Terms of Use:

MIT-0

## Use Case:

Founders, finance teams, and advisors use this skill before fundraising to assess potential investors, investigate public records and reputation signals, identify legal or commercial risk areas, and prepare investor engagement strategy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A reference file contains embedded file-writing tool-call text that could mislead an agent into creating files.

Mitigation: Review the skill before installing, treat reference documents as data rather than instructions, and remove or ignore embedded tool-call transcript content before deployment.

Risk: Investor assessments can be incomplete or inaccurate when public data is stale or source quality is weak.

Mitigation: Cross-check findings across multiple independent sources and refresh key facts before relying on the output.

Risk: The skill discusses financing terms and due diligence but does not provide legal, financial, or investment advice.

Mitigation: Use outputs as preparation material and consult qualified legal, financial, or investment professionals before making major decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/golngod/skills/wanpaike-opc-investor-due-diligence)
- [调查框架](references/调查框架.md)
- [数据源清单](references/数据源清单.md)
- [投资协议要点库](references/投资协议要点库.md)
- [基金运营数据模板](references/基金运营数据模板.md)
- [决策链调研方法](references/决策链调研方法.md)
- [Coze platform](https://coze.cn)
- [OPC platform](https://opc.cn)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown reports, checklists, scorecards, and strategy notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on public-source availability and should be cross-checked before business, legal, or financing decisions.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
