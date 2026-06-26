## Description: <br>
One-click A-share analysis covering technical, valuation, risk, and fundamental signals, with automated Markdown and Word-style investment report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jy02577302-ux](https://clawhub.ai/user/jy02577302-ux) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and financial research workflows can use this skill to analyze Chinese A-share stocks and ETFs, screen candidates by factors, and generate investment research reports. Outputs should be treated as research support rather than investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce investment recommendations from placeholder, static, or incomplete data. <br>
Mitigation: Treat generated reports as research drafts only and independently verify all financial data, assumptions, and recommendations before use. <br>
Risk: The skill fetches market data from network sources and may cache data under /tmp. <br>
Mitigation: Run it in a workspace where network access and temporary cache files are acceptable, and avoid providing account credentials or session cookies. <br>
Risk: Report generation can write analysis outputs to local files. <br>
Mitigation: Review generated files before sharing and run the skill only where local report writes are expected. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jy02577302-ux/stock-analysis-cn) <br>
- [Publisher profile](https://clawhub.ai/user/jy02577302-ux) <br>
- [API usage guide](references/api_usage.md) <br>
- [Technical indicators reference](references/indicators.md) <br>
- [Factor model reference](references/factors.md) <br>
- [Valuation benchmarks reference](references/valuation_benchmarks.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown reports, Markdown tables, Python result objects, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write report files and cache fetched market data under /tmp.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
