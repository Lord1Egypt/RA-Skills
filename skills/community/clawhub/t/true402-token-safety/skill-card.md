## Description:

Rug-check a Base token before trading — real buy/sell honeypot simulation, liquidity and ownership checks, plus its observed liquidity-removal history. Free daily checks; ~$0.008/call via x402 after.

This skill is ready for commercial/non-commercial use.

## Publisher:

[true402](https://clawhub.ai/user/true402)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading agents use this skill to assess a token's sellability, liquidity, ownership risks, and observed liquidity-removal history before buying or approving it. It provides risk findings to inform a decision; a current OK result does not guarantee future safety.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automation example can proceed with a purchase after a CAUTION warning without waiting for the user's decision.

Mitigation: Keep CAUTION decisions under explicit user control and existing trading authorization; do not let a warning trigger an automatic purchase.

Risk: A token can appear sellable at check time and later lose liquidity; the historical removal archive is limited to its recorded block range.

Mitigation: Treat OK as a point-in-time result rather than a safety guarantee, and do not interpret 'none observed' as proof that no liquidity was removed.

Risk: A wallet private key supplied through an environment variable can be exposed to processes, shell history, dumps, or logs; anyone who obtains it can spend the wallet balance.

Mitigation: Use the free checks when possible. For paid checks, use a dedicated wallet with a small balance and keep the key out of files and logs.

Risk: The optional swap guard allows a trade to pass when it cannot check the token.

Mitigation: Review the plugin separately and do not treat it as a fail-closed trading control when checks are unavailable.

## Reference(s):

- [true402 API documentation](https://true402.dev/docs/api)
- [true402 OpenAPI specification](https://true402.dev/openapi.json)
- [true402 service catalog](https://true402.dev/api/v1/services)
- [true402 token check](https://true402.dev/check)
- [OpenClaw swap guard plugin source (separate optional plugin)](https://github.com/true402/openclaw-swap-guard)

## Skill Output:

**Output Type(s):** [Analysis, Text, Shell commands, API Calls]

**Output Format:** [Markdown risk summary with an AVOID, CAUTION, or OK verdict and supporting reasons; optional CLI commands or API requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Token check results are point-in-time; liquidity-removal history is Base-only and limited to the archive's recorded block range.]

## Skill Version(s):

1.2.5 (source: SKILL.md frontmatter; server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
