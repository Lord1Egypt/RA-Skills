## Description: <br>
Build, install, update, and use a WhiteBIT trading guidance and training skill through ClawHub (clawhub.ai) for OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zonder](https://clawhub.ai/user/zonder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operators use this skill to learn WhiteBIT spot trading workflows, validate documented API request parameters, and prepare execution-ready plans before using a separate trading executor. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may mistake documentation-backed planning output for live trading capability. <br>
Mitigation: Use the skill as a training and request-planning aid only; require a separate execution system for balances, order placement, cancellation, and order-status verification. <br>
Risk: Trading API credentials could be exposed if copied into skill files or publish artifacts. <br>
Mitigation: Keep WhiteBIT API keys only in a trusted external executor and review files before using ClawHub publish or sync commands. <br>
Risk: A prepared request could be executed externally without adequate operator review. <br>
Mitigation: Require human confirmation before any live order outside this skill and verify account state, fees, and order status through the external executor. <br>


## Reference(s): <br>
- [ClawHub whitebit skill page](https://clawhub.ai/zonder/whitebit) <br>
- [WhiteBIT Docs MCP server](https://docs.whitebit.com/mcp) <br>
- [ClawHub CLI Reference](references/clawhub-cli.md) <br>
- [MCP Setup](references/mcp-setup.md) <br>
- [Trade Checklist](references/trade-checklist.md) <br>
- [WhiteBIT API Basics](references/whitebit-api-basics.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with structured sections and inline code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces training walkthroughs, documented API request plans, lifecycle commands, validation checklists, and external execution verification guidance; it does not perform live trading by itself.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
