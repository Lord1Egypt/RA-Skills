## Description: <br>
面向中国中小企业的智能财税助手，支持税率查询、发票识别、基础记账、报税草稿、财务分析、合规检查和税务筹划辅助。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keybryant](https://clawhub.ai/user/keybryant) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
中国中小企业经营者、财务人员和支持其工作的代理人可用它查询常见税率、整理发票与记账数据、生成财务报告，并获得报税、合规和税务筹划草稿。这些输出应作为参考，最终申报和税务决策需由合格专业人员核验并以税务机关要求为准。 <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Tax filing, compliance, and planning outputs may be incomplete or misleading for high-stakes financial workflows. <br>
Mitigation: Treat all calculations and recommendations as drafts; require review by qualified tax or finance professionals and verify against current tax-authority rules before filing or acting. <br>
Risk: The artifact uses 2024 reference tax data and mock integrations, so rates, OCR results, and company-credit checks may be stale or synthetic. <br>
Mitigation: Replace mock OCR, tax-rate, and business-credit integrations with reviewed production APIs and keep the tax-rate reference updated before real business use. <br>
Risk: Real tax, invoice, bookkeeping, and API credential data is sensitive. <br>
Mitigation: Avoid entering live credentials or regulated financial data until the code and secret handling have been reviewed, hardened, and deployed in an approved environment. <br>


## Reference(s): <br>
- [中国主要税种及税率参考](references/china_tax_rates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and terminal text with JSON bookkeeping data and script command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local calculations, structured invoice fields, bookkeeping summaries, tax filing drafts, compliance findings, planning suggestions, and API replacement guidance for mock integrations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
