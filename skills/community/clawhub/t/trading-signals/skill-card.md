## Description:

量化交易信号系统，基于 MACD、RSI、KDJ、布林带和均线为股票和加密货币生成买卖信号。

This skill is ready for commercial/non-commercial use.

## Publisher:

[sanduan003](https://clawhub.ai/user/sanduan003)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to generate technical-analysis signals for stocks and cryptocurrencies as an analysis reference, including MACD, RSI, KDJ, moving-average, and Bollinger Band summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented install command uses an overbroad system Python package install method.

Mitigation: Install dependencies in an isolated virtual environment and avoid --break-system-packages.

Risk: Ticker symbols analyzed by the script are sent to the market-data provider used by yfinance.

Mitigation: Avoid submitting sensitive watchlists or symbols when that disclosure is not acceptable.

Risk: Trading signals may be incomplete, inaccurate, or mistaken for investment advice.

Mitigation: Treat outputs as analysis reference only, validate results independently, and do not make trades solely from this skill's output.

## Reference(s):

- [ClawHub skill page: 量化交易信号](https://clawhub.ai/sanduan003/skills/trading-signals)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Terminal text output with indicator values, signal labels, and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses ticker symbols as command-line inputs and retrieves market data through yfinance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
