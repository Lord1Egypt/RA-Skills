## Description:

Generates Telegram polling bot and web server scaffolds that integrate Pump.fun Tokenized Agent payments, invoice creation, payment acceptance, and Solana invoice verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[belimad](https://clawhub.ai/user/belimad)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to scaffold pay-to-use Telegram agents and web billing services for Pump.fun Tokenized Agent payment flows. It helps configure Solana RPC, token mint, currency mint, Telegram commands, payment acceptance, and invoice verification before delivering gated service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The payment bot scaffold stores wallet private keys locally and signs blockchain transactions from the server.

Mitigation: Do not use it with real funds or production Telegram users unless it is redesigned to avoid server-side private key custody and server-side signing.

Risk: The template includes an unused treasury private key setting.

Mitigation: Remove unused private key configuration before deployment and avoid collecting secrets that are not required by the payment flow.

Risk: The security evidence flags vulnerable dependencies and unclear payment trust assumptions.

Mitigation: Update vulnerable dependencies, document the payment trust model, and review the scaffold before installation or deployment.

Risk: Service-to-service billing traffic may be configured without secure transport.

Mitigation: Require secure transport and strong service authentication for non-local deployments.

## Reference(s):

- [Pump Tokenized Agents integration notes](artifact/references/PUMP_TOKENIZED_AGENTS.md)
- [Pump.fun tokenized agents reference skill](https://raw.githubusercontent.com/pump-fun/pump-fun-skills/refs/heads/main/tokenized-agents/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated Node.js project files, command snippets, and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a stamped Telegram polling bot and Fastify-style billing service scaffold that must be configured with deployment-specific payment and Telegram settings.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
