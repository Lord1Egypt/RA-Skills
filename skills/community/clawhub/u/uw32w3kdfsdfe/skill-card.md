## Description: <br>
Connect to the Newegg PC Builder MCP service to retrieve PC build configurations, component compatibility checks, and build recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[176wer](https://clawhub.ai/user/176wer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask for Newegg-backed PC build recommendations, component compatibility checks, and build configurations for gaming, workstation, and budget builds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PC build questions, budgets, and component lists may be sent to Newegg's MCP service. <br>
Mitigation: Use the skill only when comfortable sharing that context with Newegg, and ask the agent to confirm before external calls for ambiguous or sensitive purchasing context. <br>
Risk: The external MCP service may return errors or no matching build data. <br>
Mitigation: Report the service result clearly, retry failed calls once when appropriate, and fall back to general PC-building guidance when the service has no data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/176wer/uw32w3kdfsdfe) <br>
- [Newegg PC Builder MCP endpoint](https://apis.newegg.com/ex-mcp/endpoint/pcbuilder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON tool arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include build lists, compatibility reasoning, component details, or no-result fallback guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
