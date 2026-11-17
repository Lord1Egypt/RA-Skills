## Description:

Set up OpenSpend CLI and optional Coinbase payments-mcp for payment-enabled workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albertpurnama](https://clawhub.ai/user/albertpurnama)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to install, update, authenticate, and troubleshoot OpenSpend CLI, and to optionally configure Coinbase Payments MCP for payment-enabled agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer commands can execute code from external distribution paths, including a curl-based installer.

Mitigation: Review before installing, prefer the Homebrew path or a pinned and verified release, and avoid curl | sh unless the installer has been independently checked.

Risk: The Payments MCP setup uses an unpinned package and can persist client configuration.

Mitigation: Pin @coinbase/payments-mcp to a reviewed version and confirm any ~/.codex/mcp.json change before saving it.

Risk: Payment-enabled workflows can spend funds through paid requests.

Mitigation: Require explicit user approval and spending limits before paid requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/albertpurnama/skills/setup-services)
- [OpenSpend installer](https://openspend.ai/install)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes preflight checks, install and update commands, MCP configuration guidance, authentication checks, payment workflow guidance, and troubleshooting steps.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
