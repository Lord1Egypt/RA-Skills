## Description: <br>
Secure AI agent wallets via Sigil Protocol. 3-layer Guardian validation on 6 EVM chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[efe-arv](https://clawhub.ai/user/efe-arv) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to configure Sigil-protected ERC-4337 smart wallets, evaluate transactions through Guardian validation, and submit approved on-chain operations across supported EVM chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive wallet-related credentials, including an API key and agent signer material. <br>
Mitigation: Store credentials in a secrets manager, restrict local config permissions, and treat SIGIL_API_KEY and SIGIL_AGENT_SIGNER as wallet credentials. <br>
Risk: An agent could submit transactions that exceed the operator's intended authority or value limits if policies are too broad. <br>
Mitigation: Configure least-authority signer permissions, spending limits, explicit target and function whitelists, and conservative transaction policies before use. <br>
Risk: Funding the agent signer or exposing owner credentials can undermine the intended separation between owner wallet, Sigil account, and agent signer. <br>
Mitigation: Use a dedicated agent signer, keep owner wallet credentials out of the agent environment, and fund the agent signer only with minimal gas. <br>


## Reference(s): <br>
- [Agent Setup Guide](references/agent-setup-guide.md) <br>
- [Sigil Protocol API Reference](references/api-reference.md) <br>
- [Sigil Dashboard](https://sigil.codes) <br>
- [Sigil API](https://api.sigil.codes/v1) <br>
- [ClawHub Skill Page](https://clawhub.ai/efe-arv/sigil-security) <br>
- [ERC-4337](https://eips.ethereum.org/EIPS/eip-4337) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, code, API calls] <br>
**Output Format:** [Markdown with JSON, bash, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIGIL_API_KEY, SIGIL_ACCOUNT_ADDRESS, and SIGIL_AGENT_SIGNER to be configured by the operator.] <br>

## Skill Version(s): <br>
4.2.1 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
