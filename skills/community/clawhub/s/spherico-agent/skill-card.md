## Description: <br>
End-to-end Bitnow network API workflows for AI agents. Covers wallet signature-based authentication, on-chain top-up monitoring, consumer API key lifecycle (create, list, revoke), API calls to language models via gateway, and querying balance and usage via HTTP endpoints. Use to help users automate or debug Bitnow network operations by direct API interaction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Viyozc](https://clawhub.ai/user/Viyozc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to generate API-focused Bitnow workflows for wallet authentication, deposits, API key management, model inference, usage review, and provider setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports sensitive Bitnow API operations where session tokens, API keys, wallet signatures, provider auth values, or full HTTP responses could be exposed if pasted into agent chats, logs, or scripts. <br>
Mitigation: Use placeholders, environment variables, or a secret manager, and redact tokens, keys, signatures, provider auth values, wallet-sensitive data, and unneeded response fields before sharing. <br>
Risk: The workflows include fund transfers, token allowances, parent-account links, supplier registration, and GPU endpoint updates that can change balances, account relationships, or provider configuration. <br>
Mitigation: Independently verify the official gateway, chain ID, token address, deposit contract, and target account details, then manually confirm each account-changing or funds-related action before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Viyozc/spherico-agent) <br>
- [Bitnow test gateway](https://gateway-test.bitnow.ai) <br>
- [Base Sepolia RPC](https://sepolia.base.org) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with curl commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses placeholders for gateway URLs, wallet addresses, session tokens, API keys, signatures, and provider credentials.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
