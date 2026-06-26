## Description: <br>
Monitors a configured stock watchlist and produces Chinese-language market alerts using cost, price movement, volume, moving-average, RSI, MACD, Bollinger Band, OBV, gap, trailing-stop, and ATR signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skytodmoon](https://clawhub.ai/user/skytodmoon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to run scheduled monitoring of configured stocks and receive informational alerts with technical indicators, news sentiment, and suggested watch points. It is intended for market awareness and does not provide professional financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled watchlist symbols and cost values may disclose sensitive personal portfolio information. <br>
Mitigation: Review or replace the bundled watchlist and cost values before use, and keep the configuration and alert channel private. <br>
Risk: Generated stock alerts and suggestions may be incomplete, stale, or unsuitable as trading advice. <br>
Mitigation: Treat all generated suggestions as informational, verify data independently, and consult qualified financial advice before making trading decisions. <br>
Risk: The skill depends on public market and news endpoints plus local Python dependencies, so availability and data quality can vary. <br>
Mitigation: Install dependencies from trusted sources and review alert output when market-data providers are unavailable or return unexpected data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/skytodmoon/stock-monitor-lite) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Sina Finance quote endpoint](https://hq.sinajs.cn) <br>
- [Eastmoney K-line endpoint](https://push2his.eastmoney.com/api/qt/stock/kline/get) <br>
- [Eastmoney search endpoint](https://searchapi.eastmoney.com/api/suggest/get) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Chinese-language text report with lightweight HTML and Markdown-style formatting] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the configured watchlist and public market/news data to produce informational alerts, not professional financial advice.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
