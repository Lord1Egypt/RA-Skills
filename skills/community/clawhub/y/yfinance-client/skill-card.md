## Description: <br>
Provides simplified access to US and Hong Kong stock data from Yahoo Finance, including prices, history, company information, financials, analyst data, screeners, options, and news. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xdl2003](https://clawhub.ai/user/xdl2003) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query market data for US and Hong Kong equities through a Python client. It is suited for retrieving financial datasets and summaries that can support analysis workflows, while treating returned market data as external information that requires validation for financial decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Yahoo Finance data returned through yfinance may be delayed, rate-limited, incomplete, or unavailable for some symbols. <br>
Mitigation: Use the outputs as informational market data, handle network and symbol errors, and verify important results against authoritative financial sources before making decisions. <br>
Risk: Dependency behavior can change across yfinance and pandas releases. <br>
Mitigation: Run the skill in a normal Python virtual environment and pin dependency versions when reproducibility matters. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/xdl2003/yfinance-client) <br>
- [Publisher profile](https://clawhub.ai/user/xdl2003) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Python return values such as floats, dictionaries, lists, and pandas DataFrames, with Markdown and shell command guidance in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Yahoo Finance data retrieval; returned data may be delayed, rate-limited, incomplete, or unavailable for some symbols.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
