## Description: <br>
Comprehensive trading knowledge base covering fundamentals, technicals, strategies, backtesting, and risk management for agents building trading apps or evaluating strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rmbell09-lang](https://clawhub.ai/user/rmbell09-lang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill as a trading education and strategy reference when building trading apps, evaluating strategy ideas, and planning backtesting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contains trading education and strategy guidance that could be mistaken for personalized financial, legal, or tax advice. <br>
Mitigation: Treat outputs as educational references only, independently verify any strategy, and consult qualified professionals for financial, legal, or tax decisions. <br>
Risk: Following strategy suggestions without validation could lead to losses from overfitting, poor data quality, fees, slippage, or changing market conditions. <br>
Mitigation: Backtest with clean data, include fees and slippage, use out-of-sample validation, paper trade first, and start with minimal position sizes only after review. <br>
Risk: Artifact content discusses broker and exchange APIs, including live trading and API key handling. <br>
Mitigation: Do not give an agent live trading keys or withdrawal permissions without a separate security review; prefer read-only keys, testnets, paper trading, IP allowlists, and independent operator approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rmbell09-lang/trading-strategies) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional code, shell commands, and configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No automatic trading, installation, credential access, persistence, or live order execution behavior is present in artifact evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
