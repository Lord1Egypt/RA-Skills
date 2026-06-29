## Description: <br>
Use when adding a regime filter to any directional strategy on Superior Trade, with reusable bull, bear, and range regime gates based on EMA separation, ADX, and N-bar return confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[superior-ai](https://clawhub.ai/user/superior-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Traders, strategy developers, and agents working with Superior Trade use this skill to wrap directional entry signals with a market-regime filter before deciding whether to trade or skip. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading strategy assumptions may fail outside the tested market conditions. <br>
Mitigation: Backtest and paper trade the overlay with current local data before applying it to live or automated trading. <br>
Risk: A regime-confirmed signal can still lose money and the overlay is not a replacement for risk controls. <br>
Mitigation: Pair the gate with explicit entry, stop-loss, take-profit, sizing, and monitoring rules. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/superior-ai/regime-overlay) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code] <br>
**Output Format:** [Markdown guidance with Python function examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces reusable regime-gate logic and tuning guidance; it does not execute trades.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
