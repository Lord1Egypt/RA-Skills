## Description:

Payment OS for AI agents that creates MPC wallets, executes stablecoin payments with automatic policy enforcement, sets spending rules in natural language, checks balances across chains, and issues virtual cards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[efedurmaz16](https://clawhub.ai/user/efedurmaz16)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent builders use this skill to let agents provision Sardis wallets, apply spending policies, check balances, issue virtual cards, and initiate stablecoin payments through Sardis APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The executable server may expose API credentials or sensitive payment/card data.

Mitigation: Use sandbox or low-limit Sardis credentials, avoid live secrets during review, and require trusted server-side credential retrieval before production use.

Risk: Payment execution may proceed without confirmed policy approval.

Mitigation: Require authenticated execute requests and fail-closed policy checks before enabling live payment workflows.

Risk: Examples can move real funds when used with live credentials.

Mitigation: Treat all payment, card, wallet, escrow, and mandate examples as live-money operations and review parameters before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/efedurmaz16/skills/sardis)
- [Sardis Website](https://sardis.sh)
- [Sardis Documentation](https://sardis.sh/docs)
- [Sardis API Reference](https://api.sardis.sh/api/v2/docs)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SARDIS_API_KEY and network access to Sardis APIs.]

## Skill Version(s):

1.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
