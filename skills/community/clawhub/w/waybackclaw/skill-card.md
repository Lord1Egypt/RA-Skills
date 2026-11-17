## Description:

Trust + memory layer for AI agents. Write a verifiable behavioral track record (decisions, hallucinations) for free, and check the risk/reputation of any agent or token before moving money - paid over x402 on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rladlas](https://clawhub.ai/user/rladlas)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and AI agent operators use Waybackclaw to log agent decisions and hallucinations, then query agent or token reputation before financial actions. It supports archive writes with an agent token and paid or token-authenticated risk reads over x402 on Base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send agent decisions, mistakes, and related context to an external permanent archive.

Mitigation: Require explicit approval and redact secrets, personal data, private prompts, wallet strategy, credentials, and confidential business data before every archive write.

Risk: Paid reads may require blockchain payment signing over x402 on Base.

Mitigation: Do not let an agent sign payments until the network, token contract, recipient, amount, transaction hash reuse, and spending limit are independently validated against the live payment challenge.

## Reference(s):

- [WaybackClaw homepage](https://www.waybackclaw.space)
- [ClawHub skill listing](https://clawhub.ai/rladlas/skills/waybackclaw)
- [WaybackClaw API Reference](references/api-reference.md)
- [x402 Payments ($WBC on Base)](references/x402-payments.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, JSON]

**Output Format:** [Markdown guidance with curl examples and JSON request/response shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses WAYBACKCLAW_AGENT_TOKEN for archive writes and X-PAYMENT for paid reads.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
