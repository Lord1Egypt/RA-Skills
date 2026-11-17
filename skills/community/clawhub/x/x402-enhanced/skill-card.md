## Description:

Internet-native payments using the HTTP 402 Payment Required standard. Set up as a buyer to pay for API access, or as a seller to monetize your APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[notorious-d-e-v](https://clawhub.ai/user/notorious-d-e-v)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to configure x402 buyer clients, seller servers, facilitators, supported networks, paywalls, and payment examples for APIs that use HTTP 402 payment flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples require wallet private keys or payee addresses for payment flows.

Mitigation: Treat wallet keys as sensitive secrets, use dedicated wallets or spending limits, and start with testnet networks before production use.

Risk: Payment verification can depend on external facilitator services and installed packages.

Mitigation: Verify facilitator URLs and package sources before use, and select a production facilitator intentionally for production deployments.

Risk: Demo API servers can expose paid routes or payment behavior if published unintentionally.

Mitigation: Keep demo servers local unless deliberately deployed, and review host, network, and route settings before exposing them.

## Reference(s):

- [x402 Documentation](https://docs.x402.org)
- [x402 GitHub Repository](https://github.com/coinbase/x402)
- [x402 Default Facilitator](https://x402.org/facilitator)
- [Coinbase x402 Facilitator](https://api.cdp.coinbase.com/platform/v2/x402)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code examples, shell commands, configuration snippets, and reference tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only examples for buyer clients, seller servers, facilitator selection, network identifiers, paywall setup, and testing guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
