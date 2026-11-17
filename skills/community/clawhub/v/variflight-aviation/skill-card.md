## Description:

Queries VariFlight for flight status, route options, aircraft location, passenger comfort, airport weather, and connections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lancenas](https://clawhub.ai/user/lancenas)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel-planning agents use this skill to check flight details and live status, search routes and connections, and review airport weather and comfort information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill launches an external MCP package without a pinned version.

Mitigation: Pin or pre-approve the VariFlight MCP package version before installing or running the skill.

Risk: The MCP subprocess receives the full local environment, potentially exposing unrelated credentials.

Mitigation: Run in a constrained environment and pass only the required VariFlight API key to the subprocess.

## Reference(s):

- [VariFlight MCP service](https://ai.variflight.com)
- [VariFlight API key registration](https://ai.variflight.com/keys)
- [VariFlight MCP usage documentation](https://bcnucz2nnop8.feishu.cn/wiki/SDFDwQIaAiM3hxk6uyhcJxSkn2b)
- [VariFlight MCP package](https://www.npmjs.com/package/@variflight-ai/variflight-mcp)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text flight, route, weather, and travel information]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on VariFlight service availability and require a VariFlight API key.]

## Skill Version(s):

1.0.4 (source: skill frontmatter, package.json, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
