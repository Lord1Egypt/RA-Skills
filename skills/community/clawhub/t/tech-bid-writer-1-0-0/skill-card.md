## Description:

投标人侧「技术标写作专家」根据招标文件生成技术部分投标包，包括技术标正文 Word、技术偏离表、技术合规预检报告和评分点覆盖核对表，并明确排除商务报价与资格审查内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

Bidders and proposal teams use this skill to draft and package the technical portion of Chinese bid submissions from tender documents. It helps map scoring criteria to headings, produce technical-compliance checks, generate deviation tables, plan page budgets, and export a Word technical proposal while leaving business pricing, qualification materials, and final factual verification to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tender documents and optional company knowledge-base materials may contain confidential bid or company information.

Mitigation: Use the skill only in environments where processing those materials is acceptable, and avoid uploading unnecessary confidential examples or credentials.

Risk: Generated technical claims, parameters, standards, and experience statements can be incorrect or unsupported if not grounded in verified materials.

Mitigation: Review all generated technical claims before submission and verify unsourced AI-generated content against tender documents, company records, and applicable standards.

Risk: The local Python helper dependencies are not pinned in the release evidence.

Mitigation: Run helper scripts in a clean virtual environment and pin dependency versions where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chesaram/skills/tech-bid-writer-1-0-0)
- [Technical compliance checklist](artifact/references/tech_compliance_checklist.md)
- [Scoring map template](artifact/references/scoring_map_template.md)
- [Page budget guide](artifact/references/pages_budget.md)
- [IMA knowledge-base template](artifact/references/ima_kb_template.md)
- [Chinese technical-bid humanizer guide](artifact/references/humanizer_zh.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and Word-oriented bid-package files, with optional shell commands for local conversion and page-estimation helpers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a technical-bid package with compliance checkpoints and user-confirmation gates; final claims, technical parameters, qualifications, and company-specific evidence require human review.]

## Skill Version(s):

1.0.0 (source: frontmatter, manifest, ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
