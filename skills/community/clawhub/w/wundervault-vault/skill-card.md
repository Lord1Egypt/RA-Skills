## Description:

Use the owner's API keys, SSH keys, wallets and signing keys without ever holding them. A Wundervault broker on this computer makes web calls, SSH commands, x402 payments and signatures for you and returns the result with the secret removed. Free account at wundervault.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snoweman](https://clawhub.ai/user/snoweman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using an agent with Wundervault configured can make approved web API calls, run SSH operations, make x402 payments, and request signatures using credentials held by the local broker.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation uses an external package and may require administrator commands.

Mitigation: Review the package and installer before running administrator commands, as the security guidance recommends.

Risk: Agent access can enable actions with credentials, SSH keys, wallets, or signing keys; agents under the same operating-system account can access one another's broker tokens.

Mitigation: Grant only needed credentials and hosts, require approval for sensitive actions, set payment limits, and run agents with different trust levels under separate operating-system accounts.

Risk: The security review covers the skill instructions and does not verify the external broker's security guarantees.

Mitigation: Review Wundervault's verification and limitations references and inspect the installer before setup.

## Reference(s):

- [Wundervault MCP tool reference](https://wundervault.com/mcp)
- [Wundervault security verification](https://wundervault.com/verify)
- [Wundervault limitations](https://wundervault.com/limitations)
- [Computer setup guide](https://wundervault.com/help/computer)
- [Installation and upgrade guide](https://wundervault.com/install)
- [Wundervault](https://wundervault.com)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance, Text]

**Output Format:** [Structured tool requests and text responses; Markdown setup guidance with shell commands and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the owner's configured entries and approvals; the skill instructions say tools return results without secret values.]

## Skill Version(s):

2.1.0 (source: server-resolved release metadata, artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
