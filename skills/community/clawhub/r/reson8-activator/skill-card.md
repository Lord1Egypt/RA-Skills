## Description: <br>
The meta-skill that maps user intent to available tools, skills, MCP servers, APIs, marketplaces, and external repositories so an agent can propose and run capability chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[toolate28](https://clawhub.ai/user/toolate28) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and external agents use this skill to discover available capabilities, route natural-language requests to suitable tools or skill chains, compose multi-step workflows, and prepare marketplace packaging guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can route into powerful account, deployment, file, and public-posting workflows without enough clear boundaries. <br>
Mitigation: Require explicit approval before connected-account access, CHECKPOINT or full-state sharing, execution logging, file writes, connector or plugin creation, cloud provisioning, deployments, package publishing, or public social posting. <br>
Risk: Broad orchestration may activate capabilities outside the user's intended scope. <br>
Mitigation: Review the proposed capability chain with the user before execution and keep high-impact operations gated behind confirmation. <br>


## Reference(s): <br>
- [ClawHub Listing](https://clawhub.ai/toolate28/reson8-activator) <br>
- [Activation Map](references/activation-map.md) <br>
- [Composition Patterns](references/composition-patterns.md) <br>
- [Marketplace Bridges](references/marketplace-bridges.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown plans, capability inventories, workflow chains, and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose actions that require user confirmation before connected-account access, file writes, provisioning, deployment, publishing, or public posting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
