## Description:

Stipend gives an AI agent a non-custodial USDC wallet on Base for receiving payments, making limited payouts, paying HTTP 402/x402 charges, and reporting earned-versus-spent status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[graphiker-australia](https://clawhub.ai/user/graphiker-australia)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to equip an agent with wallet setup, payment, x402, spending-limit, credit, referral, and reporting workflows. It is intended for agents that may handle real USDC on Base mainnet, so operators should approve installation, wallet custody, limits, and recovery practices before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to install remote code and create persistent wallet keys before explicit operator approval.

Mitigation: Require a human operator to review and approve the installer source, installation location, wallet creation, passphrase storage, and recovery or uninstall plan before execution.

Risk: The skill uses real USDC on Base mainnet, where transfers are final and lost keys cannot be recovered.

Mitigation: Use a small working balance, test with dry runs or testnet where appropriate, back up the keystore securely, and never expose the private key or passphrase.

Risk: Default spending limits, paid credits, x402 payments, and referral behavior can create financial activity without enough operator visibility.

Mitigation: Have the operator explicitly approve spending limits, lock or restrict destinations when possible, review payment reports, and approve any use of vendor credits or referral workflows.

## Reference(s):

- [Stipend homepage](https://stipend.sh)
- [ClawHub skill page](https://clawhub.ai/graphiker-australia/skills/stipend)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python snippets, configuration examples, and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes wallet setup, payment, x402, limits, credits, referral, directory, and troubleshooting guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 0.46.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
