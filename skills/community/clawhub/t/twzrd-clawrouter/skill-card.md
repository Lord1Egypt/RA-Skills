## Description:

TWZRD Preflight for ClawRouter helps agents call TWZRD readiness and merchant-card checks before x402 spends through ClawRouter or BlockRun.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twzrd-sol](https://clawhub.ai/user/twzrd-sol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent operators use this skill to add a pre-spend trust gate before ClawRouter or BlockRun payments. It provides guidance and TypeScript example code for readiness-card checks, merchant-card checks, and receipt verification around payment-adjacent agent flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned npm execution is recommended in a payment-adjacent workflow.

Mitigation: Use pinned package versions or a lockfile-controlled install before running the skill in an environment with wallet access.

Risk: Payment checks can be bypassed if the gate is run in advisory mode or if a wallet has too much available balance.

Mitigation: Keep the gate in enforce mode for normal use and use a dedicated low-balance wallet for ClawRouter or BlockRun spending.

Risk: The documented next_action.command step could be misread as permission for an agent to run arbitrary commands.

Mitigation: Only execute commands that are locally derived, expected for the workflow, and explicitly approved.

Risk: An untrusted CLAWROUTER_PROXY_BASE could route payment-adjacent requests through the wrong local or remote proxy.

Mitigation: Set CLAWROUTER_PROXY_BASE only to a ClawRouter proxy that you control and verify before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/twzrd-sol/skills/twzrd-clawrouter)
- [TWZRD Intel Homepage](https://intel.twzrd.xyz)
- [TWZRD Preflight API](https://intel.twzrd.xyz/v1/intel/preflight)
- [TWZRD MCP Endpoint](https://intel.twzrd.xyz/mcp)
- [TWZRD x402 Metadata](https://intel.twzrd.xyz/.well-known/x402)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash snippets, API examples, and TypeScript code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes payment-gating guidance and executable example code; review before installing or using in live payment flows.]

## Skill Version(s):

0.2.1 (source: ClawHub release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
