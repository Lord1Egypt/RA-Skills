## Description: <br>
Pay for resources via the x402 HTTP payment protocol using gasless USDC transfers on Base without accounts or KYC, enabling cryptographic identity-based access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LumenFromTheFuture](https://clawhub.ai/user/LumenFromTheFuture) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to make machine-to-machine x402 payments for paid HTTP resources such as compute, APIs, domains, and service credits using USDC on Base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can authorize real USDC payments through x402 flows without built-in confirmation or spend limits. <br>
Mitigation: Use a dedicated low-balance wallet, restrict use to trusted URLs, and review the amount, recipient, network, and token before signing. <br>
Risk: Wallet private keys may be exposed if a main wallet key is provided through environment variables or wallet files. <br>
Mitigation: Avoid using a main wallet private key, keep wallet files restricted, and use a separate wallet created for agent payment activity. <br>


## Reference(s): <br>
- [x402 Protocol Spec](https://x402.org) <br>
- [EIP-3009: Transfer With Authorization](https://eips.ethereum.org/EIPS/eip-3009) <br>
- [Conway Documentation](https://docs.conway.tech) <br>
- [ClawHub Skill Page](https://clawhub.ai/LumenFromTheFuture/x402) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with JavaScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces x402 payment helper code and command examples that may sign and submit USDC payments when supplied with a funded wallet.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
