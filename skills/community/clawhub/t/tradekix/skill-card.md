## Description: <br>
Query financial market data via the Tradekix API, including stock prices, crypto, forex, indices, market news, earnings, economic events, Congressional trades, and social sentiment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jamesjohnfox](https://clawhub.ai/user/jamesjohnfox) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use Tradekix to retrieve financial market data, market news, calendars, sentiment, and Congressional trade information through the Tradekix API. The skill also supports API key signup, account upgrade, and key revocation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Signup sends agent name and email details to Tradekix and stores a local API key. <br>
Mitigation: Run signup only after explicit user approval, protect the local config file, and avoid displaying the full API key. <br>
Risk: Upgrade and revoke commands can change billing or API-key state. <br>
Mitigation: Require explicit user approval before running upgrade or revoke actions. <br>
Risk: Displaying the documented config file can reveal the full API key. <br>
Mitigation: Use masked status output or inspect only non-secret fields instead of printing the config file. <br>


## Reference(s): <br>
- [Tradekix API Reference](references/api-docs.md) <br>
- [Tradekix API Base URL](https://www.tradekix.ai/api/v1) <br>
- [ClawHub Skill Page](https://clawhub.ai/jamesjohnfox/tradekix) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses use JSON objects with success, data, and meta fields; rate-limit status is reported in response metadata when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
