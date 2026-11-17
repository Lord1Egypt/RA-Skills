## Description:

Enables this agent to authenticate with and use the Xenodia Multimodal AI Gateway. Covers two wallet identity modes (local keypair OR CDP Server Wallet), balance checking, model availability queries, and switching your LLM provider to Xenodia.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xenodiaofficial](https://clawhub.ai/user/xenodiaofficial)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to connect an agent to Xenodia's OpenAI-compatible gateway with wallet-based authentication, then check balances, query available models, obtain tokens or API keys, and route chat calls through Xenodia.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles wallet credentials and API credentials in persistent ways, including local key files and suggested shell startup exports.

Mitigation: Use a dedicated secret store or tightly permissioned file, avoid saving CDP secrets in ~/.zshrc, and rotate any exposed keys.

Risk: A custom XENODIA_BASE_URL can direct authentication material or API traffic to an unintended endpoint.

Mitigation: Use the default Xenodia endpoint unless the operator controls and trusts the alternate endpoint.

Risk: Changing an agent's LLM provider to Xenodia can disrupt operation if the wallet is unbound or has insufficient balance.

Mitigation: Verify wallet binding, model availability, and balance before applying OpenClaw or other provider configuration changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xenodiaofficial/skills/xenodia)
- [Xenodia Gateway API](https://api.xenodia.xyz/v1)
- [Xenodia settings](https://xenodia.xyz/settings)
- [Coinbase CDP portal](https://portal.cdp.coinbase.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets; helper scripts print wallet addresses, balances, model lists, tokens, API keys, or chat responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Xenodia wallet binding and wallet or CDP credentials; outputs may include short-lived JWTs or long-lived API keys.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
