## Description: <br>
This skill retrieves real-time precious metal prices from https://i.jzj9999.com/quoteh5 and returns bid/ask prices, daily high/low prices, and trend data for 20+ metal types. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[108518](https://clawhub.ai/user/108518) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to retrieve and format real-time precious metal price data for investment monitoring, jewelry pricing, collection decisions, and procurement planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Precious metal prices are time-sensitive and the artifact states they are for reference only. <br>
Mitigation: Verify current prices with authoritative market or business sources before making financial, procurement, or pricing decisions. <br>
Risk: The skill depends on an external quote page that may change, block automation, or become unavailable. <br>
Mitigation: Use reasonable request intervals, review the source site's terms and availability, and handle failures or missing data before relying on the output. <br>
Risk: The security evidence recommends verifying the actual skill files and install commands before installation. <br>
Mitigation: Inspect SKILL.md and any install or execution commands in the release before running them in an agent environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/108518/skill-goldprice) <br>
- [Rongtong Gold quote page](https://i.jzj9999.com/quoteh5) <br>
- [Rongtong Gold website](https://i.jzj9999.com) <br>
- [Playwright documentation](https://playwright.dev/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON examples, JavaScript snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs time-sensitive third-party price data and examples for retrieving or formatting that data.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
