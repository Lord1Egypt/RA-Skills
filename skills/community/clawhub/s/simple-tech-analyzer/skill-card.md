## Description: <br>
Simple Tech Analyzer provides basic stock technical indicator analysis for MACD, RSI, volume changes, and buy/sell signal prompts using local Tongdaxin market data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[15910701838](https://clawhub.ai/user/15910701838) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request basic stock-code technical analysis backed by local Tongdaxin data. The output is intended as an informational market-analysis reference and not as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill's indicator signals may be mistaken for investment advice. <br>
Mitigation: Treat outputs as informational analysis only and require independent financial judgment before trading decisions. <br>
Risk: Market analysis depends on local Tongdaxin data being available, fresh, and sufficient. <br>
Mitigation: Confirm data availability and recency, and handle the skill's insufficient-data error before relying on any signal. <br>
Risk: The supplied security evidence reports clean telemetry but notes pending VirusTotal status and limited deeper confirmation. <br>
Mitigation: Install with normal caution and review the artifact files before deployment when higher assurance is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/15910701838/simple-tech-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Structured JSON-like analysis results with indicator values, signal labels, and upgrade guidance text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Tongdaxin data access through @tdx-local; returns an error when there is insufficient market data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact/SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
