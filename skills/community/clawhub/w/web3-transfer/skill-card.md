## Description:

Unified multi-chain transfer skill for BTC, EVM, and Solana. Use when a user wants to send ETH/ERC20, SOL/SPL, or BTC, including batch payouts, with preview confirmation, wallet signing, risk checks, and status follow-up through the transfer-request / transfer-status / transfer-cancel MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deanpeng-dotcom](https://clawhub.ai/user/deanpeng-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this instruction-only skill to coordinate BTC, EVM, Solana, and token transfers through Antalpha MCP tools with preview review, wallet signing, risk checks, and status follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill coordinates high-impact crypto transfers through a remote Antalpha MCP service and requires agent registration.

Mitigation: Install only in runtimes where that MCP service and registration flow are explicitly trusted and allowed.

Risk: The workflow persists an API credential returned by antalpha-register.

Mitigation: Store API keys in a proper secret store and never in logs, chat memory, plaintext files, or shared transcripts.

Risk: A mistaken recipient, chain, token, amount, fee, or wallet prompt can cause irreversible financial loss.

Mitigation: Require the user to independently verify transfer details and sign only after reviewing the preview and any risk warnings.

Risk: Solana address security scanning is skipped and BTC address scanning may be skipped or incomplete in this release.

Mitigation: Disclose skipped scans before confirmation and block HIGH or CRITICAL risks where scanning results are available.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/deanpeng-dotcom/skills/web3-transfer)
- [Antalpha MCP Endpoint](https://mcp-skills.ai.antalpha.com/mcp)
- [Antalpha](https://antalpha.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Configuration, Guidance]

**Output Format:** [Concise Markdown or text with transfer previews, wallet-signing next steps, MCP tool calls, and transfer status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only; transfer execution depends on connected MCP tools, server-side registration, and user wallet signing.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter and evidence.release.version; package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
