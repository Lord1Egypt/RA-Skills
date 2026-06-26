## Description: <br>
Detects doji patterns in Polymarket crypto 5-minute interval markets and trades post-doji breakouts for BTC, ETH, SOL, and XRP Up or Down bundles with conviction-based sizing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External traders and developers use this skill to run or adapt a paper-first Polymarket crypto interval strategy that scans doji-after-trend patterns and places post-doji breakout trades when explicitly configured for live execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real Polymarket trades and expose funds when run in live mode. <br>
Mitigation: Use paper mode first, review strategy behavior and position limits, and only run with --live when the SIMMER_API_KEY permissions and funded balance are acceptable. <br>
Risk: Trading behavior depends on the external simmer-sdk dependency. <br>
Mitigation: Review or pin the simmer-sdk dependency before live trading. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/diagnostikon/vpolymarket-candle-doji-breakout-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk GitHub Repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code, shell commands, and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; defaults to paper trading unless run with the --live flag.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
