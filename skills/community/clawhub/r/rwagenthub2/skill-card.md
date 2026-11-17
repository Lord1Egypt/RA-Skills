## Description:

AgentHub lets agents call 32 paid real-world APIs for travel, web search, weather, finance, blockchain, code execution, and email using USDC payments on Base via x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcelo-rowship](https://clawhub.ai/user/marcelo-rowship)

### License/Terms of Use:


## Use Case:

External developers and agents use AgentHub to retrieve real-world data, send email, and execute code through a paid API gateway. It is intended for workflows that can supply Node.js, npm, a Base wallet funded with USDC, and the MCP_WALLET_PRIVATE_KEY credential.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a wallet private key for paid API calls.

Mitigation: Use only a dedicated low-balance Base wallet and never reuse a main wallet private key.

Risk: The documented SDK installation does not pin a reviewed package version.

Mitigation: Review and pin the SDK version before installation in managed or sensitive environments.

Risk: The documented shell template writes request data into a temporary script and can be unsafe if inputs are interpolated directly.

Mitigation: Prefer a reviewed static script that passes request data as JSON without shell interpolation.

Risk: API inputs may be sent to external services and the skill supports actions such as code execution, web extraction, and email sending.

Mitigation: Avoid secrets or sensitive business data in API inputs, and review each call before spending USDC or triggering external actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marcelo-rowship/skills/rwagenthub2)
- [AgentHub gateway](https://agents-production-73c1.up.railway.app)
- [rwagenthub-sdk package](https://www.npmjs.com/package/rwagenthub-sdk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell and JavaScript snippets; API calls return JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, npm, MCP_WALLET_PRIVATE_KEY, and a Base wallet with USDC; API calls may spend USDC per request.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
