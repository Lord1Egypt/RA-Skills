## Description:

Install, bootstrap, validate, and optionally connect StablePay MCP on Codex, Claude Code, or Cursor.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bubblevan](https://clawhub.ai/user/bubblevan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install and validate StablePay CLI onboarding, handle wallet and payment setup pauses, and optionally configure the StablePay MCP runtime for Codex, Claude Code, or Cursor.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow asks users to run and optionally persist an unpinned npm package during wallet and payment onboarding.

Mitigation: Use a pinned, verified version of stablepay-agentpay-dev, avoid global install unless necessary, and review the exact package before configuring MCP.

Risk: Wallet identity, payment limits, and merchant-facing commands can affect payment behavior if configured incorrectly.

Mitigation: Verify wallet identity details, payment limits, and command targets before completing onboarding or running payment-related follow-up commands.

Risk: Onboarding may pause at browser-based X verification, which requires a real external user action.

Mitigation: Stop autonomous execution at the verification step, preserve the exact resume command, and continue only after the user completes the browser step.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bubblevan/skills/stablepay-agent-bootstrap)
- [ClawHub publisher profile](https://clawhub.ai/user/bubblevan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown operator guidance with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include OS-specific command variants, validation results, and human-in-the-loop resume steps.]

## Skill Version(s):

1.4.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
