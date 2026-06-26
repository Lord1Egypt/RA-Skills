## Description: <br>
Vegas T Trading provides Vegas Tunnel technical analysis with EMA channels, Fibonacci retracement, and multi-timeframe scoring for A-share and cryptocurrency short-term trading review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[georgetao730](https://clawhub.ai/user/georgetao730) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to run local market-data technical analysis for short-term A-share and cryptocurrency review. Its output should be treated as educational analysis, not investment advice or brokerage automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading reports include buy/sell, confidence, and position-size language that could be mistaken for financial advice. <br>
Mitigation: Treat outputs as educational technical analysis only, review them independently, and do not trade solely from the skill's output. <br>
Risk: Requested symbols may be sent to market-data providers while the analyzer retrieves prices. <br>
Mitigation: Avoid querying sensitive watchlists when provider disclosure is a concern and run the tool only in an approved network environment. <br>
Risk: Local execution can inherit dependency and environment risks from Python packages and shell invocation. <br>
Mitigation: Run without elevated privileges in a virtual environment with pinned dependencies. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/georgetao730/vegas-t-trading) <br>
- [Skill README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown-style text reports or JSON from a local Python analyzer] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May query external market-data providers for requested symbols; outputs include trading signals, confidence language, and risk caveats.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
