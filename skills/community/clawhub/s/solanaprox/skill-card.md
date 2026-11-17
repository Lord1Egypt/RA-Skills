## Description:

Call AI models through the SolanaProx HTTP API (solanaprox.com), paid per call from a prepaid USDC balance on Solana. Anthropic (/v1/messages) and OpenAI (/v1/chat/completions) formats, tool calling, streaming. Auth is a signed-in solx_ token. Use it when the user wants a model answer billed through SolanaProx with direct HTTP requests and agrees to pay.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unixlamadev-spec](https://clawhub.ai/user/unixlamadev-spec)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to request model responses through SolanaProx with prepaid USDC, using Anthropic or OpenAI-compatible endpoints. It also describes checking model prices and account balances, managing tokens, and depositing funds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account, token, and deposit actions can affect account access or funds.

Mitigation: Get explicit user confirmation before side-effecting account or payment actions, and confirm the current deposit address and amount before a transfer.

Risk: Prompts and conversation content are sent through SolanaProx to the selected model provider, and the bearer token grants access to the account.

Mitigation: Do not include secrets or personal data in prompts; never print or log the token, and use a short-lived token with a low daily spend cap.

## Reference(s):

- [SolanaProx documentation](https://solanaprox.com/docs)
- [SolanaProx service](https://solanaprox.com)
- [SolanaProx ClawHub release](https://clawhub.ai/unixlamadev-spec/skills/solanaprox)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Model response text or JSON-compatible tool-call data, optionally streamed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Anthropic and OpenAI-compatible response formats; billed per successful model request]

## Skill Version(s):

4.0.3 (source: SKILL.md frontmatter, CHANGELOG, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
