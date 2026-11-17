## Description:

Supports Yazhou District enterprise-service work by helping agents query enterprise information, recommend preferential policies, review safety-production supervision needs, provide development suggestions, and prepare reports for one or more companies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wing-art](https://clawhub.ai/user/wing-art)

### License/Terms of Use:

MIT-0

## Use Case:

Yazhou District enterprise-service, investment-promotion, and policy consultation staff use this skill to look up enterprise facts, match policy support, structure safety-production supervision records, and generate single- or multi-company service reports.

### Deployment Geography for Use:

China (Yazhou District, Sanya, Hainan)

## Known Risks and Mitigations:

Risk: The skill may activate outside its intended Yazhou District enterprise-service context.

Mitigation: Confirm activation rules and user prompts keep the skill scoped to Yazhou District enterprise-service work before installation.

Risk: Generated Word reports may contain business information or personal-identifying details.

Mitigation: Store, share, retain, and delete generated reports according to the deploying organization's data-handling rules.

Risk: Policy recommendations, enterprise records, and financial data can become stale or inaccurate.

Mitigation: Verify current policies and financial data from official or trusted sources before relying on recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wing-art/skills/yazhou-enterprise-service)
- [崖州区及上级优惠政策汇总](references/policies.md)
- [安全生产监管法规依据](references/safety-regulations.md)
- [企业类型与政策匹配指南](references/enterprise-types.md)
- [崖州区产业发展情况与规划](references/industrial-development.md)
- [海南省惠企政策兑现服务系统](https://hqzc.hainan.gov.cn/)
- [崖州区政府官网](http://www.yazhou.gov.cn/)
- [三亚市政府官网](http://www.sanya.gov.cn/)
- [海南省政府官网](http://www.hainan.gov.cn/)
- [国家企业信用信息公示系统](http://www.gsxt.gov.cn/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance, files]

**Output Format:** [Word document (.docx) reports, with Markdown/text guidance and query suggestions as intermediate agent output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-company and multi-company reports; multi-company reports are structured in one Word document with separate report sections.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
