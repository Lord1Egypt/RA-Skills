## Description: <br>
Read-only signal fetcher for TradeBot Alpha API. Subscription required for Pro tier. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zalcmann](https://clawhub.ai/user/zalcmann) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading-tool users use this skill to check TradeBot Alpha service status and request market signal analysis for a supplied symbol through the TradeBot Alpha API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The connector sends a user-provided TradeBot Alpha API key and requested trading symbol to the TradeBot Alpha HTTPS API. <br>
Mitigation: Install only if you trust BlueFeza KG and the TradeBot Alpha service with the API key and requested symbols. <br>
Risk: Passing an API key directly on the command line can expose it through shell history or process inspection. <br>
Mitigation: Prefer a safer secret-handling method than typing the key directly in a shell command. <br>
Risk: Trading signals can be incorrect, delayed, or unsuitable for a user's circumstances. <br>
Mitigation: Treat trading signals as informational rather than a guarantee or financial advice, and keep users responsible for trading decisions. <br>


## Reference(s): <br>
- [TradeBot Alpha Skill Page](https://clawhub.ai/zalcmann/tradebot-alpha) <br>
- [TradeBot Alpha Homepage](https://tradebot-alpha.bluefeza.com) <br>
- [TradeBot Alpha API Documentation](https://tradebot-alpha.bluefeza.com/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Status and analysis commands send the API key and requested symbol to the TradeBot Alpha HTTPS API.] <br>

## Skill Version(s): <br>
0.1.14 (source: server release metadata; artifact frontmatter and package.json report 0.1.13) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
