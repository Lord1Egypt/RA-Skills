## Description: <br>
股价异动实时提醒，支持行情接口、邮件和Sonos语音播报。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
CC BY-NC-SA 4.0 <br>


## Use Case: <br>
External users and developers use this skill to monitor configured stock symbols and receive console, email, or Sonos alerts when prices or percentage moves cross configured thresholds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A modified or untrusted config can point apikey_env at sensitive environment variables and send them as an API key. <br>
Mitigation: Keep the config file under user control, use a dedicated Alpha Vantage API key, and never set apikey_env to cloud tokens, session secrets, or other sensitive variables. <br>
Risk: Continuous polling can repeatedly call external quote and notification services. <br>
Mitigation: Run with --once first, confirm the watchlist and notification settings, then enable continuous polling only with an appropriate poll interval. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/stock-price-alert) <br>
- [Publisher Profile](https://clawhub.ai/user/terrycarter1985) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces stock alert status text and optional email or Sonos notification guidance based on local configuration.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
