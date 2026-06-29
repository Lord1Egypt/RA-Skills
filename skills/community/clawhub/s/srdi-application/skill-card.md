## Description: <br>
专精特新企业申报材料智能生成助手，覆盖创新型中小企业、省级专精特新和国家级小巨人三个梯度，生成申请书、自查清单、佐证材料清单、市场地位说明、研发费用说明、合规证明和交互式 HTML 可视化报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users such as Chinese SMEs, consultants, and business development teams use this skill to assess SRDI application readiness and draft application materials, checklists, supporting evidence lists, and report outputs for the relevant application tier. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML reports may include unescaped report content while containing sensitive enterprise data. <br>
Mitigation: Use trusted input, review generated reports before sharing or opening them broadly, and avoid processing confidential company data in untrusted environments. <br>
Risk: The HTML report loads Chart.js from a remote CDN. <br>
Mitigation: Bundle Chart.js locally or add integrity protections before using generated reports in sensitive or offline environments. <br>
Risk: Policy and eligibility outputs may become stale or incorrect for formal filings. <br>
Mitigation: Verify all generated materials against current MIIT notices and have a qualified reviewer check the application before submission. <br>


## Reference(s): <br>
- [专精特新申报政策数据库（2026版）](references/policy_2026.md) <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/srdi-application) <br>
- [优质中小企业梯度培育平台](https://zjtx.miit.gov.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Files, Guidance] <br>
**Output Format:** [HTML report plus plain-text application materials and checklist-style guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled generator can write HTML and text report files from enterprise input data.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
