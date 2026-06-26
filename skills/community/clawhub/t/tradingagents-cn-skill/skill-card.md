## Description: <br>
Generates Chinese-language stock analysis PDF reports through a 12-step multi-agent workflow covering analyst views, debate, trading plans, and risk review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tanteng](https://clawhub.ai/user/tanteng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn stock tickers, text, or screenshots into a Chinese stock-analysis workflow with structured JSON validation and a generated PDF report. It is intended for informational analysis rather than regulated financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process screenshots, portfolio details, or proprietary trading information through OCR, web search, local logs, and generated reports. <br>
Mitigation: Avoid providing brokerage-account screenshots, private portfolio details, or proprietary trading data unless local processing and retention are acceptable. <br>
Risk: Buy, sell, hold, target-price, and position-size outputs could be mistaken for regulated financial advice. <br>
Mitigation: Treat all trading output as informational analysis and review decisions with appropriate financial, compliance, or professional advice channels. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tanteng/tradingagents-cn-skill) <br>
- [README](artifact/README.md) <br>
- [Skill workflow](artifact/SKILL.md) <br>
- [Data schema](artifact/references/data_schema.md) <br>
- [Trader prompt](artifact/references/trader_prompt.md) <br>
- [Risk manager prompt](artifact/references/risk_manager_prompt.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Files] <br>
**Output Format:** [Chinese Markdown guidance, structured JSON outputs, shell command examples, and generated PDF reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; may create local logs and PDF reports.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
