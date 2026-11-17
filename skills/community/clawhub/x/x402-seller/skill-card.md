## Description:

Autonomously monetize your services with x402 payment collection. Set up an x402 server, define paid endpoints, and accept programmatic payments in stablecoins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beocca](https://clawhub.ai/user/beocca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan, implement, configure, deploy, and test x402-protected HTTP services that collect stablecoin payments for API access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles wallet private keys, mnemonics, and CDP API credentials.

Mitigation: Store secrets only in an encrypted secrets manager, avoid command-line arguments for private values, and keep secrets out of code, environment files, logs, and version control.

Risk: The workflow references third-party skills that may generate wallets or receive private keys.

Mitigation: Review and prefer pinned or audited third-party skills before letting them create wallets, handle mnemonics, or process API secrets.

Risk: Payment verification and settlement depend on facilitator URLs and metadata visible to the facilitator.

Mitigation: Use trusted HTTPS facilitator endpoints, restrict CDP key permissions and limits, and treat any custom facilitator as able to observe payment verification metadata.

Risk: The release evidence flags under-scoped dependency and command-line workflows for manual review.

Mitigation: Review dependency versions, pin or audit packages before deployment, and test payment flows on testnet before accepting real payments.

## Reference(s):

- [x402DOCS.md](x402DOCS.md)
- [IDEATION.md](IDEATION.md)
- [Minimal FastAPI seller example](example/README.md)
- [X402-Seller ClawHub page](https://clawhub.ai/beocca/skills/x402-seller)
- [create-crypto-wallets skill](https://clawhub.ai/beocca/skills/create-crypto-wallets)
- [keepass-cli skill](https://clawhub.ai/beocca/skills/keepass-cli)
- [x402-cli skill](https://clawhub.ai/beocca/skills/x402-cli)
- [x402 official site](https://x402.org/)
- [x402 documentation](https://docs.x402.org/introduction)
- [x402 GitHub repository](https://github.com/x402-foundation/x402)
- [CDP getting started](https://docs.cdp.coinbase.com/get-started/overview)
- [CDP x402 facilitator docs](https://docs.cdp.coinbase.com/x402/introduction)
- [x402scan](https://www.x402scan.com/)
- [x402scan GitHub repository](https://github.com/Merit-Systems/x402scan)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks, configuration examples, and runnable example files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup guidance for wallets, facilitator credentials, endpoint pricing, deployment, and a FastAPI x402 seller example.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
