## Description:

ToolRouter Gateway provides an OpenClaw skill interface for ToolRouter discovery, status checks, and cached proxy-style tool calls with local usage tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neroagent](https://clawhub.ai/user/neroagent)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users can use this skill to discover ToolRouter-style tools, check gateway status, and route configured tool requests while caching repeated results and logging usage locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill advertises a broad live ToolRouter gateway while the shipped implementation is mock or placeholder behavior.

Mitigation: Treat live gateway and 150+ tool claims as unsupported until the implementation, authentication, and documented behavior are verified.

Risk: Tool inputs and cached results can be persisted locally in plaintext JSONL files.

Mitigation: Do not send secrets, credentials, customer data, private targets, or sensitive prompts through the skill unless caching is disabled or retention controls are redesigned.

Risk: External tool routing can expand data exposure and operational scope.

Mitigation: Require clear tool scoping, authentication, retention controls, and review before using the skill in real workflows.

## Reference(s):

- [ToolRouter](https://toolrouter.com)
- [ToolRouter MCP API endpoint](https://api.toolrouter.com/mcp)
- [ClawHub skill page](https://clawhub.ai/neroagent/skills/toolrouter-gateway)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON tool responses with Markdown guidance and inline command or configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write cache and usage records to local JSONL files when caching or usage tracking is enabled.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
