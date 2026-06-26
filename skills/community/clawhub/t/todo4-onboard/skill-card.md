## Description: <br>
Todo4 Onboard guides an agent through passwordless Todo4 signup, OTP verification, and MCP connection setup from chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[panitw](https://clawhub.ai/user/panitw) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External Todo4 users use this skill to create or connect a Todo4 account and grant their agent access to Todo4 MCP tools through an email OTP onboarding flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives the agent persistent access to the user's Todo4 account through stored credentials. <br>
Mitigation: Install only from the trusted Todo4 publisher profile and revoke the connected agent from Todo4 when access is no longer needed. <br>
Risk: Todo4 tokens and MCP configuration can expose account access if printed, logged, or shared. <br>
Mitigation: Treat ~/.openclaw/.env and ~/.openclaw/mcp_config.json as sensitive files and avoid exposing token-bearing script output in chat or logs. <br>


## Reference(s): <br>
- [Todo4 Onboard ClawHub listing](https://clawhub.ai/panitw/todo4-onboard) <br>
- [Todo4 publisher profile](https://clawhub.ai/user/panitw) <br>
- [Todo4 website](https://todo4.io) <br>
- [Todo4 API base URL](https://todo4.io/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Conversational onboarding guidance with shell command execution and JSON parsing outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes Todo4 MCP configuration and stores a Todo4 agent token under ~/.openclaw when onboarding succeeds.] <br>

## Skill Version(s): <br>
1.3.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
