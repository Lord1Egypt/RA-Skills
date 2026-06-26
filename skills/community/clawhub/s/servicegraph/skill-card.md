## Description: <br>
Servicegraph helps agents use ServiceGraph to discover datasets, inspect schemas and filters, search free brief rows, and unlock contact and metric details through the ServiceGraph REST or MCP APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nostrband](https://clawhub.ai/user/nostrband) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a user explicitly asks for ServiceGraph data discovery, schema exploration, business dataset search, credit balance checks, or paid row unlocks. It is intended for dataset-agnostic ServiceGraph workflows and defers intent-only requests to more specific skills when available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use OAuth or API-key credentials for ServiceGraph access. <br>
Mitigation: Keep credentials out of model context, use environment-backed authentication, and ask the user to configure SERVICEGRAPH_API_KEY instead of pasting secrets into chat. <br>
Risk: Unlocking ServiceGraph rows spends credits. <br>
Mitigation: Read the dataset price and credit balance from the API, then confirm the exact unlock cost with the user before calling unlock_rows. <br>
Risk: Dataset names, field names, values, and prices can change over time. <br>
Mitigation: Discover datasets, schemas, filter values, and prices at runtime instead of relying on hardcoded assumptions. <br>


## Reference(s): <br>
- [ServiceGraph API](https://api.servicegraph.co) <br>
- [ServiceGraph MCP](https://mcp.servicegraph.co) <br>
- [ServiceGraph API keys](https://servicegraph.co/profile/api-keys) <br>
- [ClawHub skill page](https://clawhub.ai/nostrband/servicegraph) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with API request guidance and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use ServiceGraph MCP tools or REST calls; authenticated unlocks can spend ServiceGraph credits after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
