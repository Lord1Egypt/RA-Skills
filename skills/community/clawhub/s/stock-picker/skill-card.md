## Description: <br>
帮助用户基于彼得·林奇 13 条原则、公司类型分类、生活观察和 PEG 估值生成个股分析。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lj22503](https://clawhub.ai/user/lj22503) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to structure stock-selection analysis, classify companies, calculate PEG, and draft investment discussion outputs. Generated buy, sell, observe, or score labels should be treated as educational analysis and independently verified against financial inputs, objectives, and risk tolerance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce buy, sell, observe, or investment-score labels that may be mistaken for personalized financial advice. <br>
Mitigation: Treat outputs as educational analysis only; independently verify financial data and consider personal objectives, risk tolerance, and professional advice before acting. <br>
Risk: PEG calculations and Lynch-principle checks can be misleading when inputs are stale, incomplete, or based on unsustainable growth assumptions. <br>
Mitigation: Use current financial statements and market data, exclude one-time earnings where appropriate, and document unknown or unverifiable inputs in the analysis. <br>


## Reference(s): <br>
- [林奇 13 条原则参考](references/lynch-principles.md) <br>
- [个股分析模板](templates/stock-analysis-template.md) <br>
- [贵州茅台选股分析示例](examples/maotai-example.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown analysis with optional structured JSON-style fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided company details, business description, PE ratio, growth rate, and optional life-observation context.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
