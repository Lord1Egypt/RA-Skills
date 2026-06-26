## Description: <br>
Connect OpenClaw agents to Settld MCP for paid tool calls with quote-bound authorization and verifiable receipts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aidenlippert](https://clawhub.ai/user/aidenlippert) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to register and operate Settld MCP tooling in OpenClaw agents for paid tool calls, authorization flows, verifiable receipts, and settlement artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent access to paid calls and settlement actions without clear approval or spend controls. <br>
Mitigation: Configure policy so every paid call or settlement action shows the quote and requires explicit user approval before money is spent or records are changed. <br>
Risk: A compromised or unintended Settld API key could expose paid-call or settlement authority. <br>
Mitigation: Use a least-privilege Settld API key, treat it as secret input, and avoid printing full API keys in chat output. <br>
Risk: The MCP server package is installed through npx at runtime. <br>
Mitigation: Pin and verify the settld-mcp npm package before installing or running it in an agent environment. <br>


## Reference(s): <br>
- [Settld MCP Payments release page](https://clawhub.ai/aidenlippert/settld-mcp-payments) <br>
- [MCP server example](artifact/mcp-server.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, JSON] <br>
**Output Format:** [Markdown guidance with MCP server JSON configuration and inline shell command details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup and usage instructions for agent operators; payment and settlement outputs depend on the configured Settld MCP server.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
