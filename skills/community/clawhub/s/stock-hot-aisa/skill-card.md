## Description: <br>
Scans trending stocks and crypto movers with live AISA market signals for requests about market momentum, top gainers, and news-driven movers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aisadocs](https://clawhub.ai/user/aisadocs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and market analysts use this skill to request short market-mover scans for stocks and crypto, including momentum names, news catalysts, and watchlist ideas. The output is informational and not financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a user-provided AISA_API_KEY for live market summaries. <br>
Mitigation: Install only if you are comfortable providing that key, and manage the credential according to your organization's policy. <br>
Risk: A custom AISA_BASE_URL can send requests to a non-default endpoint. <br>
Mitigation: Leave AISA_BASE_URL unset unless you intentionally trust the custom endpoint. <br>
Risk: Market summaries can be incorrect, incomplete, or mistaken for financial advice. <br>
Mitigation: Treat results as informational analysis and verify market data before making financial decisions. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown report, with an optional compact JSON summary when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and python3; can focus on stocks, crypto, or both.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
