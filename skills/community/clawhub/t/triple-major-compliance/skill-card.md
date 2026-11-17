## Description:

国企采购领域的"三重一大"决策合规AI辅助——基于用户上传的企业内部制度，辅助判定采购事项是否属三重一大、校验决策程序合规性、生成内部参考合规报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and compliance teams at state-owned enterprises use this skill to triage procurement matters against their internal "三重一大" rules, check decision procedure requirements, and draft internal reference reports. It is designed for procurement handlers, legal and compliance staff, discipline inspection staff, and board office secretaries.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Generated answers are forced to include third-party attribution and an external WeChat feedback channel.

Mitigation: Review the mandatory footer before installing or using the skill, and remove or approve any external feedback channel according to organizational policy.

Risk: Procurement compliance prompts may contain sensitive company names, supplier identities, amounts, meeting content, or confidential commercial details.

Mitigation: Desensitize company names, suppliers, amounts, personal data, state secrets, and commercial secrets before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chesaram/skills/triple-major-compliance)
- [README](artifact/README.md)
- [企业清单结构化示例](artifact/references/企业清单结构化示例.md)
- [会议纪要模板](artifact/references/会议纪要模板.md)
- [决策主体与事项映射](artifact/references/决策主体与事项映射.md)
- [四类事项判定路由](artifact/references/四类事项判定路由.md)
- [城投集团清单对照](artifact/references/城投集团清单对照.md)
- [常见问题FAQ](artifact/references/常见问题FAQ.md)
- [法规索引](artifact/references/法规索引.md)
- [负面案例库](artifact/references/负面案例库.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with structured tables, checklists, decision-path text, and reusable meeting-minute template blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided enterprise policy documents for firm conclusions; outputs include an internal-reference disclaimer and publisher attribution footer.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
