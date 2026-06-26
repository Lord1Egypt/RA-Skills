## Description: <br>
wine & food helps an agent use Sippai's MCP service to search partner restaurants, retrieve bottle and glass wine menus, and answer with grounded wine and featured-dish suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sippai](https://clawhub.ai/user/sippai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent hosts use this skill to answer restaurant wine, glass-pour, bottle-list, and featured-dish questions from Sippai partner restaurant data. It is intended for hosts configured to use the Sippai MCP endpoint and to avoid fabricated items, prices, or restaurant choices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may require sensitive Sippai MCP credentials. <br>
Mitigation: Use a scoped Sippai MCP key only when required and inject it through the host's secure configuration rather than storing it in the skill. <br>
Risk: Using a local stdio gateway can run local code outside the hosted MCP service path. <br>
Mitigation: Prefer the documented remote MCP endpoint for normal use; review the local gateway code before enabling stdio development. <br>
Risk: Restaurant, menu, price, or pairing details could become misleading if the agent fills gaps without tool evidence. <br>
Mitigation: Use only fields returned by the Sippai MCP tools, ask the user to choose when multiple restaurants match, and state when data was not returned. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sippai/sip-wine-food) <br>
- [Sippai wine and food documentation](https://sipsiip.com/ai/getwinefood) <br>
- [Sippai MCP endpoint](https://mcp.sipsiip.com/api/sippai) <br>
- [Publisher profile](https://clawhub.ai/user/sippai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown or plain text recommendations grounded in MCP tool results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require a scoped Sippai MCP key; production use should configure only https://mcp.sipsiip.com/api/sippai.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
