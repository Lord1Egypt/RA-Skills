## Description: <br>
Route beginner-friendly natural-language requests for TradeAlpha news and login into the TradeAlpha plugin tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiuwei2](https://clawhub.ai/user/jiuwei2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to turn plain-language TradeAlpha news and login requests into calls to the TradeAlpha plugin tools. It helps route requests for market news, source filters, login, token initialization, and token refresh while preserving concise user-facing responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can route generic news requests to a third-party TradeAlpha service that may ask for credentials. <br>
Mitigation: Install only when the user intends TradeAlpha to handle these news requests and trusts quantaccess.lxaa.top. <br>
Risk: Authentication may use sensitive credentials or a persisted local token. <br>
Mitigation: Prefer a scoped TRADEALPHA_API_KEY, do not echo passwords or tokens, and remove the local config file when token persistence is not desired. <br>
Risk: The skill depends on separate plugin tools for login and news retrieval. <br>
Mitigation: Confirm tradealpha_login and tradealpha_news are loaded before attempting login or news requests. <br>


## Reference(s): <br>
- [TradeAlpha service homepage](https://quantaccess.lxaa.top) <br>
- [ClawHub release page](https://clawhub.ai/jiuwei2/tradealpha-open-platform) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API Calls, configuration] <br>
**Output Format:** [Markdown text with routed tool calls and summarized news results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request account and password for login, may use TRADEALPHA_API_KEY, and may rely on a local TradeAlpha token configuration file.] <br>

## Skill Version(s): <br>
0.6.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
