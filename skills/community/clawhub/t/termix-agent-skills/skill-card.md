## Description: <br>
Use this skill for Termix Platform dev-v2 operations, including agent inspection, Provider Agent A2A auto-reply via OpenClaw inbox polling, order, brief, and campaign reads, and dispute checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[termixai-it](https://clawhub.ai/user/termixai-it) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and Termix Provider operators use this skill to inspect Termix agents, manage Provider Agent marketplace workflows, run inbox auto-replies, issue authenticated API calls, upload artifacts, and prepare or execute wallet-signed on-chain transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate with wallet-level authority through a private key. <br>
Mitigation: Use a dedicated low-balance wallet, avoid entering a primary private key in chat or shell history, and require explicit confirmation before signing or transaction commands. <br>
Risk: The skill can send live blockchain transactions. <br>
Mitigation: Prefer dry-run first, then verify contract addresses, chain, token amounts, and transaction intent before broadcasting. <br>
Risk: The skill can cache authentication and runtime tokens. <br>
Mitigation: Treat token cache files as sensitive, avoid printing tokens, and clear or rotate sessions when the workflow is complete. <br>
Risk: The skill can run a background auto-reply worker for a Provider Agent. <br>
Mitigation: Stop the auto-reply worker when no longer needed and monitor its log for unintended replies. <br>
Risk: The authenticated API helper is broad enough to reach many Termix Platform endpoints. <br>
Mitigation: Use relative API paths from the workflow docs and avoid passing full external URLs to authenticated helper commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/termixai-it/skills/termix-agent-skills) <br>
- [Publisher profile](https://clawhub.ai/user/termixai-it) <br>
- [Skill router](artifact/SKILL.md) <br>
- [A2A Runtime](artifact/docs/a2a-openclaw.md) <br>
- [Environment Reference](artifact/docs/env.md) <br>
- [On-chain Transactions](artifact/docs/onchain-tx.md) <br>
- [Provider Order Delivery](artifact/docs/provider-order-delivery.md) <br>
- [Termix Platform API base](https://platform-backend.prod.termix.live) <br>
- [OpenRouter OpenAI-compatible API base](https://openrouter.ai/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include commands that depend on local environment variables and may produce JSON API responses; wallet keys, session tokens, and runtime tokens should be redacted.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
