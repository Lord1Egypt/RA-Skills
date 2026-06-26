## Description: <br>
Semantic quote search with source transparency. Find quotes by meaning, not keywords. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quotewisio](https://clawhub.ai/user/quotewisio) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to search for quotes by meaning, person, source, exact text, similarity, or random selection, with source transparency and attribution-checking support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill invokes third-party npm tooling with npx and connects to the Quotewise MCP service. <br>
Mitigation: Install and use it only when the user trusts Quotewise and the invoked npm tools. <br>
Risk: Configuring an Authorization header may store a Quotewise API key in client configuration. <br>
Mitigation: Use a dedicated Quotewise API key where possible and review local MCP client configuration storage. <br>
Risk: Quote-search queries may be sent to an external service. <br>
Mitigation: Avoid sending sensitive private text as quote-search or attribution-checking queries. <br>


## Reference(s): <br>
- [Quotewise homepage](https://quotewise.io) <br>
- [Quotewise MCP documentation](https://quotewise.io/developers/mcp/) <br>
- [Plans and pricing](https://quotewise.io/plans/) <br>
- [ClawHub release page](https://clawhub.ai/quotewisio/quotewise) <br>
- [MCP setup repository](https://github.com/quotewise/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell command examples and JSON MCP responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional QUOTEWISE_API_KEY enables collections and higher rate limits; anonymous access is limited to 20 requests per day.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
