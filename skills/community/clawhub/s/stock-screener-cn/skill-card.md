## Description: <br>
A Chinese A-share and Hong Kong stock technical-pattern screening skill that supports moving-average alignment, volume pullbacks, volume breakouts, candlestick-style strategy conditions, and natural-language stock-screening requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[otouman](https://clawhub.ai/user/otouman) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and external users use this skill to screen A-share and Hong Kong stocks against documented technical-analysis strategies and return ranked matches with reasons and scores. Results are informational and should not be treated as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat technical screening output as investment advice. <br>
Mitigation: Present results as informational analysis only and preserve the skill's investment-risk caveat. <br>
Risk: Public market data may be delayed or incomplete. <br>
Mitigation: Disclose data latency and verify market data before acting on any result. <br>
Risk: Dependency changes could alter screening behavior over time. <br>
Mitigation: Install dependencies in a virtual environment and pin package versions for repeated use. <br>


## Reference(s): <br>
- [A-share technical-pattern screening strategies](references/strategies.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON or table-style screening results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include stock code, name, price, matched strategy, score, reason, and percentage change.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
