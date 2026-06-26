## Description: <br>
VariflightAviation lets agents query VariFlight flight data for flight status, route search, comfort scores, airport weather, transfer planning, and aircraft tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lancenas](https://clawhub.ai/user/Lancenas) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and travel-support agents use this skill to look up flight status, routes, airport weather, transfer options, ticket-price data, and aircraft position details through VariFlight. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill starts an unpinned external npm MCP package with inherited environment variables. <br>
Mitigation: Run it with a dedicated VariFlight API key, avoid unrelated credentials in the shell environment, and prefer a pinned or locally reviewed MCP package before production use. <br>
Risk: Flight status, weather, price, and aircraft position results depend on VariFlight service availability and returned data quality. <br>
Mitigation: Treat outputs as operational travel information that should be checked against airline or airport sources before decisions with safety, cost, or schedule impact. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Lancenas/variflight-aviation) <br>
- [VariFlight MCP Website](https://ai.variflight.com) <br>
- [VariFlight API Key Registration](https://ai.variflight.com/keys) <br>
- [VariFlight MCP Documentation](https://bcnucz2nnop8.feishu.cn/wiki/SDFDwQIaAiM3hxk6uyhcJxSkn2b) <br>
- [@variflight-ai/variflight-mcp on npm](https://www.npmjs.com/package/@variflight-ai/variflight-mcp) <br>
- [Model Context Protocol Specification](https://modelcontextprotocol.io/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text and Markdown command/configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires X_VARIFLIGHT_KEY and network access to VariFlight through the MCP package.] <br>

## Skill Version(s): <br>
1.0.4 (source: SKILL.md frontmatter, package.json, evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
