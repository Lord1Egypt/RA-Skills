## Description: <br>
YRI AdX helps agents manage Facebook advertising through the baiz.ai MCP API, including campaign creation, budget management, performance monitoring, audience targeting, ad copy, and creative assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuriskills](https://clawhub.ai/user/yuriskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External advertisers, operators, and developers use this skill to prepare, launch, monitor, optimize, scale, and stop Facebook ad campaigns through baiz.ai using JSON-RPC calls and curl examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect real advertising campaigns through publishing, budget changes, start/stop actions, copying, and deletion. <br>
Mitigation: Use least-privilege ad-account credentials, start with sandbox or low-budget test campaigns, and require explicit confirmation before any publish, budget, start/stop, copy, or delete action. <br>
Risk: BAIZ_API_TOKEN is a sensitive credential used for authenticated baiz.ai requests. <br>
Mitigation: Provide the token only through environment-variable injection, use a revocable minimal-permission test token first, and halt installation if registry metadata does not declare BAIZ_API_TOKEN. <br>


## Reference(s): <br>
- [baiz.ai](https://baiz.ai) <br>
- [baiz.ai MCP endpoint](https://baiz.ai/mcp) <br>
- [ClawHub skill listing](https://clawhub.ai/yuriskills/yuri-ad-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl commands and JSON-RPC request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a sensitive BAIZ_API_TOKEN environment variable for authenticated baiz.ai requests.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
