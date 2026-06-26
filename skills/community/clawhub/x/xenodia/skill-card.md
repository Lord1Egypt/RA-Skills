## Description: <br>
Enables this agent to authenticate with and use the Xenodia Multimodal AI Gateway. Covers two wallet identity modes (local keypair OR CDP Server Wallet), balance checking, model availability queries, and switching your LLM provider to Xenodia. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xenodiaofficial](https://clawhub.ai/user/xenodiaofficial) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent operators use this skill to connect an agent to the Xenodia Multimodal AI Gateway with wallet-based authentication, then check balances, query available models, and configure Xenodia as an LLM provider. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to handle wallet-backed credentials and generated API keys that can authorize Xenodia account activity. <br>
Mitigation: Use a dedicated low-value wallet or tightly scoped CDP credentials, keep keys out of logs and transcripts, and rotate any secret that was printed, pasted, or stored in an exposed location. <br>
Risk: The artifact suggests persisting CDP secrets in a shell startup file, which can increase exposure across sessions and backups. <br>
Mitigation: Prefer a secrets manager or session-scoped environment variables; avoid saving CDP_API_KEY_SECRET, CDP_WALLET_SECRET, or generated API keys in shell profiles. <br>
Risk: An incorrect XENODIA_BASE_URL could send authentication, wallet, or model requests to an unintended endpoint. <br>
Mitigation: Verify the Xenodia base URL before running commands or changing provider configuration. <br>


## Reference(s): <br>
- [ClawHub xenodia release](https://clawhub.ai/xenodiaofficial/xenodia) <br>
- [Xenodia Gateway API](https://api.xenodia.xyz) <br>
- [Xenodia settings](https://xenodia.xyz/settings) <br>
- [Coinbase CDP portal](https://portal.cdp.coinbase.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce wallet addresses, short-lived JWTs, long-term API keys, balance information, model listings, and LLM responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
