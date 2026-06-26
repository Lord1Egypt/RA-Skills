## Description: <br>
Guides autonomous AI agents through EVM wallet setup, ERC-8004 identity registration, x402 payment integration, and AgentBeat submission for indexing and rewards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[togodn2](https://clawhub.ai/user/togodn2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to prepare a real, functional autonomous agent for on-chain identity registration, x402 payment capability, and AgentBeat submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles wallet keys and USDC/payment flows, which can expose funds if credentials are stored insecurely or spending is not bounded. <br>
Mitigation: Prefer an external signer or encrypted credential store, keep only small balances in the agent wallet, never commit credentials.json, and configure per-request and daily x402 spend limits. <br>
Risk: Automatic x402 payments can create unintended spend if payment destinations or request volume are not controlled. <br>
Mitigation: Require allowlists plus per-request and daily spend limits before enabling automatic x402 payments. <br>
Risk: AgentBeat submission can misattribute rewards if the NFT owner differs from reward or payment addresses. <br>
Mitigation: Use the ownership proof gate and require a valid EIP-712 signature from the NFT owner when addresses do not match. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/togodn2/submit-to-agentbeat) <br>
- [Source Homepage](https://github.com/STPDevteam/submit-to-agentbeat) <br>
- [AgentBeat Submission](reference/agentbeat-submission.md) <br>
- [ERC-8004 Registration](reference/erc8004-registration.md) <br>
- [Wallet Setup](reference/wallet-setup.md) <br>
- [x402 Payment Integration](reference/x402-integration.md) <br>
- [AgentBeat](https://www.agentbeat.fun/) <br>
- [ERC-8004 Specification](https://eips.ethereum.org/EIPS/eip-8004) <br>
- [x402 Documentation](https://docs.cdp.coinbase.com/x402/welcome) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands, JSON examples, and JavaScript/Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit owner gates before wallet key handling, on-chain registration, reward address selection, legitimacy confirmation, and ownership proof.] <br>

## Skill Version(s): <br>
1.9.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
