## Description: <br>
Forensic diagnosis engine for backtest order data: trade quality, ROI attribution, monthly cashflow, drawdown root-cause analysis, and LLM-readable reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tltby12341](https://clawhub.ai/user/tltby12341) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantitative researchers use this skill after a QuantConnect backtest to diagnose why a strategy performed as it did and to produce an LLM-readable report for follow-up strategy analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may include confidential trading strategy and backtest details. <br>
Mitigation: Review and redact reports before sharing them outside the intended audience. <br>
Risk: Unpinned pandas or numpy versions can change analysis behavior over time. <br>
Mitigation: Install in a clean Python environment and pin dependency versions when reproducible results are required. <br>
Risk: Incorrect input columns or the wrong anchor equity symbol can produce misleading diagnostics. <br>
Mitigation: Use the standard QuantConnect orders.csv export and set the equity symbol to match the strategy before relying on the report. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Plain-text diagnostic report with Markdown-style sections and optional Python or shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Locally analyzes user-provided orders.csv and optional result.json files; no network, credential, persistence, or destructive behavior was identified by the provided security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
