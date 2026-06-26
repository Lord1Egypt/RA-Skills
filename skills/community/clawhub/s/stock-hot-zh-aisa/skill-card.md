## Description: <br>
Scans live AISA-backed market data to surface trending stocks, cryptocurrencies, top movers, and news-driven momentum. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aisadocs](https://clawhub.ai/user/aisadocs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Traders, analysts, and market-monitoring agents use this skill to request a current hot-assets scan for equities and crypto. The output is informational and is not financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an AISA API key for live market scans. <br>
Mitigation: Use a dedicated AISA_API_KEY, keep it out of prompts and logs, and rotate it if exposure is suspected. <br>
Risk: Changing AISA_BASE_URL could route requests to an untrusted endpoint. <br>
Mitigation: Leave AISA_BASE_URL unset or set it only to the trusted AISA endpoint. <br>
Risk: Market summaries and watchlists can be mistaken for investment advice. <br>
Mitigation: Treat generated reports as informational only and require independent review before trading decisions. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/aisadocs/stock-hot-zh-aisa) <br>
- [AISA API endpoint](https://api.aisa.one/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with tables; optional appended JSON summary when the script is run with --output json] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY; supports focus selection for stocks, crypto, or both.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
