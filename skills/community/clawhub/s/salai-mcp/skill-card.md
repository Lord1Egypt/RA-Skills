## Description: <br>
Israeli grocery shopping and price-comparison assistant over Salai MCP. Use when you need product search, autocomplete, cross-retailer price comparison, cart management, store discovery, retailer discovery, and complementary product recommendations through the Salai remote MCP endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[IdoZiv](https://clawhub.ai/user/IdoZiv) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to Salai's beta MCP service for Israeli grocery product discovery, price comparison, cart management, store and retailer lookup, and complementary product recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Salai API key for access to the beta MCP service. <br>
Mitigation: Store the key only as the SALAI_API_KEY secret, obtain it from the user's Salai profile, and do not paste or expose it in chat or logs. <br>
Risk: The MCP service can add, remove, update, or delete grocery cart items. <br>
Mitigation: Ask the agent to confirm before making cart changes and review proposed cart mutations before execution. <br>
Risk: The integration depends on Salai's beta MCP service. <br>
Mitigation: Use the skill only after beta approval and only if the user trusts the Salai service and endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/IdoZiv/salai-mcp) <br>
- [Salai beta registration](https://app.salai.co.il) <br>
- [Salai MCP endpoint](https://mcp.salai.co.il/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown guidance with MCP tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Salai API key provided through the SALAI_API_KEY secret.] <br>

## Skill Version(s): <br>
0.0.4 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
