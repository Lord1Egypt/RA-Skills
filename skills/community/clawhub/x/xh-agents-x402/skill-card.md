## Description:

Helps agents discover and pay for x402 data on Base, including endpoint trust scores, token safety checks, wallet intelligence, and document extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[33ai-wq](https://clawhub.ai/user/33ai-wq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to compare prices and evaluate x402 endpoints or Base tokens, then purchase per-call data with a funded Base wallet when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid calls can spend USDC from a supplied private wallet key.

Mitigation: Use a dedicated low-balance wallet, set a tight per-call price ceiling, and allowlist known payment destinations.

Risk: Submitted documents, URLs, and other request data may be processed by xhagents.xyz.

Mitigation: Do not submit private documents, internal URLs, or regulated data unless external processing is approved.

## Reference(s):

- [XH Agents x402 ClawHub release](https://clawhub.ai/33ai-wq/skills/xh-agents-x402)
- [XH Agents API catalogue](https://xhagents.xyz/openapi.json)
- [XH Agents x402 discovery](https://xhagents.xyz/.well-known/x402)
- [Paid routes reference](references/routes.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [Terminal text and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid responses include a decoded payment settlement receipt.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
