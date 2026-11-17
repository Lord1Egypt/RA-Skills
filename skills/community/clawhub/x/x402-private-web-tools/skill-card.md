## Description:

Private web tools for AI agents: search, scrape, and screenshot the web with x402 micropayments using USDC on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kodos-vibe](https://clawhub.ai/user/kodos-vibe)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to add paid private web search, page extraction, and screenshot capture to an agent without API keys or accounts. It is suited for workflows where the agent can explicitly control small x402 payments from a funded wallet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The payment fetcher signs x402 payments from the wallet key supplied to the tool.

Mitigation: Use a dedicated low-balance wallet and invoke paid requests only for destinations the operator explicitly trusts.

Risk: Wallet private keys and sensitive request data can be exposed through command-line arguments, environment variables, URLs, bodies, or headers.

Mitigation: Prefer a protected key file, avoid confidential URLs or headers, and review commands before execution.

Risk: The setup script installs Node.js dependencies and copies executable scripts into a user-level client directory.

Mitigation: Review the artifact and installed package versions before use, and run setup in an isolated environment when possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kodos-vibe/skills/x402-private-web-tools)
- [Publisher profile](https://clawhub.ai/user/kodos-vibe)
- [Service reference](artifact/references/services.md)
- [x402 Tools MCP GitHub reference](https://github.com/kodos-vibe/x402-tools-mcp)
- [x402 private web tools gateway](https://search.reversesandbox.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell and JavaScript command examples; service responses may be JSON, Markdown, text, PNG, or JPEG.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid requests use x402 micropayments with a caller-provided wallet key; screenshots can be saved as image files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
