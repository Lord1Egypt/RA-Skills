## Description: <br>
Access ATXP paid API tools for real-time web search, AI image generation, music creation, video generation, and X/Twitter search after authenticating with `npx atxp login`. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[syveraerp](https://clawhub.ai/user/syveraerp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to access ATXP paid search, media generation, and X/Twitter search tools from an agent workflow after authenticating an ATXP account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill tells agents to run unpinned external CLI code through `npx atxp`. <br>
Mitigation: Install only if the user trusts the ATXP npm package and provider, and review the package/version before execution. <br>
Risk: The skill instructs agents to source a local ATXP credential config file. <br>
Mitigation: Confirm which ATXP account is loaded and prefer a scoped environment variable export over broadly sourcing `~/.atxp/config` in a long-lived shell. <br>
Risk: ATXP operations may consume paid usage or expose prompts to the provider. <br>
Mitigation: Expect paid usage or credit consumption, and avoid sensitive prompts unless ATXP's data handling is acceptable. <br>


## Reference(s): <br>
- [ATXP Search MCP endpoint](https://search.mcp.atxp.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, API calls] <br>
**Output Format:** [Markdown with inline bash and TypeScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents to run ATXP CLI commands or call ATXP MCP tools after authentication.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
