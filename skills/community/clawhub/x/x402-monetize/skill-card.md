## Description:

Creates paid API endpoints using the x402 micropayment protocol by wrapping existing Zo skills and tools behind per-request payment walls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssidharhubble](https://clawhub.ai/user/ssidharhubble)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to turn existing Python scripts or Zo tools into HTTP API endpoints protected by x402 per-request payment middleware. It is aimed at monetizing API calls that return trading signals, flow alerts, market analysis, or similar service responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unreviewed external Node.js server that exposes paid, always-on API endpoints.

Mitigation: Before installing or running it, inspect /home/workspace/MoneyMachine/x402_server/index.js, verify its dependencies and payment recipient configuration, and confirm that exposing the service from the environment is acceptable.

## Reference(s):

- [x402 Quickstart for Sellers](https://docs.x402.org/getting-started/quickstart-for-sellers)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe configuration for a long-running paid API service on port 4020.]

## Skill Version(s):

1.0.15 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
