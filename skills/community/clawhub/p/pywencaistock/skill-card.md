## Description: <br>
Uses the pywencai library to retrieve Tonghuashun Wencai stock data, including real-time quotes, financial indicators, Dragon Tiger List data, capital flows, and A-share market queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nnzenw](https://clawhub.ai/user/nnzenw) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, analysts, and agent builders use this skill to query Chinese stock-market data through natural-language pywencai searches and receive structured results for reporting, screening, and analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock-query text is sent to pywencai and Tonghuashun Wencai. <br>
Mitigation: Avoid submitting proprietary trading research, sensitive watchlists, or other confidential market-analysis prompts. <br>
Risk: The documentation mentions an SSL workaround that disables certificate verification. <br>
Mitigation: Do not disable certificate verification; fix certificates or dependency versions instead. <br>
Risk: The example script prepends /tmp/mootdx to the Python import path. <br>
Mitigation: Run examples only in an environment where that path cannot be controlled by another user. <br>


## Reference(s): <br>
- [PyWenCai API Reference](references/pywencai-api.md) <br>
- [PyWenCai Query Examples](references/query_examples.md) <br>
- [pywencai GitHub](https://github.com/stephanj/pywencai) <br>
- [Tonghuashun Wencai](https://www.iwencai.com/) <br>
- [PyWenCai Stock on ClawHub](https://clawhub.ai/nnzenw/pywencaistock) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance, data] <br>
**Output Format:** [Python pandas DataFrame results with optional CSV, Excel, JSON, or Markdown table conversion guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returned columns depend on the pywencai query and Tonghuashun Wencai response.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
