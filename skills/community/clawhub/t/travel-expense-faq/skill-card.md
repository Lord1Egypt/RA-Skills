## Description:

企业差旅费报销常见问题解答（FAQ）。基于公司官方差旅费报销制度、线上报销流程管理办法和客户端操作手册，整理提供差旅费报销常见问题的标准答案。

This skill is ready for commercial/non-commercial use.

## Publisher:

[longtel-skill](https://clawhub.ai/user/longtel-skill)

### License/Terms of Use:

MIT

## Use Case:

Employees use this skill to get concise Chinese-language answers about corporate travel-expense reimbursement rules, required documents, approval flows, and reimbursement-system operation. It is specific to the company policy documents packaged with the skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reimbursement login guidance may lead users to enter credentials on an unverified or non-HTTPS portal.

Mitigation: Confirm the official reimbursement portal through a trusted company source and use HTTPS before entering credentials.

Risk: Reimbursement workflows can involve bank account, invoice, and other sensitive finance data.

Mitigation: Do not share credentials, bank account numbers, or invoice data with the agent or any unverified site; keep sensitive data inside the required finance workflow.

Risk: Corporate reimbursement policies and portal screens can change after this skill release.

Mitigation: Verify answers against current company policy documents before relying on them for reimbursement decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/longtel-skill/skills/travel-expense-faq)
- [企业差旅费报销常见问题解答](artifact/assets/faq.md)
- [差旅管理制度V1.1](artifact/references/差旅管理制度V1.1_LT_总字-24008.md)
- [差旅管理制度操作说明（脱敏版）](artifact/references/差旅管理制度操作说明.md)
- [线上费用报销流程管理办法V1.0](artifact/references/线上费用报销流程管理办法V1.0.md)
- [费用报销PC端操作手册](artifact/references/费用报销PC端操作手册.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Chinese Markdown Q&A responses, with optional complete FAQ Markdown export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution, external tool calls, environment variables, or persistent storage are required.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/test-report.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
