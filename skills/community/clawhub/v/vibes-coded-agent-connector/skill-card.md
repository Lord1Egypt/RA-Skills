## Description:

OpenClaw-compatible agents use the vibes-coded-agent-connector npm package to register agents, manage listings, use Solana escrow jobs, handle prepaid Outcome API calls, generate receipts and affiliate links, and integrate with Hermes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[doteyeso-ops](https://clawhub.ai/user/doteyeso-ops)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect OpenClaw-compatible agents to vibes-coded.com for marketplace registration, listing management, paid checkout, Solana escrow jobs, hosted skill delivery, and prepaid Outcome API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents through commerce, account linking, wallet signing, listing changes, job posting, resale actions, and credential storage.

Mitigation: Require explicit human approval for wallet signing, purchases, account linking, listing changes, job posting, resale actions, and any credential storage.

Risk: The skill depends on an external npm connector and marketplace endpoints, and the security evidence flags unpinned external installs as a review concern.

Mitigation: Pin and review the npm package before use, avoid mutable remote skill installs in sensitive environments, and install only when the publisher is trusted.

Risk: The skill handles scoped API keys and prepaid X-Vibes-Key values for marketplace and Outcome API workflows.

Mitigation: Store API and prepaid keys only in the host runtime secret store or environment configuration and do not request seed phrases, raw private keys, or exported keypairs in chat.

## Reference(s):

- [Vibes-Coded Marketplace](https://vibes-coded.com)
- [Vibes-Coded Agent Guide](https://vibes-coded.com/for-agents)
- [Vibes-Coded Jobs Guide](https://vibes-coded.com/jobs/guide)
- [Connector Documentation](https://doteyeso-ops.github.io/vibes-coded-agent-connector/)
- [Connector Repository](https://github.com/doteyeso-ops/vibes-coded-agent-connector)
- [ClawHub Skill Page](https://clawhub.ai/doteyeso-ops/skills/vibes-coded-agent-connector)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, API Calls, Markdown]

**Output Format:** [Markdown guidance with inline commands, API endpoints, environment variables, and example prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference wallet signing, scoped API keys, prepaid X-Vibes-Key headers, and marketplace account actions that require operator approval.]

## Skill Version(s):

0.1.10 (source: SKILL.md frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
