## Description: <br>
Qutedance Quotes helps agents look up A-share, Hong Kong stock, and futures quotes, search symbols, and summarize A-share sector movers through a configured Qutedance quote service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yoocky](https://clawhub.ai/user/yoocky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users monitoring A-shares, Hong Kong stocks, and futures use this skill to retrieve quote tables, fuzzy symbol search results, and A-share sector leader or laggard summaries during conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ticker searches and optional API keys are sent to the configured Qutedance quote service. <br>
Mitigation: Install only when the service is trusted, keep the service URL on HTTPS unless using a local development endpoint, and store API keys in environment variables or a secret manager instead of shared config files. <br>
Risk: Market quote data can be delayed, incomplete, or unsuitable for financial decision-making. <br>
Mitigation: Present outputs as informational market data and preserve the artifact's warning that the data does not constitute investment advice. <br>


## Reference(s): <br>
- [Qutedance Quotes ClawHub release](https://clawhub.ai/yoocky/qutedance-quotes) <br>
- [Qutedance quote service endpoint](https://quotedance.api.gapgap.cc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tables and lists with command-line usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on the configured Qutedance service and may include informational market data; the artifact states that data is not investment advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
