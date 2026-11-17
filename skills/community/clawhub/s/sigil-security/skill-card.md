## Description:

Secure AI agent wallets via Sigil Protocol. 3-layer Guardian validation on 6 EVM chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[efe-arv](https://clawhub.ai/user/efe-arv)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to configure Sigil smart-account credentials, evaluate proposed ERC-4337 wallet transactions, and submit approved transactions through Sigil Guardian validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review found conflicting claims about whether low-value transactions can be signed by the agent alone.

Mitigation: Confirm Sigil's actual transaction signing policy before installation, especially any low-value co-signing thresholds.

Risk: Wallet execution can move assets if API credentials, account address, or agent signer are misconfigured or exposed.

Mitigation: Use a dedicated agent signer with minimal funds, keep secrets out of logs and client-side code, and store credentials in a production secrets manager.

Risk: Overly broad policy settings can allow unintended targets, functions, or transfer values.

Mitigation: Set conservative per-transaction and daily limits, whitelist targets and function selectors, and review rejection guidance before retrying transactions.

## Reference(s):

- [Agent Setup Guide](references/agent-setup-guide.md)
- [Sigil Protocol API Reference](references/api-reference.md)
- [Sigil Dashboard](https://sigil.codes)
- [Sigil API](https://api.sigil.codes/v1)
- [ERC-4337](https://eips.ethereum.org/EIPS/eip-4337)
- [Sigil Public Repository](https://github.com/Arven-Digital/sigil-public)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON, JavaScript, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIGIL_API_KEY, SIGIL_ACCOUNT_ADDRESS, and SIGIL_AGENT_SIGNER environment variables before use.]

## Skill Version(s):

4.2.1 (source: package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
