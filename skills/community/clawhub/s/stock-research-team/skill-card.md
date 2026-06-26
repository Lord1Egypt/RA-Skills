## Description: <br>
A multi-role stock research skill that uses MCP tools to gather market data and produce technical, fundamental, macro, sentiment, trading, risk, and final director analysis for A-share and US stocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charonling](https://clawhub.ai/user/charonling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request structured stock research reports, quick stock summaries, or comparisons across A-share and US equities. The skill is intended to support research workflows and does not replace professional financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow installs Python packages and registers a persistent local MCP server. <br>
Mitigation: Review setup.sh before installation on managed or sensitive machines, and uninstall the MCP server when the skill is no longer needed. <br>
Risk: Generated trading recommendations may be incomplete, stale, or unsuitable for a user's financial circumstances. <br>
Mitigation: Treat generated reports as research support only and verify conclusions with current market data and qualified financial judgment before acting. <br>
Risk: Market data comes from external package-backed sources and may fail, lag, or return partial data. <br>
Mitigation: Preserve the skill's behavior of disclosing data retrieval failures and continuing only from available evidence. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/charonling/stock-research-team) <br>
- [Python package requirements](references/requirements.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown research reports with structured role sections and inline setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated reports include market-data-backed analysis, trading posture, risk review, a composite score, and a financial-advice disclaimer.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, changelog, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
