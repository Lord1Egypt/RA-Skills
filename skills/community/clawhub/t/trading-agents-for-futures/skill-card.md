## Description: <br>
Trading Agents for Futures is a rule-based futures-market analysis engine that gathers public market data, calculates six classes of indicators, reports data gaps, and can produce debate-style risk and decision-support output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haoge10241024](https://clawhub.ai/user/haoge10241024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, AI agents, and quantitative developers use this skill to collect public Chinese futures-market indicators, identify missing data, and generate structured decision-support analysis for futures symbols. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound public market-data requests and writes local cache and report files. <br>
Mitigation: Run it in an isolated Python environment with expected network and filesystem access limited to market-data retrieval, cache directories, and report outputs. <br>
Risk: Dependency or data-provider behavior may change and affect analysis quality. <br>
Mitigation: Pin or audit dependencies before serious use and review generated coverage, warning flags, and data-gap reports. <br>
Risk: Search actions or follow-up web searches could expose confidential portfolio, client, or strategy details if users add them to queries. <br>
Mitigation: Do not include confidential trading, portfolio, client, or strategy information in web searches or generated search actions. <br>
Risk: The decision mode can produce position, stop-loss, and risk suggestions that may be mistaken for executable financial advice. <br>
Mitigation: Treat all outputs as decision support and require human financial review before acting on any trading recommendation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/haoge10241024/trading-agents-for-futures) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Manifest](artifact/manifest.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON objects and plain-text decision reports, with optional saved JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces market indicators, data-gap reports, search actions, and rule-based decision-support reports; outputs should be treated as advisory analysis, not executable trading advice.] <br>

## Skill Version(s): <br>
2.0.19 (source: server release evidence; artifact manifest.yaml states 2.0.26) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
