## Description: <br>
Manage your API's economic firewall from the terminal. Mint tokens, check status, validate tokens, wrap agent commands. The server-side counterpart to lnget. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wmattadeen-gif](https://clawhub.ai/user/wmattadeen-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure and operate SatGate CLI for API access governance, token minting and validation, health checks, and routing agent commands through a budget-enforced proxy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer downloads a SatGate CLI binary and may place it in a privileged install directory. <br>
Mitigation: Review the installer, prefer a user-writable install directory, and verify the release checksum or source before running scripts/install.sh. <br>
Risk: SatGate API keys or tokens can grant access to protected gateway operations. <br>
Mitigation: Use least-privilege API keys or tokens, store the generated config with restricted permissions, and avoid wrapping untrusted agent commands or MCP clients. <br>


## Reference(s): <br>
- [SatGate homepage](https://satgate.io) <br>
- [ClawHub release page](https://clawhub.ai/wmattadeen-gif/satgate-cli) <br>
- [SatGate Cloud MCP connection](https://cloud.satgate.io/cloud/mcp/connect) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes command examples for setup, status checks, token minting and validation, command wrapping, MCP bridge configuration, installation, and health checks.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
