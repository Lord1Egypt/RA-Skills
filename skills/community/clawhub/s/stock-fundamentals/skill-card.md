## Description: <br>
Run a local yfinance script to analyze stock fundamentals such as P/E, EPS, margins, debt, ROE, and analyst targets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youpele52](https://clawhub.ai/user/youpele52) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill when a user asks for a quick fundamental view of a stock, ETF, or crypto ticker beyond price movement. It returns valuation, profitability, growth, balance-sheet, dividend, analyst-target, and watch-item context for informational analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The report uses Yahoo Finance data through yfinance and may be incomplete, delayed, unavailable, or unsuitable as financial advice. <br>
Mitigation: Treat the output as informational market data and verify important investment decisions against authoritative sources. <br>
Risk: The command runs Python through uv, installs or uses yfinance, and makes outbound network requests. <br>
Mitigation: Run it only in environments where uv dependency execution and Yahoo Finance network access are allowed. <br>


## Reference(s): <br>
- [Yahoo Finance](https://finance.yahoo.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text fundamentals report with section headings and bullet lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv and network access to Yahoo Finance through yfinance; no API key is required.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
