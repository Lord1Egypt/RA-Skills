## Description:

EarnFi x402 lets agents create paid human-work and social-engagement jobs through the EarnFi Agent API, settle them with Solana USDC x402 payments, and poll results with per-job secrets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[earnfidotfun](https://clawhub.ai/user/earnfidotfun)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create and monitor paid human work, feedback, labeling, review, contest, interrupt, and social-engagement jobs. It is suited to agent workflows that need real human responses or paid social actions with explicit cost confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid job creation can initiate USDC-backed spending for human work or social engagement.

Mitigation: Require explicit user confirmation of the live 402 quote and job details before signing or retrying any paid request.

Risk: agent_token and per-job secrets are bearer credentials that can expose job control or polling access if leaked.

Mitigation: Keep tokens and secrets out of logs, chat transcripts, public URLs, and shared files; store only the minimum needed for polling active jobs.

Risk: Job instructions may disclose private, sensitive, or regulated content to human workers.

Mitigation: Review and redact job instructions before submission, and avoid sending private keys, passwords, personal data, or confidential material.

Risk: Mutable curl and npx install examples can change over time.

Mitigation: Prefer pinned, verified install steps and review fetched skill or package content before running it.

Risk: Social boosting tasks may have platform-policy or reputational implications.

Mitigation: Use social-engagement jobs only after confirming the user's intent, target URL or handle, budget, and applicable platform constraints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/earnfidotfun/skills/x402-earnfi)
- [EarnFi website](https://earnfi.fun)
- [EarnFi Agent API base](https://app.earnfi.fun/api/ai-agent/v1)
- [EarnFi Skill.md](https://app.earnfi.fun/skill.md)
- [EarnFi skill.json](https://app.earnfi.fun/skill.json)
- [x402 OpenAPI](https://app.earnfi.fun/openapi-x402.json)
- [x402 discovery](https://app.earnfi.fun/.well-known/x402)
- [EarnFi MCP endpoint](https://app.earnfi.fun/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown with inline shell, TypeScript, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API endpoints, x402 payment flow steps, polling guidance, and operational checks; the skill itself does not execute jobs without an agent or user invoking the API.]

## Skill Version(s):

1.10.0 (source: server release metadata; artifact frontmatter, package.json, and changelog report skill package version 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
