## Description: <br>
Monitors Upbit cryptocurrency positions, calculates technical indicators, and records GLM-assisted watch, sell, and adjustment signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smeuse-dev](https://clawhub.ai/user/smeuse-dev) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and traders use this skill to run a Node.js Upbit market monitor that checks position prices, calculates indicators, calls a GLM helper for analysis, and records events for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for exchange credentials and may be used around real trading accounts. <br>
Mitigation: Use a dedicated least-privilege Upbit key, prefer read-only access unless live trading is explicitly intended, and never grant withdrawal permission. <br>
Risk: The GLM analysis path depends on an unbundled ../zai/ask.sh helper that was not included in the reviewed artifact. <br>
Mitigation: Inspect, replace, or remove that helper before running the skill, especially because prompts may include position and strategy details. <br>
Risk: The release overstates implemented trading and notification behavior relative to the reviewed artifact. <br>
Mitigation: Treat the skill as a signal and monitoring bot unless the publisher ships and documents actual order execution and Telegram notification behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smeuse-dev/upbit-trading-skill) <br>
- [Upbit Open API management](https://upbit.com/mypage/open_api_management) <br>
- [Upbit accounts API endpoint](https://api.upbit.com/v1/accounts) <br>
- [Upbit ticker API endpoint](https://api.upbit.com/v1/ticker?markets=${market}) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Console text, JSON event files, JavaScript code, and setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads Upbit API credentials from environment variables and writes local positions, events, and trade log JSON files.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
