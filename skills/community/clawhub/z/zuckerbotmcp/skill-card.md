## Description: <br>
ZuckerBot lets agents create, launch, monitor, and manage Facebook and Instagram ad campaigns through the Meta Ads API using the ZuckerBot MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Crumbedsausage](https://clawhub.ai/user/Crumbedsausage) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to plan Meta ad campaigns, generate campaign assets, launch paid Facebook or Instagram campaigns, run A/B tests, monitor performance, and sync conversion feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can launch, resume, or bulk-test paid Meta ad campaigns using stored credentials. <br>
Mitigation: Require explicit human approval before launch, resume, or A/B test actions, including the ad account, campaign, daily budget, destination URL, and variant count. <br>
Risk: Stored ZuckerBot credentials may affect the connected Meta ads account beyond the current chat session. <br>
Mitigation: Connect only the intended ad account, use the least permissions available, and verify the ZuckerBot service and external MCP package before use. <br>
Risk: Conversion sync can send business or customer conversion data to Meta. <br>
Mitigation: Confirm the conversion data, campaign ID, and privacy basis with the user before syncing conversion feedback. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Crumbedsausage/zuckerbotmcp) <br>
- [ZuckerBot Developer Site](https://zuckerbot.ai) <br>
- [zuckerbot-mcp npm package](https://www.npmjs.com/package/zuckerbot-mcp/v/0.2.7) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Markdown or structured tool results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include campaign IDs, launch confirmations, performance metrics, strategy recommendations, ad creative outputs, and conversion sync confirmations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
