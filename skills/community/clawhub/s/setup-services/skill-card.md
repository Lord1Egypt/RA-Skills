## Description: <br>
Sets up OpenSpend CLI and optional Coinbase payments-mcp for payment-enabled workflows, including installation, updates, authentication, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[albertpurnama](https://clawhub.ai/user/albertpurnama) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to install, authenticate, verify, and troubleshoot OpenSpend CLI and optionally configure Coinbase Payments MCP for paid service workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet-backed paid requests can spend funds without clear per-request approval or spend limits. <br>
Mitigation: Require explicit approval for each paid request, including destination, purpose, exact maximum amount, network, and whether repeat payments are allowed. <br>
Risk: Payment tooling may remain available in the MCP client after the workflow is complete. <br>
Mitigation: Remove the payments MCP server from the client configuration when it is no longer needed. <br>
Risk: The alternative curl installer executes a remote installation script. <br>
Mitigation: Prefer the Homebrew install path and use the curl installer only with explicit user approval. <br>


## Reference(s): <br>
- [OpenSpend installer](https://openspend.ai/install) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes approval checkpoints for installation, authentication, and paid payment workflows.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
