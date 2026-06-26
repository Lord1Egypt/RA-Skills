## Description: <br>
Calls a Prana-hosted remote agent to analyze and calculate TradingView technical indicators, then returns the result to the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaochengzhen](https://clawhub.ai/user/xiaochengzhen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request TradingView technical-indicator analysis, stock indicator calculations, and related market-analysis reports through Prana. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial-analysis prompts are sent to Prana. <br>
Mitigation: Do not include private account data, credentials, unpublished trading plans, or other sensitive financial context in prompts. <br>
Risk: The skill stores PRANA_SKILL_API_FLAG persistently in OpenClaw. <br>
Mitigation: Review before installing and remove the stored key when the skill is no longer needed. <br>
Risk: The skill can expose a Prana history link. <br>
Mitigation: Share the returned history link only with the intended user and avoid logging or storing the full link. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaochengzhen/tv-indicators-analysis) <br>
- [Prana service homepage](https://www.prana.chat/) <br>
- [Prana API key endpoint](https://www.prana.chat/api/v2/api-keys) <br>
- [Prana agent execution endpoint](https://www.prana.chat/api/claw/agent-run) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, API Calls, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PRANA_SKILL_API_FLAG and sends prompts to a Prana-hosted remote agent.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
