## Description: <br>
SaySigned enables AI agents to register, create, send, sign, decline, and verify e-signature agreements through a remote MCP server or REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[klsv](https://clawhub.ai/user/klsv) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to connect agents to SaySigned so they can prepare agreements, route them to API or email recipients, collect signatures or declines, and verify completion and audit evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ClawScan flags this release as suspicious because it gives an agent legally binding signing authority and handles powerful bearer tokens. <br>
Mitigation: Set an explicit rule that the agent must ask a human before creating, sending, declining, or signing any agreement. <br>
Risk: API keys and recipient access tokens can authorize signing workflows and expose sensitive agreement access. <br>
Mitigation: Treat API keys and recipient access tokens as legal-signing credentials; do not log them, paste them into prompts, reuse them, or store them longer than needed. <br>
Risk: Contract contents and recipient data are sent to a third-party signing service. <br>
Mitigation: Install and use the skill only where the user trusts SaySigned with the agreement content, recipient data, and signing workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/klsv/saysigned) <br>
- [SaySigned documentation](https://www.saysigned.com/docs) <br>
- [SaySigned homepage](https://www.saysigned.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, code, API calls] <br>
**Output Format:** [Markdown guidance with JSON configuration snippets, shell commands, and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes MCP setup instructions, REST examples, tool schemas, signing workflow notes, and security handling guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
