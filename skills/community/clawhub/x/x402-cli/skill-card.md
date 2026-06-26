## Description: <br>
Pay for x402 payment-gated HTTP endpoints using USDC stablecoins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[razvanmacovei](https://clawhub.ai/user/razvanmacovei) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and agents use this skill to access APIs that return HTTP 402 payment requirements, first probing the endpoint for price, network, and asset details, then signing a USDC payment to retrieve the response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent raw private-key spending authority for USDC payments. <br>
Mitigation: Use a dedicated low-balance wallet, never a main wallet, and provide the private key only for the intended task. <br>
Risk: Auto-approved payment examples can spend funds without documented spend limits. <br>
Mitigation: Probe first, verify price, network, asset, endpoint, and recipient before paying, and avoid unbounded automated use. <br>
Risk: Using self-signed TLS mode can weaken endpoint verification. <br>
Mitigation: Reserve self-signed TLS usage for local development and use verified TLS before making funded payments. <br>


## Reference(s): <br>
- [x402-cli homepage](https://github.com/razvanmacovei/x402-cli) <br>
- [ClawHub skill page](https://clawhub.ai/razvanmacovei/x402-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with bash commands and JSON field references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires x402-cli and EVM_PRIVATE_KEY; payment responses may include backend response bodies and transaction hashes.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
