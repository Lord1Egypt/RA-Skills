## Description: <br>
Finds the true top-performing US stocks per year by downloading US-listed symbols, filtering by liquidity, and ranking annual returns without relying only on surviving or well-known names. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tltby12341](https://clawhub.ai/user/tltby12341) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and financial research workflows can use this skill to identify high-return US stocks within a liquidity-filtered universe and test whether scanner filters would have caught historical top performers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scripts install and use third-party Python packages and contact public market-data services. <br>
Mitigation: Run in a virtual environment, consider pinning dependency versions, and use only in environments where outbound access to those services is acceptable. <br>
Risk: Market-data downloads may contain gaps, adjusted prices, or service-specific inaccuracies. <br>
Mitigation: Cross-check important results with another market-data source before using them for research conclusions or trading decisions. <br>
Risk: The generated analysis identifies historical performers and can be mistaken for investment advice. <br>
Mitigation: Treat outputs as research artifacts only and independently verify any financial conclusions before relying on them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tltby12341/top-performer-scanner) <br>
- [Publisher Profile](https://clawhub.ai/user/tltby12341) <br>
- [NASDAQ Trader Symbol Directory](ftp://ftp.nasdaqtrader.com/symboldirectory/nasdaqtraded.txt) <br>
- [Yahoo Finance Python Package](https://pypi.org/project/yfinance/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, files, guidance] <br>
**Output Format:** [Markdown guidance with bash commands; Python scripts produce console tables and CSV files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3, pip3, pandas, yfinance, and internet access to public market-data services.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
