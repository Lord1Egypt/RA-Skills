## Description:

Guides users through installing and configuring the Simmer MCP server in their agent runtime, then verifying its trading tools are available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simmer](https://clawhub.ai/user/simmer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users configure Simmer market and trading tools for an MCP-aware runtime after registering an agent and obtaining an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installed server grants persistent access to Simmer market and trading tools in the chosen agent runtime.

Mitigation: Install only when needed and prefer local or project scope where available.

Risk: An API key stored on a shared or cloud machine could expose trading access.

Mitigation: Avoid storing live-trading keys on shared or cloud machines.

Risk: Enabling live-trading settings can permit real-money orders.

Mitigation: Keep the default paper/sim behavior unless deliberately enabling the live-trading gates.

## Reference(s):

- [Simmer documentation](https://docs.simmer.markets)
- [simmer-mcp npm package](https://www.npmjs.com/package/simmer-mcp)
- [Simmer wallet setup for real-money trading](https://clawhub.ai/skills/simmer-wallet-setup)
- [Simmer Python SDK skill](https://clawhub.ai/skills/simmer)

## Skill Output:

**Output Type(s):** [Configuration instructions, Shell commands, Guidance]

**Output Format:** [Markdown with shell commands and MCP configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runtime-specific setup and verification steps; requires SIMMER_API_KEY for authenticated tools.]

## Skill Version(s):

0.3.6 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
